我先快速核对主题管线、gate 指纹与现有主题差异，再按严重度打出对抗评审。## 1) 最可能让方案失效的假设漏洞

**A. 设计 token 与管线契约变量名错位——Phase 1 几乎必定“有文件、无皮肤”**  
方案 §2 写的是 `--ink/--paper/--navy/--green`，但 `shared.css` 与自定义主题约定消费的是 `--primary/--surface/--text/--text-muted/--border/--success`（见 `_example-warm-editorial`）。  
反例：按方案原样落 `themes/forest-editorial/theme.css`，agent 走 custom 组装（minimal + shared + 你的 `:root`），KPI/表格/timeline 仍吃 minimal 变量，肉眼≈minimal，用户否决“辨识度一致”。

**B. “主题=只动 CSS、同一 IR 内容字节不变”与“对标参考页辨识度”互斥**  
参考页的深色 hero 带、情报盘 chrome、气泡定位密度，依赖结构类与组件选择；现有差异化主题（如 `dark-board`）靠 POST-SHARED 结构规则，不是色板 alone。  
反例：用 `examples/zh/business-report.report.md` 渲 forest——无 navy hero 结构、无编辑式大圆角叙事块，用户对照源页判“不像”；agent 为过审手改 HTML/组件后，Phase 2 验收“换主题不改内容字节”直接崩。

**C. radar 的 mono/数字密度无法靠 `:root` 兑现**  
`.kpi-value`/`.report-meta` 在 shared 里写死 `font-family: ui-sans-serif, system-ui...`，不读 `--font-mono`。  
反例：radar-board 只塞 token + 指望 KPI 变 mono，gate/预览全绿，截图仍是 sans 大数字，与 dark-board 的差异进一步塌成“换了个 accent 色”。

---

## 2) 方案会引入的新风险/回归

**R-a. Phase 1 “gate 天然通过”制造假绿灯，把错误 token 晋升进内置**  
未知主题不做指纹校验；Phase 1 验收把 `valid` 当质量信号，实则只证 shell，不证主题契约。  
升 Phase 2 时再锁 `THEME_MARKERS`，会把“错名变量 + 手写近似 CSS”固化成回归基线，后续微调全被指纹绑架。

**R-b. 路由与主题表稀释：radar 必撞 `dark-board`，forest 几乎无自动命中**  
现有 `board/dashboard/status/看板 → dark-board`；情报/监测/雷达语义高度重叠，加路由行只会制造竞态或永远靠 `--theme` 的死主题。  
用户体验：主题表 8→10，自动选择更吵、辨识更弱；历史“看板关键词误路由”类 bug（v1.18 修过）复燃概率上升。

**R-c. Phase 2 “五处联动”清单漏项，文档/预览/契约不同步**  
真实联动至少还有：`SKILL.md` 内置列表、`theme-css.md` 名单与 POST-SHARED 标注、中英 `templates/*/…html` 样张、`templates/screenshots/*.png`、README 截图栅格、`context_isolation.py`、暗色主题的 highlight 皮肤。  
只改 gate+routing+preview+README+pytest 时，check-doc-sync / 截图尺寸测试 / agent 路由表会静默漂移，出现“文档写 10、skill 仍 8、预览缺图”。

---

## 3) 被忽略的更优或更简单替代

**Alt-1. 先做 1 天“契约映射 spike”，不做双主题交付**  
只把 forest 的视觉意图映射成 **标准变量名 + 必要 POST-SHARED**（hero/summary、radius、KPI 色），用同一 IR 出一张样张证明可复现；radar 默认降级为 `dark-board` 的 `theme_overrides` 或 POST-SHARED 预设，不占内置名额。  
比“两主题 × 两阶段”更小，直接杀死漏洞 A/C 和 R2。

**Alt-2. 永久停在自定义主题，但改加载约定：允许完整 CSS 覆盖而非仅 `:root` 色板**  
若目标是“像参考页”，应明确 custom `theme.css` 可含组件选择器覆盖（尤其 `.kpi-value`、summary/hero），并在样张 IR 里带齐 timeline/scatter/KPI——而不是承诺零管线改动却用错变量、再幻想升内置。  
内置升格等有 2+ 真实用户强制 `--theme` 再做，避免主题表膨胀。

---

## 4) 若只允许先做一件事

**只做一件：用标准契约变量重写 forest 的一份可渲染 `theme.css`（+ 最小 POST-SHARED），渲一张真样张，与 minimal 并排否决。**  
原因：这是整个方案的荷载测试——若标准变量 + shared 组件路径都复现不了“米绿纸感 + 深色锚区”，则 Phase 1/2 流程、radar 第二主题、升内置五处联动全部是在错误抽象上堆工作；样张失败应立刻降级为 overrides/结构需求，而不是继续写第二份 token 表。
