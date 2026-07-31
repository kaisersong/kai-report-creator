## 1) 假设漏洞（最可能失效）

**① CSS 变量 = 主题，但 AI 手写 HTML 时变量不会自动应用**
计划把 token 全写成 `--navy` / `--accent` 等变量，但渲染靠 LLM 读 `reference.md` 后手写 HTML——不存在模板引擎强制替换。反例：forest-editorial 要求"封面用 `--navy` 深色带"，但如果 AI 写 `<section class="cover" style="background:var(--bg)">`，CSS 文件再正确，输出也不会呈现深色 hero。没有任何机制强制 LLM 遵守映射规则。

**② "gate 天然通过"被当作验收标准，实际是盲区**
Phase 1 验收写了"gate valid"，但 gate 对自定义主题不校验——这是零保障，不是零问题。反例：radar-board 的 CSS 漏定义 `--font-mono` 回退栈中某个变量，或 forest 的 `--shadow` 值格式错误，gate 全部通过，用户在浏览器看到渲染异常才能发现。

**③ ECharts chart 颜色不受页面 CSS 变量控制**
radar-board 定位"气泡图 = ECharts scatter"，但 ECharts 的 series/axis 颜色在 JS 配置里写死，不读 CSS 变量。反例：`--accent:#5ee1b4` 定义在 `:root`，但 scatter 图的点仍是 ECharts 默认蓝色——AI 每次手写 chart 配置时都要自己记得填主题色，没有 gate 或模板保证一致性。

## 2) 新引入的风险

**① 主题路由拥挤：8→10 可能超出 AI 可靠选择上限**
现有 8 主题路由已存在歧义（corporate-blue vs minimal vs newspaper 都是浅色商务）。再加 forest-editorial（浅色+深色锚区）和 radar-board（dark-board 变体），AI 自动选主题的误选率会上升。计划在 theme-routing.md 加两行说明，但没评估 10 主题是否超出 LLM 路由可靠阈值。

**② Phase 2 = 5 处联动 × 2 主题 = 10 个静默不一致点**
THEME_MARKERS、theme-routing、`--themes` 预览、README、pytest——任何一处遗漏都不报错。反例：忘记重新生成 `--themes` 预览 HTML，预览页显示 8 主题但实际模板目录有 10 个 CSS，用户和测试都不会发现。

**③ forest-editorial 的结构性期望（hero band）没有 HTML 结构保障**
深色 hero 带是结构性组件（需要特定 HTML 结构 + class），不是纯 CSS 变色。现有报告 shell 是否有 hero section 容器？如果没有，CSS 变量定义了 `--navy` 也无处施加。

## 3) 被忽略的更优替代

**① 只做 forest-editorial 一个主题，radar-board 降级为 dark-board overrides 预设**
计划自己在 R2 里承认 radar-board 可能在对比后与 dark-board 肉眼难辨。既然如此，现在就不应投入 radar-board 的完整 Phase 1+2 成本。dark-board 已有暗色基底，加一组 `--accent` + `--font-mono` override 即可，省去独立主题的全部 5 处联动。

**② 先验证"AI 能否正确应用自定义主题"这一根因假设，再铺两个主题**
在写两份 theme.css 之前，先用 `_example-warm-editorial` 做一次端到端测试：给 AI 一个带明确映射规则的 reference.md，看它生成的 HTML 是否真的用了正确的变量和结构。如果这一步就暴露了 AI 不遵守映射规则的问题，两个主题的 Phase 2（升级内置 + 指纹）全白做。

## 4) 若只先做一件事

**只交付 forest-editorial 的 Phase 1 自定义主题样张，拿到用户视觉确认后停。**
原因：计划的全部 Phase 2 成本（10 处联动改动）都建立在"用户认可视觉效果"这一前提上，而这一前提尚未验证。radar-board 计划自己都标了可能降级。用最小成本验证"AI 手写 HTML + CSS 变量注入"这条路到底走不走得通，比同时铺两个主题更稳。
