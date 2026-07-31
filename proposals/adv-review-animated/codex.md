`bailian-cli` 技能的强制预检发现版本不一致：本地 Skill 版本与已安装 CLI 都是 `1.7.0`，npm 最新版是 `1.13.0`。该技能明确要求版本落后时暂停并取得你的升级决定，因此我还没有开始输出评审结论，也没有修改仓库。

是否先执行 `bl update` 升级到 `1.13.0`，然后继续完成这次只读对抗性评审？如果不升级，请回复“继续使用当前版本”，我会立即继续。

已执行的 `bl` 相关动作：仅运行 `bl --version` 完成版本预检；尚未调用模型能力。
uestFullscreen/WebGL` 的无效字符串，默认 gate 返回 `valid`。

2. **零 CDN 与 SRI 策略均可绕过。** [html_quality_gate.py:76](/Users/song/projects/report-creator/scripts/html_quality_gate.py:76) 只识别带引号的 `src`，[html_quality_gate.py:88](/Users/song/projects/report-creator/scripts/html_quality_gate.py:88) 只检查是否出现 `integrity=`；实测 iridescence 的 `<script src=https://evil.example/payload.js>`、scrollytelling 的 `integrity=""` 都返回 `valid`。

3. **scrollytelling demo 含 IR 和披露来源都不支持的市场数据。** [$0.53 市场预期](/Users/song/projects/report-creator/examples/zh/tesla-q2-2026-scrollytelling.html:287) 不存在于 [IR](/Users/song/projects/report-creator/examples/zh/tesla-q2-2026.report.md:1)，页脚却只声明 Tesla 官方材料为来源[/Users/song/projects/report-creator/examples/zh/tesla-q2-2026-scrollytelling.html:295]；这直接违反“不得编造、每项 claim 有来源”的契约。

## 2) 应修但不致命的问题

1. **图表契约自相矛盾。** [SKILL.md:65](/Users/song/projects/report-creator/SKILL.md:65) 与 [ir-contract.md:53](/Users/song/projects/report-creator/references/ir-contract.md:53) 无条件要求所有图表使用 ECharts，[overview.md:17](/Users/song/projects/report-creator/references/animated-shell/overview.md:17) 又明确禁止该规则；LLM 同时加载这些文件时没有形式化优先级。

2. **新增正例测试实际把空壳行为钉成合法。** [test_html_quality_gate.py:111](/Users/song/projects/report-creator/tests/test_html_quality_gate.py:111) 的 `keydown` 回调为空、`requestFullscreen` 只是读取属性，却在 [test_html_quality_gate.py:121](/Users/song/projects/report-creator/tests/test_html_quality_gate.py:121) 被断言为 `valid`；五个 animated 用例还全部关闭 JSON-LD 检查，未覆盖默认完整 gate。

3. **iridescence 配方与其基准产物不一致。** [iridescence.md:20](/Users/song/projects/report-creator/references/animated-shell/iridescence.md:20) 强制“一个 `const DATA=[...]` 单一数据源”，demo 却拆成 `QTRS/REV/NET/DEL/GWH/CONCLUSIONS/SEGMENTS/SOURCES` 八组常量[/Users/song/projects/report-creator/examples/zh/tesla-q2-2026.html:268]；要么删掉该硬规则，要么基准产物不能作为合格示例。

## 3) 被忽略的更简做法或应删掉的多余设计

1. 删除“从任意 HTML 内容自动猜 profile”：由已验证 IR 显式传入 `--profile animated:iridescence|scrollytelling`，再用文件内已有的 `HTMLParser` 校验根 `<html>` 属性和脚本标签。

2. 删除用字符串假装验证运行时行为的断言；静态 gate 只管结构、来源和依赖，键盘翻页/全屏/图表触发交给一个真实浏览器 smoke test，职责更小且不会产生虚假绿灯。

## 4) 结论

**NEEDS_FIX（须修改）。**
