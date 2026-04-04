# Kai Report Creator Color System Design

Date: 2026-04-04
Scope: `kai-report-creator` default report theme and color-behavior rules
Status: Approved in conversation, pending user review of this written spec

## Problem

The current report output feels visually noisy because color is allowed to spread across too many component types at once:

- KPI values can be multi-colored.
- KPI top borders can be multi-colored.
- Delta pills use saturated semantic colors.
- Generic badges/chips use many unrelated hues.
- Table badges inherit the same colorful system, making dense tables feel scattered.

This conflicts with the existing `90/8/2` color discipline documented in `references/design-quality.md`. The result is a report that feels template-driven and "AI-made" rather than editorial, deliberate, and premium.

## Design Goal

Move the default report language toward a **restrained warm business premium** aesthetic:

- warm neutral surfaces instead of cold white + blue dashboard defaults
- one restrained structural color for hierarchy
- one rare warm accent for emphasis
- weak semantic color only where it carries real meaning
- multi-entity color only when the report is explicitly comparative

The target impression is: **premium business brief / strategy memo / polished industry insight**, not "dashboard theme pack."

## Non-Goals

- This spec does not redesign all six built-in themes.
- This spec does not remove semantic meaning from delta/status entirely.
- This spec does not introduce brand-specific palettes.
- This spec does not require colorful entity differentiation in normal single-subject reports.

## Chosen Direction

The approved default palette direction is:

**Pine + Linen**: restrained warm commercial premium

This direction is derived from the approved visual references and has these properties:

- deep neutral text rather than colored text as the baseline
- paper/linen-like warm surfaces
- a subdued pine green as the structural accent
- a restrained amber/gold as a rare editorial highlight
- low-saturation semantic colors for delta/status only

## Core Palette

### Foundation tokens

- `--report-bg: #F8F5EF`
- `--report-surface: #FFFDF9`
- `--report-text: #2B2623`
- `--report-text-muted: #766B63`
- `--report-border: #E7DDD2`
- `--report-structure: #1F6F50`
- `--report-chip-bg: #F4EAD5`
- `--report-chip-text: #7A6858`
- `--report-accent-warm: #C79A2B`

### Semantic tokens

These remain separate from structural and entity color:

- `--report-delta-up-bg`
- `--report-delta-up-text`
- `--report-delta-down-bg`
- `--report-delta-down-text`
- `--report-delta-flat-bg`
- `--report-delta-flat-text`

Recommended tone:

- up: low-saturation green
- down: low-saturation red
- flat/info: low-saturation gray

These colors must read as **quiet indicators**, not visual anchors.

### Comparison-only entity tokens

These are disabled in normal reports and only available in explicit comparison mode:

- `--entity-a: #2F6B50`
- `--entity-b: #6F6A7C`
- `--entity-c: #5C768A`

These are intentionally muted. They are not allowed to become page-wide theme colors.

## Color Allocation Rule

The existing `90/8/2` principle remains in force, with tighter interpretation:

- 90%: warm neutral background, surface, border, body text
- 8%: pine green structural hierarchy
- 2%: rare warm accent or rare semantic hit

Additional rule:

- Outside of charts, a normal page should not feel like it uses more than **2.5 visible colors**.

## Modes

### 1. Default mode

Use for normal reports, KPI reports, business reviews, product reviews, and most single-subject outputs.

Allowed visual language:

- warm neutral surfaces
- deep neutral text
- pine green structural accents
- linen-style generic chips
- weak semantic delta/status colors
- rare warm accent for one-off emphasis

Forbidden in default mode:

- rainbow KPI cards
- multi-colored KPI values
- generic badges in many hues
- table badges with different colors by row/category unless semantically necessary
- using entity colors when no true comparison exists

### 2. Comparison mode

Use only when the report is explicitly comparing multiple subjects such as vendors, competitors, models, or tools.

Additional allowed usage:

- chart series
- legend markers
- entity-name chips
- tiny comparison headers or markers tied to entity identity

Still forbidden in comparison mode:

- each KPI card using a different entity color by default
- entity colors on all badges
- entity colors flooding tables
- entity colors in long-form body text
- turning the whole page into a 3-color system

## Component Rules

### KPI values

- Default KPI values use `--report-text`.
- KPI values do not default to `--report-structure`.
- At most one hero KPI per page may use pine green.
- Multi-KPI sections must rely on layout, spacing, and typography for hierarchy before color.

### KPI cards

- Background uses `--report-surface`.
- Border uses `--report-border`.
- Top rule may use `--report-structure`, but remains thin and restrained.
- No per-card accent palette in default mode.

