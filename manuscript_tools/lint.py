"""Continuity linter for the manuscript.

Checks the files referenced by the MANIFEST against a machine-readable
canon registry (canon.yaml): character-name spelling drift, impossible
calendar dates, iteration/era consistency, MANIFEST ordering, stale-model
vocabulary, unresolved wiki links, and frontmatter completeness.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import yaml

from manuscript_tools.build import parse_manifest
from manuscript_tools.frontmatter import load_frontmatter

DAYS_PER_YEAR = 365.25

VALID_TYPES = {"chapter", "wiki", "interstitial", "sketch"}
VALID_STATUSES = {"placeholder", "idea", "sketch", "draft", "polished", "final"}


@dataclass
class Finding:
    """A single lint finding."""

    severity: str  # "error" or "warning"
    path: str
    message: str

    def __str__(self) -> str:
        tag = "ERROR" if self.severity == "error" else "WARN "
        return f"{tag} {self.path}: {self.message}"


def strip_rtf(text: str) -> str:
    """Crudely extract readable text from RTF source.

    Good enough for scanning prose for names and dates; not a parser.
    """
    # Remove RTF groups that never contain prose (font tables, etc.)
    text = re.sub(r"\{\\\*[^{}]*\}", " ", text)
    text = re.sub(r"\{\\fonttbl[^{}]*(\{[^{}]*\}[^{}]*)*\}", " ", text)
    text = re.sub(r"\{\\colortbl[^;{}]*(;[^;{}]*)*\}", " ", text)
    # Hex escapes -> best-effort character
    text = re.sub(r"\\'([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), text)
    # Escaped braces and backslashes
    text = text.replace(r"\{", "{").replace(r"\}", "}").replace("\\\\", " ")
    # Control words (\word0 etc.) and remaining braces
    text = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return text


def read_prose(path: Path) -> str:
    """Read a manuscript file as scannable prose."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".rtf":
        return strip_rtf(raw)
    return raw


def load_canon(path: Path) -> dict[str, Any]:
    """Load the canon registry."""
    data: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data


def _allowed(canon: dict[str, Any], filename: str, pattern: str) -> bool:
    """Check the canon's exception list for a (file, pattern) pair.

    Matching is case-insensitive: term scanning is case-insensitive, so
    exceptions must suppress every casing of a deliberate violation.
    """
    needle = pattern.casefold()
    for exc in canon.get("exceptions", []) or []:
        if exc.get("file") == filename and exc.get("pattern", "").casefold() in needle:
            return True
    return False


def check_name_drift(canon: dict[str, Any], filename: str, prose: str) -> list[Finding]:
    """Flag forbidden spelling variants of canonical character names."""
    findings = []
    for char in canon.get("characters", []):
        for variant in char.get("forbidden_variants", []):
            for m in re.finditer(rf"\b{re.escape(variant)}\b", prose):
                context = prose[max(0, m.start() - 30) : m.end() + 30]
                context = " ".join(context.split())
                findings.append(
                    Finding(
                        "error",
                        filename,
                        f"name drift: '{variant}' should be "
                        f"'{char['name']}' (…{context}…)",
                    )
                )
    return findings


def check_calendar_dates(
    canon: dict[str, Any], filename: str, prose: str
) -> list[Finding]:
    """Flag calendar dates that cannot exist under the loop rules."""
    findings = []
    pattern = re.compile(
        r"\b(October\s+(?:2[4-9]|3[01])|November\s+\d{1,2}|December\s+\d{1,2})",
        re.IGNORECASE,
    )
    for m in pattern.finditer(prose):
        if _allowed(canon, filename, m.group(1)):
            continue
        findings.append(
            Finding(
                "error",
                filename,
                f"impossible calendar date '{m.group(1)}' — use the "
                "+X hours convention (THE_BIBLE.md §3) or add a canon "
                "exception if deliberate",
            )
        )
    return findings


