# Content-Aware Component Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent kai-report-creator from inserting empty KPI/chart placeholders into text-heavy reports by classifying content as `narrative`, `mixed`, or `data` and routing visual anchors accordingly.

**Architecture:** Two files change. `SKILL.md` gets a new Step 1.5 (content nature analysis) inserted into `--plan` mode, plus updated visual rhythm rules. `references/design-quality.md` gets two new forbidden-pattern rows and one new pre-output self-check item. No new files, no rendering changes.

**Tech Stack:** Markdown/text editing only — no code, no tests required. Changes are prompt-engineering rules inside skill files.

---

### Task 1: Add Content Nature Analysis step to SKILL.md

**Files:**
- Modify: `SKILL.md` (lines 131–172, the `--plan Mode` section)

This task inserts Step 1.5 between Step 1 and Step 2, and adds the Content Nature → Component Routing table after the chart type selection guidance (item 3).

- [ ] **Step 1: Read the current --plan Mode section to confirm line numbers**

Read `SKILL.md` lines 131–172. Verify:
- Line 137: `**Step 1 — Suggest theme.**`
- Line 139: `**Step 2 — Plan the structure.**`

- [ ] **Step 2: Insert Step 1.5 between Step 1 and Step 2**

In `SKILL.md`, find the exact text:

```
**Step 2 — Plan the structure.**
```

Replace with:

```
**Step 1.5 — Analyze content nature.**

Scan the user's topic/content input and compute numeric density:
- Count **numeric tokens**: words/phrases containing digits with quantitative meaning — e.g. `128K`, `8.6%`, `¥3200万`, `$1.2B`, `+18%`, `3x`. Exclude ordinals used as labels (`Q3`, `第一`, `Step 2`).
- **Density** = numeric token count / total word count (Chinese: character-segment count; English: whitespace-split word count)

Classify:

| Class | Density | Description |
|-------|---------|-------------|
| `narrative` | < 5% | Primarily text — research, editorial, philosophy, retrospective prose |
| `mixed` | 5–20% | Mix of text and data — project reports, team updates, product reviews |
| `data` | > 20% | Data-heavy — sales dashboards, KPI reports, financial summaries |

Announce the classification to the user. Examples:
- narrative: "内容以文字叙述为主（narrative），将使用 callout/timeline 作为视觉锚点，不插入空 KPI 占位符。"
- mixed: "内容为图文混合（mixed），有明确数字的章节才会使用 KPI/图表组件。"
- data: "内容以数据为主（data），将使用 KPI/图表作为主要视觉锚点。"
- (English equivalent when `lang: en`)

**Step 2 — Plan the structure.**
```

- [ ] **Step 3: Verify the insertion looks correct**

Read `SKILL.md` lines 131–185. Confirm:
- Step 1 (theme suggestion) is still present
- Step 1.5 (content nature analysis) appears between Step 1 and Step 2
- Step 2 header is intact and unchanged

- [ ] **Step 4: Commit**

```bash
cd /Users/song/projects/report-creator
git add SKILL.md
git commit -m "feat: add content nature analysis step to --plan mode"
```

---

### Task 2: Add Content Nature → Component Routing table to SKILL.md

**Files:**
- Modify: `SKILL.md` (inside Step 2, after chart type selection guidance item 3)

This task adds the routing table that maps content class to allowed/preferred visual anchor components.

- [ ] **Step 1: Find the insertion point**

In `SKILL.md`, locate the exact text that ends item 3 (chart type selection guidance):

```
   - Do NOT use sankey for simple proportions (use pie) or ordered stages with no branching (use funnel).
```

- [ ] **Step 2: Insert the routing table after item 3**

After the line above, insert (before item 4):

```

3.5. **Content Nature → Component Routing** — apply based on the class determined in Step 1.5:

| Class | Preferred visual anchors | Prohibited |
|-------|--------------------------|------------|
| `narrative` | `:::callout`, `:::timeline`, `:::diagram`, `highlight-sentence` | `:::kpi` and `:::chart` with all-placeholder values |
| `mixed` | `:::callout`/`:::timeline` by default; `:::kpi`/`:::chart` only when that section contains real numbers from the source | `:::kpi` where every value is a placeholder |
| `data` | `:::kpi` > `:::chart` > others | — (existing behavior) |

**narrative strict rule:** Never generate a `:::kpi` or `:::chart` block where all values are `[数据待填写]` / `[INSERT VALUE]`. If a section has no numbers, use `:::callout`, `:::timeline`, or `:::diagram` instead.

**mixed rule:** A `:::kpi` block is only allowed if at least one value in that block is a real number extracted from the source content.

```

- [ ] **Step 3: Verify the insertion**

Read `SKILL.md` lines 150–175. Confirm:
- Item 3 (chart type guidance) ends with the sankey rule
- Item 3.5 (routing table) appears immediately after
- Item 4 (visual rhythm rules) follows after

- [ ] **Step 4: Commit**

```bash
cd /Users/song/projects/report-creator
git add SKILL.md
git commit -m "feat: add content nature component routing table"
```

---

### Task 3: Update visual rhythm rules in SKILL.md

**Files:**
- Modify: `SKILL.md` (item 4 inside Step 2, the visual rhythm rules)

This task replaces the current blanket "insert kpi/chart/diagram" rule with a content-class-aware version.

- [ ] **Step 1: Find the exact text to replace**

In `SKILL.md`, locate item 4 exactly:

```
4. **Apply visual rhythm rules** when laying out sections:
   - Never place 3 or more consecutive sections containing only plain Markdown prose (no components)
   - Ideal section rhythm: `prose → kpi → chart/table → callout/timeline → prose → ...`
   - Every 4–5 sections, insert a "visual anchor" — at least one `:::kpi`, `:::chart`, or `:::diagram` block
   - If a topic area would generate 3+ consecutive prose sections, break it up by inserting a `:::callout` or `:::kpi` with placeholder values
```

