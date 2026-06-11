"""CLI entry point for manuscript build tools."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from manuscript_tools.build import build_manuscript


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="manuscript",
        description="Build tools for the manuscript (working title: Curiosity Killed the Cat (While Turning It Immortal))",
    )
    parser.add_argument(
        "format",
        nargs="?",
        default="pdf",
        choices=["pdf", "docx", "epub", "html", "lint"],
        help="Output format, or 'lint' to run the continuity linter (default: pdf)",
    )
    parser.add_argument(
        "--canon",
        type=Path,
        default=None,
        help="Path to canon.yaml for lint (default: canon.yaml next to MANIFEST)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to MANIFEST file (auto-detected if not specified)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: build/ next to MANIFEST)",
    )
    parser.add_argument(
        "--status",
        type=str,
        default=None,
        choices=["placeholder", "idea", "sketch", "draft", "polished", "final"],
        help="Minimum status threshold",
    )
    parser.add_argument(
        "--type",
        type=str,
        default=None,
        dest="type_filter",
        choices=["wiki", "chapter", "interstitial", "sketch"],
        help="Only include files of this type",
    )
    return parser


def find_manifest() -> Path:
    """Auto-detect the MANIFEST file location."""
    # Check relative to CWD
    candidates = [
        Path("MANIFEST"),
        Path("Manuscript/MANIFEST"),
    ]
    # Check relative to this script's location
    script_dir = Path(__file__).resolve().parent
    candidates.append(script_dir.parent / "Manuscript" / "MANIFEST")

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    print("Error: MANIFEST not found. Use --manifest to specify.", file=sys.stderr)
    sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    manifest_path = args.manifest or find_manifest()
    if not manifest_path.exists():
        print(f"Error: MANIFEST not found at {manifest_path}", file=sys.stderr)
        sys.exit(1)

    if args.format == "lint":
        from manuscript_tools.lint import run_lint

        sys.exit(run_lint(manifest_path, args.canon))

    try:
        result = build_manuscript(
            manifest_path=manifest_path,
            output_format=args.format,
            min_status=args.status,
            type_filter=args.type_filter,
            output_dir=args.output_dir,
        )
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Built: {result.output_path} "
        f"({result.chapter_count} chapters, "
        f"{result.section_count} sections)"
    )

    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)


if __name__ == "__main__":
    main()
