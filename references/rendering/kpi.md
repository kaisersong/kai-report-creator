# KPI Rendering

## :::kpi

Canonical input:

```md
:::kpi
items:
  - label: 总营收
    value: ¥2,450万
    delta: ↑12%
    note: 同比
:::
```

Compatibility input:

```md
:::kpi
- 总营收: ¥2,450万 ↑12%
:::
```

Trend: `↑` = positive (green), `↓` = negative (red), `→` = neutral (gray).

**Allowed input:** `value` must be a short numeric value or brief phrase. `delta` may be a symbol alone (`→`) or a short status like `↑12% MoM`.

**Compatibility note:** Labels containing literal colons should use the canonical YAML form, not the short-line form.

- `invalid_syntax`: body is neither canonical `items:` YAML nor the compatibility short-line format.
- `invalid_semantics`: `value` is a sentence/paragraph, or the whole block exists only as placeholder decoration.
- `contract_conflict`: none.
- `auto_downgrade_target`: `callout`.

Extract the numeric part of Value into `data-target-value`, set `data-prefix` and `data-suffix`.

**Default mode: do not add `data-accent` to KPI cards.** KPI values should stay on the neutral report text color, while the card top rule uses the shared structural accent.

**Comparison mode:** Set `data-report-mode="comparison"` on the comparison wrapper only when the report is explicitly comparing named entities. In that mode, keep KPI values neutral and use `.badge--entity-a`, `.badge--entity-b`, and `.badge--entity-c` only for entity identity chips or table-cell labels.

**Trend badge:** Prefer `.kpi-delta` pill over plain `.kpi-trend` for stronger visual emphasis. Keep `kpi-delta--up`, `kpi-delta--down`, and `kpi-delta--info` visually restrained so they read as status hints, not a second palette system.

**Suffix length rule:** Keep `data-suffix` short (≤4 chars: `K`, `%`, `ms`, `x`). If the unit is longer (e.g. `commits/hour`, `req/sec`, `美元/月`), split number and unit — put the numeric part directly in `.kpi-value` and wrap the unit in `<span class="kpi-suffix">unit</span>`:

    <!-- ✅ Short suffix — inline is fine -->
    <div class="kpi-value" data-target-value="128" data-suffix="K">128K</div>

    <!-- ✅ Long unit — use kpi-suffix span, NO data-target-value (countUp rewrites textContent and destroys the span) -->
    <div class="kpi-value">1,000<span class="kpi-suffix">commits/hour</span></div>

    <!-- ❌ Never put long units directly as plain text content -->
    <div class="kpi-value">1000 commits/hour</div>

    <!-- ❌ Never combine data-target-value with kpi-suffix span — countUp will overwrite the span -->
    <div class="kpi-value" data-target-value="1000">1,000<span class="kpi-suffix">commits/hour</span></div>

**KPI value length rule (MANDATORY):** The `.kpi-value` must contain ONLY a short numeric value or very brief phrase. Maximum length:
- Numeric/currency/percentage: `128K`, `¥2,450万`, `8.6%`, `72`, `↑18%` — ✅
- Short phrase (≤8 Chinese chars / ≤3 English words): `全场景`, `行业领先`, `Top 3` — ✅
- Descriptive sentences or paragraphs: `支持CSV/Excel等表格文件的统计汇总、趋势分析、数据可视化` — ❌

If the content is a full sentence or descriptive paragraph, it belongs in prose, a `:::callout`, or a table cell — **NEVER** in a KPI card. The `:::kpi` block is for at-a-glance metrics, not explanations. When planning a report, if the source content has no short numbers to extract, use `:::callout` or `:::timeline` instead of forcing a `:::kpi` block.

**Summary card KPI value rule:** The `report-summary` JSON `kpis[].value` field feeds the summary card's `.sc-kpi-row-v` (1.15rem, compact). If a KPI value exceeds the length rule above, use the kpi-label or a separate callout for the explanation, and keep the KPI value short for the card.

**Summary card title hierarchy:** When building `report-summary` JSON, support `poster_title` and `poster_subtitle` as optional fields. Use them when the strongest summary-card headline should be more poster-like than the document H1. Render them into `.sc-title-main` and `.sc-title-sub`, with the subtitle below the title rather than merged into one dense line.

