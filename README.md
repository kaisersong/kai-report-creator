# kai-report-creator

English | [简体中文](README.zh-CN.md)

> Generate beautiful, single-file HTML reports — zero dependencies, mobile responsive, AI-readable.

**v1.8.3** — KPI overflow fix: long units (e.g. `commits/hour`, `req/sec`) now render correctly inside narrow cards via a new `.kpi-suffix` child element (smaller font, block display). Added `word-break: break-word` to `.kpi-value` as a safety net. Rendering rule updated: suffixes longer than 4 characters must use `<span class="kpi-suffix">` and must not carry `data-target-value` (the countUp animation rewrites `textContent` and would destroy the span).

**v1.8.2** — Restrained color system: shared badges and KPI accents now default to one neutral palette, comparison reports can opt into entity-specific badge colors via `data-report-mode="comparison"`, and `corporate-blue` now ships as a warm premium business theme. Updated docs, tests, and demo screenshot to match.

**v1.8.1** — Export background fix: PNG/mobile/IM capture now resolves a concrete page background via `--bg` before falling back to `body` background color, so reports with gradients or background images no longer export as white/transparent. Added regression coverage for transparent-background capture paths.

**v1.8.0** — Custom themes: `--theme <name>` can now load user-defined theme folders from `themes/`. Includes bilingual theme-authoring docs and an example warm-editorial starter theme.

**v1.6.1** — Export background fix: PNG/mobile/IM capture now resolves a concrete page background via `--bg` before falling back to `body` background color, so reports with gradients or background images no longer export as white/transparent. Added regression coverage for transparent-background capture paths.

**v1.6.0** — Sankey chart: new `:::chart type=sankey` component powered by ECharts. Renders flow diagrams where data has source → target → value triples (budget allocation, multi-path conversion funnels, supply chains). Node labels show name + value with distinct typographic weight (muted name / bold primary-color number). Edge labels show flow values inline. The `--plan` mode now selects sankey automatically when it detects branching flow data. Triggers ECharts like radar/funnel.

**v1.5.2** — Template fix: shared component CSS (export button, code block, all components) is now hardcoded verbatim in the HTML shell template instead of relying on an LLM placeholder substitution. Fixes export dropdown appearing at page top and code block missing border/overflow styles in generated reports.

**v1.5.1** — Bug fixes: KPI card three-row alignment via flex column layout (cross-card delta row alignment), callout block text wrapping fix (`flex: 1; min-width: 0`), summary card export now captures only the card (not full page), and summary card export filename gets `-摘要卡` suffix.

**v1.5.0** — Design Quality Baseline: new `references/design-quality.md` encodes anti-slop rules across four disciplines — 90/8/2 color law (primary color capped to 2% bullet-point role), KPI grid column rules (4 KPIs → 2×2 not 3-column, hero metric gets `2fr`), content-tone color calibration (contemplative/brown, technical/navy, business/teal), and a `highlight-sentence` component for surfacing key insight sentences. The `--plan` mode now suggests tone-matched `primary_color` overrides in frontmatter. Pre-output self-check added: *"If you told someone 'an AI wrote this', would they immediately believe it?"*

**v1.4.1** — Summary card redesign: editorial two-column layout — large uppercase title on the left, compact KPI rows + per-section summaries on the right. Removed redundant labels and footer clutter. Fixed export-while-card-open capturing blank images (now captures `.sc-card` directly).

**v1.4.0** — Summary card overlay: every report now has a `⊞ Summary` button next to the title. Click it to open an editorial-style card drawn from the embedded `#report-summary` JSON — title, abstract, KPIs, section chips. Close with ✕, Escape, or click the backdrop. Zero extra dependencies.

**v1.3.0** — GSAP-inspired zero-dependency animation upgrade: KPI cards now spring-bounce in with stagger (cubic-bezier back.out approximation), timeline items slide in one by one, and all easing curves upgraded to power3.out. No new libraries — IntersectionObserver + CSS transitions only.

## What it does

`/report` is a Claude Code skill that turns plain text or a structured outline into a polished, standalone HTML report. Drop it in `.claude/skills/` and it's instantly available in any project.

