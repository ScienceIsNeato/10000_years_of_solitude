"""Tests for the CLI module."""

from pathlib import Path
from unittest.mock import patch

from manuscript_tools.cli import create_parser, find_manifest, main


class TestCreateParser:
    def test_default_format_is_pdf(self) -> None:
        parser = create_parser()
        args = parser.parse_args([])
        assert args.format == "pdf"

    def test_explicit_format(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["html"])
        assert args.format == "html"

    def test_manifest_flag(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["--manifest", "/some/path/MANIFEST"])
        assert args.manifest == Path("/some/path/MANIFEST")

    def test_status_flag(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["--status", "polished"])
        assert args.status == "polished"

    def test_type_filter_flag(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["--type", "wiki"])
        assert args.type_filter == "wiki"

    def test_output_dir_flag(self) -> None:
        parser = create_parser()
        args = parser.parse_args(["--output-dir", "/tmp/build"])
        assert args.output_dir == Path("/tmp/build")


class TestFindManifest:
    def test_finds_manifest_in_cwd(self, tmp_path: Path, monkeypatch: object) -> None:
        import os

        manifest = tmp_path / "MANIFEST"
        manifest.write_text("## Section\nfile.md\n")
        monkeypatch.setattr(os, "chdir", lambda p: None)  # type: ignore[attr-defined]
        # Patch Path to resolve relative to tmp_path
        with patch("manuscript_tools.cli.Path") as mock_path:
            # First candidate: Path("MANIFEST")
            mock_manifest = tmp_path / "MANIFEST"
            mock_sub_manifest = tmp_path / "Manuscript" / "MANIFEST"

            def path_side_effect(arg: str) -> Path:
                if arg == "MANIFEST":
                    return mock_manifest
                if arg == "Manuscript/MANIFEST":
                    return mock_sub_manifest
                return Path(arg)

            mock_path.side_effect = path_side_effect
            mock_path.__class__ = type(Path())

            result = find_manifest()
            assert result.name == "MANIFEST"


class TestMain:
    def test_main_with_manifest(self, tmp_path: Path) -> None:
        # Create a minimal manuscript
        manifest = tmp_path / "MANIFEST"
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test Chapter\n\nSome content here.\n")
        manifest.write_text("test.md\n")
        build_dir = tmp_path / "build"

        with patch("manuscript_tools.cli.build_manuscript") as mock_build:
            from manuscript_tools.build import BuildResult

            mock_build.return_value = BuildResult(
                output_path=build_dir / "manuscript_20260414.pdf",
                chapter_count=1,
                section_count=0,
            )
            main(
                [
                    "pdf",
                    "--manifest",
                    str(manifest),
                    "--output-dir",
                    str(build_dir),
                ]
            )
            mock_build.assert_called_once()

    def test_main_missing_manifest_exits(self, tmp_path: Path) -> None:
        fake_manifest = tmp_path / "nonexistent" / "MANIFEST"
        try:
            main(["pdf", "--manifest", str(fake_manifest)])
            raise AssertionError("Should have exited")
        except SystemExit as e:
            assert e.code == 1

    def test_main_prints_warnings(self, tmp_path: Path, capsys: object) -> None:
        manifest = tmp_path / "MANIFEST"
        manifest.write_text("test.md\n")
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\nContent.\n")
        build_dir = tmp_path / "build"

        with patch("manuscript_tools.cli.build_manuscript") as mock_build:
            from manuscript_tools.build import BuildResult

            mock_build.return_value = BuildResult(
                output_path=build_dir / "out.pdf",
                chapter_count=1,
                section_count=0,
                warnings=["Some warning"],
            )
            main(
                [
                    "pdf",
                    "--manifest",
                    str(manifest),
                    "--output-dir",
                    str(build_dir),
                ]
            )
            captured = capsys.readouterr()  # type: ignore[union-attr]
            assert "Some warning" in captured.err


class TestLintDispatch:
    def test_lint_runs_and_exits_clean(self, tmp_path: Path) -> None:
        chapter = tmp_path / "a.md"
        chapter.write_text(
            "---\ntitle: A\ntype: chapter\nstatus: draft\n---\n# A\n\nProse.\n"
        )
        (tmp_path / "MANIFEST").write_text("a.md\n")
        (tmp_path / "canon.yaml").write_text("characters: []\n")
        import pytest

        with pytest.raises(SystemExit) as exc:
            main(["lint", "--manifest", str(tmp_path / "MANIFEST")])
        assert exc.value.code == 0

    def test_lint_exits_nonzero_on_errors(self, tmp_path: Path) -> None:
        chapter = tmp_path / "a.md"
        chapter.write_text(
            "---\ntitle: A\ntype: chapter\nstatus: draft\n---\n# A\n\n"
            "It happened on October 26.\n"
        )
        (tmp_path / "MANIFEST").write_text("a.md\n")
        (tmp_path / "canon.yaml").write_text("characters: []\n")
        import pytest

        with pytest.raises(SystemExit) as exc:
            main(["lint", "--manifest", str(tmp_path / "MANIFEST")])
        assert exc.value.code == 1


class TestErrorExits:
    def test_missing_manifest_exits(self, tmp_path: Path) -> None:
        import pytest

        with pytest.raises(SystemExit) as exc:
            main(["html", "--manifest", str(tmp_path / "NOPE")])
        assert exc.value.code == 1

    def test_find_manifest_failure_exits(self) -> None:
        import pytest

        with (
            patch("pathlib.Path.exists", return_value=False),
            pytest.raises(SystemExit) as exc,
        ):
            find_manifest()
        assert exc.value.code == 1