def check_header_convention(
    canon: dict[str, Any], filename: str, prose: str
) -> list[Finding]:
    """Chapter headers must use '+X hours' loop time, never clock time.

    For canon-registered files with a declared header offset, the literal
    must appear in the opening of the file. Clock times (e.g. '7:15 am')
    near the top are flagged regardless.
    """
    findings = []
    opening = prose[:400]
    mapping = {f["file"]: f for f in canon.get("files", [])}
    entry = mapping.get(filename)

    if entry and entry.get("header"):
        expected = entry["header"]
        if expected not in opening:
            findings.append(
                Finding(
                    "error",
                    filename,
                    f"header missing loop-time marker '{expected}' "
                    "(headers show +X hours since the anomaly, not local time)",
                )
            )

    for m in re.finditer(r"\b\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)\b", opening):
        if _allowed(canon, filename, m.group(0)):
            continue
        findings.append(
            Finding(
                "error",
                filename,
                f"clock time '{m.group(0)}' in header — local time is "
                "meaningless in the loop; use +X hours since the anomaly",
            )
        )
    return findings


def check_verbatim_blocks(
    canon: dict[str, Any], filename: str, prose: str
) -> list[Finding]:
    """Canonical prose blocks must repeat character-identically.

    If a file contains a block's trigger substring, the full canonical
    text must appear verbatim — guarding ritual passages (e.g. the
    Oct 22nd journal fragment) against drift between chapters.
    """
    findings = []
    for block in canon.get("verbatim_blocks", []) or []:
        if block["trigger"] in prose and block["text"] not in prose:
            findings.append(
                Finding(
                    "error",
                    filename,
                    f"verbatim block '{block['name']}' present (trigger matched) "
                    "but text has drifted from the canonical version",
                )
            )
    return findings


def check_forbidden_terms(
    canon: dict[str, Any], filename: str, prose: str
) -> list[Finding]:
    """Flag stale-model vocabulary (e.g. midnight resets)."""
    findings = []
    for term in canon.get("forbidden_terms", []):
        for m in re.finditer(term["pattern"], prose, re.IGNORECASE):
            if _allowed(canon, filename, m.group(0)):
                continue
            findings.append(
                Finding(
                    term.get("severity", "warning"),
                    filename,
                    f"stale-model term '{m.group(0)}': {term['reason']}",
                )
            )
    return findings


def _era_ok(canon: dict[str, Any], era: str, years: float) -> bool | None:
    """Check a year value against an era's range. None = era unknown/unbounded."""
    eras = canon.get("eras", {})
    rng = eras.get(str(era))
    if not rng:
        return None
    return rng[0] <= years <= rng[1]


def check_file_canon(canon: dict[str, Any], filename: str, path: Path) -> list[Finding]:
    """Cross-check a file's day/era/pov against the canon mapping and frontmatter."""
    findings = []
    mapping = {f["file"]: f for f in canon.get("files", [])}
    entry = mapping.get(filename)

    fm = None
    if path.suffix.lower() == ".md":
        fm, _ = load_frontmatter(path)
        if not fm.title:
            findings.append(Finding("error", filename, "frontmatter missing title"))
        if fm.type not in VALID_TYPES:
            findings.append(
                Finding("error", filename, f"frontmatter type '{fm.type}' invalid")
            )
        if fm.status not in VALID_STATUSES:
            findings.append(
                Finding("error", filename, f"frontmatter status '{fm.status}' invalid")
            )

    if entry is None:
        if path.suffix.lower() == ".md" and fm and fm.type == "chapter":
            findings.append(
                Finding("warning", filename, "chapter not in canon file registry")
            )
        return findings

    day = entry.get("day")
    if day is not None:
        years = day / DAYS_PER_YEAR
        era = entry.get("era")
        if era is not None:
            ok = _era_ok(canon, str(era), years)
            if ok is False:
                findings.append(
                    Finding(
                        "error",
                        filename,
                        f"day {day:,} (~year {years:,.0f}) is outside era "
                        f"{era} range {canon['eras'][str(era)]}",
                    )
                )
        if fm is not None and fm.iteration is not None and fm.iteration != day:
            findings.append(
                Finding(
                    "error",
                    filename,
                    f"frontmatter iteration {fm.iteration:,} != canon day {day:,}",
                )
            )
    return findings


