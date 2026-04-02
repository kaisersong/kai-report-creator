# Content-Aware Component Selection

**Date:** 2026-04-02  
**Status:** Approved

## Problem

Users report that kai-report-creator forces KPI cards and charts into reports that are primarily text-based. The AI mechanically inserts `:::kpi` and `:::chart` placeholders (with `[INSERT VALUE]`) to satisfy the "visual anchor every 4–5 sections" rhythm rule, even when the source content contains no numeric data. This breaks reading flow and looks like AI slop.

The problem occurs in both `--plan` mode (IR generation) and one-step generation mode.

## Solution

Add a **content nature analysis** step before IR planning. Scan the input content, compute numeric density, classify the report as `narrative`, `mixed`, or `data`, then apply component preferences accordingly.

### Numeric Density Calculation

Scan the user's input text (topic description + any raw content provided):

- Count **numeric tokens**: words/phrases that contain digits and carry quantitative meaning — e.g. `128K`, `8.6%`, `¥3200万`, `$1.2B`, `+18%`, `3x`. Exclude ordinals used as labels (`Q3`, `第一`, `Step 2`).
- **Density** = numeric token count / total word count (Chinese: count by character segments; English: count by whitespace-split words)

### Content Nature Classification

| Class | Density | Description |
|-------|---------|-------------|
| `narrative` | < 5% | Primarily text — research, editorial, philosophy, retrospective prose |
| `mixed` | 5–20% | Mix of text and data — project reports, team updates, product reviews |
| `data` | > 20% | Data-heavy — sales dashboards, KPI reports, financial summaries |

### Component Preference by Class

| Class | Visual anchor priority | Prohibited |
|-------|----------------------|------------|
| `narrative` | `:::callout` > `:::timeline` > `:::diagram` > `highlight-sentence` | `:::kpi` and `:::chart` with placeholder values |
| `mixed` | callout/timeline when no numbers present; kpi/chart only when explicit numbers exist in that section | `:::kpi` with all-placeholder values |
| `data` | `:::kpi` > `:::chart` > others (existing behavior unchanged) | — |

**Strict rule for `narrative`:** Never generate a `:::kpi` or `:::chart` block where all values are `[INSERT VALUE]` / `[数据待填写]`. If a section has no numbers, use a different visual anchor.

**Rule for `mixed`:** A `:::kpi` block is only allowed if at least one value in that block is a real number from the source content (not a placeholder).

## Changes Required

### 1. `SKILL.md` — `--plan` mode

Insert **Step 1.5: Content Nature Analysis** between the existing Step 1 (theme suggestion) and Step 2 (plan structure):

```
Step 1.5 — Analyze content nature.
  Compute numeric density from the user's topic/content.
  Classify as narrative / mixed / data.
  Apply component preferences from the routing table below.
  Announce the classification: e.g. "内容以文字叙述为主（narrative），将使用 callout/timeline 作为视觉锚点，不插入空 KPI 占位符。"
```

Add a **Content Nature → Component Routing** table to the `--plan` section (after the chart type selection guidance).

Modify the **visual rhythm rule** in Step 2 item 4:

- Current: "Every 4–5 sections, insert a visual anchor — at least one `:::kpi`, `:::chart`, or `:::diagram` block"
- New: "Every 4–5 sections, insert a visual anchor. Type depends on content nature: narrative → callout/timeline/diagram/highlight-sentence; mixed → callout/timeline unless real numbers present; data → kpi/chart (existing behavior)."

### 2. `references/design-quality.md` — Section 4 (Forbidden Patterns)

Add two rows to the anti-slop table:

| ❌ Forbidden | ✅ Instead |
|---|---|
| `:::kpi` block where every value is `[INSERT VALUE]` in a narrative report | Use `:::callout` or `:::timeline` as the visual anchor |
| `:::chart` with fabricated/placeholder data in a text-heavy section | Use `:::diagram` (flowchart/mindmap) or `highlight-sentence` |

### 3. `references/design-quality.md` — Section 7 (Pre-Output Self-Check)

Add one checklist item:

```
- [ ] Does any :::kpi or :::chart block contain only placeholder values in a narrative/mixed report? If yes → replace with callout, timeline, or diagram.
```

## Non-Changes

- `--generate` mode rendering rules: unchanged. The fix is upstream (IR generation), not downstream (HTML rendering).
- Existing `data` class behavior: fully preserved.
- Theme routing, color rules, typography rules: unchanged.

## Success Criteria

1. A text-heavy research report (e.g. "AI认知框架研究") generates zero `:::kpi` blocks with placeholder values.
2. A mixed report (e.g. "Q1项目复盘") only generates `:::kpi` for sections that contain real numbers.
3. A data report (e.g. "Q3销售季报") behaves exactly as before.
4. Narrative reports still have visual rhythm — callout/timeline/diagram appear every 4–5 sections.
