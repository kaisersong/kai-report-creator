# kai-report-creator

> 生成美观的单文件 HTML 报告 — 零依赖，移动端自适应，AI 可读。

> 查看英文文档：[README.md](README.md)

## 功能介绍

`/report` 是一个 Claude Code 技能，可将纯文本或结构化大纲转换为精美的独立 HTML 报告。将其放入 `.claude/skills/` 目录，即可在任意项目中立即使用。

**核心特性**
- **零依赖** — 单个 `.html` 文件，支持离线使用（`--bundle` 模式）
- **4 套内置主题** — 企业蓝、极简白、深色科技、暖色编辑
- **9 种组件类型** — KPI 指标、图表、表格、时间线、流程图、代码块、标注、图片、列表
- **AI 可读输出** — 三层机器可读结构，支持下游智能体处理
- **中英双语** — 完整支持 zh/en，通过 frontmatter 中的 `lang: zh|en` 切换

## 快速开始

1. 将 `SKILL.md` 复制到 `~/.claude/skills/report-creator.md`
2. 在任意 Claude Code 会话中运行：

```
/report Q3 销售报告 — 营收增长12%，新增客户183家，目标完成率108%
```

HTML 文件将生成到当前目录，用任意浏览器打开即可查看。

## 命令说明

| 命令 | 说明 |
|------|------|
| `/report [内容]` | 一步生成：根据描述直接生成报告 |
| `/report --plan "主题"` | 先生成 `.report.md` 大纲文件 |
| `/report --generate file.report.md` | 将大纲文件渲染为 HTML |
| `/report --themes` | 并排预览全部 4 套主题 |
| `/report --bundle [内容]` | 离线 HTML，内联所有 CDN 资源 |
| `/report --theme dark-tech [内容]` | 指定使用某套主题 |
| `/report --output my-report.html [内容]` | 自定义输出文件名 |

## 报告格式（IR）

对于复杂报告，建议先用 `--plan` 生成 `.report.md` 中间文件，编辑确认后再生成 HTML。

**Frontmatter 示例：**
```yaml
---
title: Q3 销售报告
theme: corporate-blue   # corporate-blue | minimal | dark-tech | warm-editorial
author: 销售团队
date: 2024-10-08
lang: zh                # en | zh
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

| 主题 | 适用场景 | 风格 |
|------|----------|------|
| `corporate-blue` | 企业蓝 · 商务正式 | 专业整洁 |
| `minimal` | 极简白 · 学术研究 | 衬线字体，版式优先 |
| `dark-tech` | 深色科技 · 技术文档 | 深色背景，等宽字体 |
| `warm-editorial` | 暖色编辑 · 内容输出 | 暖色调，编辑风格 |

预览全部主题：`/report --themes` → 打开 `report-themes-preview.html`

## 模板

在 `templates/` 目录中浏览可直接使用的模板：

| 语言 | 企业蓝 | 极简白 | 深色科技 | 暖色编辑 |
|------|--------|--------|----------|----------|
| English | [templates/en/corporate-blue.html](templates/en/corporate-blue.html) | [templates/en/minimal.html](templates/en/minimal.html) | [templates/en/dark-tech.html](templates/en/dark-tech.html) | [templates/en/warm-editorial.html](templates/en/warm-editorial.html) |
| 中文 | [templates/zh/corporate-blue.html](templates/zh/corporate-blue.html) | [templates/zh/minimal.html](templates/zh/minimal.html) | [templates/zh/dark-tech.html](templates/zh/dark-tech.html) | [templates/zh/warm-editorial.html](templates/zh/warm-editorial.html) |

## 示例

| 文件 | 说明 |
|------|------|
| [examples/en/business-report.html](examples/en/business-report.html) | 2024 Q3 Sales Performance Report（英文）|
| [examples/en/monthly-progress.html](examples/en/monthly-progress.html) | Monthly Project Progress Report（英文）|
| [examples/zh/business-report.html](examples/zh/business-report.html) | 2024 Q3 销售业绩报告（中文）|
| [examples/zh/monthly-progress.html](examples/zh/monthly-progress.html) | 月度项目进展报告（中文）|

## 许可证

MIT
