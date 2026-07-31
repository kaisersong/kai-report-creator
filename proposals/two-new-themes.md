# 方案：为 kai-report-creator 新增主题 — forest-editorial（+ radar 覆盖预设）

状态：**Step 0 spike 已完成并通过** · 2026-07-31
（forest-editorial 作为自定义主题落地并实证；radar 降级决定被实证坐实。
 Phase 2「升内置」尚未做——等用户确认视觉后再启动。）
评审记录：`proposals/adv-review-themes/`（两轮，codex/kiro/xiaok/grok/claude 五方
第二轮一致 ACCEPT；本版已合并 4 条「动工前小修」）

## 0. 一句话（v2 结论先行）

**只立项一个主题 `forest-editorial`，radar-board 降级为 `dark-board` 的
`theme_overrides` 预设**；在写任何 theme.css 之前，先做一次
**冻结夹具换肤 spike** 验证「CSS 能否单独表达该设计」——spike 不过即止损。

## v1 → v2 的关键修订（对应评审结论）

| # | v1 缺陷（评审共识） | v2 修订 |
|---|---|---|
| 1 | token 用了 `--ink/--paper/--navy`，但管线契约变量是 `--primary/--surface/--text/--border/--success`（shared.css 实际消费的名字）——照 v1 落地=「minimal 换色」 | §2 全部重写为契约变量名 + 明确 gap 清单 |
| 2 | 自定义主题装配只追加 `:root`（minimal 基座），**结构性特征（深色 hero 带、大圆角、mono KPI）根本产不出来** | forest 直接走**内置主题轨**（含 POST-SHARED 组件段）；砍掉「Phase 1 自定义主题」阶段 |
| 3 | 「gate valid」对自定义主题是空真命题，「辨识度一致」主观不可判 | 验收改为冻结夹具并排截图 + 4 点硬检查（§4） |
| 4 | AI 每次手写 HTML 有措辞/结构漂移，样张对比污染 | 用**一份冻结的全组件 HTML 夹具**换 CSS 对比，隔离主题变量（codex Alt-2） |
| 5 | radar 与 dark-board 路由必撞车（board/看板/监测词重叠），且 `.kpi-value` 写死 sans 栈，mono 差异化会蒸发 | radar 不立独立主题：做成文档化的 `theme_overrides` 预设，不加路由行 |
| 6 | ECharts 颜色不读 CSS 变量，暗色图表可读性无保障 | forest 主题文件头部附**图表色板注释块**（AI 写 chart 配色的唯一来源，与现有主题惯例一致） |
| 7 | 「五处联动」漏项：主题截图资产测试、SKILL.md 内置名单、theme-css.md 名单、context_isolation、README 截图栅格 | §5 联动清单扩为 9 项 |

## Step 0 spike 结果（2026-07-31，已完成）

夹具：`tests/fixtures/theme-skin-fixture.html`（class 取自真实渲染产物
`examples/zh/business-report.html` + `shared.css`；scatter 用静态 SVG 替身，
不内联 ECharts）。换肤脚本：`tests/fixtures/skin_fixture.py`，按
`theme-css.md` 的真实装配顺序注入。

### forest-editorial：**通过**（§4 硬断言 5/5，headless getComputedStyle）

| 断言 | 实测值 |
|---|---|
| `body` 背景 | `rgb(245, 247, 243)` = `#f5f7f3` ✅ |
| 锚区背景 | `linear-gradient(150deg, rgb(16,45,39), rgb(23,63,53))` 含 `#102d27` ✅ |
| 锚区圆角 | `26px`（主题声明值，证明 POST-SHARED 级联生效）✅ |
| `.kpi-card` 顶边 | `rgb(11, 107, 85)` = `#0b6b55` ✅ |
| `.kpi-value` | `rgb(23, 33, 28)` 中性 —— 符合 §2 gap 的既定选择 ✅ |

与 minimal 对照（同一 DOM）：minimal 为白底 + Georgia 衬线 + 4px 圆角 + 近黑
顶边；forest 为纸绿底 + 系统无衬线 + 17/26px 圆角 + 深绿锚区。**一眼可辨**。

