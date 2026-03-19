# Component Rendering Rules

When rendering IR to HTML, apply these rules per block type. Each component must be wrapped with `data-component` attribute for AI readability.

## CRITICAL: IR Directive Parsing — Never Let `:::` Leak Into Output

**Before emitting any HTML, do a mental pass to ensure zero `:::` sequences appear in the final output.** Any `:::` in the output means an IR directive was not converted — this is a bug.

### Block Detection Rules

A `:::` directive block has this structure:

    :::tag [param=value ...]
    [content — can be multiple lines, YAML, or a Markdown list]
    :::

**The closing `:::` is ALWAYS on its own line.** Parse the IR line by line:
1. When you see a line starting with `:::tag`, begin collecting the block body.
2. Collect all lines until you hit a line that is exactly `:::` (the closing marker).
3. Convert the entire block (opening tag + body + closing `:::`) to HTML per the rules below.
4. Never output the `:::tag`, params, closing `:::`, or any part of the directive syntax as text.

**Single-line `:::` format also exists** (generated when the block body is short):

    :::list style=ordered 1. Item A 2. Item B :::

When the opening and closing `:::` appear on the same line, treat everything between the tag/params and the trailing `:::` as the block body, split on the item separators (numbered or bullet items).

**NEVER pass `:::` lines through to HTML as `<p>` tags or any other text node.** If in doubt: parse it as a block, not as prose.

## Plain Markdown (default)

Convert using standard Markdown rules. Wrap each `##` section in:

    <section data-section="[heading text]" data-summary="[one sentence summary]">
      <h2 id="section-[slug]">[heading text]</h2>
      [section content]
    </section>

**`data-summary` must be plain text only** — write a short human-readable summary of the section in natural language. Never copy raw IR content (lists, prose, component bodies) into it. Especially never include `:::` directive syntax in `data-summary`.

For `###` headings: `<h3 id="section-[slug]">[heading text]</h3>`

## :::kpi

Each list item format: `- Label: Value TrendSymbol`
Trend: `↑` = positive (green), `↓` = negative (red), `→` = neutral (gray).

Extract the numeric part of Value into `data-target-value`, set `data-prefix` and `data-suffix`.

**Accent system:** When a KPI grid has 2+ cards, assign `data-accent` cycling `blue → green → purple → orange` (also: `teal`, `red`). Each card gets a distinct top-border color and matching value color — avoids the flat single-color look.

**Trend badge:** Prefer `.kpi-delta` pill over plain `.kpi-trend` for stronger visual emphasis. Use `kpi-delta--up` (green), `kpi-delta--down` (red), `kpi-delta--info` (blue, neutral comparisons).

    <div data-component="kpi" class="kpi-grid">
      <div class="kpi-card fade-in-up" data-accent="blue">
        <div class="kpi-label">MAU</div>
        <div class="kpi-value" data-target-value="128" data-suffix="K">128K</div>
        <div class="kpi-delta kpi-delta--up">↑18% MoM</div>
      </div>
      <div class="kpi-card fade-in-up" data-accent="green">
        <div class="kpi-label">Paid Conversion</div>
        <div class="kpi-value" data-target-value="8.6" data-suffix="%">8.6%</div>
        <div class="kpi-delta kpi-delta--up">↑1.2 pts</div>
      </div>
      <div class="kpi-card fade-in-up" data-accent="purple">
        <div class="kpi-label">D1 Retention</div>
        <div class="kpi-value" data-target-value="67" data-suffix="%">67%</div>
        <div class="kpi-delta kpi-delta--info">vs 55% avg</div>
      </div>
      <div class="kpi-card fade-in-up" data-accent="orange">
        <div class="kpi-label">NPS</div>
        <div class="kpi-value" data-target-value="72">72</div>
        <div class="kpi-delta kpi-delta--up">↑8 pts</div>
      </div>
    </div>

**Badges / chips** (`.badge .badge--[color]`): Use inline in prose, table cells, and timeline items to add categorical color. Colors: `blue`, `green`, `purple`, `orange`, `red`, `gray`, `teal`.

    <span class="badge badge--green">Shipped</span>
    <span class="badge badge--orange">In Progress</span>
    <span class="badge badge--red">Critical</span>
    <span class="badge badge--blue">Q4 Priority</span>

## :::chart

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

## :::table

