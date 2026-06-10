"""Tests for the frontmatter parser."""

from pathlib import Path
from textwrap import dedent

from manuscript_tools.frontmatter import (
    Frontmatter,
    load_frontmatter,
    parse_frontmatter,
)


class TestParseFrontmatter:
    def test_no_frontmatter_returns_defaults(self) -> None:
        text = "# Hello World\n\nSome content."
        fm, body = parse_frontmatter(text)
        assert fm.title == ""
        assert fm.type == "chapter"
        assert fm.status == "draft"
        assert body == text

    def test_basic_frontmatter_is_parsed(self) -> None:
        text = dedent("""\
            ---
            title: The Boards
            type: wiki
            status: polished
            draft: 2
            ---
            # The Boards

            Content here.
        """)
        fm, body = parse_frontmatter(text)
        assert fm.title == "The Boards"
        assert fm.type == "wiki"
        assert fm.status == "polished"
        assert fm.draft == 2
        assert body.startswith("# The Boards")

    def test_frontmatter_with_all_fields(self) -> None:
        text = dedent("""\
            ---
            title: Thud
            type: chapter
            status: draft
            draft: 3
            pov: Jeff
            iteration: 945366
            era: "5"
            todos:
              - Fix the ending
              - Add more detail to paragraph 3
            ---
            Body text.
        """)
        fm, body = parse_frontmatter(text)
        assert fm.title == "Thud"
        assert fm.pov == "Jeff"
        assert fm.iteration == 945366
        assert fm.era == "5"
        assert len(fm.todos) == 2
        assert "Fix the ending" in fm.todos
        assert body == "Body text.\n"

    def test_invalid_yaml_returns_defaults(self) -> None:
        text = "---\n: invalid: yaml: [broken\n---\nContent."
        fm, body = parse_frontmatter(text)
        assert fm.title == ""
        assert body == text

    def test_unclosed_frontmatter_returns_defaults(self) -> None:
        text = "---\ntitle: Oops\nNo closing delimiter"
        fm, body = parse_frontmatter(text)
        assert fm.title == ""
        assert body == text

    def test_leading_newlines_are_tolerated(self) -> None:
        text = "\n\n---\ntitle: Test\n---\nBody."
        fm, body = parse_frontmatter(text)
        assert fm.title == "Test"
        assert body == "Body."

    def test_non_dict_yaml_returns_defaults(self) -> None:
        text = "---\n- a list\n- not a dict\n---\nBody."
        fm, body = parse_frontmatter(text)
        assert fm.title == ""
        assert body == text


class TestStatusAtLeast:
    def test_polished_meets_draft_threshold(self) -> None:
        fm = Frontmatter(status="polished")
        assert fm.status_at_least("draft") is True

    def test_sketch_does_not_meet_polished_threshold(self) -> None:
        fm = Frontmatter(status="sketch")
        assert fm.status_at_least("polished") is False

    def test_final_meets_final_threshold(self) -> None:
        fm = Frontmatter(status="final")
        assert fm.status_at_least("final") is True

    def test_placeholder_is_lowest(self) -> None:
        fm = Frontmatter(status="placeholder")
        assert fm.status_at_least("placeholder") is True
        assert fm.status_at_least("idea") is False

    def test_unknown_status_fails_threshold(self) -> None:
        fm = Frontmatter(status="unknown_status")
        assert fm.status_at_least("draft") is False


class TestLoadFrontmatter:
    def test_md_file(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("---\ntitle: Test Article\ntype: wiki\n---\nBody.\n")
        fm, body = load_frontmatter(md)
        assert fm.title == "Test Article"
        assert fm.type == "wiki"
        assert body == "Body.\n"

    def test_rtf_with_sidecar(self, tmp_path: Path) -> None:
        rtf = tmp_path / "Thud.rtf"
        rtf.write_text("{\\rtf1 content}")
        sidecar = tmp_path / "Thud.meta.yaml"
        sidecar.write_text("title: Thud\ntype: chapter\nstatus: polished\npov: Jeff\n")
        fm, body = load_frontmatter(rtf)
        assert fm.title == "Thud"
        assert fm.type == "chapter"
        assert fm.status == "polished"
        assert fm.pov == "Jeff"

    def test_rtf_without_sidecar_uses_filename(self, tmp_path: Path) -> None:
        rtf = tmp_path / "My Story.rtf"
        rtf.write_text("{\\rtf1 content}")
        fm, body = load_frontmatter(rtf)
        assert fm.title == "My Story"
        assert fm.type == "chapter"
        assert fm.status == "draft"

    def test_md_without_frontmatter(self, tmp_path: Path) -> None:
        md = tmp_path / "plain.md"
        md.write_text("# Just a heading\n\nNo frontmatter here.\n")
        fm, body = load_frontmatter(md)
        assert fm.title == ""
        assert body == "# Just a heading\n\nNo frontmatter here.\n"

    def test_rtf_with_invalid_sidecar_yaml(self, tmp_path: Path) -> None:
        rtf = tmp_path / "Bad.rtf"
        rtf.write_text("{\\rtf1 content}")
        sidecar = tmp_path / "Bad.meta.yaml"
        sidecar.write_text(": invalid: yaml: [broken")
        fm, body = load_frontmatter(rtf)
        # Falls back to filename-derived defaults
        assert fm.title == "Bad"
        assert fm.type == "chapter"

    def test_unsupported_extension_returns_defaults(self, tmp_path: Path) -> None:
        txt = tmp_path / "notes.txt"
        txt.write_text("some text")
        fm, body = load_frontmatter(txt)
        assert fm.title == "notes"
        assert body == ""