**Features**
- **Zero dependencies** — single `.html` file, works offline (with `--bundle`)
- **6 built-in themes + custom theme folders** — corporate-blue, minimal, dark-tech, dark-board, data-story, newspaper, or your own `themes/<name>/theme.css`
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
| `/report --theme dark-tech --from file.md` | Use a built-in or custom theme |
| `/report --template my-template.html` | Use a custom HTML template |
| `/report --output my-report.html --from file.md` | Custom output filename |
| `/report [content]` | One-step: generate from a short description |

Custom themes: create `themes/<name>/theme.css`, then run `/report --theme <name> --from file.md`.

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
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/en/corporate-blue.html"><img src="templates/screenshots/corporate-blue.png" width="360" alt="corporate-blue"/><br/><b>corporate-blue</b></a><br/><sub>Warm Premium · Business</sub></td>
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

### 5. Design Quality Baseline: Against AI Slop

A generated report's greatest enemy is looking instantly AI-made — uniform border radii everywhere, primary color flooding six element types simultaneously, three equal-column KPI grids regardless of count, section headings that sound like templates ("Overview", "Key Findings", "Next Steps").

v1.5.0 introduces `references/design-quality.md`, a shared quality baseline that the AI loads alongside rendering rules during `--generate`. It encodes four disciplines:

**The 90/8/2 Color Law.** Every report allocates color in three tiers: 90% neutral surface (background, body text), 8% structural accent (one emphasis block, borders), 2% bullet point (at most 1–2 precise high-contrast hits). When `--primary` floods headings, KPI values, chart bars, callout borders, TOC links, and badges all at once — it stops being a signal and becomes noise.

**Typography Tension: 10:1 Scale Ratio.** The largest element on a page should be at least 10× the smallest readable element. A report title should feel like an anchor, not a label — minimum 2.8rem, ideally 3.2–4rem with tight leading. When every element lives in the 15–22px range, the page has no hierarchy. It looks like a spreadsheet export.

**KPI Grid Column Rules.** The default is not always 3 columns. 4 KPIs belong in a 2×2 grid. A hero metric deserves `grid-template-columns: 2fr 1fr 1fr`. 7+ KPIs need visual group dividers. Rigid 3-column grids for any count are a template smell — they signal the AI wasn't paying attention to the data.

**Content-Tone Color Calibration.** A philosophical research report and a quarterly business dashboard have different emotional registers. The `--plan` mode now suggests tone-matched `primary_color` overrides in frontmatter:

| Content tone | `primary_color` | Feel |
|---|---|---|
| Contemplative / Research | `#7C6853` warm brown | Grounded, editorial |
| Technical / Engineering | `#3D5A80` navy | Precise, authoritative |
| Business / Data | `#0F7B6C` deep teal | Confident, forward |
| Narrative / Annual | `#B45309` amber | Warm, momentum |

The pre-output self-check in `design-quality.md` ends with a final gate: *"If you told someone 'an AI wrote this', would they immediately believe it? If yes — find the most generic-looking part and redesign it."*

## Use Cases

### Daily work report via OpenClaw → Telegram / Discord

Ask your OpenClaw assistant at the end of the day:

```
Generate a report of your work today in dark-board style, export it as an IM image, and send it to me via Telegram (or Discord).
```

OpenClaw will:
1. Summarize today's completed tasks, key decisions, and next steps
2. Render them into a `dark-board` HTML report with KPI cards and a timeline
3. Screenshot the page as an 800 px JPEG (IM long-image format, animations disabled automatically)
4. Deliver the image directly to your Telegram or Discord channel

The result is a visually rich daily summary readable right inside the chat — no browser required.

> **Why this works:** Every generated report detects headless screenshot environments (`navigator.webdriver`) and immediately disables fade-in animations, so tables, timelines, and KPI grids are fully visible in the captured image.

---

## Examples

| File | Description |
|------|-------------|
| [examples/en/business-report.html](examples/en/business-report.html) | 2024 Q3 Sales Performance Report (EN) |
| [examples/zh/business-report.html](examples/zh/business-report.html) | 2024 Q3 销售业绩报告（中文）|

## License

MIT
