"""YAML frontmatter parser for manuscript files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


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

    # Status ordering for filtering
    STATUS_ORDER: dict[str, int] = field(
        default_factory=lambda: {
            "placeholder": 0,
            "idea": 1,
            "sketch": 2,
            "draft": 3,
            "polished": 4,
            "final": 5,
        },
        repr=False,
    )

    def status_at_least(self, minimum: str) -> bool:
        """Check if this file's status meets a minimum threshold."""
        return self.STATUS_ORDER.get(self.status, -1) >= self.STATUS_ORDER.get(
            minimum, 0
        )


def parse_frontmatter(text: str) -> tuple[Frontmatter, str]:
    """Extract YAML frontmatter from markdown text.

    Returns a tuple of (Frontmatter, body_text).
    If no frontmatter is found, returns defaults and the full text.
    """
    stripped = text.lstrip("\n")
    if not stripped.startswith("---"):
        return Frontmatter(), text

    # Find closing ---
    end_idx = stripped.find("\n---", 3)
    if end_idx == -1:
        return Frontmatter(), text

    yaml_block = stripped[3:end_idx].strip()
    body = stripped[end_idx + 4 :].lstrip("\n")

    try:
        data: dict[str, Any] = yaml.safe_load(yaml_block) or {}
    except yaml.YAMLError:
        return Frontmatter(), text

    if not isinstance(data, dict):
        return Frontmatter(), text

    fm = Frontmatter(
        title=str(data.get("title", "")),
        type=str(data.get("type", "chapter")),
        status=str(data.get("status", "draft")),
        draft=int(data.get("draft", 1)),
        pov=data.get("pov"),
        iteration=data.get("iteration"),
        era=data.get("era"),
        todos=data.get("todos") or [],
        raw=data,
    )
    return fm, body


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
                fm = Frontmatter(
                    title=str(data.get("title", path.stem)),
                    type=str(data.get("type", "chapter")),
                    status=str(data.get("status", "draft")),
                    draft=int(data.get("draft", 1)),
                    pov=data.get("pov"),
                    iteration=data.get("iteration"),
                    era=data.get("era"),
                    todos=data.get("todos") or [],
                    raw=data,
                )
                return fm, ""
        # No sidecar — return defaults derived from filename
        return Frontmatter(title=path.stem, type="chapter"), ""

    return Frontmatter(title=path.stem), ""
