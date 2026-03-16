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
