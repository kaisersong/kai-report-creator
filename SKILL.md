---
name: kai-report-creator
description: Generate beautiful single-file HTML reports with mixed text, charts, KPI cards, timelines, diagrams, and images. Use when the user wants to create a report, business summary, research doc, or formatted HTML output. Supports --plan (generate IR outline), --generate (render IR to HTML), --themes (preview styles), --bundle (offline HTML), --from (read file), --output (custom filename).
version: 1.0.0
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
    lang: zh                               # Optional. zh | en. Default: zh
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

## --plan Mode

When the user runs `/report --plan "topic"`:

1. Think about the report structure: appropriate sections, data the user likely has.
2. Generate a complete `.report.md` IR file containing:
   - Complete frontmatter with all relevant fields filled in
   - At least 3–5 sections with `##` headings
   - A mix of component types (kpi, chart, table, timeline, callout, etc.)
   - Placeholder values for data: use `[INSERT VALUE]` — **never fabricate numbers**
   - Comments for fields the user should customize
3. Save to `report-<slug>.report.md` using the Write tool.
4. Tell the user:
   - The IR file path
   - Which placeholders need to be filled in
   - The command to render: `/report --generate <filename>.report.md`

**Stop after saving the IR file. Do NOT generate HTML in --plan mode.**

## --themes Mode

