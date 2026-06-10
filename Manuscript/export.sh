#!/usr/bin/env bash
#
# export.sh — Build the manuscript into a single document.
#
# Usage:
#   ./export.sh              # Defaults to PDF output
#   ./export.sh pdf          # PDF  (via LaTeX)
#   ./export.sh docx         # Word document
#   ./export.sh epub         # EPUB
#   ./export.sh html         # Single-page HTML
#
# Reads MANIFEST for chapter ordering. Supports .md and .rtf input files.
# Output goes to build/ directory.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST="$SCRIPT_DIR/MANIFEST"
BUILD_DIR="$SCRIPT_DIR/build"
TITLE="10,000 Years of Solitude"
AUTHOR=""

FORMAT="${1:-pdf}"

# Validate
if [[ ! -f "$MANIFEST" ]]; then
    echo "Error: MANIFEST not found at $MANIFEST" >&2
    exit 1
fi

if ! command -v pandoc &>/dev/null; then
    echo "Error: pandoc is required. Install with: brew install pandoc" >&2
    exit 1
fi

mkdir -p "$BUILD_DIR"

# Parse MANIFEST into an ordered list of files and section dividers.
# Lines starting with ## are section dividers.
# Lines starting with # (single) are comments.
# Blank lines are ignored.
TMPDIR_EXPORT=$(mktemp -d)
trap 'rm -rf "$TMPDIR_EXPORT"' EXIT

COMBINED="$TMPDIR_EXPORT/combined.md"
: > "$COMBINED"

file_count=0
section_count=0

while IFS= read -r line; do
    # Skip blank lines
    [[ -z "$line" ]] && continue

    # Section divider (##)
    if [[ "$line" =~ ^##\  ]]; then
        section_title="${line#\#\# }"
        # Add a page break and section title
        if (( file_count > 0 || section_count > 0 )); then
            printf '\n\\newpage\n\n' >> "$COMBINED"
        fi
        printf '# %s\n\n' "$section_title" >> "$COMBINED"
        section_count=$((section_count + 1))
        continue
    fi

    # Comment (single #)
    [[ "$line" =~ ^# ]] && continue

    # It's a file path
    filepath="$SCRIPT_DIR/$line"

    if [[ ! -f "$filepath" ]]; then
        echo "Warning: file not found, skipping: $line" >&2
        continue
    fi

    # Add page break between chapters (not before the first one)
    if (( file_count > 0 )); then
        printf '\n\\newpage\n\n' >> "$COMBINED"
    fi

    # Convert file to markdown and append
    ext="${filepath##*.}"
    ext="${ext,,}"  # lowercase

    # Generate unique footnote prefix from filename to avoid collisions
    fn_prefix=$(echo "$line" | sed 's/[^a-zA-Z0-9]/_/g')

    case "$ext" in
        md)
            # Rewrite footnotes to be unique per file
            sed -E "s/\[\^([0-9]+)\]/[^${fn_prefix}_\\1]/g" "$filepath" >> "$COMBINED"
            ;;
        rtf)
            pandoc "$filepath" -t markdown --wrap=none \
                | sed -E "s/\[\^([0-9]+)\]/[^${fn_prefix}_\\1]/g" >> "$COMBINED"
            ;;
        *)
            echo "Warning: unsupported format .$ext, skipping: $line" >&2
            continue
            ;;
    esac

    printf '\n\n' >> "$COMBINED"
    file_count=$((file_count + 1))

done < "$MANIFEST"

if (( file_count == 0 )); then
    echo "Error: no files found in MANIFEST" >&2
    exit 1
fi

# Build output filename
TIMESTAMP=$(date +%Y%m%d)
OUTPUT_BASE="$BUILD_DIR/manuscript_${TIMESTAMP}"

# Format-specific pandoc options
COMMON_OPTS=(
    --from markdown
    --standalone
    --toc
    --toc-depth=2
    --metadata title="$TITLE"
)

# Add author only if set
if [[ -n "$AUTHOR" ]]; then
    COMMON_OPTS+=(--metadata author="$AUTHOR")
fi

case "$FORMAT" in
    pdf)
        OUTPUT="$OUTPUT_BASE.pdf"
        pandoc "$COMBINED" "${COMMON_OPTS[@]}" \
            --pdf-engine=xelatex \
            -V geometry:margin=1in \
            -V fontsize=12pt \
            -V documentclass=report \
            -V linkcolor=black \
            -V urlcolor=black \
            -V mainfont="Times New Roman" \
            -o "$OUTPUT"
        ;;
    docx)
        OUTPUT="$OUTPUT_BASE.docx"
        pandoc "$COMBINED" "${COMMON_OPTS[@]}" \
            -o "$OUTPUT"
        ;;
    epub)
        OUTPUT="$OUTPUT_BASE.epub"
        pandoc "$COMBINED" "${COMMON_OPTS[@]}" \
            -o "$OUTPUT"
        ;;
    html)
        OUTPUT="$OUTPUT_BASE.html"
        pandoc "$COMBINED" "${COMMON_OPTS[@]}" \
            --self-contained \
            -o "$OUTPUT"
        ;;
    *)
        echo "Error: unsupported format '$FORMAT'" >&2
        echo "Supported: pdf, docx, epub, html" >&2
        exit 1
        ;;
esac

echo "Built: $OUTPUT ($file_count chapters, $section_count sections)"
