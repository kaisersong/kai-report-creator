# Animated Shell (动效网页报告) — Overview

Route here when frontmatter has `animations: scrollytelling` or
`animations: iridescence`, or the user asks for a **动效网页 / 滚动叙事 /
scrollytelling / 动画长页 / 虹彩 / iridescence** page. This mode produces ONE
animated single-file HTML **web page** (scroll narrative), not the standard
report shell.

Mode recipes: [scrollytelling.md](scrollytelling.md) (dark, GSAP) ·
[iridescence.md](iridescence.md) (light, WebGL hero, zero CDN).

## What changes vs the standard shell

- `references/html-shell/*.md` do **NOT** apply: no TOC sidebar, card mode,
  edit mode, or export menu. **Skip the L2 standard shell ID checks** in
  SKILL.md `--generate` step 11.
- Charts are **hand-built** (SVG + GSAP draw-ins, or CSS bar fills). The
  「ECharts for ALL charts」 rule does NOT apply in this mode.
- Theme CSS files (`templates/themes/*.css`) do not apply; the visual system
  is defined by the mode recipe. `theme_overrides.primary_color` may tint the
  brand ramp.

## Pipeline invariants (still REQUIRED)

1. `scripts/guard_validate.py` on the IR before render.
2. Never fabricate numbers. Undisclosed fields render as 「未公开」 with ghost
   bars (see mode recipes) — never estimate to fill a chart.
3. `<html lang>` + JSON-LD metadata per [output-metadata.md](../output-metadata.md).
4. `report-summary` JSON script (machine-readable KPIs), same contract as the
   standard shell.
5. Root container attributes:
   `data-template="kai-report-creator"`, `data-version="<skill version>"`,
   `data-theme="<animation mode>"`, `data-render-mode="animated"`,
   `data-animation="scrollytelling|iridescence"`.
6. Post-render gate: `scripts/html_quality_gate.py <file>` — the animated
   profile is auto-detected from `data-render-mode="animated"` and replaces
   the standard shell/theme checks with animated assertions (paging JS, play
   mode, font/CDN policy, shader fallback).

## IR mapping

| IR | Animated page |
|---|---|
| `title` / `poster_title` / `abstract` | Hero title + subtitle |
| `##` section | One full scroll section with mono kicker `0N / NAME` |
| `:::kpi` items | KPI cards (CountUp or big-number entrance) |
| `:::chart` | Hand-built animated chart (bars scaleY, line dash draw-in, rings) |
| `:::table` | Comparison table section |
| `:::callout` | Conclusion cel / risk card |
| `must_include` | Sources section content (every claim gets its source + date) |

Drop sections the data cannot support; never pad. 8–10 sections is the
default arc (see mode recipes).

## Frame chrome (both modes, always)

1. **Keyboard section paging**: `→/↓/PageDown/Space` next, `←/↑/PageUp` prev,
   `Home/End` first/last via `scrollIntoView({behavior:'smooth'})`. Maintain a
   dedicated `navSec` index: `goSec()` sets it **immediately**, and a
   per-section observer re-syncs it on real scroll — never step from the
   scroll-tracked index alone. Skip when focus is in an input/textarea.
2. **Play (present) mode**: round ▶ button + `F5` toggle `body.playing` +
   fullscreen; wheel (`passive:false`, ~700ms lock) and click (left quarter =
   back) page exactly ONE section per gesture; `Esc` / leaving fullscreen
   exits. Hide the scroll hint while playing. Do NOT set `overflow:hidden` on
   `body.playing` — it breaks `scrollIntoView` paging.

## Delivery & QA

Write to the requested path (default report filename rules apply). QA = open
in a real browser and scroll end-to-end once: charts fire exactly once,
keyboard paging lands each section, play mode enters/exits fullscreen, no
console errors, KPIs not stuck at 0. Then run
`python scripts/html_quality_gate.py <file>` and fix findings until it passes.