When the user runs `/report --themes`, write the following HTML verbatim to `report-themes-preview.html`, then tell the user the file path and ask them to open it in a browser:

    <!DOCTYPE html>
    <html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>report-creator — Theme Previews</title>
    <style>
      body{margin:0;font-family:system-ui;background:#F3F4F6}
      .page{max-width:980px;margin:0 auto;padding:2rem}
      h1{text-align:center;margin-bottom:2rem;color:#111;font-size:1.5rem}
      .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:1.5rem}
      .card{border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.12)}
      .card-header{padding:1.25rem 1.5rem;display:flex;justify-content:space-between;align-items:flex-start}
      .card-header h2{margin:0;font-size:1rem;font-weight:700}
      .card-header .desc{font-size:0.78rem;opacity:0.7;margin-top:2px}
      .swatches{display:flex;gap:6px;flex-shrink:0}
      .swatch{width:20px;height:20px;border-radius:50%;border:2px solid rgba(255,255,255,.4)}
      .card-body{padding:1.5rem}
      .mini-h2{font-size:1.05rem;font-weight:700;margin:0 0 0.85rem}
      .mini-kpi{display:flex;gap:0.6rem;margin-bottom:1rem}
      .mini-kpi-item{flex:1;padding:0.65rem 0.5rem;border-radius:6px;text-align:center}
      .mini-kpi-label{font-size:0.68rem;opacity:0.6;text-transform:uppercase;letter-spacing:.04em}
      .mini-kpi-value{font-size:1.3rem;font-weight:700;line-height:1.2;margin:2px 0}
      .mini-kpi-trend{font-size:0.72rem}
      .mini-p{font-size:0.83rem;line-height:1.65;margin:0;opacity:0.75}
    </style></head><body>
    <div class="page">
      <h1>report-creator — Theme Previews</h1>
      <div class="grid">
        <div class="card" style="background:#fff">
          <div class="card-header" style="background:#1A56DB;color:#fff">
            <div><h2 style="color:#fff">corporate-blue</h2><div class="desc">Professional · Business</div></div>
            <div class="swatches"><div class="swatch" style="background:#1A56DB"></div><div class="swatch" style="background:#E3EDFF;border-color:#1A56DB"></div><div class="swatch" style="background:#111928"></div></div>
          </div>
          <div class="card-body" style="font-family:Inter,system-ui,sans-serif;color:#111928">
            <div class="mini-h2" style="border-left:4px solid #1A56DB;padding-left:.6rem">Q3 Core Metrics</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#E3EDFF"><div class="mini-kpi-label">Revenue</div><div class="mini-kpi-value" style="color:#1A56DB">$2.45M</div><div class="mini-kpi-trend" style="color:#057A55">↑12%</div></div>
              <div class="mini-kpi-item" style="background:#E3EDFF"><div class="mini-kpi-label">New Clients</div><div class="mini-kpi-value" style="color:#1A56DB">183</div><div class="mini-kpi-trend" style="color:#057A55">↑8%</div></div>
              <div class="mini-kpi-item" style="background:#E3EDFF"><div class="mini-kpi-label">Achievement</div><div class="mini-kpi-value" style="color:#1A56DB">108%</div><div class="mini-kpi-trend" style="color:#6B7280">→</div></div>
            </div>
            <p class="mini-p">South region exceeded target at 115%, best performance of the year. Recommend expanding team headcount in Q4.</p>
          </div>
        </div>
        <div class="card" style="background:#fff;border:1px solid #E5E7EB">
          <div class="card-header" style="background:#F9FAFB;color:#111827;border-bottom:1px solid #E5E7EB">
            <div><h2 style="color:#111827">minimal</h2><div class="desc" style="color:#6B7280">Academic · Research</div></div>
            <div class="swatches"><div class="swatch" style="background:#111827;border-color:#111827"></div><div class="swatch" style="background:#F3F4F6;border-color:#9CA3AF"></div><div class="swatch" style="background:#6B7280;border-color:#6B7280"></div></div>
          </div>
          <div class="card-body" style="font-family:Georgia,serif;color:#374151">
            <div class="mini-h2" style="border-bottom:1px solid #E5E7EB;padding-bottom:.35rem">Key Findings</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#F3F4F6"><div class="mini-kpi-label" style="color:#9CA3AF">Sample</div><div class="mini-kpi-value" style="color:#111827">1,200</div><div class="mini-kpi-trend" style="color:#9CA3AF">ppl</div></div>
              <div class="mini-kpi-item" style="background:#F3F4F6"><div class="mini-kpi-label" style="color:#9CA3AF">Satisfaction</div><div class="mini-kpi-value" style="color:#111827">78%</div><div class="mini-kpi-trend" style="color:#065F46">↑</div></div>
              <div class="mini-kpi-item" style="background:#F3F4F6"><div class="mini-kpi-label" style="color:#9CA3AF">Products</div><div class="mini-kpi-value" style="color:#111827">6</div><div class="mini-kpi-trend" style="color:#9CA3AF">items</div></div>
            </div>
            <p class="mini-p">78% of users report AI assistants improve daily coding efficiency by 30%+. Enterprise demand for on-premise deployment is strong.</p>
          </div>
        </div>
        <div class="card">
          <div class="card-header" style="background:#1E1B4B;color:#E2E8F0">
            <div><h2 style="color:#818CF8;font-family:monospace">dark-tech</h2><div class="desc" style="color:#94A3B8">Dark Tech · Docs</div></div>
            <div class="swatches"><div class="swatch" style="background:#818CF8"></div><div class="swatch" style="background:#1E1B4B;border-color:#818CF8"></div><div class="swatch" style="background:#A78BFA"></div></div>
          </div>
          <div class="card-body" style="background:#0F172A;font-family:Inter,system-ui;color:#E2E8F0">
            <div class="mini-h2" style="color:#818CF8;font-family:monospace;border-bottom:1px solid #334155;padding-bottom:.35rem">System Status</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#1E293B;border:1px solid #334155"><div class="mini-kpi-label" style="color:#94A3B8">Latency</div><div class="mini-kpi-value" style="color:#818CF8">12ms</div><div class="mini-kpi-trend" style="color:#34D399">↓ good</div></div>
              <div class="mini-kpi-item" style="background:#1E293B;border:1px solid #334155"><div class="mini-kpi-label" style="color:#94A3B8">Uptime</div><div class="mini-kpi-value" style="color:#818CF8">99.9%</div><div class="mini-kpi-trend" style="color:#34D399">↑</div></div>
              <div class="mini-kpi-item" style="background:#1E293B;border:1px solid #334155"><div class="mini-kpi-label" style="color:#94A3B8">Deploy</div><div class="mini-kpi-value" style="color:#818CF8">v2.4</div><div class="mini-kpi-trend" style="color:#94A3B8">Stable</div></div>
            </div>
            <p class="mini-p" style="color:#94A3B8">Current version deployed to production. All health checks passing, no active alerts.</p>
          </div>
        </div>
        <div class="card" style="background:#FFFBEB;border:1px solid #E7E5E4">
          <div class="card-header" style="background:#FEF3C7;color:#1C1917;border-bottom:1px solid #E7E5E4">
            <div><h2 style="color:#B45309">warm-editorial</h2><div class="desc" style="color:#78716C">Editorial · Content</div></div>
            <div class="swatches"><div class="swatch" style="background:#B45309;border-color:#B45309"></div><div class="swatch" style="background:#FEF3C7;border-color:#D97706"></div><div class="swatch" style="background:#1C1917;border-color:#1C1917"></div></div>
          </div>
          <div class="card-body" style="font-family:Georgia,serif;color:#1C1917">
            <div class="mini-h2" style="color:#1C1917">Industry Insights</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#FEF9EE;border:1px solid #E7E5E4"><div class="mini-kpi-label" style="color:#78716C">Readers</div><div class="mini-kpi-value" style="color:#B45309">12,400</div><div class="mini-kpi-trend" style="color:#166534">↑18%</div></div>
              <div class="mini-kpi-item" style="background:#FEF9EE;border:1px solid #E7E5E4"><div class="mini-kpi-label" style="color:#78716C">Read Rate</div><div class="mini-kpi-value" style="color:#B45309">64%</div><div class="mini-kpi-trend" style="color:#166534">↑</div></div>
              <div class="mini-kpi-item" style="background:#FEF9EE;border:1px solid #E7E5E4"><div class="mini-kpi-label" style="color:#78716C">Shares</div><div class="mini-kpi-value" style="color:#B45309">890</div><div class="mini-kpi-trend" style="color:#166534">↑</div></div>
            </div>
            <p class="mini-p">This issue's read-through rate of 64% far exceeds the 42% industry average. Curated content strategy is working.</p>
          </div>
        </div>
      </div>
    </div></body></html>

