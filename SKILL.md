---
name: kai-report-creator
description: Use when the user wants to CREATE or GENERATE a report, business summary, data dashboard, or research doc — 报告/数据看板/商业报告/研究文档/KPI仪表盘. Handles Chinese and English equally. Supports generating from raw notes, data, URLs, or an approved plan file. Use for --plan (structure first), --generate (render to HTML), --themes (preview styles), --from <file>, --bundle, --export-image flags. Does NOT apply to exporting finished HTML to PPTX/PNG (use kai-html-export) or creating slide decks (use kai-slide-creator).
version: 1.2.3
user-invocable: true
metadata: {"openclaw": {"emoji": "📊"}}
---

# kai-report-creator

Generate beautiful, single-file HTML reports with mixed text, charts, KPIs, timelines, diagrams, and images — zero build dependencies, mobile responsive, embeddable anywhere, and machine-readable for AI pipelines.

## Core Principles

1. **Zero Dependencies** — Single HTML files with all CSS/JS inline or from CDN. No npm, no build tools.
2. **User Provides Data, AI Provides Structure** — Never fabricate numbers or facts. Use placeholder text (`[INSERT VALUE]`) if data is missing.
3. **Progressive Disclosure for AI** — Output HTML embeds a 3-layer machine-readable structure (summary JSON → section annotations → component raw data) so downstream AI agents can read reports efficiently.
4. **Mobile Responsive** — Reports render correctly on both desktop and mobile.
5. **Plan Before Generate** — For complex reports, `--plan` creates a `.report.md` IR file first; `--generate` renders it to HTML.

## Command Routing

When invoked as `/report [flags] [content]`, parse flags and route:

| Flag | Action |
|------|--------|
| `--plan "topic"` | Generate a `.report.md` IR file only. Do NOT generate HTML. Save as `report-<slug>.report.md`. |
| `--generate [file]` | Read the specified `.report.md` file (or IR from context if no file given), render to HTML. |
| `--themes` | Output `report-themes-preview.html` showing all 6 built-in themes. Do not generate a report. |
| `--bundle` | Generate HTML with all CDN libraries inlined. Overrides `charts: cdn` in frontmatter. |
| `--from <file>` | If file's first line is `---`, treat as IR and render directly. Otherwise treat as raw content, generate IR first then render. If ambiguous, ask user to confirm. |
| `--theme <name>` | Override theme. Valid: `corporate-blue`, `minimal`, `dark-tech`, `dark-board`, `data-story`, `newspaper`. |
| `--template <file>` | Use a custom HTML template file. Read it and inject rendered content into placeholders. |
| `--output <filename>` | Save HTML to this filename instead of the default. |
| `--export-image [mode]` | After generating HTML, also export to image via `scripts/export-image.py`. Mode: `im` (default), `mobile`, `desktop`, `all`. Requires: `pip install playwright && playwright install chromium`. |
| (no flags, text given) | One-step: generate IR internally (do not save it), immediately render to HTML. |
| (no flags, no text, IR in context) | Detect IR in context (starts with `---`), render directly to HTML. |

**`--export-image` usage:** When this flag is present, after saving the HTML file run:
```
python <skill-dir>/scripts/export-image.py <output.html> --mode <mode>
```
Report the image path(s) to the user. If playwright is not installed, print the install instructions and skip — do not error out.

**Default output filename:** `report-<YYYY-MM-DD>-<slug>.html`

**Slug rule:** Lowercase the title/topic. Replace spaces and non-ASCII characters with hyphens. Keep only alphanumeric ASCII and hyphens. Collapse consecutive hyphens. Trim leading/trailing hyphens. Max 30 chars. Examples: `"2024 Q3 销售报告"` → `2024-q3`, `"AI产品调研"` → `ai`, `"Monthly Sales Report"` → `monthly-sales-report`.

**Flag precedence:** `--bundle` CLI flag overrides `charts: cdn` or `charts: bundle` in frontmatter.

## IR Format (.report.md)

The Intermediate Representation (IR) is a `.report.md` file with three parts:
1. YAML frontmatter (between `---` delimiters)
2. Markdown prose (regular headings, paragraphs, bold, lists)
3. Fence blocks for components: `:::tag [param=value] ... :::`

