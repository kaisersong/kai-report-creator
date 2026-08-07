"""Anchor-block regression tests for the forest-editorial theme.

The deep forest-green header block is this theme's identifying feature, but it
was scoped to `.report-wrapper > h1:first-of-type` while the standard shell
wraps h1 in `.title-row` to seat the summary-card button. Every generated report
therefore rendered a plain title with no anchor and no gold eyebrow, and only
the older hand-built preview decks still looked right.

The fingerprint markers in html_quality_gate.py cannot catch this: they check
that declarations are present, not that they still match the shipped DOM. These
tests pin the computed result for both structures.

Skipped automatically when playwright is unavailable.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME_CSS = ROOT / "templates" / "themes" / "forest-editorial.css"
ANCHOR_GRADIENT = "linear-gradient(150deg, rgb(16, 45, 39), rgb(23, 63, 53))"
EYEBROW_GOLD = "rgb(199, 149, 29)"

BARE_TITLE = "<h1>T</h1>"
WRAPPED_TITLE = (
    '<div class="title-row"><h1>T</h1>'
    '<button class="card-mode-btn" id="card-mode-btn">S</button></div>'
)


def _document(title_markup: str) -> str:
    return f"""<!DOCTYPE html><html lang="en" data-theme="forest-editorial"><head><style>
    :root {{ --font-sans: system-ui; }}
    .title-row {{ display: flex; align-items: flex-end; gap: 1rem; }}
    .title-row h1 {{ flex: 1; }}
    .card-mode-btn {{ background: var(--surface); border: 1px solid var(--border); }}
    {THEME_CSS.read_text(encoding="utf-8")}
    </style></head><body><main class="main-with-toc"><div class="report-wrapper">
    {title_markup}<p class="report-meta">m</p>
    </div></main></body></html>"""


def _anchor_styles(page, title_markup: str, selector: str) -> tuple[str, str]:
    page.set_content(_document(title_markup))
    background = page.eval_on_selector(selector, "el => getComputedStyle(el).backgroundImage")
    eyebrow = page.eval_on_selector(
        selector, "el => getComputedStyle(el, '::before').backgroundColor"
    )
    return background, eyebrow


def test_anchor_renders_for_bare_h1(page):
    background, eyebrow = _anchor_styles(page, BARE_TITLE, "h1")
    assert background == ANCHOR_GRADIENT
    assert eyebrow == EYEBROW_GOLD


def test_anchor_renders_when_shell_wraps_h1_in_title_row(page):
    background, eyebrow = _anchor_styles(page, WRAPPED_TITLE, ".title-row")
    assert background == ANCHOR_GRADIENT
    assert eyebrow == EYEBROW_GOLD


def test_wrapped_h1_does_not_stack_a_second_anchor(page):
    page.set_content(_document(WRAPPED_TITLE))
    inner = page.eval_on_selector(
        ".title-row > h1", "el => getComputedStyle(el).backgroundImage"
    )
    assert inner == "none"


def test_summary_card_button_is_legible_on_the_anchor(page):
    page.set_content(_document(WRAPPED_TITLE))
    colour = page.eval_on_selector("#card-mode-btn", "el => getComputedStyle(el).color")
    assert colour == "rgb(232, 239, 233)"