**Column count rule (from design-quality.md):** Do NOT default all grids to 3 columns. Match to KPI count:
- 1–2 KPIs → `grid-template-columns: repeat(2, 1fr)`
- 3 KPIs → `grid-template-columns: repeat(3, 1fr)`
- 4 KPIs → `grid-template-columns: repeat(2, 1fr)` (2×2 grid)
- 5–6 KPIs → `grid-template-columns: repeat(3, 1fr)`
- 7+ KPIs → `grid-template-columns: repeat(3, 1fr)` with larger `gap` and visual group dividers
- When one KPI is the hero metric, consider `grid-template-columns: 2fr 1fr 1fr` for emphasis

    <div data-component="kpi" class="kpi-grid">
      <div class="kpi-card fade-in-up">
        <div class="kpi-label">MAU</div>
        <div class="kpi-value" data-target-value="128" data-suffix="K">128K</div>
        <div class="kpi-delta kpi-delta--up">↑18% MoM</div>
      </div>
      <div class="kpi-card fade-in-up">
        <div class="kpi-label">Paid Conversion</div>
        <div class="kpi-value" data-target-value="8.6" data-suffix="%">8.6%</div>
        <div class="kpi-delta kpi-delta--up">↑1.2 pts</div>
      </div>
      <div class="kpi-card fade-in-up">
        <div class="kpi-label">D1 Retention</div>
        <div class="kpi-value" data-target-value="67" data-suffix="%">67%</div>
        <div class="kpi-delta kpi-delta--info">vs 55% avg</div>
      </div>
      <div class="kpi-card fade-in-up">
        <div class="kpi-label">NPS</div>
        <div class="kpi-value" data-target-value="72">72</div>
        <div class="kpi-delta kpi-delta--up">↑8 pts</div>
      </div>
    </div>

**Badges / chips** (`.badge .badge--[color]`): Generic badge classes remain valid input, but they should render through one neutral linen chip system by default, including in prose, table cells, and timeline items.

**Badges are optional visual enhancements, not a first-class IR tag.** Use them only when they materially improve scanability:

| Location | Example | Recommended badge |
|----------|---------|-------------------|
| Section `##` heading | `## 核心能力 <span class="badge badge--teal">核心</span>` | `badge--teal`, `badge--blue`, `badge--purple` |
| `:::kpi` card label | `<div class="kpi-label">转化率 <span class="badge badge--green">已上线</span></div>` | `badge--green`, `badge--orange`, `badge--blue` |
| `:::table` cell | `<td><span class="badge badge--wip">进行中</span></td>` | `badge--wip`, `badge--done`, `badge--todo` |
| `:::timeline` item | `<div class="timeline-content"><span class="badge badge--blue">里程碑</span> 内容</div>` | `badge--blue`, `badge--purple` |
| Callout header area | Before callout body content as a category tag | `badge--orange`, `badge--teal` |

**Badge color selection:** Choose color based on semantic meaning, not aesthetics:
- Status/progress: `badge--done` (completed), `badge--wip` (in progress), `badge--todo` (planned)
- Severity: `badge--warn` (caution), `badge--err` (error/blocker)
- Category/tag: `badge--teal` (capability), `badge--blue` (priority/important), `badge--purple` (feature/special), `badge--orange` (highlight), `badge--green` (positive/verified), `badge--gray` (misc/neutral)
- Entity comparison (only in `data-report-mode="comparison"`): `badge--entity-a`, `badge--entity-b`, `badge--entity-c`

**Do NOT overuse:** Maximum 3 badges per section. More than 3 dilutes their signal value.

**Entity badges:** Only in explicit comparison reports should entity identity use `.badge--entity-a`, `.badge--entity-b`, and `.badge--entity-c`.

    <span class="badge badge--green">Shipped</span>
    <span class="badge badge--orange">In Progress</span>
    <span class="badge badge--red">Critical</span>
    <span class="badge badge--blue">Q4 Priority</span>

    <div data-report-mode="comparison">
      <span class="badge badge--entity-a">OpenAI</span>
      <span class="badge badge--entity-b">Anthropic</span>
      <span class="badge badge--entity-c">Cursor</span>
    </div>
