# Report Review System

**Date:** 2026-04-06  
**Status:** Approved in conversation, implemented in this repo

## Problem

`kai-report-creator` already has strong generation rules for structure, rendering, color discipline, export behavior, and AI-readable HTML. What it lacks is a **report-specific post-generation review layer**.

That gap causes two problems:

1. The tool can generate reports that are visually acceptable but still weak at asynchronous communication: slow openings, template-like headings, data without interpretation, or dense prose blocks with no scan anchors.
2. The docs already hint at a reviewable two-step flow, but the repo has no formal `--review` mode, no report-specific checklist, and no contract tests to keep `SKILL.md`, `README.md`, and supporting references aligned.

Unlike `slide-creator`, `report-creator` is not a multi-step human-in-the-loop polish workflow. It is usually a **single-pass report generation tool**. That means review rules must be filtered aggressively: only rules that an AI can judge with high enough confidence and fix automatically should enter the system.

## Goal

Add a **report-specific review system** that improves report quality in a one-pass automatic flow.

The system should:

- define a report-only `references/review-checklist.md`
- document `--review` as an explicit command in `SKILL.md` and both READMEs
- allow `--generate` to use the same checklist as a silent final review pass
- classify rules into `hard`, `ai-advised`, and `rejected`
- add doc contract tests so the feature cannot drift out of sync

## Non-Goals

- No interactive confirmation window like `slide-creator`
- No image-understanding-dependent review loop for screenshots
- No attempt to prove full MECE completeness
- No requirement that every report must declare target audience or prerequisite knowledge
- No new HTML runtime or browser-side feature; this is a skill/rule/documentation change

## Review Philosophy

The review layer exists to ensure that a report succeeds as **asynchronous system knowledge delivery**.

The system should optimize for three questions:

1. **Why should I keep reading?**
   Solve with a stronger opening and clear summary value.
2. **Can I follow the argument quickly?**
   Solve with better heading logic, reduced template language, and section-level interpretation.
3. **Can I skim this without getting lost?**
   Solve with fewer prose walls, stronger scan anchors, and explicit takeaways after data.

## Rule Selection Filter

A review rule is allowed into `report-creator` only if all three conditions hold:

1. The AI can evaluate it from the source content, IR, and generated HTML alone.
2. The AI can act on the diagnosis with a direct rewrite or deterministic adjustment.
3. The rule does not require external human validation, business truth verification, or visual interpretation of raw images.

Anything that fails this filter belongs in human editorial review, not in the automated system.

## Final Rule Set

The first version should keep **8 rules**.

### Hard Rules

These should be applied automatically when violated.

#### 1. BLUF opening

The first paragraph must establish at least two of:

- document purpose
- core finding
- expected action

If the opening is mostly background, it should be rewritten into an executive-summary paragraph.

#### 2. Heading stack logic

Extract H1/H2/H3. The heading stack should read like a meaningful outline, not a bag of nouns.

The system should prefer headings that imply progression such as problem, mechanism, implication, decision, or action.

#### 3. Anti-template section headings

Generic headings like `Overview`, `Background`, `Key Findings`, `Next Steps`, `Summary`, `问题分析` should be rewritten into information-bearing headings tied to the actual section argument.

#### 4. Prose wall detection

Long undifferentiated paragraphs should be split.

Suggested thresholds:

- Chinese: over 150 characters
- English: over 120 words
- or visibly 5+ lines with no bullets, no sub-breaks, and no emphasis anchors

#### 5. Takeaway after data

Every KPI/chart/table block should have adjacent explanatory text that tells the reader what the data means. Data-only presentation is insufficient.

### AI-Advised Rules

These should run only when the model has enough context to improve the document without making things up.

#### 6. Insight over data

A data-heavy section should not only repeat numbers. It should state implication, cause, risk, or action where the source material supports that move.

#### 7. Scan-anchor coverage

Long sections need at least one scan anchor:

- bold phrase
- callout
- highlight sentence
- list
- explicit mini-summary sentence

This is not a “bold more text” rule. It is a skimmability rule.

#### 8. Conditional reader guidance

For tutorial-like or implementation-guidance reports, the opening should include some form of:

- who this is for
- what baseline knowledge is expected
- what the reader will get

This should not be applied to ordinary business updates, dashboards, or research summaries.

## Rejected Candidates

These should be explicitly documented as **rejected** so the system stays honest about its limits.

- “Can a coworker understand this chart with no context?”  
  Rejected because it depends on external human validation.

- “Every screenshot must be red-boxed, highlighted, and blurred correctly.”  
  Rejected because current flow has no reliable image review/editing loop.

- “MECE must be fully exhaustive.”  
  Rejected because the system can spot overlap or jump cuts, but cannot reliably prove completeness.

- “Every report must label target reader and prerequisite knowledge.”  
  Rejected because this over-constrains summary and reporting documents.

## Information Architecture Changes

### 1. New file: `references/review-checklist.md`

This file should become the source of truth for report review rules. It should:

- explain the one-pass automatic review model
- group rules into hard / ai-advised / rejected
- describe trigger, detection, auto-fix, and fallback per rule
- state execution order

### 2. `SKILL.md`

Update command routing to include:

- `--review [file.html]`

Define behavior as:

- load `references/review-checklist.md`
- inspect the target HTML or planned output
- apply hard rules automatically
- apply ai-advised rules only when confidence is high
- output the revised HTML or diagnosis summary

Also define that `--generate` runs a **silent final review pass** using the same checklist before writing HTML.

### 3. `README.md` and `README.zh-CN.md`

Both READMEs should:

- announce the new release
- list `--review` in the command table
- explain the 8-checkpoint report review system
- clarify that `--review` is one-pass automatic refinement, not an interactive approval loop
- align the existing “two-step with review” phrasing with the actual feature

### 4. `references/design-quality.md`

This file currently covers visual and presentation quality. It should gain an explicit L1 handoff to the report review checklist:

- L0: visual/layout/presentation quality
- L1: content/structure/reading-flow quality

This keeps the repo’s quality model explicit and layered.

### 5. Doc contract checker

Add a lightweight `check-doc-sync.py` similar in spirit to the one in `slide-creator`, but scoped to `report-creator`’s real surfaces:

- `SKILL.md`
- `README.md`
- `README.zh-CN.md`
- `references/review-checklist.md`

It should verify that the user-facing contract stays aligned around:

- `--review`
- the 8-checkpoint review system
- the one-pass automatic behavior
- the silent final review in `--generate`

## Testing Strategy

Because this feature is prompt/document contract work rather than runtime code, the tests should focus on repository invariants.

### New tests

- `tests/test_review_docs.py`
  Validates the existence and required content of `references/review-checklist.md`, plus the corresponding mentions in `SKILL.md`, `README.md`, `README.zh-CN.md`, and `references/design-quality.md`.

- `tests/test_doc_sync.py`
  Exercises the new checker script against:
  - a valid fixture repo
  - a drifted fixture repo
  - the real repo

### Existing test runner

`run_tests.sh --fast` should include these doc tests so the feature remains cheap to verify locally.

## Success Criteria

1. The repo contains a report-specific `references/review-checklist.md`.
2. `SKILL.md` documents `--review` and silent final review inside `--generate`.
3. Both READMEs expose the feature consistently in zh/en.
4. `references/design-quality.md` clearly links visual quality with report review quality.
5. Doc-sync tests fail when the user-facing contract drifts.
6. The new tests pass in the repo.
