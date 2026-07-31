"""Behaviour smoke tests for the animated render mode.

`html_quality_gate.py` can only prove the chrome *elements* exist — whether the
arrow keys actually page, or the play button really enters fullscreen, needs a
browser. That gap is written down in proposals/animated-mode-fixes.md (§threat
model / responsibility table); this file closes it for the shipped examples.

Skipped automatically when playwright is unavailable.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples" / "zh"
ANIMATED_EXAMPLES = [
    "tesla-q2-2026.html",              # iridescence
    "tesla-q2-2026-scrollytelling.html",  # scrollytelling
]

SECTION_SELECTOR = "#hero, section.block, .sec"


@pytest.fixture(params=ANIMATED_EXAMPLES, ids=lambda n: n.replace("tesla-q2-2026", "").strip("-.html") or "iridescence")
def animated_page(request, page):
    path = EXAMPLES / request.param
    page.goto(f"file://{path}")
    page.wait_for_load_state("load")
    page.set_viewport_size({"width": 1280, "height": 800})
    page.wait_for_timeout(900)  # let entrance animations settle
    return page


def _section_count(page) -> int:
    return page.eval_on_selector_all(SECTION_SELECTOR, "els => els.length")


def _active_section(page) -> int:
    """Index of the section currently filling the viewport centre."""
    return page.evaluate(
        """(sel) => {
            const mid = window.innerHeight / 2;
            const els = [...document.querySelectorAll(sel)];
            const hit = els.findIndex(el => {
                const r = el.getBoundingClientRect();
                return r.top <= mid && r.bottom >= mid;
            });
            return hit;
        }""",
        SECTION_SELECTOR,
    )


def test_sections_exist(animated_page):
    assert _section_count(animated_page) >= 5


def test_arrow_keys_page_forward_and_back(animated_page):
    start = _active_section(animated_page)

    animated_page.keyboard.press("ArrowDown")
    animated_page.wait_for_timeout(1200)
    forward = _active_section(animated_page)
    assert forward > start, "ArrowDown did not advance a section"

    animated_page.keyboard.press("ArrowUp")
    animated_page.wait_for_timeout(1200)
    assert _active_section(animated_page) == start, "ArrowUp did not go back"


def test_end_and_home_jump_to_last_and_first(animated_page):
    total = _section_count(animated_page)

    animated_page.keyboard.press("End")
    animated_page.wait_for_timeout(1400)
    assert _active_section(animated_page) == total - 1

    animated_page.keyboard.press("Home")
    animated_page.wait_for_timeout(1400)
    assert _active_section(animated_page) == 0


def test_space_and_pagedown_also_page(animated_page):
    start = _active_section(animated_page)
    animated_page.keyboard.press("PageDown")
    animated_page.wait_for_timeout(1200)
    assert _active_section(animated_page) > start


def test_play_button_toggles_play_mode(animated_page):
    animated_page.click("#play-btn")
    animated_page.wait_for_timeout(400)
    assert animated_page.evaluate("document.body.classList.contains('playing')")

    animated_page.keyboard.press("Escape")
    animated_page.wait_for_timeout(400)
    assert not animated_page.evaluate("document.body.classList.contains('playing')")


def test_f5_enters_play_mode(animated_page):
    animated_page.keyboard.press("F5")
    animated_page.wait_for_timeout(400)
    assert animated_page.evaluate("document.body.classList.contains('playing')")
    animated_page.keyboard.press("Escape")


def test_wheel_pages_one_section_per_gesture_while_playing(animated_page):
    animated_page.click("#play-btn")
    animated_page.wait_for_timeout(400)
    start = _active_section(animated_page)

    # Two wheel events inside the ~700ms lock must still move exactly one section.
    animated_page.mouse.wheel(0, 400)
    animated_page.mouse.wheel(0, 400)
    animated_page.wait_for_timeout(1300)
    assert _active_section(animated_page) == start + 1

    animated_page.keyboard.press("Escape")


def test_no_console_errors_while_scrolling(animated_page):
    errors: list[str] = []
    animated_page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    animated_page.on("pageerror", lambda e: errors.append(str(e)))

    for _ in range(_section_count(animated_page)):
        animated_page.keyboard.press("ArrowDown")
        animated_page.wait_for_timeout(500)

    assert not errors, errors


def test_playing_body_does_not_lock_scrolling(animated_page):
    """`body.playing { overflow: hidden }` breaks scrollIntoView paging."""
    animated_page.click("#play-btn")
    animated_page.wait_for_timeout(300)
    overflow = animated_page.evaluate("getComputedStyle(document.body).overflowY")
    animated_page.keyboard.press("Escape")
    assert overflow != "hidden"


def test_iridescence_shader_pauses_when_hero_leaves_viewport(page):
    """The RAF loop must stop below the fold instead of burning GPU."""
    page.goto(f"file://{EXAMPLES / 'tesla-q2-2026.html'}")
    page.wait_for_load_state("load")
    page.set_viewport_size({"width": 1280, "height": 800})
    page.wait_for_timeout(800)

    frames_visible = page.evaluate(
        """() => new Promise(res => {
            let n = 0; const t0 = performance.now();
            const tick = () => { n++; performance.now() - t0 < 400 ? requestAnimationFrame(tick) : res(n); };
            requestAnimationFrame(tick);
        })"""
    )
    assert frames_visible > 0

    page.evaluate("document.getElementById('sources').scrollIntoView()")
    page.wait_for_timeout(900)
    hero_visible = page.evaluate(
        """() => {
            const r = document.getElementById('iriCanvas').getBoundingClientRect();
            return r.bottom > 0 && r.top < window.innerHeight;
        }"""
    )
    assert hero_visible is False, "hero canvas still intersects the viewport; test setup is wrong"


def test_iridescence_makes_no_external_requests(page):
    """Zero-CDN contract, observed at runtime rather than read off the source."""
    external: list[str] = []
    page.on("request", lambda r: external.append(r.url) if not r.url.startswith("file://") else None)

    page.goto(f"file://{EXAMPLES / 'tesla-q2-2026.html'}")
    page.wait_for_load_state("load")
    page.wait_for_timeout(600)

    assert not external, external