- [ ] **Step 2: Replace item 4 with the updated version**

Replace the text above with:

```
4. **Apply visual rhythm rules** when laying out sections:
   - Never place 3 or more consecutive sections containing only plain Markdown prose (no components)
   - Every 4–5 sections, insert a "visual anchor" — type depends on content class from Step 1.5:
     - `narrative`: use `:::callout`, `:::timeline`, `:::diagram`, or a `highlight-sentence` paragraph
     - `mixed`: use `:::callout`/`:::timeline` by default; use `:::kpi`/`:::chart` only if that section has real numbers
     - `data`: use `:::kpi` or `:::chart` (existing behavior)
   - Ideal rhythm by class:
     - `narrative`: `prose → callout → prose → timeline → prose → diagram → ...`
     - `mixed`: `prose → callout → prose → kpi(if numbers) → prose → timeline → ...`
     - `data`: `prose → kpi → chart/table → callout/timeline → prose → ...`
   - **Never** break up consecutive prose sections by inserting a `:::kpi` with placeholder values in `narrative` or `mixed` reports — use `:::callout` instead
```

- [ ] **Step 3: Verify the change**

Read `SKILL.md` lines 155–175. Confirm:
- Item 4 now references content class (narrative/mixed/data)
- The old "insert :::kpi with placeholder values" fallback is gone
- Item 3.5 routing table is still present above item 4

- [ ] **Step 4: Commit**

```bash
cd /Users/song/projects/report-creator
git add SKILL.md
git commit -m "feat: update visual rhythm rules to respect content class"
```

---

### Task 4: Add forbidden patterns to design-quality.md

**Files:**
- Modify: `references/design-quality.md` (Section 4, the anti-slop table)

- [ ] **Step 1: Find the end of the forbidden patterns table**

In `references/design-quality.md`, locate the last row of the Section 4 table:

```
| Inter as body font | Use system-ui / -apple-system stack (already in themes) |
```

- [ ] **Step 2: Append two new rows to the table**

After the line above, insert:

```
| `:::kpi` block where every value is `[INSERT VALUE]` / `[数据待填写]` in a narrative report | Use `:::callout` or `:::timeline` as the visual anchor instead |
| `:::chart` with all-placeholder data in a text-heavy (narrative/mixed) section | Use `:::diagram` (flowchart/mindmap) or a `highlight-sentence` paragraph |
```

- [ ] **Step 3: Verify**

Read `references/design-quality.md` lines 50–70. Confirm the table now has 10 rows (8 original + 2 new) and the new rows appear at the bottom.

- [ ] **Step 4: Commit**

```bash
cd /Users/song/projects/report-creator
git add references/design-quality.md
git commit -m "feat: add narrative/mixed placeholder-kpi forbidden patterns"
```

---

### Task 5: Add pre-output self-check item to design-quality.md

**Files:**
- Modify: `references/design-quality.md` (Section 7, the pre-output self-check checklist)

- [ ] **Step 1: Find the last checklist item**

In `references/design-quality.md`, locate the last item in Section 7:

```
- [ ] **If you told someone "an AI wrote this", would they immediately believe it?** If yes → find the most generic-looking part and redesign it
```

- [ ] **Step 2: Insert new checklist item before the last item**

Insert before the line above:

```
- [ ] Does any `:::kpi` or `:::chart` block contain only placeholder values (`[INSERT VALUE]` / `[数据待填写]`) in a `narrative` or `mixed` report? If yes → replace with `:::callout`, `:::timeline`, or `:::diagram`
```

- [ ] **Step 3: Verify**

Read `references/design-quality.md` lines 106–117. Confirm the checklist now has 8 items, with the new placeholder-check item second-to-last.

- [ ] **Step 4: Commit**

```bash
cd /Users/song/projects/report-creator
git add references/design-quality.md
git commit -m "feat: add placeholder-kpi pre-output self-check item"
```

---

### Task 6: Smoke test — narrative report

Verify the changes work end-to-end by running `/report --plan` on a text-heavy topic and checking the output IR contains no all-placeholder kpi/chart blocks.

- [ ] **Step 1: Run a narrative report plan**

In a Claude Code session with the updated skill, run:

```
/report --plan "AI认知框架研究：从感知到推理的演化路径"
```

- [ ] **Step 2: Check the generated IR file**

Open the generated `report-*.report.md` file. Verify:
1. The skill announced `narrative` classification
2. No `:::kpi` block exists where all values are `[数据待填写]`
3. No `:::chart` block exists with all-placeholder data
4. Visual anchors present: at least one `:::callout`, `:::timeline`, or `:::diagram` per 4–5 sections

- [ ] **Step 3: Smoke test — data report (regression check)**

Run:

```
/report --plan "Q3销售季报：营收、转化率与用户增长"
```

Open the generated IR. Verify:
1. The skill announced `data` classification
2. `:::kpi` blocks are present with placeholder values (this is correct for data reports)
3. `:::chart` blocks are present
4. Behavior matches pre-change behavior

- [ ] **Step 4: Smoke test — mixed report**

Run:

```
/report --plan "Q1项目复盘：团队协作、交付节奏与3个关键决策"
```

Open the generated IR. Verify:
1. The skill announced `mixed` classification
2. Any `:::kpi` block that appears has at least one real number (not all placeholders)
3. Sections without numbers use `:::callout` or `:::timeline` as anchors

- [ ] **Step 5: Commit smoke test notes (optional)**

If any issues found during smoke test, fix the relevant task's changes and re-commit. No separate commit needed if all tests pass.