### radar-board：**坐实降级**（不立独立主题）

`dark-board` 与 `dark-board + primary_color=#5ee1b4` 的实测差异**只有 accent 色**：

| 项 | dark-board | radar-board 预设 |
|---|---|---|
| `body` 背景 | `rgb(13,17,23)` | `rgb(13,17,23)`（同） |
| `.kpi-card` 顶边 | `rgb(88,166,255)` 蓝 | `rgb(94,225,180)` 荧光绿 |
| 圆角 / 字体 | `6px` / Inter | `6px` / Inter（同） |

即 §5 R2 预期的结果 —— 已按 §6 写成 `themes/README*.md` 的预设配方，
并注明 mono KPI / 时间戳 chrome 超出 overrides 能力。

### 交付物

- `themes/forest-editorial/theme.css`（双段结构，含 POST-SHARED 与 chart palette 注释）
- `tests/fixtures/theme-skin-fixture.html` + `tests/fixtures/skin_fixture.py`
- `themes/README.md` / `README.zh-CN.md`：forest 用法 + radar 预设 + 夹具对比命令

## 1. 范围

- **做**：`forest-editorial` 内置主题（米绿纸感编辑风：`#f5f7f3` 纸底 +
  `#102d27` 深林绿锚区 + 金/橙点缀，大圆角）。
- **做**：`radar-board` 预设 = `dark-board` + `theme_overrides`
  （accent `#5ee1b4`、状态三色、底色微调），写入 `themes/README` 作为示例配方；
  若日后有 ≥2 个真实用户显式要求独立主题再升格。
- **不做**：dark toggle、新组件、新渲染模式、radar 独立主题、自动路由改动
  （forest 初期仅显式 `--theme` 可选，观察一个周期后再议路由行）。

## 2. Step 0 — 冻结夹具换肤 spike（先做，半天，不过即止损）

1. 构建 `tests/fixtures/theme-skin-fixture.html`：一份**冻结的** DOM，覆盖
   hero/summary、KPI 卡、表格、timeline、ECharts scatter 全组件。
2. 按真实装配顺序（base → shared → POST-SHARED → overrides）注入三套 CSS：
   `minimal`（对照）、`forest-editorial` 草稿、`dark-board`+radar overrides。
3. 并排截图评审。**通过判据**：forest 与 minimal 一眼可辨（深色锚区呈现、
   圆角/阴影生效、`.kpi-card` 顶边命中主题绿）；radar overrides 与 dark-board
   的差异是否值得独立主题（预期：不值得，坐实降级决定）。
4. spike 产出即 Phase 1 交付给用户确认的样张（冻结 DOM，无 AI 漂移）。

**夹具两条纪律**（评审要求）：
- 夹具骨架**必须从真实渲染产物提取 class**：先用一份真实 IR 跑通 minimal
  渲染，从产出 HTML 拿实际 class 名做骨架，不凭文档想象（否则 POST-SHARED
  选择器在夹具命中、真实渲染 miss）。
- 夹具**不内联 ECharts**：scatter 位用静态 SVG 替身占位，图表配色验证推到
  Phase 1 真实样张一并做，避免夹具引入 CDN 与体积膨胀。

### forest-editorial 契约变量映射（v2 修正版）

```css
:root {
  --primary: #0b6b55;        /* 主 accent（原 --green） */
  --primary-light: #e3f0e9;
  --accent: #c7951d;         /* eyebrow/次 accent（原 --gold） */
  --bg: #f5f7f3;  --surface: #ffffff;
  --text: #17211c; --text-muted: #68766e;
  --border: #dbe5dd;
  --success: #0b6b55; --warning: #c7951d; --danger: #de6d40;
  --radius: 17px;
}
/* === POST-SHARED OVERRIDE === */
/* 深林绿锚区：summary/poster 卡与 h2 章节带 → #102d27 底 + 金 eyebrow；
   卡片 radius 26px、柔和大阴影；badge 三组 soft 色。
   （具体选择器 spike 阶段按夹具实测定型） */
```

