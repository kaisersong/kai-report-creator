# kai-report-creator

> Generate beautiful, single-file HTML reports — zero dependencies, mobile responsive, AI-readable.

## What it does

`/report` is a Claude Code skill that turns plain text or a structured outline into a polished, standalone HTML report. Drop it in your `.claude/skills/` folder and it's instantly available in any project.

**Features**
- **Zero dependencies** — single `.html` file, works offline (with `--bundle`)
- **4 built-in themes** — corporate-blue, minimal, dark-tech, warm-editorial
- **9 component types** — KPIs, charts, tables, timelines, diagrams, code blocks, callouts, images, lists
- **AI-readable output** — 3-layer machine-readable structure for downstream agents
- **Bilingual** — full zh/en support; choose with `lang: zh|en` in frontmatter

## Quick Start

1. Copy `SKILL.md` to `~/.claude/skills/report-creator.md`
2. In any Claude Code session, run:

```
/report Q3 Sales Report — revenue up 12%, 183 new clients, target achieved 108%
```

An HTML file is generated in your current directory. Open it in any browser.

## Commands

| Command | Description |
|---------|-------------|
| `/report [content]` | One-step: generate report from description |
| `/report --plan "topic"` | Create a `.report.md` outline first |
| `/report --generate file.report.md` | Render an outline to HTML |
| `/report --themes` | Preview all 4 themes side by side |
| `/report --bundle [content]` | Offline HTML with all CDN assets inlined |
| `/report --theme dark-tech [content]` | Use a specific theme |
| `/report --output my-report.html [content]` | Custom output filename |

## Report Format (IR)

For complex reports, use `--plan` to create a `.report.md` intermediate file, then edit it before generating HTML.

**Frontmatter example:**
```yaml
---
title: Q3 Sales Report
theme: corporate-blue   # corporate-blue | minimal | dark-tech | warm-editorial
author: Sales Team
date: 2024-10-08
lang: en                # en | zh
toc: true
animations: true
abstract: "Q3 revenue grew 12% YoY with record new customer acquisition."
---
```

**Available component blocks:**
```
:::kpi
- Revenue: $2.45M ↑12%
- New Clients: 183 ↑8%
:::

:::chart type=line title="Monthly Revenue"
labels: [Jul, Aug, Sep]
datasets:
  - label: Actual
    data: [780000, 820000, 850000]
:::

:::timeline
- 2024-10-15: Q4 targets released
- 2024-10-31: Product launch event
:::

:::callout type=tip
Highlight key insight here.
:::

:::table caption="Regional Performance"
| Region | Achievement |
|--------|-------------|
| South  | 115%        |
:::
```

## Themes

| Theme | Best for | Style |
|-------|----------|-------|
| `corporate-blue` | Business reports, executive summaries | Professional, clean |
| `minimal` | Research reports, academic papers | Serif, typographic |
| `dark-tech` | Technical docs, engineering reports | Dark, monospace |
| `warm-editorial` | Content reports, newsletters | Warm, editorial |

Preview all themes: `/report --themes` → open `report-themes-preview.html`

## Templates

Browse ready-to-use examples in the `templates/` directory:

| Language | corporate-blue | minimal | dark-tech | warm-editorial |
|----------|---------------|---------|-----------|----------------|
| English  | [templates/en/corporate-blue.html](templates/en/corporate-blue.html) | [templates/en/minimal.html](templates/en/minimal.html) | [templates/en/dark-tech.html](templates/en/dark-tech.html) | [templates/en/warm-editorial.html](templates/en/warm-editorial.html) |
| 中文 | [templates/zh/corporate-blue.html](templates/zh/corporate-blue.html) | [templates/zh/minimal.html](templates/zh/minimal.html) | [templates/zh/dark-tech.html](templates/zh/dark-tech.html) | [templates/zh/warm-editorial.html](templates/zh/warm-editorial.html) |

## Examples

| File | Description |
|------|-------------|
| [examples/en/business-report.html](examples/en/business-report.html) | 2024 Q3 Sales Performance Report (EN) |
| [examples/en/monthly-progress.html](examples/en/monthly-progress.html) | Monthly Project Progress Report (EN) |
| [examples/zh/business-report.html](examples/zh/business-report.html) | 2024 Q3 销售业绩报告（中文）|
| [examples/zh/monthly-progress.html](examples/zh/monthly-progress.html) | 月度项目进展报告（中文）|

## License

MIT
