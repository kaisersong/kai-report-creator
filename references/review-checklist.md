# Report Review Checklist

Load this file when `--review` is called and as the silent final review pass during `--generate`.

This checklist is designed for **one-pass automatic refinement**. It is not an interactive approval workflow.

## Overview

The report review system keeps only the rules that fit `kai-report-creator`'s operating model:

- the AI can judge the issue from source/IR/HTML alone
- the AI can fix it directly with a rewrite or structural adjustment
- the rule does not depend on outside human feedback or image-level interpretation

The system has **8 checkpoints**:

- **Category 1: Hard Rules (5)** — auto-apply when violated
- **Category 2: AI-Advised Rules (3)** — apply only when confidence is high

## Category 1: Hard Rules

These rules are deterministic enough to apply automatically.

### 1.1 BLUF Opening

**Trigger:** Every report.

**Detection:** Check the opening paragraph. It should establish at least two of:

- the document's purpose
- the core finding
- the expected action

If the opening is mostly background, definitions, or scene-setting, it fails.

**Auto-fix:** Rewrite the first paragraph into a short executive summary:

- sentence 1: what this report is for
- sentence 2: the main finding or most important judgment
- sentence 3: what the reader should do, watch, or decide next

**Fallback:** If the source does not support a concrete action, keep purpose + finding and avoid inventing a recommendation.

### 1.2 Heading Stack Logic

**Trigger:** Reports with H1/H2/H3 structure.

**Detection:** Read the heading stack alone. It should form a meaningful outline, not a bag of disconnected nouns.

Bad patterns:

- headings that are all pure labels
- repeated generic section types with no progression
- adjacent headings that do not imply problem, mechanism, implication, or action

**Auto-fix:** Rewrite headings into information-bearing statements that preserve the original content but improve progression.

**Fallback:** If the overall outline is sound, only rewrite the weak headings rather than reordering sections.

### 1.3 Anti-Template Section Headings

**Trigger:** Every H2/H3.

**Detection:** Flag headings such as:

- `Overview`
- `Background`
- `Key Findings`
- `Summary`
- `Next Steps`
- `问题分析`
- `关键发现`
- `总结`

when they do not carry section-specific information.

**Auto-fix:** Rewrite the heading into a concrete, content-specific statement or implication.

**Fallback:** If the section itself is too vague, tighten the opening lines of that section along with the heading.

### 1.4 Prose Wall Detection

**Trigger:** Every prose section.

**Detection:** Flag paragraphs that are too dense to skim:

- Chinese paragraphs over ~150 characters
- English paragraphs over ~120 words
- or visually 5+ lines with no list, no sub-break, and no emphasis anchor

**Auto-fix:** Split the text into shorter paragraphs, bullets, or a `claim -> explanation` structure.

**Fallback:** If the text is a continuous argument, preserve the reasoning but add paragraph breaks and one scan anchor.

### 1.5 Takeaway After Data

**Trigger:** Every `:::kpi`, `:::chart`, and `:::table` block.

**Detection:** Check the adjacent prose. If the component appears without a clear interpretation of what it means, it fails.

**Auto-fix:** Add a takeaway sentence after the component, such as:

- "This shows ..."
- "The key implication is ..."
- "What matters here is ..."

**Fallback:** If the source does not justify causal claims, summarize pattern or contrast only.

## Category 2: AI-Advised Rules

These rules require judgment. Apply them only when the source supports the move with high confidence.

### 2.1 Insight Over Data

**Trigger:** A section is dominated by KPI/chart/table content.

**Detection:** The section repeats numbers but does not explain significance, cause, risk, or action.

**Auto-fix:** Add a short insight paragraph connecting the numbers to implication, risk, or next move.

**Fallback:** If root cause is not supported, provide implication only and avoid speculation.

### 2.2 Scan-Anchor Coverage

**Trigger:** Long sections or multiple consecutive prose paragraphs.

**Detection:** Flag sections that have no skim anchors, such as:

- bold phrase
- callout
- highlight sentence
- list
- explicit mini-summary sentence

**Auto-fix:** Add the lightest anchor that improves scanning without adding visual noise.

Preferred order:

1. mini-summary sentence
2. `highlight-sentence`
3. local bold emphasis
4. `:::callout`

**Fallback:** If the section is already visually dense, add one strong concluding sentence instead of a new component.

### 2.3 Conditional Reader Guidance

**Trigger:** Tutorial, implementation guide, solution proposal, or internal methodology report.

**Detection:** If the report is clearly instructional, check whether the opening tells the reader:

- who this is for
- what prior knowledge is assumed
- what the reader will gain

**Auto-fix:** Add a compact audience / prerequisite / outcome block near the summary.

**Fallback:** Skip entirely for dashboards, business updates, research summaries, or general analysis reports.

## Rejected Candidates

These ideas were considered and intentionally excluded from the automated system.

- **"Can a coworker understand this chart with no context?"**
  Rejected because it depends on external human validation.

- **"Every screenshot must have red boxes, blur, and precise highlighting."**
  Rejected because the current workflow does not include reliable image review/editing.

- **"MECE must be fully exhaustive."**
  Rejected because the AI can spot overlap and jump cuts, but cannot reliably prove completeness.

- **"Every report must declare target reader and prerequisite knowledge."**
  Rejected because that would over-constrain summary and reporting documents.

## Execution Order

Run the review in this order:

1. BLUF Opening
2. Heading Stack Logic
3. Anti-Template Section Headings
4. Prose Wall Detection
5. Takeaway After Data
6. Insight Over Data
7. Scan-Anchor Coverage
8. Conditional Reader Guidance

This order prioritizes:

- why the reader should keep going
- how the argument is organized
- how easily the document can be skimmed
- how data gets interpreted into action