已知 gap（spike 要验证的点）：**`shared.css` 把 `.kpi-value` 写死为
`var(--report-text, var(--text))`（注释明写 neutral, no accent）**，所以
「KPI 变主题绿」不能靠 `--primary` 实现——本方案选择**不覆写 KPI 文字色**
（保持中性，符合现有主题惯例），主题绿改由 `.kpi-card` 顶边（`--primary`
既有消费点）承载；`color-mix()` 不进主题文件（PNG 导出兼容）。

### 图表色板注释块（写进主题 CSS 头部，供 AI 配 ECharts）

```
/* chart palette: #0b6b55 #c7951d #de6d40 #4e6a9f #93a098
   axis/label on light: #68766e · grid: #dbe5dd */
```

## 3. Phase 1 — forest-editorial 内置实现（spike 通过后）

1. `templates/themes/forest-editorial.css`（双段结构，含 POST-SHARED）。
2. 用真实 IR（`examples/zh/business-report.report.md`）渲一份样张，
   与夹具截图对照，确认 AI 渲染路径不劣化。
3. 交用户视觉确认。

## 4. 验收（自动化硬检查，禁止主观口子）

用 headless 浏览器读 `getComputedStyle` 断言（不是 grep 字符串、不是「或截图抽样」）：

1. 锚区块背景计算值 = `rgb(16, 45, 39)`（`#102d27`）且至少一处存在；
2. `.kpi-card` 顶边色计算值命中 `rgb(11, 107, 85)`（`#0b6b55`）；
   —— **不断言 `.kpi-value` 文字色**（shared.css 强制中性，见 §2 gap）；
3. 卡片 `border-radius` 计算值 = 主题声明值（radius 生效证明 POST-SHARED 级联对）；
4. `body` 背景 = `rgb(245, 247, 243)`；零新增外部字体/CDN 请求。

截图只作视觉佐证。gate 的 THEME_MARKERS 指纹（注释 + `--bg` + 1 个变量）
仅作**回归下限**，不承担「级联生效」的证明责任。
ECharts 配色验证方式：读渲染后 series 实际色值，不只看 CSS 注释存在。

## 5. Phase 2 — 联动清单（9 项，一次做完）

THEME_MARKERS 指纹 · theme-routing.md（仅登记，不加自动触发词）·
theme-css.md 内置名单 + POST-SHARED 标注 · SKILL.md 内置主题列表 ·
`--themes` 预览重生成 · README 中英主题表 + 截图栅格（补 1280×800 截图，
过 `test_theme_screenshot_assets.py`）· `context_isolation.py` 名单核对 ·
pytest 指纹用例 · check-doc-sync 全绿。

## 6. radar 预设交付物（轻量，只承诺管线真能做到的）

`theme_overrides` 实际只映射 `primary_color`（→ `--primary`）与 `font_family`
（见 `toc-and-template.md`）。因此预设**只承诺换 accent**，状态三色/底色微调
/mono KPI 一律不写进交付描述：

```yaml
theme: dark-board
theme_overrides:
  primary_color: "#5ee1b4"
```

`themes/README.md` / `README.zh-CN.md` 增加「radar-board 预设」小节，并写明边界：
状态三色、底色微调、KPI mono 字型、更新时间戳 chrome **均超出 overrides 能力**，
需完整 radar 风格必须升格独立主题（触发条件：≥2 真实用户显式要求）。

## 7. 风险（v2 残余）

- **R1 spike 不过**：POST-SHARED 也表达不了锚区 → 止损，转「结构需求」立项
  （shell 级），本方案关闭。
- **R2 指纹字符串在、级联不生效**（codex #2-3）：验收 §4 用**计算样式/截图**
  抽样而非 grep 字符串，指纹测试只作回归下限。
- **R3 主题表 9 个的路由噪音**：forest 不加自动触发词即无增量噪音；
  登记为「仅显式选择」主题。
