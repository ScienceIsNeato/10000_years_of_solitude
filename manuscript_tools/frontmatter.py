"""YAML frontmatter parser for manuscript files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

import yaml

if TYPE_CHECKING:
    from pathlib import Path

# Status ordering for filtering (class-level constant, not per-instance state)
STATUS_ORDER: dict[str, int] = {
    "placeholder": 0,
    "idea": 1,
    "sketch": 2,
    "draft": 3,
    "polished": 4,
    "final": 5,
}

# Closing fence: a line consisting of exactly --- (optional trailing spaces)
_CLOSING_FENCE = re.compile(r"\n---[ \t]*(?:\r?\n|$)")


def _coerce_int(value: Any, default: int) -> int:
    """Coerce a YAML value to int, falling back to a default on bad input."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_optional_int(value: Any) -> int | None:
    """Coerce a YAML value to int or None on bad/missing input."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@dataclass
class Frontmatter:
    """Parsed YAML frontmatter from a manuscript file."""

    title: str = ""
    type: str = "chapter"  # wiki | chapter | interstitial | sketch
    status: str = "draft"  # placeholder | idea | sketch | draft | polished | final
    draft: int = 1
    pov: str | None = None
    iteration: int | None = None
    era: str | None = None
    todos: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    STATUS_ORDER: ClassVar[dict[str, int]] = STATUS_ORDER

    def status_at_least(self, minimum: str) -> bool:
        """Check if this file's status meets a minimum threshold.

        Raises ValueError for an unknown minimum so typos in --status
        filters fail loudly instead of silently passing every file.
        """
        if minimum not in self.STATUS_ORDER:
            valid = ", ".join(self.STATUS_ORDER)
            raise ValueError(f"Unknown status threshold '{minimum}' (valid: {valid})")
        return self.STATUS_ORDER.get(self.status, -1) >= self.STATUS_ORDER[minimum]


def _frontmatter_from_dict(data: dict[str, Any], default_title: str) -> Frontmatter:
    """Build a Frontmatter from a parsed YAML mapping, coercing bad values."""
    return Frontmatter(
        title=str(data.get("title", default_title)),
        type=str(data.get("type", "chapter")),
        status=str(data.get("status", "draft")),
        draft=_coerce_int(data.get("draft", 1), default=1),
        pov=data.get("pov"),
        iteration=_coerce_optional_int(data.get("iteration")),
        era=data.get("era"),
        todos=data.get("todos") or [],
        raw=data,
    )


def parse_frontmatter(text: str) -> tuple[Frontmatter, str]:
    """Extract YAML frontmatter from markdown text.

    Returns a tuple of (Frontmatter, body_text).
    If no frontmatter is found, returns defaults and the full text.
    """
    stripped = text.lstrip("\n")
    if not stripped.startswith("---"):
        return Frontmatter(), text

    # Find the closing fence: a whole line of exactly '---'. Searching for a
    # bare '\n---' would false-match inline dashes inside the YAML block.
    match = _CLOSING_FENCE.search(stripped, 3)
    if match is None:
        return Frontmatter(), text

    yaml_block = stripped[3 : match.start()].strip()
    body = stripped[match.end() :].lstrip("\n")

    try:
        data: dict[str, Any] = yaml.safe_load(yaml_block) or {}
    except yaml.YAMLError:
        # Broken metadata should not be exported into the book: strip the
        # fence block anyway and fall back to default frontmatter.
        return Frontmatter(), body

    if not isinstance(data, dict):
        return Frontmatter(), body

    return _frontmatter_from_dict(data, default_title=""), body


def load_frontmatter(path: Path) -> tuple[Frontmatter, str]:
    """Load frontmatter from a file path.

    For .md files, reads frontmatter from the file itself.
    For .rtf files, looks for a companion .meta.yaml sidecar.
    """
    ext = path.suffix.lower()

    if ext == ".md":
        text = path.read_text(encoding="utf-8")
        return parse_frontmatter(text)

    if ext == ".rtf":
        sidecar = path.with_suffix(".meta.yaml")
        if sidecar.exists():
            try:
                data = yaml.safe_load(sidecar.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                data = {}
            if isinstance(data, dict):
                return _frontmatter_from_dict(data, default_title=path.stem), ""
        # No sidecar — return defaults derived from filename
        return Frontmatter(title=path.stem, type="chapter"), ""

    return Frontmatter(title=path.stem), ""
