---
name: kai-report-creator
description: Use when the user wants to CREATE or GENERATE a report, business summary, data dashboard, or research doc — 报告/数据看板/商业报告/研究文档/KPI仪表盘. Handles Chinese and English equally. Supports generating from raw notes, data, URLs, or an approved plan file. Use for --plan (structure first), --generate (render to HTML), --review (one-pass automatic refinement), --themes (preview styles), --from FILE, --bundle, --export-image flags. Does NOT apply to exporting finished HTML to PPTX/PNG (use kai-html-export) or creating slide decks (use kai-slide-creator).
version: 1.22.0
user-invocable: true
metadata: {"openclaw": {"emoji": "📊"}}
---

# kai-report-creator

Generate single-file HTML reports from source notes or `.report.md` IR. Keep this file as a thin router: load only the references needed for the current path, and move detailed contracts into `references/`, scripts, tests, or templates.

## Core Principles

1. **Zero Dependencies** — generated reports are self-contained HTML, with CDN or bundled assets only when needed.
2. **User Provides Data, AI Provides Structure** — never fabricate facts or numbers; use `[数据待填写]` / `[INSERT VALUE]` when data is missing.
3. **Plan Before Generate** — complex reports should become `.report.md` IR first, then HTML.
4. **Progressive Disclosure for AI** — output keeps `report-summary`, section annotations, and component data machine-readable.
5. **Thin Routing Over Prompt Growth** — `SKILL.md` routes work and names hard gates; detailed rules live in references.
6. **Contracts and Gates Beat Prompt Soup** — prefer IR, guard validation, shell tests, and post-render review over adding more prose to this hot path.

## Command Routing

When invoked as `/report [flags] [content]`, parse flags first:

| Flag | Action |
|------|--------|
| `--plan "topic"` | Write `.report.md` IR only. Stop after saving it. |
| `--generate [file]` | Render one `.report.md` IR to HTML. With no file given, extract exactly one valid IR block from context. |
| `--review [file]` | Refine an existing HTML report with `references/review-checklist.md`. |
| `--themes` | Write the themes preview HTML. |
| `--from <file>` | If the file starts with frontmatter, treat as IR; otherwise create IR, then render. |
| `--theme <name>` | Override the theme. Built-ins: `corporate-blue`, `minimal`, `dark-tech`, `dark-board`, `data-story`, `newspaper`, `regular-lumen`. |
| `--template <file>` | Use a custom HTML template. See `references/toc-and-template.md`. |
| `--output <file>` | Save to this path instead of the default. |
| `--bundle` | Inline CDN assets where supported. |
| `--export-image [mode]` | After HTML generation, run `scripts/export-image.py`; mode is `im`, `mobile`, `desktop`, or `all`. |
| no flags + text | Create IR internally, then render HTML. |
| no flags + IR in context | Treat as `--generate` from context. |

Default output filename: `report-<YYYY-MM-DD>-<slug>.html`. Slug: lowercase ASCII, non-alphanumeric to hyphens, collapse hyphens, trim, max 30 chars.

## Reference Loading

Load references by route; do not read every reference by default.

| Route | Always load | Conditional load |
|-------|-------------|------------------|
| `--plan` | `references/spec-loading-matrix.md`, `references/design-quality.md` | `references/regular-report-content-rules.md` for periodic reports |
| `--generate` | `references/html-shell-template.md` + every `references/html-shell/*.md`, `references/theme-css.md`, `references/review-checklist.md` | `references/rendering-rules.md` then only the `references/rendering/*.md` files required by the IR; `references/anti-patterns.md` for visual anchors; `references/diagram-decision-rules.md` for diagrams; `references/regular-report-content-rules.md` for periodic reports |
| `--review` | `references/review-checklist.md` | `references/review-report-template.md` if a structured change summary is requested |
| custom theme/template | `references/theme-css.md`, `references/toc-and-template.md` | custom theme `reference.md` or `theme.css` |

Load `references/spec-loading-matrix.md` before `--plan` and `--generate` as a silent classifier. It covers optional archetypes: `brief`, `research`, `comparison`, `update`.

Always load `references/anti-patterns.md` before `--generate`. Load `references/diagram-decision-rules.md` whenever a diagram or diagram-like structure is being considered.

## IR Quick Contract

`.report.md` has three parts:

1. YAML frontmatter between `---` delimiters.
2. Markdown prose with `##` / `###` headings.
3. Component fences: `:::tag [param=value]` ... `:::`.

Minimal frontmatter:

```yaml
---
title: Report Title
theme: corporate-blue                  # Optional. Default: corporate-blue
date: YYYY-MM-DD
lang: zh
report_class: mixed
archetype: research                    # Optional lightweight archetype hint for silent classification.
audience: "Busy decision-maker"
decision_goal: "Decide next move"
must_include:
  - Source truth that must survive compression
must_avoid:
  - Decorative placeholder chart
charts: cdn
toc: true
animations: true
abstract: "One-sentence summary"
poster_title: "Optional stronger poster headline"
poster_subtitle: "Optional poster subtitle"
poster_note: "Optional short closing sentence"
template: ./my-template.html
theme_overrides:
  primary_color: "#E63946"
custom_blocks:
  my-tag: |
    <div class="my-class">{{content}}</div>
---
```

For trivial reports, omit optional fields. For high-stakes or complex reports, keep `report_class`, `audience`, `decision_goal`, `must_include`, and `must_avoid` so review/evals can detect drift.

Poster summary mode is opt-in. Do not infer `poster_title` or `poster_subtitle` from punctuation in `title`.

IR validity terms: `invalid_syntax`, `invalid_semantics`, `contract_conflict`, `auto_downgrade_target`.

Canonical component routing lives in `references/rendering-rules.md`; component details live in `references/rendering/*.md`. Compatibility anchors that must remain discoverable here:

- `:::kpi` canonical body uses `items:`.
- Timeline Allowed `Date` tokens: `YYYY-MM-DD`, `YYYY-MM`, `YYYY`, `Q[1-4] YYYY`, `Day N`, `Week N`, `Month N`.
- Use **ECharts** for ALL charts.
- Badges are optional visual enhancements, not a first-class IR tag.

## Language, Theme, And Class

Auto-detect `lang` unless frontmatter sets it: use `zh` when CJK is material or appears in the title/topic; otherwise use `en`. Apply language to placeholders, TOC labels, date display, and shell labels.

If no theme is provided, pick by intent, first match wins:

| Signal | Theme |
|--------|-------|
| weekly/daily/monthly/work progress/周报/日报/月报/本周/下周 | `regular-lumen` |
| sales/revenue/KPI/quarterly/business/销售/营收/业绩/季报 | `corporate-blue` |
| research/survey/whitepaper/internal/研究/调研/白皮书 | `minimal` |
| tech/architecture/API/system/performance/工程/架构 | `dark-tech` |
| news/industry/trend/新闻/行业/趋势 | `newspaper` |
| annual/story/growth/retrospective/年度/增长/复盘 | `data-story` |
| board/dashboard/status/看板 | `dark-board` |
| generic project progress/项目进展/项目状态 | `corporate-blue` |

Classify content by numeric density: `narrative` < 5%, `mixed` 5-20%, `data` > 20%; short topics default to `mixed`.

## `--plan` Flow

1. Detect language and suggest theme.
2. Classify `report_class`; optionally add `archetype` only when the report clearly matches `brief`, `research`, `comparison`, or `update`.
3. For `regular-lumen` or periodic keywords, load `references/regular-report-content-rules.md`.
4. Generate `.report.md` with complete frontmatter, 3-5 useful sections, source-faithful structure, and placeholders only where data is missing.
5. Use real visual anchors only. In `narrative` and `mixed`, never use placeholder-only KPI/chart blocks; prefer callout, timeline, diagram, table, or prose scan anchors.
6. Keep KPI values short: <=8 Chinese chars or <=3 English words. Explanations belong in prose, callouts, or tables.
7. Use `theme_overrides` only for a small content-tone color hint; do not create a new design system in the IR.
8. Save as `report-<slug>.report.md`.
9. Tell the user the IR path, placeholder fields, suggested theme, and render command.
10. Stop. Do not generate HTML in `--plan` mode.

Narrative rhythm reminders: `lead-block`, `section-quote`, and `action-grid` are optional prose upgrades. `claim -> explanation -> scan anchor` is a cadence, not a quota. These are optional prose upgrades, not default required blocks. If uncertain, keep normal paragraphs and add one clearer scan anchor instead of forcing a cadence block. Do not add more than one of `lead-block` / `section-quote` / `action-grid` by default inside the same section unless the source material clearly warrants it.