def check_manifest_order(canon: dict[str, Any], manifest_path: Path) -> list[Finding]:
    """Within ordered sections, files must run in ascending canon day order."""
    findings = []
    ordered_sections = set(canon.get("ordered_sections", []))
    mapping = {f["file"]: f.get("day") for f in canon.get("files", [])}

    section = ""
    last: tuple[int, str] | None = None
    for entry in parse_manifest(manifest_path):
        if entry.kind == "section":
            section = entry.section_title
            last = None
            continue
        if section not in ordered_sections:
            continue
        day = mapping.get(entry.path)
        if day is None:
            continue
        if last is not None and day < last[0]:
            findings.append(
                Finding(
                    "error",
                    "MANIFEST",
                    f"'{entry.path}' (day {day:,}) is out of order after "
                    f"'{last[1]}' (day {last[0]:,}) in section '{section}'",
                )
            )
        last = (day, entry.path)
    return findings


def check_wiki_links(
    canon: dict[str, Any], filename: str, prose: str, wiki_dir: Path
) -> list[Finding]:
    """Flag [[wiki links]] that resolve to neither a file nor a planned article."""
    findings = []
    existing = {p.stem for p in wiki_dir.glob("*.md")} if wiki_dir.exists() else set()
    planned = set(canon.get("planned_articles", []))
    for m in re.finditer(r"\[\[([^\]]+)\]\]", prose):
        target = m.group(1).strip()
        if target in existing or target in planned:
            continue
        findings.append(
            Finding(
                "warning",
                filename,
                f"wiki link [[{target}]] resolves to no article file and "
                "is not in canon planned_articles",
            )
        )
    return findings


def check_assertions(canon: dict[str, Any]) -> list[Finding]:
    """Verify day<->year arithmetic assertions declared in the canon."""
    findings = []
    for a in canon.get("assertions", []):
        years = a["day"] / DAYS_PER_YEAR
        if abs(years - a["years_approx"]) > a.get("tolerance", 5):
            findings.append(
                Finding(
                    "error",
                    "canon.yaml",
                    f"assertion failed: day {a['day']:,} = ~year {years:,.1f}, "
                    f"canon claims ~{a['years_approx']:,}",
                )
            )
    return findings


def lint_manuscript(
    manifest_path: Path, canon_path: Path | None = None
) -> list[Finding]:
    """Run all checks over the MANIFEST's files. Returns findings."""
    base_dir = manifest_path.parent
    if canon_path is None:
        canon_path = base_dir / "canon.yaml"
    if not canon_path.exists():
        return [Finding("error", str(canon_path), "canon registry not found")]
    canon = load_canon(canon_path)
    wiki_dir = base_dir / canon.get("wiki_dir", "Interstitials/Wiki")

    findings = check_assertions(canon)
    findings += check_manifest_order(canon, manifest_path)

    for entry in parse_manifest(manifest_path):
        if entry.kind != "file":
            continue
        path = base_dir / entry.path
        if not path.exists():
            findings.append(Finding("error", entry.path, "file missing on disk"))
            continue
        prose = read_prose(path)
        findings += check_name_drift(canon, entry.path, prose)
        findings += check_calendar_dates(canon, entry.path, prose)
        findings += check_header_convention(canon, entry.path, prose)
        findings += check_verbatim_blocks(canon, entry.path, prose)
        findings += check_forbidden_terms(canon, entry.path, prose)
        findings += check_file_canon(canon, entry.path, path)
        findings += check_wiki_links(canon, entry.path, prose, wiki_dir)

    return findings


def run_lint(manifest_path: Path, canon_path: Path | None = None) -> int:
    """CLI entry: print findings, return exit code (1 if any errors)."""
    findings = lint_manuscript(manifest_path, canon_path)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    for f in findings:
        print(f)
    print(f"\nmanuscript lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0
