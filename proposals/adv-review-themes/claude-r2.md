# 自评 r2 — two-new-themes v2

## 1) 仍然致命的问题

无。v1 的地基性缺陷（:root-only 装配、契约变量错位、主观验收、radar 独立
主题）在 v2 中均已用「内置轨 + 冻结夹具 spike + 计算样式验收 + overrides
降级」结构性解决，且每条修订都能对应到管线的真实代码行为。

## 2) 动工前应修的非致命问题

1. **夹具的 ECharts 依赖**：`tests/fixtures/theme-skin-fixture.html` 若内联
   ECharts 会让夹具体积膨胀且引入 CDN；建议夹具中 scatter 用静态 SVG 快照
   替身，图表配色验证放到 Phase 1 真实 IR 样张一步做。
2. **§4-3 的「计算色命中」检查落点**：gate 是纯文本工具，查不了计算样式；
   应明确写「由 spike/样张阶段的截图人工核验承担，gate 只锁指纹下限」，
   避免实现者误以为要给 gate 加 headless 渲染。

## 3) 结论

ACCEPT（附上述两个动工前小修）。