Body is a Markdown table. Convert to HTML. If `caption` param is provided, emit `<caption>[caption text]</caption>` as the first child of `<table>`.

    <div data-component="table" class="table-wrapper fade-in-up">
      <table class="report-table">
        <caption>Table title if provided</caption>
        <thead><tr><th>Col1</th>...</tr></thead>
        <tbody><tr><td>Val</td>...</tr></tbody>
      </table>
    </div>

## :::list

Body is a Markdown list (ordered `1. Item` or unordered `- Item`). `style=ordered` → `<ol>`, default → `<ul>`.

**Single-line format:** `:::list style=ordered 1. A 2. B :::` — split on `N. ` or `- ` separators to recover individual items; render the same HTML below.

    <div data-component="list" class="report-list">
      <ul class="styled-list">  <!-- or <ol> if style=ordered -->
        <li>Item</li>
        <li>Item with sub-items
          <ul><li>Sub-item</li></ul>
        </li>
      </ul>
    </div>

If an item has indented sub-items (2-space or 4-space indent), render them as nested `<ul>` or `<ol>` inside the parent `<li>`.

**Do NOT output `:::list`, params, or `:::` closing marker as text — they are never user-visible content.**

## :::image

    <figure data-component="image" class="report-image report-image--[layout]">
      <img src="[src]" alt="[alt]" loading="lazy">
      <figcaption>[caption]</figcaption>
    </figure>

layout=left: float left, max-width 40%, text wraps right.
layout=right: float right, max-width 40%, text wraps left.
layout=full (default): full width, centered.

## :::timeline

Each item: `- Date: Description` or `- Label: Description`

    <div data-component="timeline" class="timeline fade-in-up">
      <div class="timeline-item">
        <div class="timeline-date">2024-07</div>
        <div class="timeline-dot"></div>
        <div class="timeline-content">Project kickoff</div>
      </div>
    </div>

## :::diagram

Generate inline SVG. All SVGs must be self-contained (no external refs). Wrap in:

    <div data-component="diagram" data-type="[type]" class="diagram-wrapper fade-in-up">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 [w] [h]">
        <!-- generated SVG -->
      </svg>
    </div>

**viewBox height rule:** Always add 30px of bottom padding beyond the last drawn element's bottom edge. For example, if the lowest element ends at y=346, set viewBox height to 376. This prevents content clipping.

**type=sequence:** Draw vertical lifelines for each actor, horizontal arrows for each step. Actors as columns at top with labels, steps numbered on left, arrows with labels between lifelines.
Sizing: width = 180 × (actor count), height = 80 + 50 × (step count).

**type=flowchart:** Draw nodes as shapes (circle=oval, diamond=rhombus, rect=rectangle). Connect with directed arrows. Use edge labels where provided.
Sizing: width = 600, height = 120 × (node count).

**type=tree:** Top-down tree with root at top, children below, connected by lines.
Sizing: width = 200 × (max leaf count at any level), height = 120 × (depth).

**type=mindmap:** Radial layout, center node in middle, branches radiating out with items as leaf nodes.
Sizing: width = 700, height = 500.

## :::code

    <div data-component="code" class="code-wrapper">
      <div class="code-title">[title if provided]</div>
      <pre><code class="language-[lang]">[HTML-escaped code content]</code></pre>
    </div>

Add `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github.min.css">` and `<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/highlight.min.js"></script>` + `<script>hljs.highlightAll();</script>` in head (or inline the full highlight.js CSS and JS if `--bundle` mode).

For dark-tech theme use `github-dark.min.css` instead of `github.min.css`.

## :::callout

    <div data-component="callout" class="callout callout--[type] fade-in-up">
      <span class="callout-icon">[icon or default]</span>
      <div class="callout-body">[content]</div>
    </div>

Default icons: note→ℹ️, tip→💡, warning→⚠️, danger→🚫

## Custom Blocks

For each `:::tag-name` matching a key in frontmatter `custom_blocks`:
1. Get the HTML template string from `custom_blocks.[tag-name]`
2. Parse block body as YAML to get field values
3. Replace `{{field}}` with the value
4. Replace `{{content}}` with any non-YAML plain text lines in the block
5. For `{{#each list}}...{{this}}...{{/each}}`, iterate the array and repeat the inner template
6. Wrap result in: `<div data-component="custom" data-tag="[tag-name]">[expanded HTML]</div>`