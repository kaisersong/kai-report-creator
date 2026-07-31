逐一验证了 v2 所有修复项对仓库实际代码的可行性：

**已确认可实施的项（全部跑过实证）：**

| 修复 | 验证结果 |
|---|---|
| P0-0 `strip_comments` + P0-1 注释剥离后锚定 `<html>` | 注释劫持 `<html data-render-mode>` → 被拦截 ✅ |
| P0-2 注释剥离后匹配 `<[^>]*id="play-btn">` | 注释伪标签 → 被拦截 ✅；两个 demo 用 `playBtn`，方案已要求改名 |
| P0-3 显式非空 KPI 校验 | `kpis:[{"value":""}]` → 被拦截 ✅；两个 demo 的 4 个 KPI 均含真数字，不会误杀 |
| P1-1 无引号 `src` + SRI hash 实检 | `<script src=https://evil>` 被捕获 ✅；`integrity=""`/`"x"` 被拒 ✅；demo 三条 CDN hash 全过 ✅ |
| P1-1 iridescence 零 CDN | demo 外部 src = `[]` ✅ |
| P1-2 `canvas.style.background=` 赋值检查 | iridescence demo 含此赋值 ✅ |
| P1-3 `data-theme == data-animation` | 两个 demo 均一致（scrollytelling/iridescence）✅ |

**无阻塞问题。** v2 的所有修复项（P0-0～P1-4）均可直接对现有 `html_quality_gate.py` + 两个 demo HTML + 4 个 .md 配方文件实施；验收的 7 项假阳性拦截和「不承诺编造数字检测」的能力边界均诚实且可兑现；P1-3 修正了 v1 的色值指纹自相矛盾（避免重犯 F6），无内部冲突。

**ACCEPT。**