## Component Rendering Rules

When rendering IR to HTML, apply these rules per block type. Each component must be wrapped with `data-component` attribute for AI readability.

### Plain Markdown (default)

Convert using standard Markdown rules. Wrap each `##` section in:

    <section data-section="[heading text]" data-summary="[one sentence summary]">
      <h2 id="section-[slug]">[heading text]</h2>
      [section content]
    </section>

For `###` headings: `<h3 id="section-[slug]">[heading text]</h3>`

### :::kpi

Each list item format: `- Label: Value TrendSymbol`
Trend: `↑` = positive (green), `↓` = negative (red), `→` = neutral (gray). If no trend symbol is present, omit the `kpi-trend` div entirely.

Extract the numeric part of Value into `data-target-value`, set `data-prefix` and `data-suffix`.

    <div data-component="kpi" class="kpi-grid">
      <div class="kpi-card fade-in-up">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value" data-target-value="2450" data-prefix="$" data-suffix="K">$2,450K</div>
        <div class="kpi-trend kpi-trend--up">↑12%</div>
      </div>
    </div>

### :::chart

Choose library: Chart.js for bar/line/pie/scatter; ECharts for radar/funnel/heatmap/multi-axis. If any chart in report needs ECharts, use ECharts for ALL charts. Never load both libraries.

    <div data-component="chart" data-type="bar" data-raw='{"labels":[...],"datasets":[...]}' class="fade-in-up">
      <canvas id="chart-[unique-id]"></canvas>
      <script>
        new Chart(document.getElementById('chart-[unique-id]'), {
          type: 'bar',
          data: { labels: [...], datasets: [{ label: '...', data: [...], backgroundColor: 'rgba(26,86,219,0.8)' }] },
          options: { responsive: true, plugins: { legend: { position: 'top' } } }
        });
      </script>
    </div>

Use theme's `--primary` color for chart colors. Add `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>` in `<head>` (or inline if `--bundle`).

**ECharts rendering** (used when any chart in the report requires radar/funnel/heatmap/multi-axis):

    <div data-component="chart" data-type="radar" data-raw='{"legend":["..."],"series":[{"name":"...","data":[...]}]}' class="fade-in-up">
      <div id="chart-[unique-id]" style="height:300px"></div>
      <script>
        var chart = echarts.init(document.getElementById('chart-[unique-id]'));
        chart.setOption({
          legend: { data: ['...'] },
          series: [{ type: 'radar', data: [{ value: [...], name: '...' }] }]
        });
      </script>
    </div>

Add `<script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>` in `<head>` (or inline if `--bundle`). The `data-raw` attribute for ECharts uses `series` format matching the ECharts `setOption` data structure.

### :::table

Body is a Markdown table. Convert to HTML. If `caption` param is provided, emit `<caption>[caption text]</caption>` as the first child of `<table>`.

    <div data-component="table" class="table-wrapper fade-in-up">
      <table class="report-table">
        <caption>Table title if provided</caption>
        <thead><tr><th>Col1</th>...</tr></thead>
        <tbody><tr><td>Val</td>...</tr></tbody>
      </table>
    </div>

### :::list

    <div data-component="list" class="report-list">
      <ul class="styled-list">  <!-- or <ol> if style=ordered -->
        <li>Item</li>
        <li>Item with sub-items
          <ul><li>Sub-item</li></ul>
        </li>
      </ul>
    </div>

If an item has indented sub-items (2-space or 4-space indent), render them as nested `<ul>` or `<ol>` inside the parent `<li>`.

### :::image

    <figure data-component="image" class="report-image report-image--[layout]">
      <img src="[src]" alt="[alt]" loading="lazy">
      <figcaption>[caption]</figcaption>
    </figure>

layout=left: float left, max-width 40%, text wraps right.
layout=right: float right, max-width 40%, text wraps left.
layout=full (default): full width, centered.

