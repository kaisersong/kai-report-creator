# Design Quality Baseline

This file defines the design quality rules for every generated report. Load alongside `rendering-rules.md` during `--generate` mode. These rules exist to prevent AI-slop patterns and enforce visual discipline.

## 1. The 90/8/2 Color Law

Every report must follow this color allocation:

| Share | Role | Variable | Usage |
|-------|------|----------|-------|
| **90%** | Neutral surface | `--bg`, `--surface`, `--text` | Background, body text, cards |
| **8%** | Structural color | `--primary` | Section borders, one accent block, h2 underlines |
| **2%** | Bullet point | `--accent-pop` (default = `--primary` at full opacity) | At most 1-2 precise hits: a single KPI value, one callout border, one chart series |

**Violations to avoid:**
- `var(--primary)` used on heading text, KPI values, chart bars, callout borders, TOC links, AND badges simultaneously → this is a primary-color flood
- Every KPI card a different accent color → accent system should feel like seasoning, not confetti
- Using more than 2 accent colors per page (chart series excluded)

## 2. Typography: 10:1 Scale Ratio

The largest text element on any page must be ≥ 10× the smallest readable element.

| Element | Min size | Max size |
|---------|----------|---------|
| Fine print, badges, meta | 11px | — |
| Body text | 15px | — |
| h3 | 17px | — |
| h2 | 20px | — |
| Report title | 2.6rem+ | — |

**Apply to report title:** Minimum `font-size: 2.8rem`. For strong content topics, push to `3.5–4rem` with `line-height: 1.05` and `letter-spacing: -0.03em`. The title should feel like an anchor, not a label.

**Apply to section headings:** `h2` gets a subtle left border or underline using `--primary` at 8% allocation — not a background color.

## 3. KPI Grid Column Rules

Do not default all KPI grids to 3 columns. Match columns to KPI count for better proportion:

| KPI count | Grid columns | CSS |
|-----------|-------------|-----|
| 1–2 | 2 columns | `grid-template-columns: repeat(2, 1fr)` |
| 3 | 3 columns | `grid-template-columns: repeat(3, 1fr)` |
| 4 | 2×2 | `grid-template-columns: repeat(2, 1fr)` |
| 5–6 | 3 columns (last row 2) | `grid-template-columns: repeat(3, 1fr)` |
| 7+ | 3 columns with dividers between groups | `grid-template-columns: repeat(3, 1fr)` + `gap: 0.5rem 1rem` |

**Non-equal widths:** When one KPI is the "hero" metric, use `grid-template-columns: 2fr 1fr 1fr` or `1.5fr 1fr` to create visual hierarchy.

## 4. Forbidden Patterns (Anti-AI-Slop)

These patterns make a report look instantly AI-generated. Do not produce them:

| ❌ Forbidden | ✅ Instead |
|---|---|
| Every section starts with a one-sentence definition: "X is a..." | Start sections in the middle of the idea, with data or a claim |
| 3-equal-column KPI grid when you have 4 KPIs | Use 2×2 grid |
| All h2 headings are 3–4 words ("Overview", "Key Findings", "Next Steps") | Allow longer, specific headings that reflect actual content |
| `border-radius: 12px` on every card and button | Mix radii: sharp (2px) for data elements, soft (8px) for prose cards |
| Callout boxes for every key insight | Use `.highlight-sentence` for inline highlights; reserve callout for truly exceptional notes |
| Same font size for every paragraph | Vary prose density: lead paragraphs slightly larger (16px), supporting detail smaller (14px) |
| Symmetrical two-column layouts everywhere | Use `2fr 1fr` or `3fr 1fr` — asymmetry implies hierarchy |
| Inter as body font | Use system-ui / -apple-system stack (already in themes) |
| `:::kpi` block where every value is `[INSERT VALUE]` / `[数据待填写]` in a narrative report | Use `:::callout` or `:::timeline` as the visual anchor instead |
| `:::chart` with all-placeholder data in a text-heavy (narrative/mixed) section | Use `:::diagram` (flowchart/mindmap) or a `highlight-sentence` paragraph |

## 5. Content-Tone Color Calibration

When generating `theme_overrides` in `--plan` mode, suggest a tone-appropriate primary color based on content keywords:

| Content tone | Trigger keywords | Suggested `primary_color` override | Feel |
|---|---|---|---|
| **Contemplative / Research** | 认知、思维、本质、意义、哲学、研究、白皮书、学术 / philosophy, cognition, research, academic | `#7C6853` (warm brown) | Grounded, editorial |
| **Technical / Engineering** | 架构、系统、API、性能、部署、代码、工程 / architecture, system, API, performance, engineering | `#3D5A80` (navy blue) | Precise, authoritative |
| **Business / Data** | 销售、营收、KPI、增长、季报、业绩 / sales, revenue, KPI, growth, quarterly | `#1F6F50` (pine green) | Restrained, commercial, premium |
| **Narrative / Annual** | 故事、增长、复盘、年度 / story, growth, retrospective, annual | `#B45309` (amber) | Warm, momentum |
| **Editorial / News** | 新闻、行业、趋势、观察 / news, industry, trend | `#1C1C1E` (near-black) | Authoritative, print |

No override needed if the default theme color already matches the tone.

## 6. Semantic Highlight Extraction

When rendering prose sections, identify **key-insight sentences** and apply `.highlight-sentence`:

A sentence qualifies if it meets ALL of:
- Stands alone as its own paragraph
- ≤ 45 characters (Chinese) or ≤ 80 characters (English)
- Declarative/conclusive tone (states a fact, principle, or finding)
- Not already inside a `:::callout` or `:::kpi` block

```html
<p class="highlight-sentence">真正的增长来自产品本身，而非渠道。</p>
```

CSS for `.highlight-sentence` (add to shared.css section in html-shell-template.md):
```css
.highlight-sentence {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--primary);
  border-left: 3px solid var(--primary);
  padding-left: 1rem;
  margin: 1.5rem 0;
  line-height: 1.5;
}
```

## 7. Pre-Output Self-Check

Before writing the final HTML, answer each question. Fix any "no":

- [ ] Does the report title feel like an anchor, or just a label? (target: anchor — at least 2.8rem)
- [ ] Is `var(--primary)` used in more than 4 distinct element types? If yes → reduce
- [ ] Are any KPI grids 3 columns when the count is 4 or 7+? If yes → fix column rule
- [ ] Are there 3+ consecutive all-prose sections with no component? If yes → insert visual anchor
- [ ] Do all section headings feel like AI-generated template phrases? If yes → make them content-specific
- [ ] Is every card's `border-radius` identical? If yes → vary radii between data elements and prose cards
- [ ] Does any `:::kpi` or `:::chart` block contain only placeholder values (`[INSERT VALUE]` / `[数据待填写]`) in a `narrative` or `mixed` report? If yes → replace with `:::callout`, `:::timeline`, or `:::diagram`
- [ ] **If you told someone "an AI wrote this", would they immediately believe it?** If yes → find the most generic-looking part and redesign it

## L1 Content Review

For content, structure, and reading-flow checks, see [review-checklist.md](review-checklist.md).

**L0 (Visual)**: This file — color, typography, layout, anti-slop presentation rules.
**L1 (Content)**: `review-checklist.md` — BLUF opening, heading logic, prose walls, takeaways, scan anchors.

**When to apply:**

- `--generate`: run a **silent final review pass** using the L1 checklist before writing HTML
- `--review`: run the same one-pass automatic refinement explicitly against an existing report
