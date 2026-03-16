# kai-report-creator

English | [简体中文](README.zh-CN.md)

> Generate beautiful, single-file HTML reports — zero dependencies, mobile responsive, AI-readable.

## What it does

`/report` is a Claude Code skill that turns plain text or a structured outline into a polished, standalone HTML report. Drop it in `.claude/skills/` and it's instantly available in any project.

**Features**
- **Zero dependencies** — single `.html` file, works offline (with `--bundle`)
- **6 built-in themes** — corporate-blue, minimal, dark-tech, dark-board, data-story, newspaper
- **9 component types** — KPIs, charts, tables, timelines, diagrams, code blocks, callouts, images, lists
- **AI-readable output** — 3-layer machine-readable structure for downstream agents
- **Bilingual** — full zh/en support with auto-detection

## Quick Start

**Option A — Claude Code (manual install)**

1. Copy `SKILL.md` to `~/.claude/skills/report-creator.md`
2. Point it at a document or URL:

```
/report --from meeting-notes.md
/report --from https://example.com/data-page --output market-analysis.html
/report --plan "Q3 Sales Summary" --from q3-data.csv
```

**Option B — OpenClaw / ClawHub (one command)**

```
clawhub install kai-report-creator
```

An HTML file is generated in your current directory. Open it in any browser.

## Commands

| Command | Description |
|---------|-------------|
| `/report --from file.md` | Generate from an existing document |
| `/report --from URL` | Generate from a web page |
| `/report --plan "topic"` | Create a `.report.md` outline first |
| `/report --generate file.report.md` | Render an outline to HTML |
| `/report --themes` | Preview all 6 themes side by side |
| `/report --bundle --from file.md` | Offline HTML with all CDN assets inlined |
| `/report --theme dark-tech --from file.md` | Use a specific theme |
| `/report --template my-template.html` | Use a custom HTML template |
| `/report --output my-report.html --from file.md` | Custom output filename |
| `/report [content]` | One-step: generate from a short description |

## Export

Every generated report has a built-in **↓ Export** button (bottom-right corner). No extra tools needed.

| Option | How it works |
|--------|--------------|
| 🖨 Print / PDF | Opens the browser print dialog. Select **Save as PDF** as the destination. |
| 🖥 Save PNG (Desktop) | Captures the full page at 2× resolution. |
| 📱 Save PNG (Mobile) | Captures the report body scaled to 1170 px wide (≈ 3× iPhone width). |

**For clean PDFs, uncheck "Headers and footers" in the print dialog** — otherwise the browser adds the page URL, date, and page numbers as print headers/footers. In Chrome: *Print → More settings → uncheck Headers and footers*.

## Theme Demos

Click any screenshot to open the live demo:

<table>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/corporate-blue.html"><img src="templates/screenshots/corporate-blue.png" width="360" alt="corporate-blue"/><br/><b>corporate-blue</b></a><br/><sub>Business · Executive</sub></td>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/minimal.html"><img src="templates/screenshots/minimal.png" width="360" alt="minimal"/><br/><b>minimal</b></a><br/><sub>Research · Academic</sub></td>
</tr>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/dark-tech.html"><img src="templates/screenshots/dark-tech.png" width="360" alt="dark-tech"/><br/><b>dark-tech</b></a><br/><sub>Engineering · Ops</sub></td>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/dark-board.html"><img src="templates/screenshots/dark-board.png" width="360" alt="dark-board"/><br/><b>dark-board</b></a><br/><sub>Dashboards · Architecture</sub></td>
</tr>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/data-story.html"><img src="templates/screenshots/data-story.png" width="360" alt="data-story"/><br/><b>data-story</b></a><br/><sub>Annual Reports · Growth</sub></td>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/newspaper.html"><img src="templates/screenshots/newspaper.png" width="360" alt="newspaper"/><br/><b>newspaper</b></a><br/><sub>Editorial · Industry Analysis</sub></td>
</tr>
</table>

Preview all themes in one page: `/report --themes` → opens `report-themes-preview.html`

## Report Format (IR)

For complex reports, use `--plan` to create a `.report.md` intermediate file, then edit it before generating HTML.

**Frontmatter example:**
```yaml
---
title: Q3 Sales Report
theme: corporate-blue
author: Sales Team
date: 2024-10-08
lang: en                # en | zh — auto-detected if omitted
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

Need a different color palette? Use `theme_overrides` to customize any theme:
```yaml
theme_overrides:
  primary_color: "#B45309"          # swap the accent color
  font_family: "Merriweather, serif" # swap the font
```

## Custom Templates

Copy `templates/_custom-template.example.html`, customize it with your branding, and reference it:

```yaml
---
template: ./my-brand-template.html
---
```

Available placeholders: `{{report.title}}`, `{{report.author}}`, `{{report.date}}`, `{{report.abstract}}`, `{{report.theme_css}}`, `{{report.body}}`, `{{report.summary_json}}`

## For AI Agents & Skills

report-creator is designed for machine-to-machine use. Other agents and skills can call it programmatically.

**Calling `/report` from another skill or agent:**

```
# From a document
/report --from ./analysis.md --output summary.html

# From a URL (Claude fetches and analyzes the page)
/report --from https://example.com/report-page --theme data-story

