# kai-report-creator

简体中文 | [English](README.md)

> 生成美观的单文件 HTML 报告 — 零依赖，移动端自适应，AI 可读。

## 功能介绍

`/report` 是一个 Claude Code 技能，可将文档或结构化大纲转换为精美的独立 HTML 报告。将其放入 `.claude/skills/` 目录，即可在任意项目中立即使用。

**核心特性**
- **零依赖** — 单个 `.html` 文件，支持离线使用（`--bundle` 模式）
- **6 套内置主题** — 企业蓝、极简、深色科技、深色看板、数据叙事、报纸
- **9 种组件类型** — KPI 指标、图表、表格、时间线、流程图、代码块、标注、图片、列表
- **AI 可读输出** — 三层机器可读结构，支持下游智能体处理
- **中英双语** — 完整支持 zh/en，自动检测语言

## 快速开始

**方式 A — Claude Code（手动安装）**

1. 将 `SKILL.md` 复制到 `~/.claude/skills/report-creator.md`
2. 指向一个文档或链接：

```
/report --from meeting-notes.md
/report --from https://example.com/data-page --output market-analysis.html
/report --plan "Q3 销售总结" --from q3-data.csv
```

**方式 B — OpenClaw / ClawHub（一行命令）**

```
clawhub install kai-report-creator
```

HTML 文件将生成到当前目录，用任意浏览器打开即可查看。

## 命令说明

| 命令 | 说明 |
|------|------|
| `/report --from file.md` | 从已有文档生成报告 |
| `/report --from URL` | 从网页生成报告 |
| `/report --plan "主题"` | 先生成 `.report.md` 大纲文件 |
| `/report --generate file.report.md` | 将大纲文件渲染为 HTML |
| `/report --themes` | 并排预览全部 6 套主题 |
| `/report --bundle --from file.md` | 离线 HTML，内联所有 CDN 资源 |
| `/report --theme dark-tech --from file.md` | 指定使用某套主题 |
| `/report --template my-template.html` | 使用自定义 HTML 模板 |
| `/report --output my-report.html --from file.md` | 自定义输出文件名 |
| `/report [内容]` | 一步生成：根据描述直接生成报告 |

## 导出

每份生成的报告右下角都有内置的 **↓ Export** 按钮，无需任何额外工具。

| 选项 | 说明 |
|------|------|
| 🖨 Print / PDF | 调起浏览器打印对话框，目标选择**另存为 PDF**。 |
| 🖥 Save PNG (Desktop) | 以 2× 分辨率截取完整页面。 |
| 📱 Save PNG (Mobile) | 截取报告正文区域并缩放至 1170 px 宽（约为 iPhone 宽度的 3 倍）。 |

**导出 PDF 前，请在打印对话框中取消勾选「页眉和页脚」**，否则浏览器会在页面顶部和底部打印网址、日期和页码。Chrome 操作路径：*打印 → 更多设置 → 取消勾选「页眉和页脚」*。

## 主题演示

点击截图可在浏览器中直接打开演示：

<table>
<tr>
<td align="center"><a href="https://kaisersong.github.io/kai-report-creator/templates/zh/corporate-blue.html"><img src="templates/screenshots/corporate-blue.png" width="360" alt="corporate-blue"/><br/><b>corporate-blue</b></a><br/><sub>商务 · 高管汇报</sub></td>
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

## 报告格式（IR）

对于复杂报告，建议先用 `--plan` 生成 `.report.md` 中间文件，编辑确认后再生成 HTML。

**Frontmatter 示例：**
```yaml
---
title: Q3 销售报告
theme: corporate-blue
author: 销售团队
date: 2024-10-08
lang: zh                # en | zh — 不填时自动检测
toc: true
animations: true
abstract: "Q3 营收同比增长12%，新客户数创历史新高。"
---
```

**可用组件块：**
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
在此填写关键洞察。
:::

:::table caption="区域业绩"
| 区域 | 完成率 |
|------|--------|
| 华南 | 115%   |
:::
```

## 主题

需要不同配色？用 `theme_overrides` 自定义任意主题：
```yaml
theme_overrides:
  primary_color: "#B45309"           # 替换主色
  font_family: "Merriweather, serif" # 替换字体
```

## 自定义模板

复制 `templates/_custom-template.example.html`，加入你的品牌样式后引用：

```yaml
---
template: ./my-brand-template.html
---
```

可用占位符：`{{report.title}}`、`{{report.author}}`、`{{report.date}}`、`{{report.abstract}}`、`{{report.theme_css}}`、`{{report.body}}`、`{{report.summary_json}}`

## 面向 AI 智能体与技能开发者

report-creator 专为机器间协作设计，其他智能体和技能可以直接调用它。

**从其他技能或智能体调用 `/report`：**

```
# 从文档生成
/report --from ./analysis.md --output summary.html

# 从 URL 生成（Claude 自动抓取并分析页面内容）
/report --from https://example.com/report-page --theme data-story

# 两步流程（支持中间审查）
/report --plan "市场分析" --from ./raw-data.md
# （如需要，编辑生成的 .report.md 文件）
/report --generate market-analysis.report.md
```

**以编程方式读取报告输出：**

每份生成的 HTML 都内嵌了三层机器可读结构：

```
第一层 — <script type="application/json" id="report-summary">
          文档级：标题、作者、摘要、所有 KPI 汇总
          → 单次 JSON 解析即可获取完整文档概览

