#!/usr/bin/env python3
"""Build theme-skinning comparisons from one frozen fixture.

The fixture DOM never changes, so any visual difference between outputs comes
from CSS alone. That is what makes "does this theme actually look different?"
answerable — AI-rendered sample reports drift in wording and structure, which
pollutes the comparison.

Assembly follows references/theme-css.md exactly:
  built-in : <theme before POST-SHARED> + shared.css + <theme after POST-SHARED>
  custom   : minimal (before POST-SHARED) + shared.css + minimal (after) + :root
             overrides, then optional extra overrides

Usage:
    python tests/fixtures/skin_fixture.py minimal dark-board forest-editorial
    python tests/fixtures/skin_fixture.py dark-board --overrides primary_color=#5ee1b4 --label radar-board
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = Path(__file__).resolve().parent / "theme-skin-fixture.html"
BUILTIN_DIR = ROOT / "templates" / "themes"
CUSTOM_DIR = ROOT / "themes"
POST_SHARED_MARKER = "/* === POST-SHARED OVERRIDE"


def split_theme(css: str) -> tuple[str, str]:
    """Return (before, after) around the POST-SHARED marker."""
    if POST_SHARED_MARKER not in css:
        return css, ""
    head, _, tail = css.partition(POST_SHARED_MARKER)
    return head, tail


def assemble_css(theme: str, overrides: dict[str, str] | None = None) -> str:
    shared = (BUILTIN_DIR / "shared.css").read_text(encoding="utf-8")
    builtin = BUILTIN_DIR / f"{theme}.css"
    custom = CUSTOM_DIR / theme / "theme.css"

    if builtin.exists():
        before, after = split_theme(builtin.read_text(encoding="utf-8"))
    elif custom.exists():
        base_before, base_after = split_theme((BUILTIN_DIR / "minimal.css").read_text(encoding="utf-8"))
        before = base_before
        after = f"{base_after}\n{custom.read_text(encoding='utf-8')}"
    else:
        raise SystemExit(f"unknown theme: {theme}")

    parts = [before, shared, after]
    if overrides:
        mapped = {"primary_color": "--primary", "font_family": "--font-sans"}
        decls = "".join(f"  {mapped.get(k, '--' + k)}: {v};\n" for k, v in overrides.items())
        parts.append(f"/* theme_overrides */\n:root {{\n{decls}}}\n")
    return "\n".join(parts)


def render(theme: str, label: str, overrides: dict[str, str] | None, out_dir: Path) -> Path:
    html = FIXTURE.read_text(encoding="utf-8")
    html = html.replace("__THEME_CSS__", assemble_css(theme, overrides))
    html = html.replace("__THEME_NAME__", label)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"skin-{label}.html"
    target.write_text(html, encoding="utf-8")
    return target


def parse_overrides(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        key, _, value = item.partition("=")
        if not value:
            raise SystemExit(f"--overrides expects key=value, got {item!r}")
        out[key.strip()] = value.strip()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("themes", nargs="+", help="built-in or themes/<name> theme ids")
    parser.add_argument("--overrides", nargs="*", default=[], help="key=value theme_overrides (applied to every theme)")
    parser.add_argument("--label", help="output label (only valid with a single theme)")
    parser.add_argument("--out", default="/tmp/theme-skin", help="output directory")
    args = parser.parse_args()

    if args.label and len(args.themes) != 1:
        raise SystemExit("--label only applies to a single theme")

    overrides = parse_overrides(args.overrides)
    out_dir = Path(args.out)
    for theme in args.themes:
        label = args.label or theme
        print(render(theme, label, overrides, out_dir))


if __name__ == "__main__":
    main()
