---
title: 【模板】工作周报 - [日期范围]
theme: dark-board
author: [填写人姓名]
date: [YYYY-MM-DD]
lang: zh
abstract: [一句话总结本周核心进展，例如：本周完成项目A阶段性交付，推进项目B需求评审，处理3个临时需求，下周重点启动项目C开发。]
---

<!-- 使用说明：本模板为仪表板式周报，数据优先，快速汇报用。填写时替换 [] 内容，删除不需要的组件。 -->

## 本周核心指标

<!-- 根据实际数据填写，保留 2-4 个核心指标，不硬凑 -->

:::kpi
items:
  - label: 项目完成数
    value: [例如：2/3]
    delta: [例如：↑或↓数值]
    note: [说明]
  - label: 进度百分比
    value: [例如：85%]
    delta: [例如：→]
    note: [说明]
  - label: 风险/阻塞数
    value: [例如：1]
    delta: [例如：↑或↓数值]
    note: [说明]
  - label: 临时需求处理
    value: [例如：3]
    delta: [例如：↑或↓数值]
    note: [说明]
:::

## 项目进展

<!-- 每个项目一个 subsection，Badge 标注状态 -->

### 项目 A：[项目名称]

**状态：<span style="background:#0F7B6C;color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">进行中</span>**

- 本周完成：[关键成果 1-2 条]
- 进度说明：[简要描述进度，例如：需求评审完成，进入开发阶段]
- 下周计划：[关键里程碑]

<!-- 如果有里程碑，使用 Timeline -->

:::timeline
- [YYYY-MM-DD]: [里程碑事件]
- [YYYY-MM-DD]: [里程碑事件]
:::

<!-- 如果有风险或需要支持，使用 Callout -->

:::callout type=warning
[风险描述或需要的支持，例如：依赖外部接口文档，需协调技术团队提供。]
:::

---

### 项目 B：[项目名称]

**状态：<span style="background:#B45309;color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">阻塞</span>**

- 阻塞原因：[简要说明]
- 当前进展：[已完成部分]
- 下周计划：[解除阻塞后计划]

:::callout type=danger
[严重风险或紧急支持需求，例如：资源不足，需申请额外开发人力。]
:::

---

### 项目 C：[项目名称]

**状态：<span style="background:#059669;color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">已完成</span>**

- 完成内容：[关键成果]
- 交付日期：[YYYY-MM-DD]
- 下一步：[验收或后续跟进]

---

## 日常工作

<!-- 简洁列表，不需要详细描述 -->

- [例行任务 1，例如：周例会组织]
- [例行任务 2，例如：数据报表更新]
- [临时需求 1，例如：协助 QA 测试环境配置]
- [临时需求 2，例如：处理客户反馈问题]

<!-- 如果日常任务较多且有数据，可用 Table -->

:::table
headers: [任务类型, 任务内容, 耗时, 备注]
rows:
  - [例行, [任务名], [例如：2h], [说明]]
  - [临时, [任务名], [例如：1h], [说明]]
:::

---

## 跨团队协作

<!-- 依赖方、需求、状态 -->

- **协作方**：[团队/部门名称]
- **需求内容**：[简要描述]
- **当前状态**：<span style="background:#D97706;color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">等待对方</span> 或 <span style="background:#059669;color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">进行中</span>
- **预期完成**：[日期或时间范围]

<!-- 如有多个协作事项，可用 Table -->

:::table
headers: [协作方, 需求内容, 状态, 预期完成]
rows:
  - [[团队A], [需求A], [等待/进行中], [日期]]
  - [[团队B], [需求B], [等待/进行中], [日期]]
:::

---

## 下周计划

<!-- Timeline 连接本周/下周，展示连续性 -->

:::timeline
- [YYYY-MM-DD]: [下周里程碑 1]
- [YYYY-MM-DD]: [下周里程碑 2]
- [YYYY-MM-DD]: [下周里程碑 3]
:::

<!-- 如有需要的资源或决策，使用 Callout -->

:::callout type=info
[下周需要的资源支持或关键决策，例如：需确认项目D的技术方案选型。]
:::

---

<!-- 模板结束。生成命令：/report --generate weekly-work-report-template.report.md -->