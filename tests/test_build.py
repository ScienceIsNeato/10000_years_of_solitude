"""Tests for the build module."""

from pathlib import Path
from textwrap import dedent

from manuscript_tools.build import (
    ChapterSource,
    ManifestEntry,
    assemble_markdown,
    make_footnote_prefix,
    parse_manifest,
    resolve_chapters,
    rewrite_footnotes,
)
from manuscript_tools.frontmatter import Frontmatter


class TestParseManifest:
    def test_basic_manifest(self, tmp_path: Path) -> None:
        manifest = tmp_path / "MANIFEST"
        manifest.write_text(
            dedent("""\
            # Comment line
            ## Character Chapters

            Thud/Thud.rtf
            Jennifer/Jennifer.rtf

            ## Wiki Articles

            Wiki/The Boards.md
        """)
        )
        entries = parse_manifest(manifest)
        assert len(entries) == 5
        assert entries[0].kind == "section"
        assert entries[0].section_title == "Character Chapters"
        assert entries[1].kind == "file"
        assert entries[1].path == "Thud/Thud.rtf"
        assert entries[2].kind == "file"
        assert entries[2].path == "Jennifer/Jennifer.rtf"
        assert entries[3].kind == "section"
        assert entries[3].section_title == "Wiki Articles"
        assert entries[4].kind == "file"
        assert entries[4].path == "Wiki/The Boards.md"

    def test_empty_manifest(self, tmp_path: Path) -> None:
        manifest = tmp_path / "MANIFEST"
        manifest.write_text("# Only comments\n# Nothing else\n")
        entries = parse_manifest(manifest)
        assert entries == []

    def test_comments_and_blanks_are_skipped(self, tmp_path: Path) -> None:
        manifest = tmp_path / "MANIFEST"
        manifest.write_text("# comment\n\n# another comment\nfile.md\n")
        entries = parse_manifest(manifest)
        assert len(entries) == 1
        assert entries[0].path == "file.md"


class TestFootnotes:
    def test_make_footnote_prefix(self) -> None:
        prefix = make_footnote_prefix("Wiki/The Boards.md")
        assert prefix == "Wiki_The_Boards_md"
        assert " " not in prefix
        assert "/" not in prefix

    def test_rewrite_footnotes_numeric(self) -> None:
        text = "Some text[^1] and more[^2].\n\n[^1]: First note\n[^2]: Second note"
        result = rewrite_footnotes(text, "myfile")
        assert "[^myfile_1]" in result
        assert "[^myfile_2]" in result
        assert "[^1]" not in result

    def test_rewrite_footnotes_no_footnotes(self) -> None:
        text = "Plain text with no footnotes."
        result = rewrite_footnotes(text, "prefix")
        assert result == text

    def test_rewrite_footnotes_named(self) -> None:
        text = "Reference[^note1].\n\n[^note1]: A named footnote"
        result = rewrite_footnotes(text, "pre")
        assert "[^pre_note1]" in result


class TestAssembleMarkdown:
    def test_single_chapter(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            ChapterSource(
                path=Path("test.md"),
                manifest_entry=ManifestEntry(path="test.md", kind="file"),
                frontmatter=Frontmatter(title="Test"),
                body="# Test\n\nContent here.",
            )
        ]
        combined, file_count, section_count = assemble_markdown(chapters)
        assert file_count == 1
        assert section_count == 0
        assert "Content here." in combined

    def test_section_plus_chapter(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            ManifestEntry(path="", kind="section", section_title="Part One"),
            ChapterSource(
                path=Path("ch1.md"),
                manifest_entry=ManifestEntry(path="ch1.md", kind="file"),
                frontmatter=Frontmatter(title="Chapter 1"),
                body="Chapter text.",
            ),
        ]
        combined, file_count, section_count = assemble_markdown(chapters)
        assert file_count == 1
        assert section_count == 1
        assert "# Part One" in combined
        assert "Chapter text." in combined

    def test_multiple_chapters_get_page_breaks(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            ChapterSource(
                path=Path("a.md"),
                manifest_entry=ManifestEntry(path="a.md", kind="file"),
                frontmatter=Frontmatter(),
                body="Chapter A.",
            ),
            ChapterSource(
                path=Path("b.md"),
                manifest_entry=ManifestEntry(path="b.md", kind="file"),
                frontmatter=Frontmatter(),
                body="Chapter B.",
            ),
        ]
        combined, file_count, _ = assemble_markdown(chapters)
        assert file_count == 2
        assert "\\newpage" in combined

    def test_footnotes_are_rewritten_per_file(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            ChapterSource(
                path=Path("a.md"),
                manifest_entry=ManifestEntry(path="a.md", kind="file"),
                frontmatter=Frontmatter(),
                body="Text[^1].\n\n[^1]: Note from A",
            ),
            ChapterSource(
                path=Path("b.md"),
                manifest_entry=ManifestEntry(path="b.md", kind="file"),
                frontmatter=Frontmatter(),
                body="Text[^1].\n\n[^1]: Note from B",
            ),
        ]
        combined, _, _ = assemble_markdown(chapters)
        # Both files had [^1], but they should now be unique
        assert "[^1]" not in combined
        assert "[^a_md_0_1]" in combined
        assert "[^b_md_1_1]" in combined