### Generic chips / badges

- Default chip background uses `--report-chip-bg`.
- Default chip text uses `--report-chip-text`.
- Generic chips are for classification and secondary labeling only.
- Generic chips are not allowed to imply urgency through bright color.

### Delta pills

- Keep semantic distinction.
- Reduce saturation relative to current implementation.
- Up/down/flat remain visually distinguishable, but subordinate to the KPI value itself.

### Table badges

- Table badges default to the same linen chip system as generic badges.
- Only true warning, risk, or exception states may use weak semantic color.
- Dense tables should look calm first, encoded second.

### Section accents

- Top lines, side rules, underlines, and small structural markers may use pine green.
- H1/H2 text should generally remain deep neutral rather than green.
- Structural color belongs to framing, not to every text element.

### Warm accent usage

`--report-accent-warm` is intentionally rare. It may be used for:

- one important editorial highlight
- one opportunity marker
- one emphasized callout or sentence

It must not become:

- the default chip color
- the default KPI color
- the default status color

## Legacy Multicolor Constraint

The old multicolor system must be constrained even when legacy class names still exist.

Current legacy behavior includes classes and attributes such as:

- `data-accent="blue|green|purple|orange|red|teal"`
- `.badge--blue`
- `.badge--green`
- `.badge--purple`
- `.badge--orange`
- `.badge--red`
- `.badge--teal`
- `.badge--done`
- `.badge--wip`
- `.badge--todo`
- `.badge--ok`
- `.badge--warn`
- `.badge--err`

### New rule for legacy classes

Legacy multicolor classes remain syntactically supported for backward compatibility, but they no longer imply vivid visual output by default.

By default:

- old generic badge color classes map to the neutral linen chip system
- old KPI accent variants map back to the restrained default KPI card look
- old colorful table badge variants map to neutral unless explicitly semantic

Exceptions:

- semantic states that truly mean up/down/warn/error may map to weak semantic colors
- explicit comparison-mode entity labels may map to `entity-a/b/c`

Theme-specific workflow/status classes such as `done/wip/todo` or `ok/warn/err` must also be constrained:

- `warn/error` may use weak semantic color
- `done/ok/wip/todo` should prefer neutral or near-neutral treatment unless strong semantic emphasis is genuinely needed

### Practical migration behavior

If old content asks for many colorful badges, the renderer should degrade them into one restrained chip system unless one of these conditions is true:

1. The color carries semantic status meaning.
2. The report is in comparison mode and the color denotes a subject identity.
3. The component is a chart series where color differentiation is required.

This allows compatibility without preserving the old visual noise.

## Triggering Comparison Mode

Comparison mode should only activate when the content clearly compares distinct subjects.

Good triggers:

- multiple named companies compared side by side
- multiple models/vendors/tools compared in a table or chart
- explicit comparative wording such as "A vs B", "competitive landscape", "vendor comparison"

Bad triggers:

- multiple KPIs about one company
- multiple sections in one report
- generic category tags
- normal table rows that happen to contain different labels

If confidence is low, stay in default mode.

## Rendering Priorities

When a component could use either color or structure, prefer this order:

1. Typography
2. Spacing
3. Grouping/layout
4. Border/rule
5. Color

This keeps color from becoming the first and only organizing system.

## Accessibility and Readability

- Body text and KPI values must preserve strong contrast on warm surfaces.
- Linen chips must remain readable without looking heavy.
- Semantic colors must be distinguishable but not neon.
- Comparison colors must remain distinguishable from one another without dominating the page.

## Validation Checklist

Before considering implementation complete, verify:

- normal reports do not show rainbow KPI cards
- generic chips and table chips feel like one family
- KPI values are mostly neutral, not accent-colored
- delta pills are quieter than before
- comparison-mode reports can distinguish entities without turning the page colorful
- legacy color classes no longer explode into many unrelated hues
- page impression is closer to "premium brief" than "dashboard template"

## Implementation Notes for the Next Plan

The execution plan should cover at least:

- shared CSS token additions or replacements
- default component class remapping
- legacy class fallback behavior
- explicit comparison-mode API or heuristic
- regression coverage for default mode vs comparison mode
- demo/fixture updates showing the new visual discipline

## Final Decision Summary

Approved design decisions:

- Default palette direction is warm-neutral commercial premium, not tech-blue minimal.
- KPI numbers return to neutral by default.
- Generic chips and table chips unify into a linen system.
- Semantic color stays only as weak status signaling.
- Multi-entity color becomes explicit and mode-gated.
- Legacy multicolor support is retained only as a compatibility surface, not as a default visual behavior.
