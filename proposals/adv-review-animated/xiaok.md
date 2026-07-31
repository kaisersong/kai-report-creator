读完代码，问题主要出在 `validate_animated_shell` 的检测太"软"——它跟标准 shell 的硬 ID 检查完全不在一个强度上。

## 1) 致命问题

**1. 子串检查可被 HTML 注释绕过（gate 失效）**
`html_quality_gate.py:63-66` 用 `if "keydown" not in html` 这类全局子串判断，不限定在 `<script>` 或真实事件处理器内。实测：在 HTML 里写一句 `<!-- TODO: keydown + scrollIntoView + playing + requestFullscreen -->`、**完全不实现**这些功能，gate 只会因 WebGL 字面量缺失报一条，其余全部通过——agent 可以把没有翻页/播放模式的残次页认证为 valid。

**2. `data-render-mode="animated"` 与 IR 无任何一致性校验（契约漏洞）**
gate 的 animated 分支只看 HTML 标记，不读 IR。`ir-contract.md:27` 规定 `animations: true` = 标准模式、`scrollytelling|iridescence` 才走 animated；但只要 HTML 里出现 `data-render-mode="animated"`，所有 `STANDARD_REQUIRED_IDS` 和 theme 指纹检查全被旁路。没有一道关卡把 HTML 标记关联回 IR 的 `animations` 字段。

**3. SRI 检查只验标签里有 `integrity=` 字样**
`html_quality_gate.py:88-91` 仅判断 `<script>` 标签内是否出现 `integrity=` 子串，不校验哈希格式或长度。`integrity="x"` 即可通过，scrollytelling 配方里"防 CDN 投毒"的承诺实际是空头支票。

## 2) 应修但不致命

**1. 动效模式下 DOM 内 KPI 完全不被检查**
`validate_kpi_values` 仍会跑，但其 `kpi-value` class 正则在 scrollytelling demo 里命中 0 次（CountUp 卡片没有这个 class）。动效页只靠 `report-summary` JSON 兜底，页面上显示的数字是否真实/是否带占位符无人管。

**2. 动效主题没有任何指纹校验**
`THEME_MARKERS`（`html_quality_gate.py:95-116`）没有 `iridescence`/`scrollytelling` 条目，加上 `validate_theme_fidelity` 对 animated 直接跳过——配方里规定的毛玻璃卡、径向光晕、shader uniforms 等视觉契约一个都没被 gate 锁定。标准主题有指纹、动效主题没有，保护等级不对等。

**3. WebGL fallback 检查是字面量子串匹配**
`html_quality_gate.py:82` 要求 `"linear-gradient(135deg,#cfe0ff,#f0f6ff)"` 原样出现，任何空格、引号、rgba 写法都会误报。配方里确实给了精确字符串所以勉强能跑，但极脆。

## 3) 更简做法 / 应删冗余

**1. 子串检查应改成 ID 驱动**
标准 shell 用 `id="toc-toggle-btn"` 这种不可伪造的硬标识；动效模式完全可以同样要求 `id="play-btn"`/`id="nav-dots"`/`id="progress-bar"` 等真实可见元素，既更有意义（用户真的看得到）又不会被注释绕过。现在的做法是"降级到关键词匹配"，等于自废武功。

**2. `body.playing { overflow:hidden }` 的正则只覆盖单行块**
`html_quality_gate.py:67` 用 `body\.playing\s*\{[^}]*overflow...`，若该规则被拆到多选择器或换行书写即可漏检——属于花力气写了但覆盖面窄的检查。

## 4) 结论

**NEEDS_FIX** — 致命问题 1 是真实可复现的 gate 绕过（我已用最小用例验证：仅靠一句注释就能让无翻页/无播放模式的页面通过），必须把子串检查收紧到 `<script>` 范围内或改成 ID 驱动后再上线。
