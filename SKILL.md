---
name: kai-report-creator
description: Use when the user wants to create a report, business summary, data dashboard, research doc, or formatted HTML output from notes, data, or a URL. Triggers: /report, --plan, --generate, --themes, --from, --bundle, or any mention of "HTML report", "KPI dashboard", "generate report".
version: 1.0.0
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

**viewBox height rule:** Always add 30px of bottom padding beyond the last drawn element's bottom edge. For example, if the lowest element ends at y=346, set viewBox height to 376. This prevents content clipping.

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

When generating HTML, load theme CSS from `templates/themes/` (relative to this skill file's directory).

**CSS assembly order in `<style>`:**
1. Read `templates/themes/[theme-name].css` — embed everything **before** `/* === POST-SHARED OVERRIDE */`
2. Read `templates/themes/shared.css` — embed in full
3. From `[theme-name].css` — embed everything **after** `/* === POST-SHARED OVERRIDE */` (if present)
4. If `theme_overrides` is set in frontmatter, append `:root { ... }` override block last

**Theme names:** `corporate-blue`, `minimal`, `dark-tech`, `dark-board`, `data-story`, `newspaper`

**Themes with POST-SHARED OVERRIDE sections:** `dark-board`, `data-story`, `newspaper`

**Special code block note:** `dark-tech` and `dark-board` use `github-dark.min.css` instead of `github.min.css` for highlight.js.

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
          overflow-y: auto; padding: 3rem 1rem 1.5rem; background: var(--surface);
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

      <!-- Edit mode (always present) -->
      <div class="edit-hotzone" id="edit-hotzone"></div>
      <button class="edit-toggle" id="edit-toggle" title="Edit mode (E)">✏ Edit</button>

      <!-- Export (always present) -->
      <!-- lang:en labels: "↓ Export" / "🖨 Print / PDF" / "🖥 Save PNG (Desktop)" / "📱 Save PNG (Mobile)" -->
      <!-- lang:zh labels: "↓ 导出"  / "🖨 打印 / PDF"  / "🖥 保存图片（桌面）"    / "📱 保存图片（手机）"  -->
      <div class="export-menu" id="export-menu">
        <button class="export-item" onclick="window.print()">[🖨 Print / PDF|🖨 打印 / PDF]</button>
        <button class="export-item" id="export-png-desktop">[🖥 Save PNG (Desktop)|🖥 保存图片（桌面）]</button>
        <button class="export-item" id="export-png-mobile">[📱 Save PNG (Mobile)|📱 保存图片（手机）]</button>
      </div>
      <button class="export-btn" id="export-btn" title="Export">[↓ Export|↓ 导出]</button>

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
            if (!locked) scheduleClose();
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

      <script>
        // Edit mode: hover bottom-left hotzone to reveal button, click to toggle
        (function() {
          const hotzone = document.getElementById('edit-hotzone');
          const toggle  = document.getElementById('edit-toggle');
          if (!hotzone || !toggle) return;
          let active = false, hideTimer;
          function showBtn() { clearTimeout(hideTimer); toggle.classList.add('show'); }
          function schedHide() { hideTimer = setTimeout(() => { if (!active) toggle.classList.remove('show'); }, 400); }
          hotzone.addEventListener('mouseenter', showBtn);
          hotzone.addEventListener('mouseleave', schedHide);
          toggle.addEventListener('mouseenter', showBtn);
          toggle.addEventListener('mouseleave', schedHide);
          function enterEdit() {
            active = true; toggle.classList.add('active', 'show'); toggle.textContent = '✓ Done';
            document.body.classList.add('edit-mode');
            document.querySelectorAll('h1,h2,h3,p,li,td,th,figcaption').forEach(el => el.setAttribute('contenteditable', 'true'));
          }
          function exitEdit() {
            active = false; toggle.classList.remove('active'); toggle.textContent = '✏ Edit';
            document.body.classList.remove('edit-mode');
            document.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
            schedHide();
          }
          hotzone.addEventListener('click', () => active ? exitEdit() : enterEdit());
          toggle.addEventListener('click', () => active ? exitEdit() : enterEdit());
          document.addEventListener('keydown', e => {
            if ((e.key === 'e' || e.key === 'E') && !document.activeElement.getAttribute('contenteditable')) {
              active ? exitEdit() : enterEdit();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
              e.preventDefault();
              const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
              const a = Object.assign(document.createElement('a'), {
                href: URL.createObjectURL(new Blob([html], {type: 'text/html'})),
                download: location.pathname.split('/').pop() || 'report.html'
              });
              a.click(); URL.revokeObjectURL(a.href);
            }
          });
        })();
      </script>

      <script>
        // Export: Print/PDF via window.print(); PNG via html2canvas (lazy CDN)
        // Desktop PNG: full-page at 2× scale
        // Mobile PNG: .report-wrapper only, scaled to 1170px wide (≈ 3× iPhone width)
        (function() {
          const exportBtn  = document.getElementById('export-btn');
          const exportMenu = document.getElementById('export-menu');
          const pngDesktop = document.getElementById('export-png-desktop');
          const pngMobile  = document.getElementById('export-png-mobile');
          if (!exportBtn || !exportMenu) return;
          const LABEL = exportBtn.textContent;

          exportBtn.addEventListener('click', e => { e.stopPropagation(); exportMenu.classList.toggle('open'); });
          document.addEventListener('click', e => {
            if (!exportBtn.contains(e.target) && !exportMenu.contains(e.target))
              exportMenu.classList.remove('open');
          });

          function withLib(fn) {
            exportMenu.classList.remove('open');
            exportBtn.style.visibility = 'hidden';
            if (window.html2canvas) { fn(); return; }
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1/dist/html2canvas.min.js';
            s.onload = fn; document.head.appendChild(s);
          }
          function restore() { exportBtn.style.visibility = ''; exportBtn.textContent = LABEL; }
          function download(canvas, suffix) {
            canvas.toBlob(blob => {
              const a = Object.assign(document.createElement('a'), {
                href: URL.createObjectURL(blob),
                download: (document.title || 'report') + suffix + '.png'
              });
              a.click(); URL.revokeObjectURL(a.href); restore();
            }, 'image/png');
          }

          pngDesktop && pngDesktop.addEventListener('click', () => withLib(() => {
            exportBtn.textContent = '…';
            document.querySelectorAll('.fade-in-up').forEach(el => el.classList.add('visible'));
            html2canvas(document.documentElement, {
              scale: 2, useCORS: true, allowTaint: true,
              scrollX: 0, scrollY: 0,
              width: document.documentElement.scrollWidth,
              height: document.documentElement.scrollHeight,
              windowWidth: document.documentElement.scrollWidth,
              windowHeight: document.documentElement.scrollHeight
            }).then(c => download(c, ''));
          }));

          pngMobile && pngMobile.addEventListener('click', () => withLib(() => {
            exportBtn.textContent = '…';
            document.querySelectorAll('.fade-in-up').forEach(el => el.classList.add('visible'));
            const el = document.querySelector('.report-wrapper') || document.documentElement;
            const scale = Math.min(3, 1170 / el.offsetWidth);
            html2canvas(el, {
              scale, useCORS: true, allowTaint: true,
              scrollX: 0, scrollY: 0,
              width: el.scrollWidth, height: el.scrollHeight
            }).then(c => download(c, '-mobile'));
          }));
        })();
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
   - `{{report.theme_css}}` → selected theme CSS + shared component CSS (assembled per Theme CSS rules above)
   - `{{report.summary_json}}` → the complete `<script type="application/json" id="report-summary">...</script>` block (including the script tags)
3. If `logo` is set in `theme_overrides`, prepend `<img src="[logo]" alt="Company logo" class="report-logo" style="height:48px;margin-bottom:1.5rem;display:block">` at the start of `{{report.body}}` content.
4. Output the result as the HTML file

**Example template:** `templates/_custom-template.example.html` — a documented starting point showing all available placeholders. Users can copy and customize it for their own branding. The leading underscore signals that this file is not loaded automatically.

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
