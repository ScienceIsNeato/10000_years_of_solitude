"""Tests for the continuity linter."""

from pathlib import Path

import yaml

from manuscript_tools.lint import (
    Finding,
    check_calendar_dates,
    check_file_canon,
    check_manifest_order,
    check_name_drift,
    check_wiki_links,
    lint_manuscript,
    strip_rtf,
)

CANON = {
    "wiki_dir": "Wiki",
    "ordered_sections": ["The Loop, In Order"],
    "eras": {"1": [0, 10], "2": [10, 200]},
    "assertions": [{"day": 3653, "years_approx": 10, "tolerance": 1}],
    "characters": [
        {"name": "Caius", "forbidden_variants": ["Cauis", "Gaius"]},
    ],
    "forbidden_terms": [
        {
            "pattern": "midnight UTC",
            "severity": "error",
            "reason": "no shared clock",
        }
    ],
    "files": [
        {"file": "a.md", "day": 100, "era": 1, "pov": "Caius"},
        {"file": "b.md", "day": 5000, "era": 2, "pov": "Caius"},
    ],
    "exceptions": [{"file": "allowed.md", "pattern": "October 24"}],
    "planned_articles": ["Planned Article"],
}


def errors(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.severity == "error"]


class TestStripRtf:
    def test_strips_control_words(self) -> None:
        rtf = r"{\rtf1\ansi {\fonttbl{\f0 Times;}} Hello \b world\b0 .}"
        text = strip_rtf(rtf)
        assert "Hello" in text and "world" in text
        assert "\\b" not in text and "fonttbl" not in text

    def test_decodes_hex_escapes(self) -> None:
        assert "café" in strip_rtf(r"caf\'e9")


class TestNameDrift:
    def test_flags_variant(self) -> None:
        found = check_name_drift(CANON, "x.md", "And then Cauis smiled.")
        assert len(found) == 1
        assert "Cauis" in found[0].message and "Caius" in found[0].message

    def test_clean_prose_passes(self) -> None:
        assert check_name_drift(CANON, "x.md", "And then Caius smiled.") == []

    def test_no_substring_false_positive(self) -> None:
        assert check_name_drift(CANON, "x.md", "the Gaiusian heresy") == []


class TestCalendarDates:
    def test_flags_impossible_date(self) -> None:
        found = check_calendar_dates(CANON, "x.md", "By October 25 it was done.")
        assert len(found) == 1

    def test_october_23_is_fine(self) -> None:
        assert check_calendar_dates(CANON, "x.md", "October 23rd, again.") == []

    def test_exception_allows_deliberate_date(self) -> None:
        found = check_calendar_dates(
            CANON, "allowed.md", "It was October 24 when she landed."
        )
        assert found == []

    def test_november_flagged(self) -> None:
        found = check_calendar_dates(CANON, "x.md", "On November 3 they met.")
        assert len(found) == 1


class TestFileCanon:
    def test_era_day_mismatch(self, tmp_path: Path) -> None:
        p = tmp_path / "a.md"
        p.write_text(
            "---\ntitle: A\ntype: chapter\nstatus: draft\niteration: 100\n---\n# A\n"
        )
        # day 100 = year 0.27 -> era 1 OK
        assert errors(check_file_canon(CANON, "a.md", p)) == []
        # b.md: day 5000 = year 13.7 -> era 2 OK
        p2 = tmp_path / "b.md"
        p2.write_text(
            "---\ntitle: B\ntype: chapter\nstatus: draft\niteration: 5000\n---\n# B\n"
        )
        assert errors(check_file_canon(CANON, "b.md", p2)) == []

    def test_era_violation_caught(self, tmp_path: Path) -> None:
        canon = dict(CANON)
        canon["files"] = [{"file": "a.md", "day": 5000, "era": 1}]
        p = tmp_path / "a.md"
        p.write_text("---\ntitle: A\ntype: chapter\nstatus: draft\n---\n# A\n")
        found = errors(check_file_canon(canon, "a.md", p))
        assert len(found) == 1 and "outside era" in found[0].message

    def test_frontmatter_iteration_mismatch(self, tmp_path: Path) -> None:
        p = tmp_path / "a.md"
        p.write_text(
            "---\ntitle: A\ntype: chapter\nstatus: draft\niteration: 999\n---\n# A\n"
        )
        found = errors(check_file_canon(CANON, "a.md", p))
        assert any("iteration" in f.message for f in found)

    def test_invalid_frontmatter_fields(self, tmp_path: Path) -> None:
        p = tmp_path / "weird.md"
        p.write_text("---\ntitle: W\ntype: saga\nstatus: vibes\n---\n# W\n")
        found = errors(check_file_canon(CANON, "weird.md", p))
        assert len(found) == 2


class TestManifestOrder:
    def test_out_of_order_flagged(self, tmp_path: Path) -> None:
        m = tmp_path / "MANIFEST"
        m.write_text("## The Loop, In Order\n\nb.md\na.md\n")
        found = check_manifest_order(CANON, m)
        assert len(found) == 1 and "out of order" in found[0].message

    def test_ascending_passes(self, tmp_path: Path) -> None:
        m = tmp_path / "MANIFEST"
        m.write_text("## The Loop, In Order\n\na.md\nb.md\n")
        assert check_manifest_order(CANON, m) == []

    def test_unordered_sections_ignored(self, tmp_path: Path) -> None:
        m = tmp_path / "MANIFEST"
        m.write_text("## Appendix\n\nb.md\na.md\n")
        assert check_manifest_order(CANON, m) == []


class TestWikiLinks:
    def test_existing_and_planned_resolve(self, tmp_path: Path) -> None:
        wiki = tmp_path / "Wiki"
        wiki.mkdir()
        (wiki / "Real Article.md").write_text("# Real Article\n")
        prose = "See [[Real Article]] and [[Planned Article]]."
        assert check_wiki_links(CANON, "x.md", prose, wiki) == []

    def test_unknown_link_warns(self, tmp_path: Path) -> None:
        wiki = tmp_path / "Wiki"
        wiki.mkdir()
        found = check_wiki_links(CANON, "x.md", "See [[Ghost Article]].", wiki)
        assert len(found) == 1 and found[0].severity == "warning"


class TestEndToEnd:
    def test_full_lint_run(self, tmp_path: Path) -> None:
        (tmp_path / "Wiki").mkdir()
        a = tmp_path / "a.md"
        a.write_text(
            "---\ntitle: A\ntype: chapter\nstatus: draft\niteration: 100\n---\n"
            "# A\n\nCauis waited until October 26. There is no midnight UTC.\n"
        )
        m = tmp_path / "MANIFEST"
        m.write_text("## The Loop, In Order\n\na.md\n")
        (tmp_path / "canon.yaml").write_text(yaml.safe_dump(CANON))
        findings = lint_manuscript(m)
        msgs = " | ".join(f.message for f in findings)
        assert "Cauis" in msgs
        assert "October 26" in msgs
        assert "midnight UTC" in msgs

    def test_missing_canon_is_error(self, tmp_path: Path) -> None:
        m = tmp_path / "MANIFEST"
        m.write_text("a.md\n")
        findings = lint_manuscript(m)
        assert len(findings) == 1 and findings[0].severity == "error"

    def test_missing_file_is_error(self, tmp_path: Path) -> None:
        m = tmp_path / "MANIFEST"
        m.write_text("ghost.md\n")
        (tmp_path / "canon.yaml").write_text(yaml.safe_dump(CANON))
        findings = lint_manuscript(m)
        assert any("missing on disk" in f.message for f in findings)
