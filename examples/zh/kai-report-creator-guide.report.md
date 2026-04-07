---
title: "kai-report-creator 使用指南"
theme: corporate-blue
author: kai-report-creator
date: 2024-04-07
lang: zh
toc: true
abstract: "一行命令生成异步友好的 HTML 报告——决策者 30 秒抓住要点，下游 AI 可解析三层结构。"
---

## 为什么需要这个技能

决策者没时间读完所有材料。AI 能生成报告，但往往一眼就能看出是模板产物：章节标题像填空、主色泛滥在六种元素上、KPI 不管几个都是三列。

kai-report-creator 解决三个问题：

- **异步阅读** — 报告没有讲述者在场，必须让读者 30 秒内抓住要点
- **AI 模板感** — 90/8/2 配色、字号张力、KPI 网格规则，避免"一眼 AI"
- **机器可读** — 输出内嵌三层结构，下游智能体可自动解析

## 一行命令生成报告

:::kpi
- 零依赖: 单文件 HTML
- 6 套主题: 企业蓝/极简/深色科技/看板/数据叙事/报纸
- 9 种组件: KPI/图表/表格/时间线/流程图/代码块/标注/图片/列表
- AI 可读: 三层机器结构
:::

**安装后立即可用：**

```
/report --from meeting-notes.md
/report --from https://example.com/data-page --output market-analysis.html
```

对 Claude 说「安装 https://github.com/kaisersong/report-creator」即可。

## 核心工作流

### 一步生成

从文档或 URL 直接生成 HTML：

```
/report --from ./analysis.md --theme corporate-blue
/report --from https://example.com/report --output summary.html
```

### 两阶段流程

复杂报告建议先生成大纲，确认后再渲染：

```
/report --plan "Q3 销售总结" --from q3-data.csv
# 编辑生成的 .report.md 文件
/report --generate q3-sales.report.md
```

### Review 优化

已有报告可用 8 项检查点自动优化：

```
/report --review market-analysis.html
```

检查点包括：BLUF 开场、标题栈逻辑、去模板腔标题、文字砖块拆解、数据后 takeaway、洞察优于数据、扫读锚点覆盖、条件触发读者指引。

## 报告格式（IR）

:::callout type=tip
IR 是人机协作的契约：人类自然书写，AI 确定性渲染。
:::

**Frontmatter 声明文档身份：**

```yaml
---
title: Q3 销售报告
theme: corporate-blue
abstract: "Q3 营收同比增长12%，新客户数创历史新高。"
---
```

**组件块传递结构化数据：**

```
:::kpi
- 营收: ¥2,450万 ↑12%
- 新客户数: 183 ↑8%
:::

:::chart type=line title="月度营收"
labels: [7月, 8月, 9月]
datasets:
  - data: [780000, 820000, 850000]
:::

:::timeline
- 2024-10-15: Q4 目标下发
- 2024-10-31: 新品发布会
:::
```

## 设计理念

### 渐进式披露

命令路由表确保每次只加载必要内容：`--plan` 不接触 CSS，`--generate` 只加载一个主题。

### 硅碳协作设计

**输入端：** IR 三层结构（Frontmatter/正文/组件块），人类自然书写。

**输出端：** HTML 三层 AI 可读结构（文档级/章节级/组件级），机器渐进解析。

渐进式披露为双物种设计：IR 为碳基读者揭示结构，HTML 为硅基读者揭示数据。

### 视觉节奏即认知节拍

禁止连续 3 个纯文字章节，每 4-5 章节必须有视觉锚点（KPI 网格/图表/流程图）。

### 异步决策支持

报告必须独立承受第一次阅读——读者扫开头、看标题、瞥数据，30 秒内决定是否继续。

### 设计质量基线

- **90/8/2 配色** — 90% 中性面，8% 结构色，2% 弹点
- **10:1 字号张力** — 标题有锚点感，不是标签感
- **KPI 网格规则** — 4 个 KPI 用 2×2，英雄指标用 2fr 1fr 1fr
- **内容气质色调** — 思辨用暖棕、技术用藏蓝、商业用深青绿

## 主题选择

| 主题 | 风格 | 适合场景 |
|------|------|----------|
| corporate-blue | 暖感商务 | 高管汇报、商业报告 |
| minimal | 简洁学术 | 研究论文、分析报告 |
| dark-tech | 工程感 | 运维报告、技术文档 |
| dark-board | 看板风格 | 架构图、指标看板 |
| data-story | 叙事驱动 | 年度报告、增长故事 |
| newspaper | 编辑感 | 行业分析、通讯 |

## 创建自定义主题

1. 创建 `themes/你的主题/theme.css`
2. 定义 CSS 变量：`--primary`、`--bg`、`--text`、`--font-heading`
3. 运行 `/report --theme 你的主题 --from file.md`

## 面向 AI 智能体

其他技能可直接调用：

```
/report --from ./analysis.md --output summary.html
/report --from https://example.com/data --theme dark-board
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

## 安装

**Claude Code：** 对 Claude 说「安装 https://github.com/kaisersong/report-creator」

**OpenClaw：** `clawhub install kai-report-creator`