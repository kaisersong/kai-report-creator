我按对抗性评审直接读代码，先抓 animated 配方、gate 分支、测试和 demo 产物。## 1) 致命问题

1. **`data-render-mode="animated"` 一票否决标准 shell，替身断言是子串剧场，可被注释绕过。**  
   `is_animated_html` 仅认该属性后整段跳过 `STANDARD_REQUIRED_IDS`（`html_quality_gate.py:509-514`）；`validate_animated_shell` 对 paging/play 只查 `"keydown" in html` / `"scrollIntoView"` / `"playing"` / `"requestFullscreen"`（`:63-66`）。反例：HTML 注释里塞这四个词 + WebGL 字面量，`validate_animated_shell` 返回 `[]`；测试夹具 `_animated_html` 本身是空 `keydown` 回调 + 裸标识符 `requestFullscreen`，仍断言 `status=="valid"`（`test_html_quality_gate.py:94-123`）。这不是“软检查”，是**门禁被设计成可通过死代码**。

2. **IR 契约与 animated 配方硬冲突。**  
   `ir-contract.md:53` 写死 `Use **ECharts** for ALL charts`，示例 frontmatter 默认 `charts: cdn`；`animated-shell/overview.md:17-18` 却写「ECharts 规则不适用于本模式 / 手写 SVG+GSAP」。Agent 若只信 contract 会在 iridescence（零 CDN）里塞 ECharts CDN，与 mode 配方和 gate 的 external_script 规则对撞——**契约层 `contract_conflict`，不是风格分歧**。

3. **`--generate` 主路径未分叉，animated 是旁路补丁。**  
   `generate-flow.md:5-8` 仍无条件「Build the standard shell / theme-css」；Reference Loading 的 `--generate` 行仍 always-load `html-shell*`，animated 另起一行说 skip。同一 IR 带 `animations: iridescence` 时两套路由同时成立，**没有单一真源**；产物错误来自路由漂移，不是 gate 能补的。

## 2) 应修但不致命

1. **scrollytelling CDN 策略名存实亡。**  
   配方要求且仅允许 3 个 pin 版 GSAP/ScrollTrigger/CountUp + SRI；gate 只校验 `src` 是否 `startswith(cdnjs...)` 且 tag 含 `integrity=`（`:84-91`），**不要求三库存在、不校验 hash、任意 cdnjs 路径可过**（含 `evil.min.js` + 任意 integrity 字面量）。零 CDN 的 scrollytelling 也 `valid`。

2. **模式元数据不自洽。**  
   不校验 `data-theme == data-animation`；`data-theme="corporate-blue"` + `data-animation="iridescence"` 全量 KPI 路径仍 valid。WebGL fallback 锁死字面量 `linear-gradient(135deg,#cfe0ff,#f0f6ff)`（`:82-83`），改一个色值即假失败。

3. **SKILL 自相矛盾 + 测试不防回归。**  
   `--generate` step 10 仍写 “must pass **standard shell IDs**, theme fidelity…”（`SKILL.md:110`），与 Animated 节 step 10 换断言集（`:123`）冲突。5 个用例只覆盖“能跳过 shell / 能报几个子串码”，**从不断言真实 `goSec`/`navSec`/F5/wheel lock**。

## 3) 更简做法 / 该删的

1. **删掉“看起来像 gate 的子串检查”**：要么抽一份必须原文内联的 frame-chrome 片段（hash/指纹），要么明文声明 animated 只验 `data-*` + CDN 策略，交互靠浏览器 QA——别让 CI 给死代码盖章。  
2. **不要四套同义标记**（`animations:` + `theme: iridescence` + `data-theme` + `data-animation`）：IR 一个字段 `render: scrollytelling|iridescence`，HTML 一个 `data-animation`，`data-theme` 继续留给真实主题；并在 `ir-contract` 给 ECharts 规则加 animated 例外。

## 4) 结论

**NEEDS_FIX** — 两个 demo 人工 QA 过关不能洗白：gate 对 animated 几乎不可信，且 IR/generate 主契约与旁路配方互相打架。
