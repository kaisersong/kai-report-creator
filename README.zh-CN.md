# kai-report-creator

> 你有数据、决策和截止日期，但决策者没时间读完所有材料。AI 能生成报告，但往往一眼就能看出是模板产物——章节标题像填空、主色泛滥在六种元素上、KPI 不管几个都是三列。kai-report-creator 一行命令输出"异步友好"的报告：扔一个文档或链接，选个主题，得到单文件 HTML——决策者扫 30 秒就能抓住要点。下游 AI 智能体也能解析：输出内嵌三层机器可读结构。
>
> **[看这份指南本身生成的报告 →](https://kaisersong.github.io/kai-report-creator/examples/zh/kai-report-creator-guide.html)** — 本文档由 kai-report-creator 自己生成。

适用于 [Claude Code](https://claude.ai/claude-code) 和 [OpenClaw](https://openclaw.ai) 的报告生成技能，将文档或结构化大纲转换为精美的独立 HTML 报告。

[English](README.md) | 简体中文

---

## 效果展示

点击截图可在浏览器中直接打开演示：

<table>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/corporate-blue.html"><img src="templates/screenshots/corporate-blue.png" width="360" alt="corporate-blue"/><br/><b>corporate-blue</b></a><br/><sub>暖感商务 · 高级汇报</sub></td>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/minimal.html"><img src="templates/screenshots/minimal.png" width="360" alt="minimal"/><br/><b>minimal</b></a><br/><sub>研究 · 学术论文</sub></td>
</tr>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/dark-tech.html"><img src="templates/screenshots/dark-tech.png" width="360" alt="dark-tech"/><br/><b>dark-tech</b></a><br/><sub>工程 · 运维</sub></td>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/dark-board.html"><img src="templates/screenshots/dark-board.png" width="360" alt="dark-board"/><br/><b>dark-board</b></a><br/><sub>看板 · 架构</sub></td>
</tr>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/data-story.html"><img src="templates/screenshots/data-story.png" width="360" alt="data-story"/><br/><b>data-story</b></a><br/><sub>年度报告 · 增长叙事</sub></td>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/newspaper.html"><img src="templates/screenshots/newspaper.png" width="360" alt="newspaper"/><br/><b>newspaper</b></a><br/><sub>行业分析 · 通讯</sub></td>
</tr>
</table>

预览全部主题：`/report --themes` → 打开 `report-themes-preview.html`

---

## 设计理念：Skills 作为领域 Harness 工程

本节介绍 report-creator 的设计原则——既包括作为用户工具的设计，也包括作为 Claude Code 技能的设计。这些原则对任何编写技能的人都有参考价值。

### 一、渐进式披露

技能文件每次被调用时，会完整加载到 AI 的上下文窗口中。文件大小直接影响 AI 的专注程度。

report-creator 的解法是：**规则放在技能里，资产放在文件里**：

```
--plan        → 只需 IR 规则 + 组件语法；不涉及 CSS 和 HTML Shell
--generate    → 只读取一个主题 CSS + 一个共享 CSS；其他 5 套主题保留在磁盘
--themes      → 直接读取预构建的预览 HTML；技能不需要解析内部细节
```

**最终效果：** `--plan` 调用从不接触 CSS；单主题生成从不加载其他 5 套主题。

这是渐进式披露原则在 AI 上下文管理中的应用：**在需要信息的那一刻才披露，而不是提前全部加载**。

### 二、硅碳协作设计

report-creator 在输入端和输出端都为人机协作而设计。

**输入端：IR 作为人机契约**

`.report.md` 中间表示是人类意图与 AI 渲染之间的契约：

```
---                         ← Frontmatter：文档身份
title: Q3 销售报告             这是什么？谁写的？应该如何呈现？
theme: corporate-blue          声明意图，不包含内容。
---

## 章节标题               ← 正文：人类叙述
普通 Markdown 文本...        自然书写，AI 渲染为语义化 HTML。

:::kpi                     ← 组件块：结构化数据
- 营收: ¥2,450万 ↑12%       机器可解析，AI 按确定性模板渲染。
:::
```

人类可以自然地书写和编辑，无需了解 HTML。AI 对每个层次使用不同的渲染规则——正文做 Markdown 转换，组件块做模板渲染。IR 文件可检查、可版本管理。

**输出端：三层 AI 可读结构**

每份生成的 HTML 都内嵌机器可读结构：

```
第一层 — <script id="report-summary">    文档级：标题、摘要、所有 KPI
第二层 — data-section data-summary       章节级：标题 + 一句话摘要
第三层 — data-component data-raw         组件级：原始 KPI/图表/表格数据
```

AI 智能体读取第一层即可获得 3 秒全局概览，进入第二层获取章节级理解，仅在需要特定数据时才访问第三层。

**渐进式披露为双物种设计：** IR 为碳基读者揭示结构，HTML 为硅基读者揭示数据。同一原则应用两次——一次为人，一次为机器。

### 三、视觉节奏即认知节拍

优秀的报告遵循一种节奏：**正文建立背景，组件传递数据，正文再做解读**。

技能强制执行视觉节奏规则：不允许连续出现 3 个以上只有纯文字的章节，每 4-5 个章节必须包含一个"视觉锚点"——KPI 网格、图表或流程图。这不是美学偏好，而是认知节拍的需要。大段密集的文字让读者疲惫；没有背景的数据让读者迷失。交替出现才能形成阅读流。

这也是 IR 组件块语法（`:::tag ... :::`）被设计得如此直观的原因：作者扫一眼 IR 文件就能看出数据密集的章节在哪里。

### 四、报告是异步决策支持

幻灯片默认有讲述者在场，报告没有。报告必须独立承受第一次阅读：读者通常只会扫开头、看标题、瞥一眼数据，然后在不到一分钟内决定这份文档值不值得继续读。

这个约束直接改变了产品设计：

- `--review` 被设计成**一次性自动优化阶段**，而不是交互式编辑回路
- `--generate` 在写出 HTML 前，会执行同一套 **静默终审**
- 检查体系被拆成 **L0 视觉/渲染质量** 和 **L1 内容/阅读质量**
- 只有 AI 能稳定判断、且能稳定修复的规则，才会进入系统

**判断标准：** 一份生成报告应该显著降低读者理解成本。只要决策者能通过快速扫读看明白结论、证据和下一步动作，这份报告就达标了。

### 五、设计质量基线：拒绝 AI 审美

生成报告最大的敌人，是让人一眼就看出"这是 AI 做的"——每个元素都用相同的圆角、主色泛滥在六种元素上、KPI 不管几个都是三列、章节标题听起来像模板。

`references/design-quality.md` 编码了四个维度的约束：

**90/8/2 配色法则。** 90% 中性面（背景、正文），8% 结构色（一个强调块、边框），2% 弹点（最多 1-2 处精准命中）。当主色同时出现在标题、KPI、图表、callout、目录和标签上时，它就不再是信号，而是噪音。

**10:1 字号张力。** 页面上最大的元素应该是最小可读元素的 10 倍以上。报告标题应该有"锚点感"（2.8–4rem），而非"标签感"。所有元素集中在 15–22px 区间时，页面没有层次，看起来像表格导出。

**KPI 网格分列规则。** 默认不是 3 列。4 个 KPI 应该是 2×2。英雄指标应该用 `2fr 1fr 1fr`。7 个以上需要视觉分组分隔线。无论几个都用三列是模板气息。

**内容气质色调校准。** 不同情绪基调需要不同配色：

| 气质 | `primary_color` | 感受 |
|------|-----------------|------|
| 思辨 / 研究 | `#7C6853` 暖棕 | 沉稳，编辑感 |
| 技术 / 工程 | `#3D5A80` 藏蓝 | 精准，权威感 |
| 商业 / 数据 | `#0F7B6C` 深青绿 | 自信，向前感 |
| 叙事 / 年度 | `#B45309` 琥珀 | 温暖，势能感 |

**输出前自检：** *"如果告诉别人这是 AI 写的，他们会立刻相信吗？如果会——找出最像模板的那个地方，重新设计它。"*

---

## 安装

### Claude Code

对 Claude 说：「安装 https://github.com/kaisersong/report-creator」

或手动：
```bash
git clone https://github.com/kaisersong/report-creator ~/.claude/skills/report-creator
```

重启 Claude Code，使用 `/report` 调用。

### OpenClaw

```bash
# 通过 ClawHub 安装（推荐）
clawhub install kai-report-creator

# 或手动克隆
git clone https://github.com/kaisersong/report-creator ~/.openclaw/skills/report-creator
```

---

## 使用方式

### 基本命令

| 命令 | 说明 |
|------|------|
| `/report --from file.md` | 从已有文档生成报告 |
| `/report --from URL` | 从网页生成报告 |
| `/report --plan "主题"` | 先生成 `.report.md` 大纲文件 |
| `/report --generate file.report.md` | 将大纲渲染为 HTML |
| `/report --review file.html` | 用 Review 清单优化已有报告 |
| `/report --themes` | 并排预览全部 6 套主题 |
| `/report --bundle --from file.md` | 离线 HTML，内联所有 CDN 资源 |
| `/report --theme <name> --from file.md` | 指定使用内置或自定义主题 |
| `/report [内容]` | 一步生成：根据描述直接生成报告 |

### 典型工作流

**一步生成：**
```
/report --from meeting-notes.md
/report --from https://example.com/data-page --output market-analysis.html
```

**两阶段工作流（复杂内容）：**
```
/report --plan "Q3 销售总结" --from q3-data.csv
# 如需要，编辑生成的 q3-sales-summary.report.md
/report --generate q3-sales-summary.report.md
```

**Review 优化：**
```
/report --review market-analysis.html
```

### Review 模式

运行 `--review`，用 8 项检查点对已有报告做一次性自动优化：

```
/report --review market-analysis.html
```

**行为：**
1. 加载 `references/review-checklist.md`
2. 自动应用 hard rules
3. 高置信度时应用 ai-advised rules
4. 将优化后的 HTML 写回原文件

这是**一次性自动优化**流程，不是交互式确认流程。

`--generate` 也会在写出 HTML 前执行同一套 **静默终审**。

**8 项检查点：**
- BLUF 开场（结论先行）
- 标题栈逻辑
- 去模板腔章节标题
- 文字砖块拆解
- 数据后的 takeaway
- 洞察优于数据
- 扫读锚点覆盖
- 条件触发的读者指引

---

## 功能特性

### 核心功能

- **零依赖** — 单个 `.html` 文件，`--bundle` 模式支持离线
- **6 套内置主题** — corporate-blue、minimal、dark-tech、dark-board、data-story、newspaper
- **9 种组件类型** — KPI 指标、图表、表格、时间线、流程图、代码块、标注、图片、列表
- **Report Review 系统** — 8 项检查点自动优化
- **AI 可读输出** — 三层机器可读结构

### 交互功能

- **摘要卡片** — 标题旁 `⊞ 摘要卡` 按钮，展示 KPI 和章节标签
- **内置导出** — ↓ Export 按钮，支持 Print/PDF、PNG (Desktop)、PNG (Mobile)
- **移动端自适应** — 适配任意屏幕尺寸
- **中英双语** — 自动检测语言

### 输出功能

- **自定义主题** — `themes/<name>/theme.css` + `--theme <name>`
- **自定义模板** — `template: ./my-brand-template.html`
- **主题覆盖** — frontmatter 中设置 `theme_overrides.primary_color`
- **离线打包** — `--bundle` 内联所有 CDN 资源

---

## 主题

| 主题 | 风格 | 适合场景 |
|------|------|----------|
| **corporate-blue** | 暖感商务 | 商业报告、高管汇报 |
| **minimal** | 简洁学术 | 研究论文、分析报告 |
| **dark-tech** | 工程感 | 运维报告、技术文档 |
| **dark-board** | 看板风格 | 架构图、指标看板 |
| **data-story** | 叙事驱动 | 年度报告、增长故事 |
| **newspaper** | 编辑感 | 行业分析、通讯 |

### corporate-blue

暖感商务主题，适用于面向高管的报告。主色克制地用于关键元素——KPI 数值、章节链接、每报告一个强调块。主色最多出现在 3 类元素上，形成清晰的视觉层次，避免"AI 把所有东西都染蓝"的效果。

---

## 创建自定义主题

1. 创建 `themes/你的主题/` 目录
2. 编写 `theme.css`，使用 CSS 自定义属性：
```css
:root {
  --primary: #B45309;
  --bg: #FAFAF9;
  --text: #1C1917;
  --font-heading: "Merriweather", serif;
}
```
3. 运行：`/report --theme 你的主题 --from file.md`

**附带的示例主题：** `themes/warm-editorial/`

---

## 报告格式（IR）

对于复杂报告，建议先用 `--plan` 生成 `.report.md` 中间文件。

**Frontmatter：**
```yaml
---
title: Q3 销售报告
theme: corporate-blue
author: 销售团队
date: 2024-10-08
lang: zh
toc: true
abstract: "Q3 营收同比增长12%，新客户数创历史新高。"
---
```

**组件块：**
```
:::kpi
- 营收: ¥2,450万 ↑12%
- 新客户数: 183 ↑8%
:::

:::chart type=line title="月度营收趋势"
labels: [7月, 8月, 9月]
datasets:
  - label: 实际营收
    data: [780000, 820000, 850000]
:::

:::timeline
- 2024-10-15: Q4 目标下发
- 2024-10-31: 新品发布会
:::

:::callout type=tip
关键洞察填写在此。
:::
```

---

## 面向 AI 智能体

其他智能体和技能可以直接调用 report-creator：

```
# 从文档生成
/report --from ./analysis.md --output summary.html

# 从 URL 生成
/report --from https://example.com/report-page --theme data-story

# 两步流程 + review
/report --plan "市场分析" --from ./raw-data.md
/report --generate market-analysis.report.md
/report --review report.html
```

**提取结构化数据：**
```python
from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(open("report.html"), "html.parser")
summary = json.loads(soup.find("script", {"id": "report-summary"}).string)
print(summary["title"], summary["kpis"])
```

---

## 导出

每份报告右下角有内置 **↓ Export** 按钮：

| 选项 | 说明 |
|------|------|
| Print / PDF | 调起浏览器打印对话框，目标选择"另存为 PDF" |
| PNG (Desktop) | 以 2× 分辨率截取完整页面 |
| PNG (Mobile) | 截取报告正文并缩放至 1170px 宽 |

**提示：** 打印对话框中取消勾选"页眉和页脚"，可避免浏览器打印网址和日期。

---

## 使用案例：每日工作日报 → Telegram

```
将今天的工作情况用 dark-board 风格生成报告，导出为 IM 图片，通过 Telegram 发给我。
```

OpenClaw 会自动：
1. 整理今日完成的工作、关键决策和后续计划
2. 渲染成带 KPI 卡片和时间线的 `dark-board` 风格报告
3. 截图为 800px 宽的 JPEG（动画自动禁用）
4. 直接发送到你的 Telegram 频道

---

## 示例

| 文件 | 说明 |
|------|------|
| [examples/zh/business-report.html](examples/zh/business-report.html) | 2024 Q3 销售业绩报告（中文）|
| [examples/zh/monthly-progress-reviewed-demo.html](examples/zh/monthly-progress-reviewed-demo.html) | 月报 reviewed demo（中文）|
| [examples/en/business-report.html](examples/en/business-report.html) | Q3 Sales Report（英文）|
| [examples/review-reports/](examples/review-reports/) | 结构化 review report 示例 |

---

## 依赖要求

无依赖。任何现代浏览器均可打开。

`--bundle` 模式需要一次网络连接以获取 CDN 资源。

---

## 兼容性

| 平台 | 版本 | 安装路径 |
|------|------|----------|
| Claude Code | 任意 | `~/.claude/skills/report-creator/` |
| OpenClaw | ≥ 0.9 | `~/.openclaw/skills/report-creator/` |

---

## 版本日志

**v1.9.0** — Report Review 系统：`--review` 8 项检查点；`--generate` 静默终审；L0/L1 质量分层。

**v1.8.3** — KPI 溢出修复：`.kpi-suffix` 处理长单位。

**v1.8.2** — 克制配色系统：共享 badge 默认中性色；`data-report-mode="comparison"` 启用实体颜色。

**v1.8.1** — 导出背景修复：优先解析 `--bg`。

**v1.8.0** — 自定义主题：`--theme <name>` 加载 `themes/<name>/`。

**v1.6.0** — 桑基图：`:::chart type=sankey` 流向图。

**v1.5.0** — 设计质量基线：90/8/2 配色、KPI 网格规则、内容气质色调。

**v1.4.0** — 摘要卡片：KPI + 章节标签。

**v1.3.0** — 零依赖动画：KPI 弹入、时间线滑入。

**v1.0.0** — 初始发布，6 套主题 + 9 种组件。