### Frontmatter Fields

    ---
    title: Report Title                    # Required
    theme: corporate-blue                  # Optional. Default: corporate-blue
    author: Name                           # Optional
    date: YYYY-MM-DD                       # Optional. Default: today
    lang: zh                               # Optional. zh | en. Auto-detected from content if omitted.
    charts: cdn                            # Optional. cdn | bundle. Default: cdn
    toc: true                              # Optional. true | false. Default: true
    animations: true                       # Optional. true | false. Default: true
    abstract: "One-sentence summary"       # Optional. Used in AI summary block.
    template: ./my-template.html           # Optional. Custom HTML template path.
    theme_overrides:                       # Optional. Override theme CSS variables.
      primary_color: "#E63946"
      font_family: "PingFang SC"
      logo: "./logo.png"
    custom_blocks:                         # Optional. User-defined component tags.
      my-tag: |
        <div class="my-class">{{content}}</div>
    ---

### Component Block Syntax

    :::tag [param=value ...]
    [YAML fields or plain text]
    :::

Plain Markdown between blocks renders as rich text (headings, paragraphs, bold, lists, links).

### Built-in Tag Reference

| Tag | Required params | Optional params |
|-----|----------------|-----------------|
| `:::kpi` | (none — list items in body) | (none) |
| `:::chart` | `type` (bar\|line\|pie\|scatter\|radar\|funnel) | `title`, `height` |
| `:::table` | (none — Markdown table in body) | `caption` |
| `:::list` | (none — list items in body) | `style` (ordered\|unordered) |
| `:::image` | `src` | `layout` (left\|right\|full), `caption`, `alt` |
| `:::timeline` | (none — list items in body) | (none) |
| `:::diagram` | `type` (sequence\|flowchart\|tree\|mindmap) | (none) |
| `:::code` | `lang` | `title` |
| `:::callout` | `type` (note\|tip\|warning\|danger) | `icon` |

**Plain text (default):** Any Markdown outside a `:::` block is rendered as rich text — no explicit `:::text` tag needed.

**Chart library rule:** Default to Chart.js (bar/line/pie/scatter). If ANY chart in the report uses radar, funnel, heatmap, or multi-axis, use ECharts for ALL charts in the report. Never load both libraries.

## Language Auto-Detection

When generating any report, auto-infer `lang` from the user's message if not explicitly set in frontmatter:
- Count Unicode range `\u4e00-\u9fff` (CJK characters) in the user's topic/message
- If CJK characters > 10% of total characters, or the title/topic contains any CJK characters → `lang: zh`
- Otherwise → `lang: en`
- If `lang:` is explicitly set in frontmatter, always use that value

Apply `lang` to: the HTML `lang` attribute, placeholder text (`[数据待填写]` for zh, `[INSERT VALUE]` for en), TOC label (`目录` vs `Contents`), and `report-meta` date format.

## Content-Type → Theme Routing

When no `--theme` is specified and no `theme:` in frontmatter, suggest a theme based on the topic keywords. This is a recommendation only — the user can always override with `--theme`.

| Topic keywords | Recommended theme | Use case |
|---------------|-------------------|---------|
| 季报、销售、业绩、营收、KPI、数据分析 / quarterly, sales, revenue, KPI, business | `corporate-blue` | Business & commercial |
| 研究、调研、学术、白皮书、内部、团队 / research, survey, academic, whitepaper, internal, team | `minimal` | Academic & research & editorial |
| 技术、架构、API、系统、性能、部署 / tech, architecture, API, system, performance | `dark-tech` | Technical documentation |
| 新闻、行业、趋势、观察 / news, industry, trend, newsletter | `newspaper` | Editorial & news |
| 年度、故事、增长、复盘 / annual, story, growth, retrospective | `data-story` | Data narrative |
| 项目、看板、状态、进展、品牌、用研 / project, board, status, progress, brand, UX | `dark-board` | Project boards & system dashboards |

When routing, output: *"推荐使用 `[theme]` 主题 ([theme description])，可用 `--theme` 覆盖。"* (or English equivalent).

## --plan Mode

When the user runs `/report --plan "topic"`:

**Step 0 — Auto-detect language.** Apply language auto-detection rules above.

**Step 1 — Suggest theme.** Check content-type routing table. If a match is found, suggest the recommended theme in the IR frontmatter and inform the user.

**Step 2 — Plan the structure.**

1. Think about the report structure: appropriate sections, data the user likely has.
2. Generate a complete `.report.md` IR file containing:
   - Complete frontmatter with all relevant fields filled in
   - At least 3–5 sections with `##` headings
   - A mix of component types (kpi, chart, table, timeline, callout, etc.)
   - Placeholder values for data: use `[数据待填写]` (zh) or `[INSERT VALUE]` (en) — **never fabricate numbers**
   - Comments for fields the user should customize
3. **Apply visual rhythm rules** when laying out sections:
   - Never place 3 or more consecutive sections containing only plain Markdown prose (no components)
   - Ideal section rhythm: `prose → kpi → chart/table → callout/timeline → prose → ...`
   - Every 4–5 sections, insert a "visual anchor" — at least one `:::kpi`, `:::chart`, or `:::diagram` block
   - If a topic area would generate 3+ consecutive prose sections, break it up by inserting a `:::callout` or `:::kpi` with placeholder values