## `--generate` Flow

1. Read IR input only. With no file given, extract exactly one valid IR block from context. Treat this as IR from context, not chat history. If zero or multiple are present, stop and ask for an explicit file or single IR block. Never render the surrounding conversation.
2. Load reference files minimally but reliably; load only the references that materially help the current render path. Standard HTML shell generation always loads the shell entry plus all `references/html-shell/*.md`; component rules load by IR inventory via `references/rendering-rules.md`.
3. Parse frontmatter and resolve `lang`, `theme`, `report_class: mixed` default, `archetype`, date display, chart mode, TOC, animation, template, and theme overrides.
4. Run guard validation before rendering:
   - Use `scripts/guard_validate.py` with IR text from file or extracted context.
   - If fatal metadata is missing, stop and report the error.
   - If a block is invalid, apply its `auto_downgrade_target` (`kpi -> callout`, `chart -> table`, `timeline -> list`, `diagram -> callout`) and mention the downgrade.
5. Render components using `references/rendering-rules.md`, `references/design-quality.md`, and the path-specific `references/rendering/*.md` files selected from the IR.
6. Build the standard shell from `references/html-shell-template.md` plus all `references/html-shell/*.md`; follow Shell metadata, version/theme metadata, export completeness, and the duplicate-date guard.
7. Compute and embed `<meta name="ir-hash" content="sha256:[ir-hash]">` from the exact IR text, not the file path.
8. Assemble CSS through `references/theme-css.md`: theme before-marker, shared CSS, theme post-shared override, TOC/shell CSS, frontmatter overrides.
9. Run pre-write validation and fix all violations:
   - no raw `:::` in HTML
   - valid `ir-hash`
   - no generic/template h2 headings
   - short `.kpi-value` and short `report-summary` KPI values
   - `.number` body numerals use tabular lining numerals
   - badges clarify status/category/entity, never quota-fill
   - timeline dates are real time markers
   - no U+FE0F
   - no `text-align: justify`, black-background flood, body letter-spacing > `0.05em`, or mobile-hidden critical controls
10. Run L2 shell checks. Required: `data-template="kai-report-creator"`, `data-version`, `data-theme`, `id="toc-toggle-btn"`, `id="toc-sidebar"`, `id="card-mode-btn"`, `id="sc-overlay"`, `id="export-btn"`, `id="export-menu"`, `id="export-print"`, `id="export-png-desktop"`, `id="export-png-mobile"`, `id="export-im-share"`, `id="report-summary"`, plus the JS bindings for print/desktop/mobile/IM export. If any export item or binding is missing, rebuild the whole export block from `references/html-shell/export.md`.
11. Run the silent final review pass from `references/review-checklist.md`, then write the HTML and report the path.

When the report is explicitly comparing named vendors, models, or tools, set `data-report-mode="comparison"` on the outer report container and use `.badge--entity-a/.badge--entity-b/.badge--entity-c` only for entity identity.

## `--review` Flow

When the user runs `/report --review [file]`:

1. Read the HTML file.
2. Load `references/review-checklist.md`.
3. Apply hard rules automatically.
4. Apply AI-advised rules only when confidence is high and factual accuracy is preserved.
5. This is one-pass automatic refinement; no confirmation window.
6. Use `references/review-report-template.md` when the user wants a structured summary.
7. Write back unless the user asked for diagnosis only.
8. Tell the user what changed and what was intentionally left untouched.

## `--themes` And `--export-image`

For `--themes`, read the theme preview template and write `report-themes-preview.html` verbatim.

For `--export-image`, after HTML generation run:

```bash
python <skill-dir>/scripts/export-image.py <output.html> --mode <mode>
```

If Playwright is unavailable, print install instructions and skip image export without failing HTML generation.

## Shell And Template Boundary

Generate complete self-contained HTML. The shell entry contract lives in `references/html-shell-template.md`; full shell structure, inline JS, export behavior, summary card, edit mode, TOC, print rules, and footer/watermark degradation rules live in `references/html-shell/*.md`.

All scripts are inline in the shell template. Never load nonexistent files such as `templates/scripts/*.js`.

For custom templates and TOC slug rules, use `references/toc-and-template.md`.

## Final Output

Always end with the file path and a one-sentence summary. If a validation, guard, or export step could not run, say exactly which step was skipped and why.
