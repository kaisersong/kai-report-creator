我需要先阅读实际代码，以验证修复方案中的主张——特别是 gate logic、KPI validation 和 animated demos。现在让我读取关键支持文件：现在，让我来验证对评审至关重要的一个细节——即 KPI 空值防护行为：---

## 对抗性评审（第二轮）— 修复方案

### 1) 修复方案仍然遗漏或做错的地方

**无重大遗漏。** 逐条核对后，13 个问题（F1–F12 + F5b）全部有对应修复，优先级排序合理。

对用户特别标记的两点判断：

- **P0-2（行为断言移出 gate → 元素 ID 契约 + 浏览器 QA）**：合理，不是新漏检。旧断言 `"keydown" in html` / `"scrollIntoView" in html` 是纯字符串匹配——注释、死代码均可过，等于零检查。改为 `id="play-btn"` 在真实标签内存在（`<[^>]*id=["']play-btn["']`），注释无法伪造，严格更强。行为本身（F5 真翻页）本就不该由静态文本 gate 验证，归浏览器 QA 是正确职责切分。
- **P0-3（report-summary kpis 兜底 KPI 真实性）**：在 gate 能力范围内已足够。数字在 JS 里（CountUp / `var REV=[...]`）确实无法由 gate 校验语义正确性（282.4 vs 999999），但 gate 无法拿到原始 IR 做交叉比对。要求 report-summary 必须有非空 kpis + 真实数字，是把「数字暴露到可审计面」的最低合理门槛，overview.md 同步写铁律使下游可查。

### 2) 动工前应调整的细节

1. **P0-3 的覆盖声明有误**：`validate_kpi_values` 第 234 行 `if value and not has_real_number(value)` 的 `value and` 前缀会使空字符串 value 短路跳过——`{"value": ""}` 不报错。方案说「无数字的 value 已被覆盖」不准确。建议实施时把该行改为 `if not has_real_number(value)`（去掉 `value and`），否则 P0-3 新增的 `if not summary.get("kpis")` 只能拦空列表，拦不住空 value。

2. **P1-3 的 THEME_MARKERS 新增项缺具体标记**：方案说「把 iridescence/scrollytelling 加入 THEME_MARKERS，锁主题注释 + 1 个底色变量」，但没给具体字符串。两个 demo 的视觉系统自建（非标准 theme CSS），实现者需从实际产物里提取标记。建议动工前直接定死，如 scrollytelling 锁 `--bg:#0a0a12` + `/* scrollytelling */`，避免猜测。

### 3) 结论

**ACCEPT** — 可按此实施。两条调整是实施细节，不改变方案设计。
