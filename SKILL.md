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
   - Placeholder values for data: use `[数据待填写]` or `[INSERT VALUE]` — **never fabricate numbers**
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
    <html lang="zh"><head><meta charset="UTF-8">
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
            <div><h2 style="color:#fff">corporate-blue</h2><div class="desc">企业蓝 · 正式商务</div></div>
            <div class="swatches"><div class="swatch" style="background:#1A56DB"></div><div class="swatch" style="background:#E3EDFF;border-color:#1A56DB"></div><div class="swatch" style="background:#111928"></div></div>
          </div>
          <div class="card-body" style="font-family:Inter,system-ui,sans-serif;color:#111928">
            <div class="mini-h2" style="border-left:4px solid #1A56DB;padding-left:.6rem">Q3 核心指标</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#E3EDFF"><div class="mini-kpi-label">营收</div><div class="mini-kpi-value" style="color:#1A56DB">¥2,450万</div><div class="mini-kpi-trend" style="color:#057A55">↑12%</div></div>
              <div class="mini-kpi-item" style="background:#E3EDFF"><div class="mini-kpi-label">新客户</div><div class="mini-kpi-value" style="color:#1A56DB">183</div><div class="mini-kpi-trend" style="color:#057A55">↑8%</div></div>
              <div class="mini-kpi-item" style="background:#E3EDFF"><div class="mini-kpi-label">完成率</div><div class="mini-kpi-value" style="color:#1A56DB">108%</div><div class="mini-kpi-trend" style="color:#6B7280">→</div></div>
            </div>
            <p class="mini-p">华南区超额完成目标 115%，全年最佳表现。建议 Q4 扩大该区域销售团队编制。</p>
          </div>
        </div>
        <div class="card" style="background:#fff;border:1px solid #E5E7EB">
          <div class="card-header" style="background:#F9FAFB;color:#111827;border-bottom:1px solid #E5E7EB">
            <div><h2 style="color:#111827">minimal</h2><div class="desc" style="color:#6B7280">极简白 · 研究报告</div></div>
            <div class="swatches"><div class="swatch" style="background:#111827;border-color:#111827"></div><div class="swatch" style="background:#F3F4F6;border-color:#9CA3AF"></div><div class="swatch" style="background:#6B7280;border-color:#6B7280"></div></div>
          </div>
          <div class="card-body" style="font-family:Georgia,serif;color:#374151">
            <div class="mini-h2" style="border-bottom:1px solid #E5E7EB;padding-bottom:.35rem">核心发现</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#F3F4F6"><div class="mini-kpi-label" style="color:#9CA3AF">样本量</div><div class="mini-kpi-value" style="color:#111827">1,200</div><div class="mini-kpi-trend" style="color:#9CA3AF">人</div></div>
              <div class="mini-kpi-item" style="background:#F3F4F6"><div class="mini-kpi-label" style="color:#9CA3AF">满意度</div><div class="mini-kpi-value" style="color:#111827">78%</div><div class="mini-kpi-trend" style="color:#065F46">↑</div></div>
              <div class="mini-kpi-item" style="background:#F3F4F6"><div class="mini-kpi-label" style="color:#9CA3AF">产品数</div><div class="mini-kpi-value" style="color:#111827">6</div><div class="mini-kpi-trend" style="color:#9CA3AF">款</div></div>
            </div>
            <p class="mini-p">78% 的用户表示 AI 助手使日常编码效率提升 30% 以上，企业用户对本地部署需求强烈。</p>
          </div>
        </div>
        <div class="card">
          <div class="card-header" style="background:#1E1B4B;color:#E2E8F0">
            <div><h2 style="color:#818CF8;font-family:monospace">dark-tech</h2><div class="desc" style="color:#94A3B8">深色科技 · 技术文档</div></div>
            <div class="swatches"><div class="swatch" style="background:#818CF8"></div><div class="swatch" style="background:#1E1B4B;border-color:#818CF8"></div><div class="swatch" style="background:#A78BFA"></div></div>
          </div>
          <div class="card-body" style="background:#0F172A;font-family:Inter,system-ui;color:#E2E8F0">
            <div class="mini-h2" style="color:#818CF8;font-family:monospace;border-bottom:1px solid #334155;padding-bottom:.35rem">系统状态</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#1E293B;border:1px solid #334155"><div class="mini-kpi-label" style="color:#94A3B8">延迟</div><div class="mini-kpi-value" style="color:#818CF8">12ms</div><div class="mini-kpi-trend" style="color:#34D399">↓优</div></div>
              <div class="mini-kpi-item" style="background:#1E293B;border:1px solid #334155"><div class="mini-kpi-label" style="color:#94A3B8">可用性</div><div class="mini-kpi-value" style="color:#818CF8">99.9%</div><div class="mini-kpi-trend" style="color:#34D399">↑</div></div>
              <div class="mini-kpi-item" style="background:#1E293B;border:1px solid #334155"><div class="mini-kpi-label" style="color:#94A3B8">部署</div><div class="mini-kpi-value" style="color:#818CF8">v2.4</div><div class="mini-kpi-trend" style="color:#94A3B8">稳定</div></div>
            </div>
            <p class="mini-p" style="color:#94A3B8">当前版本已部署至生产环境，所有健康检查通过，无异常告警。</p>
          </div>
        </div>
        <div class="card" style="background:#FFFBEB;border:1px solid #E7E5E4">
          <div class="card-header" style="background:#FEF3C7;color:#1C1917;border-bottom:1px solid #E7E5E4">
            <div><h2 style="color:#B45309">warm-editorial</h2><div class="desc" style="color:#78716C">暖色编辑 · 内容输出</div></div>
            <div class="swatches"><div class="swatch" style="background:#B45309;border-color:#B45309"></div><div class="swatch" style="background:#FEF3C7;border-color:#D97706"></div><div class="swatch" style="background:#1C1917;border-color:#1C1917"></div></div>
          </div>
          <div class="card-body" style="font-family:Georgia,serif;color:#1C1917">
            <div class="mini-h2" style="color:#1C1917">行业洞察</div>
            <div class="mini-kpi">
              <div class="mini-kpi-item" style="background:#FEF9EE;border:1px solid #E7E5E4"><div class="mini-kpi-label" style="color:#78716C">读者数</div><div class="mini-kpi-value" style="color:#B45309">12,400</div><div class="mini-kpi-trend" style="color:#166534">↑18%</div></div>
              <div class="mini-kpi-item" style="background:#FEF9EE;border:1px solid #E7E5E4"><div class="mini-kpi-label" style="color:#78716C">完读率</div><div class="mini-kpi-value" style="color:#B45309">64%</div><div class="mini-kpi-trend" style="color:#166534">↑</div></div>
              <div class="mini-kpi-item" style="background:#FEF9EE;border:1px solid #E7E5E4"><div class="mini-kpi-label" style="color:#78716C">分享</div><div class="mini-kpi-value" style="color:#B45309">890</div><div class="mini-kpi-trend" style="color:#166534">↑</div></div>
            </div>
            <p class="mini-p">本期简报完读率达 64%，远高于行业均值 42%。精选内容策略效果显著。</p>
          </div>
        </div>
      </div>
    </div></body></html>