4. Save to `report-<slug>.report.md` using the Write tool.
5. Tell the user:
   - The IR file path
   - Which placeholders need to be filled in
   - The suggested theme (from routing) and how to override it
   - The command to render: `/report --generate <filename>.report.md`

**Stop after saving the IR file. Do NOT generate HTML in --plan mode.**

## --themes Mode

When the user runs `/report --themes`:
1. Read `templates/themes-preview.html` (relative to this skill file's directory) using the Read tool.
2. Write its content verbatim to `report-themes-preview.html` using the Write tool.
3. Tell the user the file path and ask them to open it in a browser.

## Component Rendering Rules

When rendering IR to HTML, apply component-specific rendering rules. Each component must be wrapped with `data-component` attribute for AI readability.

**Detailed rendering rules are in `references/rendering-rules.md`** — load when generating HTML.

**CRITICAL: The final HTML must contain zero `:::` sequences.** Any `:::tag`, param line, or closing `:::` appearing in the output means a directive was not converted — find it and fix it before writing the file.

### Component Overview

| Tag | Purpose | Required params | Optional params |
|-----|---------|----------------|-----------------|
| `:::kpi` | KPI cards with trend indicators | (none — list items in body) | (none) |
| `:::chart` | Charts (bar/line/pie/scatter/radar/funnel) | `type` | `title`, `height` |
| `:::table` | Data tables | (none — Markdown table in body) | `caption` |
| `:::list` | Styled lists | (none — list items in body) | `style` (ordered\|unordered) |
| `:::image` | Images with captions | `src` | `layout` (left\|right\|full), `caption`, `alt` |
| `:::timeline` | Timeline visualization | (none — list items in body) | (none) |
| `:::diagram` | Diagrams (sequence/flowchart/tree/mindmap) | `type` | (none) |
| `:::code` | Syntax-highlighted code blocks | `lang` | `title` |
| `:::callout` | Callout boxes | `type` (note\|tip\|warning\|danger) | `icon` |

Plain Markdown outside `:::` blocks renders as rich text (headings, paragraphs, bold, lists, links).

**Chart library rule:** Default to Chart.js (bar/line/pie/scatter). If ANY chart in the report uses radar, funnel, heatmap, or multi-axis, use ECharts for ALL charts. Never load both libraries.

## Theme CSS

Load theme CSS from `templates/themes/` and assemble in order.

**See `references/theme-css.md` for CSS assembly rules.**

## HTML Shell Template

Generate a complete self-contained HTML file with embedded CSS/JS.

**See `references/html-shell-template.md` for the full HTML structure.**

## TOC Link Generation

**See `references/toc-and-template.md` for TOC link rules, theme override injection, and custom template mode.**

## --generate Mode

When the user runs `/report --generate [file]`:
1. If a file is specified, read it with the Read tool. If no file given, look for IR in context (starts with `---`).
2. Parse the frontmatter to get metadata and settings.
3. Select the appropriate theme CSS.
4. Render all components according to Component Rendering Rules.
5. Apply chart library selection rule.
6. Build the HTML shell with TOC, AI summary, animations.
7. **Pre-write validation:** Before writing, mentally scan the assembled HTML for any occurrence of `:::`. If found, locate the unconverted directive and fix it by converting it to the correct HTML component. The final HTML MUST NOT contain any `:::` sequences.
8. Write to `[output_filename].html` using the Write tool.
9. Tell the user the file path and a 1-sentence summary of the report.

**CRITICAL: Follow `references/html-shell-template.md` EXACTLY**

When building the HTML shell, you MUST follow the template structure from `references/html-shell-template.md`:

**CSS Assembly Order** (see `references/theme-css.md`):
1. Theme CSS (part before `/* === POST-SHARED OVERRIDE */`)
2. Shared component CSS (entire `shared.css`)
3. Theme CSS (part after `/* === POST-SHARED OVERRIDE */`)
4. **TOC CSS** (inline, defined in `html-shell-template.md` — DO NOT SKIP THIS)
5. Theme overrides (if `theme_overrides` in frontmatter)

**JavaScript** (inline, NOT from external files):
- Animation scripts (scroll-triggered fade-in, KPI counter)
- TOC scripts (hover to open, click to lock, active state tracking)
- Edit mode scripts
- Export scripts (html2canvas for image export)

All scripts are defined inline in `references/html-shell-template.md`. **Never** attempt to load scripts from external files like `templates/scripts/*.js` — those files do not exist.