### :::timeline

Each item: `- Date: Description` or `- Label: Description`

    <div data-component="timeline" class="timeline fade-in-up">
      <div class="timeline-item">
        <div class="timeline-date">2024-07</div>
        <div class="timeline-dot"></div>
        <div class="timeline-content">Project kickoff</div>
      </div>
    </div>

### :::diagram

Generate inline SVG. All SVGs must be self-contained (no external refs). Wrap in:

    <div data-component="diagram" data-type="[type]" class="diagram-wrapper fade-in-up">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 [w] [h]">
        <!-- generated SVG -->
      </svg>
    </div>

**type=sequence:** Draw vertical lifelines for each actor, horizontal arrows for each step. Actors as columns at top with labels, steps numbered on left, arrows with labels between lifelines.
Sizing: width = 180 × (actor count), height = 80 + 50 × (step count).

**type=flowchart:** Draw nodes as shapes (circle=oval, diamond=rhombus, rect=rectangle). Connect with directed arrows. Use edge labels where provided.
Sizing: width = 600, height = 120 × (node count).

**type=tree:** Top-down tree with root at top, children below, connected by lines.
Sizing: width = 200 × (max leaf count at any level), height = 120 × (depth).

**type=mindmap:** Radial layout, center node in middle, branches radiating out with items as leaf nodes.
Sizing: width = 700, height = 500.

### :::code

    <div data-component="code" class="code-wrapper">
      <div class="code-title">[title if provided]</div>
      <pre><code class="language-[lang]">[HTML-escaped code content]</code></pre>
    </div>

Add `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github.min.css">` and `<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/highlight.min.js"></script>` + `<script>hljs.highlightAll();</script>` in head (or inline the full highlight.js CSS and JS if `--bundle` mode).

For dark-tech theme use `github-dark.min.css` instead of `github.min.css`.

### :::callout

    <div data-component="callout" class="callout callout--[type] fade-in-up">
      <span class="callout-icon">[icon or default]</span>
      <div class="callout-body">[content]</div>
    </div>

Default icons: note→ℹ️, tip→💡, warning→⚠️, danger→🚫

### Custom Blocks

For each `:::tag-name` matching a key in frontmatter `custom_blocks`:
1. Get the HTML template string from `custom_blocks.[tag-name]`
2. Parse block body as YAML to get field values
3. Replace `{{field}}` with the value
4. Replace `{{content}}` with any non-YAML plain text lines in the block
5. For `{{#each list}}...{{this}}...{{/each}}`, iterate the array and repeat the inner template
6. Wrap result in: `<div data-component="custom" data-tag="[tag-name]">[expanded HTML]</div>`

## Theme CSS

When generating HTML, embed the selected theme's CSS verbatim in `<style>` inside `<head>`, followed by shared component CSS. Apply `theme_overrides` by appending CSS variable overrides after the theme block.

### Theme: corporate-blue

    :root {
      --primary: #1A56DB; --primary-light: #E3EDFF; --accent: #1C64F2;
      --bg: #FFFFFF; --surface: #F9FAFB; --text: #111928; --text-muted: #6B7280;
      --border: #E5E7EB; --success: #057A55; --warning: #B45309; --danger: #E02424;
      --font-sans: 'Inter', 'PingFang SC', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace; --radius: 8px;
    }
    body { font-family: var(--font-sans); color: var(--text); background: var(--bg); margin: 0; line-height: 1.7; }
    h1 { font-size: 2.25rem; font-weight: 700; color: var(--primary); border-bottom: 3px solid var(--primary); padding-bottom: .5rem; margin-bottom: 1.5rem; }
    h2 { font-size: 1.5rem; font-weight: 600; color: var(--text); border-left: 4px solid var(--primary); padding-left: .75rem; margin-top: 2.5rem; }
    h3 { font-size: 1.15rem; font-weight: 600; color: var(--text); margin-top: 1.5rem; }
    p { margin: .75rem 0; } a { color: var(--primary); }
    strong { font-weight: 700; } blockquote { border-left: 3px solid var(--border); margin: 1rem 0; padding: .5rem 1rem; color: var(--text-muted); }