class TestResolveChapters:
    def test_missing_file_is_skipped(self, tmp_path: Path) -> None:
        entries = [
            ManifestEntry(path="nonexistent.md", kind="file"),
        ]
        result = resolve_chapters(entries, tmp_path)
        assert len(result) == 0

    def test_section_entries_pass_through(self, tmp_path: Path) -> None:
        entries = [
            ManifestEntry(path="", kind="section", section_title="Part One"),
        ]
        result = resolve_chapters(entries, tmp_path)
        assert len(result) == 1
        assert isinstance(result[0], ManifestEntry)

    def test_md_file_is_resolved(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("---\ntitle: Test\ntype: wiki\nstatus: polished\n---\nBody.\n")
        entries = [ManifestEntry(path="test.md", kind="file")]
        result = resolve_chapters(entries, tmp_path)
        assert len(result) == 1
        chapter = result[0]
        assert isinstance(chapter, ChapterSource)
        assert chapter.frontmatter.title == "Test"
        assert chapter.frontmatter.type == "wiki"
        assert chapter.body == "Body.\n"

    def test_status_filter_excludes_low_status(self, tmp_path: Path) -> None:
        md = tmp_path / "sketch.md"
        md.write_text("---\ntitle: Sketch\nstatus: sketch\n---\nSketch body.\n")
        entries = [ManifestEntry(path="sketch.md", kind="file")]
        result = resolve_chapters(entries, tmp_path, min_status="polished")
        # Sketch doesn't meet polished threshold
        assert len(result) == 0

    def test_type_filter(self, tmp_path: Path) -> None:
        wiki = tmp_path / "wiki.md"
        wiki.write_text("---\ntitle: Wiki\ntype: wiki\n---\nWiki body.\n")
        chapter = tmp_path / "chapter.md"
        chapter.write_text("---\ntitle: Chapter\ntype: chapter\n---\nChapter body.\n")
        entries = [
            ManifestEntry(path="wiki.md", kind="file"),
            ManifestEntry(path="chapter.md", kind="file"),
        ]
        result = resolve_chapters(entries, tmp_path, type_filter="wiki")
        assert len(result) == 1
        assert isinstance(result[0], ChapterSource)
        assert result[0].frontmatter.type == "wiki"


class TestBugbotFixes:
    """Regression tests for the PR review findings."""

    def _chapter(self, path: str, body: str = "Prose.") -> ChapterSource:
        return ChapterSource(
            path=Path(path),
            manifest_entry=ManifestEntry(path=path, kind="file"),
            frontmatter=Frontmatter(),
            body=body,
        )

    def test_skipped_paths_are_recorded(self, tmp_path: Path) -> None:
        manifest = tmp_path / "MANIFEST"
        manifest.write_text("real.md\nghost.md\n")
        (tmp_path / "real.md").write_text(
            "---\ntitle: R\ntype: chapter\nstatus: draft\n---\n# R\n"
        )
        skipped: list[str] = []
        resolved = resolve_chapters(parse_manifest(manifest), tmp_path, skipped=skipped)
        assert skipped == ["ghost.md"]
        assert len([c for c in resolved if isinstance(c, ChapterSource)]) == 1

    def test_empty_sections_are_dropped(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            ManifestEntry(path="", kind="section", section_title="Empty"),
            ManifestEntry(path="", kind="section", section_title="Full"),
            self._chapter("a.md"),
        ]
        combined, file_count, section_count = assemble_markdown(chapters)
        assert section_count == 1
        assert "# Empty" not in combined
        assert "# Full" in combined

    def test_non_pdf_formats_avoid_latex_newpage(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            self._chapter("a.md"),
            self._chapter("b.md"),
        ]
        combined, _, _ = assemble_markdown(chapters, "html")
        assert "\\newpage" not in combined
        assert "page-break-after" in combined

    def test_footnote_prefixes_unique_for_colliding_paths(self) -> None:
        chapters: list[ManifestEntry | ChapterSource] = [
            self._chapter("a b.md", "X[^1].\n\n[^1]: from space"),
            self._chapter("a_b.md", "Y[^1].\n\n[^1]: from underscore"),
        ]
        combined, _, _ = assemble_markdown(chapters)
        assert "[^a_b_md_0_1]" in combined
        assert "[^a_b_md_1_1]" in combined
