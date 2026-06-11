"""Core build logic for the manuscript export pipeline."""

from __future__ import annotations

import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from manuscript_tools.frontmatter import Frontmatter, load_frontmatter


@dataclass
class ManifestEntry:
    """A single entry from the MANIFEST file."""

    path: str  # Relative path from Manuscript/
    kind: str  # "file" or "section"
    section_title: str = ""


@dataclass
class ChapterSource:
    """A resolved chapter ready for assembly."""

    path: Path
    manifest_entry: ManifestEntry
    frontmatter: Frontmatter
    body: str  # markdown body (frontmatter stripped)


@dataclass
class BuildResult:
    """Result of a manuscript build."""

    output_path: Path
    chapter_count: int
    section_count: int
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_manifest(manifest_path: Path) -> list[ManifestEntry]:
    """Parse a MANIFEST file into ordered entries.

    Format:
    - Lines starting with ## are section dividers
    - Lines starting with # (single) are comments
    - Blank lines are ignored
    - Everything else is a file path relative to the manifest's directory
    """
    entries: list[ManifestEntry] = []

    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("## "):
            entries.append(
                ManifestEntry(path="", kind="section", section_title=line[3:])
            )
            continue

        if line.startswith("#"):
            continue

        entries.append(ManifestEntry(path=line, kind="file"))

    return entries


def make_footnote_prefix(relative_path: str) -> str:
    """Generate a unique footnote prefix from a file path."""
    return re.sub(r"[^a-zA-Z0-9]", "_", relative_path)


def rewrite_footnotes(markdown: str, prefix: str) -> str:
    """Rewrite footnote references and definitions to be unique per file.

    Transforms [^1] to [^prefix_1] to avoid collisions when combining files.
    """
    return re.sub(r"\[\^(\w+)\]", rf"[^{prefix}_\1]", markdown)


def convert_rtf_to_markdown(rtf_path: Path) -> str:
    """Convert an RTF file to markdown using pandoc."""
    result = subprocess.run(
        ["pandoc", str(rtf_path), "-t", "markdown", "--wrap=none"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def resolve_chapters(
    entries: list[ManifestEntry],
    base_dir: Path,
    *,
    min_status: str | None = None,
    type_filter: str | None = None,
) -> list[ManifestEntry | ChapterSource]:
    """Resolve manifest entries to chapter sources with frontmatter.

    Filters by status and type if specified.
    Returns a mixed list of ManifestEntry (for sections) and ChapterSource (for files).
    """
    resolved: list[ManifestEntry | ChapterSource] = []

    for entry in entries:
        if entry.kind == "section":
            resolved.append(entry)
            continue

        filepath = base_dir / entry.path
        if not filepath.exists():
            continue

        fm, body = load_frontmatter(filepath)

        if min_status and not fm.status_at_least(min_status):
            continue

        if type_filter and fm.type != type_filter:
            continue

        # For RTF files, body comes from pandoc conversion
        if filepath.suffix.lower() == ".rtf":
            body = convert_rtf_to_markdown(filepath)

        resolved.append(
            ChapterSource(
                path=filepath,
                manifest_entry=entry,
                frontmatter=fm,
                body=body,
            )
        )

    return resolved


def assemble_markdown(
    chapters: list[ManifestEntry | ChapterSource],
) -> tuple[str, int, int]:
    """Assemble resolved chapters into a single markdown document.

    Returns (combined_markdown, file_count, section_count).
    """
    parts: list[str] = []
    file_count = 0
    section_count = 0

    for item in chapters:
        if isinstance(item, ManifestEntry):
            # Section divider
            if file_count > 0 or section_count > 0:
                parts.append("\n\\newpage\n")
            parts.append(f"# {item.section_title}\n")
            section_count += 1
            continue

        # Chapter source
        if file_count > 0:
            parts.append("\n\\newpage\n")

        prefix = make_footnote_prefix(item.manifest_entry.path)
        body = rewrite_footnotes(item.body, prefix)
        parts.append(body)
        parts.append("\n")
        file_count += 1

    return "\n".join(parts), file_count, section_count


def build_manuscript(
    manifest_path: Path,
    output_format: str = "pdf",
    *,
    min_status: str | None = None,
    type_filter: str | None = None,
    output_dir: Path | None = None,
) -> BuildResult:
    """Build the manuscript from MANIFEST to the specified output format.

    Args:
        manifest_path: Path to the MANIFEST file.
        output_format: One of 'pdf', 'docx', 'epub', 'html'.
        min_status: Minimum status threshold for inclusion.
        type_filter: Only include files of this type.
        output_dir: Output directory (defaults to build/ next to MANIFEST).
    """
    base_dir = manifest_path.parent
    if output_dir is None:
        output_dir = base_dir / "build"
    output_dir.mkdir(parents=True, exist_ok=True)

    entries = parse_manifest(manifest_path)
    chapters = resolve_chapters(
        entries,
        base_dir,
        min_status=min_status,
        type_filter=type_filter,
    )

    combined, file_count, section_count = assemble_markdown(chapters)

    if file_count == 0:
        raise ValueError("No files matched the given filters")

    # Write combined markdown to temp file for pandoc
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(combined)
        combined_path = Path(tmp.name)

    try:
        output_path = _run_pandoc(combined_path, output_format, output_dir)
    finally:
        combined_path.unlink(missing_ok=True)

    return BuildResult(
        output_path=output_path,
        chapter_count=file_count,
        section_count=section_count,
    )


TITLE = "Curiosity Killed the Cat (While Turning It Immortal)"


def _run_pandoc(
    input_path: Path,
    output_format: str,
    output_dir: Path,
) -> Path:
    """Run pandoc to produce the final output."""
    from datetime import UTC, datetime

    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d")
    output_path = output_dir / f"manuscript_{timestamp}.{output_format}"

    common_args = [
        "pandoc",
        str(input_path),
        "--from",
        "markdown",
        "--standalone",
        "--toc",
        "--toc-depth=2",
        f"--metadata=title:{TITLE}",
    ]

    format_args = _get_format_args(output_format)

    cmd = [*common_args, *format_args, "-o", str(output_path)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    return output_path


def _get_format_args(output_format: str) -> list[str]:
    """Get pandoc arguments specific to the output format."""
    if output_format == "pdf":
        return [
            "--pdf-engine=xelatex",
            "-V",
            "geometry:margin=1in",
            "-V",
            "fontsize=12pt",
            "-V",
            "documentclass=report",
            "-V",
            "linkcolor=black",
            "-V",
            "urlcolor=black",
            "-V",
            "mainfont=Times New Roman",
        ]
    if output_format == "html":
        return ["--self-contained"]
    # docx and epub need no extra args
    return []
