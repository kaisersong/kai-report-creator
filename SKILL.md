---
name: report-creator
description: Generate beautiful single-file HTML reports with mixed text, charts, KPI cards, timelines, diagrams, and images. Use when the user wants to create a report, business summary, research doc, or formatted HTML output. Supports --plan (generate IR outline), --generate (render IR to HTML), --themes (preview styles), --bundle (offline HTML), --from (read file), --output (custom filename).
version: 1.0.0
---

# report-creator

Generate beautiful, single-file HTML reports with mixed text, charts, KPIs, timelines, diagrams, and images — zero build dependencies, mobile responsive, embeddable anywhere, and machine-readable for AI pipelines.

## Core Principles

1. **Zero Dependencies** — Single HTML files with all CSS/JS inline or from CDN. No npm, no build tools.
2. **User Provides Data, AI Provides Structure** — Never fabricate numbers or facts. Use placeholder text (`[数据待填写]`) if data is missing.
3. **Progressive Disclosure for AI** — Output HTML embeds a 3-layer machine-readable structure (summary JSON → section annotations → component raw data) so downstream AI agents can read reports efficiently.
4. **Mobile Responsive** — Reports render correctly on both desktop and mobile.
5. **Plan Before Generate** — For complex reports, `--plan` creates a `.report.md` IR file first; `--generate` renders it to HTML.

## Command Routing

When invoked as `/report [flags] [content]`, parse flags and route:

| Flag | Action |
|------|--------|
| `--plan "topic"` | Generate a `.report.md` IR file only. Do NOT generate HTML. Save as `report-<slug>.report.md`. |
| `--generate [file]` | Read the specified `.report.md` file (or IR from context if no file given), render to HTML. |
| `--themes` | Output `report-themes-preview.html` showing all 4 built-in themes. Do not generate a report. |
| `--bundle` | Generate HTML with all CDN libraries inlined. Overrides `charts: cdn` in frontmatter. |
| `--from <file>` | If file's first line is `---`, treat as IR and render directly. Otherwise treat as raw content, generate IR first then render. If ambiguous, ask user to confirm. |
| `--theme <name>` | Override theme. Valid: `corporate-blue`, `minimal`, `dark-tech`, `warm-editorial`. |
| `--template <file>` | Use a custom HTML template file. Read it and inject rendered content into placeholders. |
| `--output <filename>` | Save HTML to this filename instead of the default. |
| (no flags, text given) | One-step: generate IR internally (do not save it), immediately render to HTML. |
| (no flags, no text, IR in context) | Detect IR in context (starts with `---`), render directly to HTML. |

**Default output filename:** `report-<YYYY-MM-DD>-<slug>.html`

**Slug rule:** Lowercase the title/topic. Replace spaces and non-ASCII characters with hyphens. Keep only alphanumeric ASCII and hyphens. Collapse consecutive hyphens. Trim leading/trailing hyphens. Max 30 chars. Examples: `"2024 Q3 销售报告"` → `2024-q3`, `"AI产品调研"` → `ai`, `"Monthly Sales Report"` → `monthly-sales-report`.

**Flag precedence:** `--bundle` CLI flag overrides `charts: cdn` or `charts: bundle` in frontmatter.