### Theme: minimal

    :root {
      --primary: #111827; --primary-light: #F3F4F6; --accent: #6B7280;
      --bg: #FFFFFF; --surface: #F9FAFB; --text: #374151; --text-muted: #9CA3AF;
      --border: #E5E7EB; --success: #065F46; --warning: #92400E; --danger: #991B1B;
      --font-sans: 'Georgia', 'Noto Serif SC', serif;
      --font-mono: 'Courier New', monospace; --radius: 4px;
    }
    body { font-family: var(--font-sans); color: var(--text); background: var(--bg); margin: 0; line-height: 1.85; }
    h1 { font-size: 2rem; font-weight: 700; color: var(--primary); letter-spacing: -.02em; margin-bottom: 1.5rem; }
    h2 { font-size: 1.35rem; font-weight: 700; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: .4rem; margin-top: 2.5rem; }
    h3 { font-size: 1.1rem; font-weight: 700; color: var(--text); margin-top: 1.5rem; }
    p { margin: .85rem 0; } a { color: var(--primary); text-decoration: underline; }
    strong { font-weight: 700; } blockquote { border-left: 2px solid var(--border); margin: 1rem 0; padding: .5rem 1.25rem; font-style: italic; color: var(--text-muted); }

### Theme: dark-tech

    :root {
      --primary: #818CF8; --primary-light: #312E81; --accent: #A78BFA;
      --bg: #0F172A; --surface: #1E293B; --text: #E2E8F0; --text-muted: #94A3B8;
      --border: #334155; --success: #34D399; --warning: #FCD34D; --danger: #F87171;
      --font-sans: 'Inter', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace; --radius: 6px;
    }
    body { font-family: var(--font-sans); color: var(--text); background: var(--bg); margin: 0; line-height: 1.7; }
    h1 { font-size: 2rem; font-weight: 700; color: var(--primary); font-family: var(--font-mono); margin-bottom: 1.5rem; }
    h2 { font-size: 1.4rem; font-weight: 600; color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: .4rem; margin-top: 2.5rem; font-family: var(--font-mono); }
    h3 { font-size: 1.1rem; font-weight: 600; color: var(--accent); margin-top: 1.5rem; }
    p { margin: .75rem 0; } a { color: var(--primary); }
    strong { font-weight: 700; color: var(--accent); } blockquote { border-left: 2px solid var(--border); margin: 1rem 0; padding: .5rem 1rem; color: var(--text-muted); font-family: var(--font-mono); font-size: .9rem; }

### Theme: warm-editorial

    :root {
      --primary: #B45309; --primary-light: #FEF3C7; --accent: #D97706;
      --bg: #FFFBEB; --surface: #FEF9EE; --text: #1C1917; --text-muted: #78716C;
      --border: #E7E5E4; --success: #166534; --warning: #92400E; --danger: #991B1B;
      --font-sans: 'Merriweather', 'Noto Serif SC', Georgia, serif;
      --font-mono: 'Courier New', monospace; --radius: 4px;
    }
    body { font-family: var(--font-sans); color: var(--text); background: var(--bg); margin: 0; line-height: 1.9; }
    h1 { font-size: 2.25rem; font-weight: 700; color: var(--primary); border-bottom: 2px solid var(--primary-light); padding-bottom: .5rem; margin-bottom: 1.5rem; }
    h2 { font-size: 1.4rem; font-weight: 700; color: var(--text); margin-top: 2.5rem; }
    h3 { font-size: 1.1rem; font-weight: 700; color: var(--primary); margin-top: 1.5rem; }
    p { margin: .85rem 0; } a { color: var(--primary); text-decoration: underline; }
    strong { font-weight: 700; } blockquote { border-left: 3px solid var(--accent); margin: 1rem 0; padding: .75rem 1.25rem; background: var(--primary-light); border-radius: var(--radius); }