第二层 — data-section="..." data-summary="..."  挂载在每个 <section> 上
          章节级：每个章节的标题和一句话摘要
          → 遍历章节，构建结构化目录

第三层 — data-component="kpi" data-raw='{...}'  挂载在每个组件上
          组件级：每个 KPI、图表、表格的原始结构化数据
          → 按需查询特定组件，供下游数据处理使用
```

**示例：从生成的报告中提取第一层摘要**

```python
from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(open("report.html"), "html.parser")
summary = json.loads(soup.find("script", {"id": "report-summary"}).string)
print(summary["title"], summary["abstract"])
print(summary["kpis"])  # 所有 KPI 数据
```

**推荐调用模式：**

| 场景 | 命令 |
|------|------|
| 将长文档汇总为报告 | `/report --from doc.md --theme minimal` |
| 将抓取数据转为看板 | `/report --from data.json --theme dark-board` |
| 在流水线中生成报告 | `/report --generate plan.report.md --output out.html` |
| 离线交付 | `/report --bundle --from doc.md` |

## 设计理念

本节介绍 report-creator 的设计原则——既包括作为用户工具的设计，也包括作为 Claude Code 技能的设计。理解这些原则，有助于你构建更好的技能和更好的报告。

### 一、技能的渐进式披露

技能文件每次被调用时，会完整加载到 AI 的上下文窗口中。这意味着技能文件的大小直接影响 AI 的专注程度。

report-creator 的解法是：**规则放在技能里，资产放在文件里**。

- **`--plan` 模式** — 只需要 IR 规则和组件语法，不涉及任何 CSS 或 HTML Shell，技能保持专注。
- **`--generate` 模式** — 只读取一个主题 CSS 文件（`templates/themes/[theme].css`）和一个共享 CSS 文件，其他 5 套主题保留在磁盘上，不进入上下文。
- **`--themes` 模式** — 直接读取预构建的预览 HTML 文件，技能不需要知道文件内部的细节。

最终效果：每条命令只加载它需要的内容。`--plan` 调用从不接触 CSS；单主题生成从不加载其他 5 套主题。

这是渐进式披露原则在 AI 上下文管理中的应用：**在需要信息的那一刻才披露，而不是提前全部加载**。

### 二、IR 作为人与 AI 的协作界面

`.report.md` 中间表示（Intermediate Representation）是人类意图与 AI 渲染之间的契约。

它有三个层次，各司其职：

```
---                         ← Frontmatter：文档身份
title: Q3 销售报告             这是什么？谁写的？应该如何呈现？
theme: corporate-blue          声明意图，不包含内容。
abstract: "..."
---

## 章节标题               ← 正文：人类叙述
普通 Markdown 文本...        自然书写，AI 渲染为语义化 HTML。

:::kpi                     ← 组件块：结构化数据
- 营收: ¥2,450万 ↑12%       机器可解析，AI 按确定性模板渲染。
:::                           每种块类型有明确的输出契约。
```

这种分层设计带来三个好处：
- 人类可以自然地书写和编辑 IR，无需了解 HTML
- AI 对每个层次使用不同的渲染规则——正文做 Markdown 转换，组件块做确定性模板渲染
- 在生成 HTML 之前，IR 文件是可检查、可版本管理的

### 三、Frontmatter 是文档身份，章节是文档正文

Frontmatter 和章节内容回答的是不同的问题：

| 层次 | 回答的问题 | 示例 |
|------|------------|------|
| Frontmatter | *这是什么文档？* | 标题、作者、主题、语言、摘要 |
| 章节 | *这份文档说了什么？* | 标题、正文、KPI、图表 |

`abstract` 字段是最重要的桥梁：它让下游 AI 智能体无需阅读每一个章节，就能从一句话中理解整份报告的核心内容。这驱动了每份生成 HTML 中内嵌的**三层 AI 可读结构**的第一层：

```
第一层 — <script type="application/json" id="report-summary">
          文档级：标题、作者、摘要、所有 KPI 汇总

第二层 — data-section="..." data-summary="..."  挂载在每个 <section> 上
          章节级：每个章节的标题和一句话摘要

第三层 — data-component="kpi" data-raw='{...}'  挂载在每个组件上
          组件级：每个 KPI、图表、表格的原始结构化数据
```

AI 智能体读取报告时，可以从第一层用 3 秒完成全局概览，进入第二层获取章节级理解，仅在需要特定数据时才访问第三层。——同样的渐进式披露原则，这次是为机器读取报告而设计的。

### 四、视觉节奏即认知节拍

优秀的报告在结构上遵循一种节奏：**正文建立背景，数据组件传递信息，正文再做解读**。

技能中强制执行了视觉节奏规则：不允许连续出现 3 个以上只有纯文字的章节，每 4-5 个章节必须包含一个"视觉锚点"——KPI 网格、图表或流程图。这不是美学偏好，而是认知节拍的需要。大段密集的文字让读者疲惫；没有背景的数据让读者迷失。交替出现才能形成阅读流。

这也是 IR 组件块语法（`:::tag ... :::`）被设计得如此直观的原因：作者扫一眼 IR 文件就能看出数据密集的章节在哪里，无需解析 HTML 或 YAML。

## 示例

| 文件 | 说明 |
|------|------|
| [examples/en/business-report.html](examples/en/business-report.html) | 2024 Q3 Sales Performance Report（英文）|
| [examples/zh/business-report.html](examples/zh/business-report.html) | 2024 Q3 销售业绩报告（中文）|

## 许可证

MIT