# Two-step with review
/report --plan "Market Analysis" --from ./raw-data.md
# (edit the generated .report.md if needed)
/report --generate market-analysis.report.md
```

**Reading report output programmatically:**

Every generated HTML embeds a 3-layer machine-readable structure:

```
Layer 1 — <script type="application/json" id="report-summary">
           Document-level: title, author, abstract, all KPIs extracted
           → Read this for a full document overview in one JSON parse

Layer 2 — data-section="..." data-summary="..."  on each <section>
           Section-level: heading and one-sentence summary per section
           → Loop over sections for structured table of contents

Layer 3 — data-component="kpi" data-raw='{...}'  on each component
           Component-level: raw structured data for every KPI, chart, table
           → Query specific components for downstream data processing
```

**Example: extracting Layer 1 summary from a generated report**

```python
from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(open("report.html"), "html.parser")
summary = json.loads(soup.find("script", {"id": "report-summary"}).string)
print(summary["title"], summary["abstract"])
print(summary["kpis"])  # all KPI values extracted
```

**Recommended calling patterns for agents:**

| Scenario | Command |
|----------|---------|
| Summarize a long doc into a report | `/report --from doc.md --theme minimal` |
| Turn scraped data into a dashboard | `/report --from data.json --theme dark-board` |
| Generate a report in a pipeline | `/report --generate plan.report.md --output out.html` |
| Offline delivery | `/report --bundle --from doc.md` |

## Design Philosophy

This section explains the design principles behind report-creator — both as a user-facing tool and as a Claude Code skill. Understanding these helps you build better skills and better reports.

### 1. Skill as Progressive Disclosure

A skill file is loaded entirely into the AI's context window every time it's invoked. This means skill size directly affects what the AI can focus on.

report-creator solves this by keeping **rules in the skill, assets in files**:

- **`--plan` mode** — only needs IR rules and component syntax. No CSS, no HTML shell. The skill stays focused.
- **`--generate` mode** — reads exactly one theme CSS file (`templates/themes/[theme].css`) and one shared CSS file. All other 5 themes stay on disk, out of context.
- **`--themes` mode** — reads the pre-built preview HTML verbatim. The skill doesn't need to know what's inside it.

The result: each command loads only what it needs. A `--plan` invocation never touches CSS. A single-theme generation never loads the other 5 themes.

This is progressive disclosure applied to AI context management: **reveal information at the moment it's needed, not before**.

### 2. IR as a Human-AI Interface

The `.report.md` Intermediate Representation is the contract between human intent and AI rendering.

It has three layers, each with a clear responsibility:

```
---                         ← Frontmatter: document identity
title: Q3 Sales Report         What is this? Who made it? How should it look?
theme: corporate-blue          Declares intent, not content.
abstract: "..."
---

## Section Heading         ← Prose: human narrative
Plain Markdown text...        Written naturally. AI renders to semantic HTML.

:::kpi                     ← Component blocks: structured data
- Revenue: $2.45M ↑12%       Machine-parseable. AI renders deterministically.
:::                           Each block type has an unambiguous output contract.
```

This separation means:
- Humans can write and edit the IR naturally, without knowing HTML
- AI renders each layer with different rules — prose gets Markdown conversion, components get deterministic templates
- The IR is inspectable and version-controllable before any HTML is generated

### 3. Frontmatter as Document Identity, Sections as Document Body

Frontmatter and section content answer different questions:

| Layer | Question | Examples |
|-------|----------|---------|
| Frontmatter | *What is this document?* | title, author, theme, lang, abstract |
| Sections | *What does this document say?* | headings, prose, KPIs, charts |

The `abstract` field is the most important bridge: it lets downstream AI agents understand the full report from a single sentence — without reading every section. This powers **Layer 1** of the 3-layer AI readability system embedded in every generated HTML file:

```
Layer 1 — <script type="application/json" id="report-summary">
           Document-level: title, author, abstract, all KPIs extracted

Layer 2 — data-section="..." data-summary="..."  on each <section>
           Section-level: heading and one-sentence summary per section

Layer 3 — data-component="kpi" data-raw='{...}'  on each component
           Component-level: raw structured data for every KPI, chart, table
```

An AI agent reading a report can start at Layer 1 for a 3-second overview, drill into Layer 2 for section-level understanding, and reach Layer 3 only for the specific data it needs. The same progressive disclosure principle — this time for machines reading reports.

### 4. Visual Rhythm as Cognitive Pacing

Reports that work well for humans follow a rhythm: **prose sets context, components deliver data, prose interprets it**.

The skill enforces a visual rhythm rule: never place 3+ consecutive sections with only prose and no components. Every 4–5 sections must include a "visual anchor" — a KPI grid, chart, or diagram. This isn't aesthetic preference; it's cognitive pacing. Dense prose fatigues readers. Data without context loses them. The alternation creates flow.

This is also why the IR's component block syntax (`:::tag ... :::`) was designed to be visually obvious: authors can scan an IR file and immediately see where the data-heavy sections are, without parsing HTML or YAML.

## Examples

| File | Description |
|------|-------------|
| [examples/en/business-report.html](examples/en/business-report.html) | 2024 Q3 Sales Performance Report (EN) |
| [examples/zh/business-report.html](examples/zh/business-report.html) | 2024 Q3 销售业绩报告（中文）|

## License

MIT