### Shared Component CSS (append after theme CSS for all themes)

    /* Layout */
    *, *::before, *::after { box-sizing: border-box; }
    .report-wrapper { max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem; }
    @media (min-width: 1100px) { .report-wrapper { padding: 2.5rem 3rem; } }
    .report-meta { color: var(--text-muted); font-size: .9rem; margin-top: -.5rem; margin-bottom: 2rem; }

    /* KPI */
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
    .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; text-align: center; }
    .kpi-label { font-size: .78rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: .05em; margin-bottom: .4rem; }
    .kpi-value { font-size: 1.9rem; font-weight: 700; color: var(--primary); line-height: 1.2; }
    .kpi-trend { font-size: .85rem; margin-top: .3rem; }
    .kpi-trend--up { color: var(--success); } .kpi-trend--down { color: var(--danger); } .kpi-trend--neutral { color: var(--text-muted); }

    /* Tables */
    .table-wrapper { overflow-x: auto; margin: 1.5rem 0; }
    .report-table { width: 100%; border-collapse: collapse; font-size: .9rem; }
    .report-table th { background: var(--surface); border-bottom: 2px solid var(--primary); padding: .7rem 1rem; text-align: left; font-weight: 600; }
    .report-table td { padding: .6rem 1rem; border-bottom: 1px solid var(--border); }
    .report-table tr:hover td { background: var(--surface); }

    /* Callout */
    .callout { display: flex; gap: .75rem; padding: .9rem 1.1rem; border-radius: var(--radius); margin: 1rem 0; border-left: 4px solid; align-items: flex-start; }
    .callout--note { background: #EFF6FF; border-color: #3B82F6; }
    .callout--tip { background: #F0FDF4; border-color: #22C55E; }
    .callout--warning { background: #FFFBEB; border-color: #F59E0B; }
    .callout--danger { background: #FEF2F2; border-color: #EF4444; }
    .callout-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: .05rem; }
    .callout-body { line-height: 1.6; font-size: .93rem; }

    /* Timeline */
    .timeline { position: relative; padding-left: 2rem; margin: 1.5rem 0; }
    .timeline::before { content: ''; position: absolute; left: .45rem; top: 0; bottom: 0; width: 2px; background: var(--border); }
    .timeline-item { position: relative; margin-bottom: 1.4rem; }
    .timeline-dot { position: absolute; left: -1.65rem; top: .3rem; width: 12px; height: 12px; border-radius: 50%; background: var(--primary); border: 2px solid var(--bg); }
    .timeline-date { font-size: .78rem; color: var(--text-muted); margin-bottom: .15rem; font-weight: 600; }
    .timeline-content { color: var(--text); line-height: 1.6; }

    /* Image */
    .report-image { margin: 1.5rem 0; } .report-image img { max-width: 100%; border-radius: var(--radius); }
    .report-image figcaption { font-size: .82rem; color: var(--text-muted); text-align: center; margin-top: .4rem; }
    .report-image--left { float: left; max-width: 40%; margin-right: 1.5rem; margin-bottom: .5rem; }
    .report-image--right { float: right; max-width: 40%; margin-left: 1.5rem; margin-bottom: .5rem; }
    .report-image--full { width: 100%; display: block; }
    .clearfix::after { content: ''; display: table; clear: both; }

    /* Code */
    .code-wrapper { margin: 1.5rem 0; border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); }
    .code-title { background: var(--surface); padding: .35rem 1rem; font-size: .78rem; color: var(--text-muted); font-family: var(--font-mono); border-bottom: 1px solid var(--border); }
    .code-wrapper pre { margin: 0; overflow-x: auto; }

    /* List */
    .report-list { margin: 1rem 0; }
    .styled-list { padding-left: 1.5rem; line-height: 1.8; }
    .styled-list li { margin-bottom: .25rem; }

    /* Diagram */
    .diagram-wrapper { margin: 1.5rem 0; overflow-x: auto; text-align: center; }
    .diagram-wrapper svg { max-width: 100%; height: auto; }

    /* Chart */
    [data-component="chart"] { margin: 1.5rem 0; }

    /* Animations */
    .fade-in-up { opacity: 0; transform: translateY(18px); transition: opacity .5s ease, transform .5s ease; }
    .fade-in-up.visible { opacity: 1; transform: translateY(0); }
    body.no-animations .fade-in-up { opacity: 1; transform: none; transition: none; }

    /* Theme override variables (appended after theme block when theme_overrides is set) */
    /* :root { --primary: [override_value]; ... } */

## HTML Shell Template

When generating the final HTML report, produce a complete self-contained HTML file using this structure. Replace all `[...]` placeholders with actual content.

    <!DOCTYPE html>
    <html lang="[lang]">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>[title]</title>

      <!-- CDN libraries (add only what's needed; omit if --bundle, inline instead) -->
      <!-- If any :::chart blocks present AND using Chart.js: -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script> -->
      <!-- If any :::chart blocks present AND using ECharts: -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script> -->
      <!-- If any :::code blocks present: -->
      <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github.min.css"> -->
      <!-- (use github-dark.min.css for dark-tech theme) -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/highlight.min.js"></script> -->
      <!-- <script>document.addEventListener('DOMContentLoaded', () => hljs.highlightAll());</script> -->

      <style>
        /* [Paste the selected theme CSS here, e.g., the corporate-blue block] */

        /* [Paste the shared component CSS here] */

        /* Floating TOC overlay — default collapsed on all screen sizes */
        .toc-sidebar {
          position: fixed; top: 0; left: 0; width: 240px; height: 100vh;
          overflow-y: auto; padding: 1.5rem 1rem; background: var(--surface);
          border-right: 1px solid var(--border); font-size: .83rem; z-index: 100;
          transform: translateX(-100%); transition: transform .28s ease;
        }
        .toc-sidebar.open {
          transform: translateX(0); box-shadow: 4px 0 24px rgba(0,0,0,.18);
        }
        .toc-sidebar h4 {
          font-size: .72rem; text-transform: uppercase; letter-spacing: .08em;
          color: var(--text-muted); margin: 0 0 .75rem; font-weight: 600;
        }
        .toc-sidebar a {
          display: block; color: var(--text-muted); text-decoration: none;
          padding: .28rem .5rem; border-radius: 4px; margin-bottom: 1px; transition: all .18s;
          white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .toc-sidebar a:hover, .toc-sidebar a.active { color: var(--primary); background: var(--primary-light); }
        .toc-sidebar a.toc-h3 { padding-left: 1.1rem; font-size: .78rem; opacity: .85; }
        .main-with-toc { margin-left: 0; }
        .toc-toggle {
          position: fixed; top: .75rem; left: .75rem; z-index: 200;
          background: var(--primary); color: #fff; border: none; border-radius: 6px;
          padding: .45rem .7rem; cursor: pointer; font-size: 1rem; line-height: 1;
          box-shadow: 0 2px 8px rgba(0,0,0,.2);
        }
        .toc-toggle.locked { box-shadow: 0 0 0 2px #fff, 0 2px 8px rgba(0,0,0,.2); }
        @media (max-width: 768px) {
          .report-wrapper { padding: 1.5rem 1rem; }
        }
        body.no-toc .toc-sidebar, body.no-toc .toc-toggle { display: none; }
        body.no-toc .main-with-toc { margin-left: 0; }
      </style>
    </head>
    <body class="[add 'no-toc' if toc:false] [add 'no-animations' if animations:false]">

      <!-- AI Readability Layer 1: Report Summary JSON -->
      <!-- Always present, even if not visible to humans -->
      <script type="application/json" id="report-summary">
      {
        "title": "[title]",
        "author": "[author or empty string]",
        "date": "[date]",
        "abstract": "[abstract from frontmatter, or auto-generate a 1-sentence summary of the report content]",
        "sections": ["[heading of section 1]", "[heading of section 2]", "..."],
        "kpis": [
          {"label": "[label]", "value": "[display value]", "trend": "[trend text or empty]"}
        ]
      }
      </script>

      <!-- Floating TOC (omit entirely if toc:false) -->
      <!-- TOC label localization: lang:en → aria-label="Contents" / "Table of Contents" / <h4>Contents</h4> -->
      <!--                         lang:zh → aria-label="目录" / "报告目录" / <h4>目录</h4> -->
      <button class="toc-toggle" id="toc-toggle-btn" aria-label="[Contents|目录]" aria-expanded="false">☰</button>
      <nav class="toc-sidebar" id="toc-sidebar" aria-label="[Table of Contents|报告目录]">
        <h4>[Contents|目录]</h4>
        <!-- Generate one <a> per ## heading and one per ### heading in the report -->
        <!-- Example (lang:en): <a href="#section-core-metrics" data-section="Core Metrics">Core Metrics</a> -->
        <!-- For ### heading: add class="toc-h3" -->
        [TOC links generated from all ## and ### headings in the IR]
      </nav>

      <div class="main-with-toc">
        <div class="report-wrapper">

          <!-- Report title and meta -->
          <h1>[title]</h1>
          [if author or date: <p class="report-meta">[author] · [date]</p>]

          <!-- AI Readability Layer 2: Section annotations are on each <section> element -->
          <!-- Rendered sections — each ## becomes: -->
          <!-- <section data-section="[heading]" data-summary="[1-sentence summary]"> -->
          <!--   <h2 id="section-[slug]">[heading]</h2> -->
          <!--   [section content] -->
          <!-- </section> -->

          [All rendered section content here]

        </div>
      </div>

      <script>
        // Scroll-triggered fade-in animations
        if (!document.body.classList.contains('no-animations')) {
          const fadeObserver = new IntersectionObserver(
            entries => entries.forEach(e => {
              if (e.isIntersecting) { e.target.classList.add('visible'); fadeObserver.unobserve(e.target); }
            }),
            { threshold: 0.08 }
          );
          document.querySelectorAll('.fade-in-up').forEach(el => fadeObserver.observe(el));

          // KPI counter animation
          const kpiObserver = new IntersectionObserver(entries => {
            entries.forEach(e => {
              if (!e.isIntersecting) return;
              const el = e.target;
              const target = parseFloat(el.dataset.targetValue);
              if (isNaN(target)) return;
              const prefix = el.dataset.prefix || '';
              const suffix = el.dataset.suffix || '';
              const isFloat = String(target).includes('.');
              const decimals = isFloat ? String(target).split('.')[1].length : 0;
              let startTime = null;
              const duration = 1200;
              const animate = ts => {
                if (!startTime) startTime = ts;
                const progress = Math.min((ts - startTime) / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                const current = isFloat
                  ? (ease * target).toFixed(decimals)
                  : Math.floor(ease * target).toLocaleString();
                el.textContent = prefix + current + suffix;
                if (progress < 1) requestAnimationFrame(animate);
                else el.textContent = prefix + (isFloat ? target.toFixed(decimals) : target.toLocaleString()) + suffix;
              };
              requestAnimationFrame(animate);
              kpiObserver.unobserve(el);
            });
          }, { threshold: 0.3 });
          document.querySelectorAll('.kpi-value[data-target-value]').forEach(el => kpiObserver.observe(el));
        }

        // TOC: hover to open, click to lock, no backdrop
        const tocBtn = document.getElementById('toc-toggle-btn');
        const tocSidebar = document.getElementById('toc-sidebar');
        if (tocBtn && tocSidebar) {
          let locked = false, closeTimer;
          function openToc() {
            clearTimeout(closeTimer);
            tocSidebar.classList.add('open');
            tocBtn.setAttribute('aria-expanded', 'true');
          }
          function scheduleClose() {
            closeTimer = setTimeout(() => {
              if (!locked) {
                tocSidebar.classList.remove('open');
                tocBtn.setAttribute('aria-expanded', 'false');
              }
            }, 150);
          }
          tocBtn.addEventListener('mouseenter', openToc);
          tocSidebar.addEventListener('mouseenter', openToc);
          tocBtn.addEventListener('mouseleave', scheduleClose);
          tocSidebar.addEventListener('mouseleave', scheduleClose);
          tocBtn.addEventListener('click', () => {
            locked = !locked;
            tocBtn.classList.toggle('locked', locked);
            if (locked) openToc(); else scheduleClose();
          });
          document.querySelectorAll('.toc-sidebar a').forEach(a => a.addEventListener('click', () => {
            locked = false; tocBtn.classList.remove('locked'); scheduleClose();
          }));
        }

        // TOC active state tracking
        const tocLinks = document.querySelectorAll('.toc-sidebar a[data-section]');
        if (tocLinks.length) {
          const sectionObserver = new IntersectionObserver(entries => {
            entries.forEach(e => {
              const id = e.target.dataset.section;
              const link = document.querySelector(`.toc-sidebar a[data-section="${CSS.escape(id)}"]`);
              if (link) link.classList.toggle('active', e.isIntersecting);
            });
          }, { rootMargin: '-10% 0px -60% 0px' });
          document.querySelectorAll('section[data-section]').forEach(s => sectionObserver.observe(s));
        }
      </script>

    </body>
    </html>

## TOC Link Generation Rule

For each `##` heading with text `[heading]`, slug = heading lowercased with spaces/non-ASCII replaced by hyphens:

    <a href="#section-[slug]" data-section="[heading]">[heading]</a>

For `###` heading, same but add `class="toc-h3"`:

    <a href="#section-[slug]" data-section="[heading]" class="toc-h3">[heading]</a>

Add `id="section-[slug]"` to the corresponding `<section>` or `<h3>` elements.

## Theme Override Injection

If `theme_overrides` is set in frontmatter, append CSS variable overrides after the theme CSS block:

    :root {
      [--primary: value if primary_color set]
      [--font-sans: value if font_family set]
    }
    [if logo set: .report-wrapper::before { content: ''; display: block; background: url([logo]) no-repeat left center; background-size: contain; height: 48px; margin-bottom: 1.5rem; }]

## Custom Template Mode

If `template:` is set in frontmatter:
1. Read the template file
2. Replace these placeholders:
   - `{{report.body}}` → all rendered section content HTML
   - `{{report.title}}` → title value
   - `{{report.author}}` → author value
   - `{{report.date}}` → date value
   - `{{report.abstract}}` → abstract value
   - `{{report.theme_css}}` → selected theme CSS + shared component CSS
   - `{{report.summary_json}}` → the complete `<script type="application/json" id="report-summary">...</script>` block (including the script tags)
3. If `logo` is set in `theme_overrides`, prepend `<img src="[logo]" alt="Company logo" class="report-logo" style="height:48px;margin-bottom:1.5rem;display:block">` at the start of `{{report.body}}` content.
4. Output the result as the HTML file

## --generate Mode

When the user runs `/report --generate [file]`:
1. If a file is specified, read it with the Read tool. If no file given, look for IR in context (starts with `---`).
2. Parse the frontmatter to get metadata and settings.
3. Select the appropriate theme CSS.
4. Render all components according to Component Rendering Rules.
5. Apply chart library selection rule.
6. Build the HTML shell with TOC, AI summary, animations.
7. Write to `[output_filename].html` using the Write tool.
8. Tell the user the file path and a 1-sentence summary of the report.
