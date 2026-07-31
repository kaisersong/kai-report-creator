1) 修复方案仍然遗漏或做错的地方

1. **P0-2 缩小 gate 职责本身合理，但方案没有把浏览器 QA 变成可执行、可留证的验收门。** 仅写入清单后，验收项“破坏翻页必须 `invalid`”无法实现；反例：保留可见的 `play-btn` 和 `nav-sections`，删除全部事件监听与翻页函数，静态 gate 仍会 `valid`。

2. **P0-3 只能证明摘要里“有数字”，不能证明动画实际展示的 KPI 真实或与摘要一致。** 反例：`report-summary` 写 `282.4亿元`，JS 的 `DATA.revenue=999999`，CountUp 读取后者；现有 summary 校验零 findings，验收项“编造 KPI 数字必须 `invalid`”仍无法满足。

2) 动工前应调整的细节

1. P0-1 应直接复用 `HTMLParser` 读取真实文档根元素，不能继续用首个 `<html...>` 正则；反例：`<!-- <html data-render-mode="animated"> -->` 放在真实根元素前，方案中的新实现仍会被注释劫持。

2. 明确两条可执行契约：行为由独立 Playwright smoke test 验收并留结果；KPI 则让 `report-summary.kpis` 成为动画代码实际读取的唯一数据源，或让 gate 接收 IR 做逐项比对。验收表需注明每个反例由静态 gate、浏览器测试还是 IR 对账拦截。

3) 结论：**REJECT（需再改方案）**
