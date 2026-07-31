# 自评（对抗视角，含实证）— animated render mode 已落地实现

方法：不空想，直接对 `scripts/html_quality_gate.py` 做绕过测试。
复现脚本见文末。

## 1) 致命问题

### F1. animated 断言组是纯子串匹配 → gate 提供虚假保证（已实证）

`validate_animated_shell()` 全部检查都是 `"keydown" not in html` 这类子串匹配。
**实证**：构造一份几乎空白的 HTML（无 section、无 canvas、无任何动效/翻页 JS），
只在 `<script>` 注释里写下 `keydown scrollIntoView playing requestFullscreen
getContext('webgl') linear-gradient(135deg,#cfe0ff,#f0f6ff)`，
补齐 JSON-LD 后 **gate 报 `valid`，findings 为空**。
另一实证：把 Tesla iridescence demo 的真实 `keydown` 监听器改坏、仅注释留词，
gate 仍报 `valid`。

后果：SKILL.md 承诺「step 10 仍运行、gate 会校验 animated 断言」，实际上
gate 只能证明「文件里出现过这些字符」，无法证明翻页/播放/shader 真的存在。
这比没有检查更糟——它给 AI 一个可以合法通过的假门禁。

### F2. iridescence 的 fallback 检查硬编码了具体颜色 → 与配方意图冲突（已实证）

`html_quality_gate.py`：
`elif "linear-gradient(135deg,#cfe0ff,#f0f6ff)" not in html: missing_webgl_fallback`。
**实证**：把 Tesla 页的 fallback 换成品牌色 `#ffd9da→#fff5f5`（完全合理的改动，
且配方 §Hard rules 4 明确鼓励「multiply by brand tint」），gate 立刻
`invalid / animated.missing_webgl_fallback`。

后果：gate 事实上强制**所有** iridescence 报告必须使用那一个蓝色渐变，
与「按品牌着色」的配方自相矛盾。我的 Tesla demo 之所以通过，只是因为
我照抄了原始颜色值——这是过拟合而非契约。

### F3. `data-render-mode="animated"` 是自我声明的逃逸开关，且 data-theme 无人校验（已实证）

animated 分支同时跳过 `validate_standard_shell`（13 个必需控件 ID）与
`validate_theme_fidelity`。**实证**：把 demo 的 `data-theme` 改成
`totally-bogus-theme`，gate 仍报 `valid`——而 `overview.md` §5 明确要求
`data-theme="<animation mode>"`。契约写在文档里，没有任何代码执行。

后果：① 标注即豁免——AI 只要写上这个属性就能跳过标准报告的全部控件要求，
没有任何机制判定「这份报告是否真的该走 animated 轨」；
② `data-animation` 与 `data-theme` 的一致性、与 IR 里 `animations:` 值的
一致性均未校验，三处可以互相矛盾。

## 2) 应修但不致命

1. **`overview.md` 的 section 数与 iridescence 配方不一致**：overview §IR mapping
   写「8–10 sections is the default arc」，但 iridescence 的 page arc 只列 6 段
   （hero/cards/bars/conclusions/table/sources），实际 demo 也是 6 段。
   虽有「never pad」兜底，措辞仍会误导。
2. **测试用例复制了被测实现的弱点**：`tests/test_html_quality_gate.py` 里
   `_animated_html()` 夹具用 `document.addEventListener('keydown',e=>{})` 这类
   **空实现**就能让断言通过，等于把「子串匹配即合格」固化成回归基线。
3. **`report-summary` 之外无内容完整性检查**：animated 轨不校验 section 数、
   不校验 summary.sections 与真实 `<section>` 是否对齐（两个 demo 恰好对齐，
   属偶然）。

## 3) 更简做法 / 应删的设计

1. **把无法可靠静态验证的断言降级为「文档纪律 + 人工 QA 清单」，只保留能真检的**：
   可靠可检的是「零外部字体域」「iridescence 无 `<script src>`」「scrollytelling
   的 CDN 白名单 + 每个 script 带 integrity」——这些是**结构性**判定。
   而「翻页/播放模式存在」用 grep 根本证明不了，应从 gate 移出，改由
   `references` 的 QA 清单 + 浏览器验证承担（正如动效模式 QA 本来就要求开浏览器）。
2. **删掉 fallback 颜色的硬编码**，改判「`getContext('webgl')` 的失败分支里存在
   对 `canvas.style.background` 的赋值」（正则可查、与颜色无关）；或直接不检。

## 4) 结论

**NEEDS_FIX**。F1/F2/F3 都已实证复现，且 F1 使 SKILL.md 对该门禁的描述
成为不准确陈述。修复方向：收缩 gate 到「真能静态判定」的子集 + 移除颜色
过拟合 + 补 data-theme/data-animation 一致性校验（这三项都是小改动）。

---

## 复现脚本

```bash
cd ~/projects/report-creator
python3 - <<'PY'
import sys; sys.path.insert(0,'.')
from scripts.html_quality_gate import validate_html_text
h = open('examples/zh/tesla-q2-2026.html',encoding='utf-8').read()
print("A) data-theme 胡写:", validate_html_text(
    h.replace('data-theme="iridescence"','data-theme="totally-bogus-theme"'),
    jsonld_check=False)['status'])                       # -> valid
print("B) 品牌色 fallback:", validate_html_text(
    h.replace("linear-gradient(135deg,#cfe0ff,#f0f6ff)",
              "linear-gradient(135deg,#ffd9da,#fff5f5)"),
    jsonld_check=False)['status'])                       # -> invalid (误杀)
print("C) 破坏翻页仅留注释:", validate_html_text(
    h.replace("document.addEventListener('keydown'",
              "/*x*/(function(){}) //keydown scrollIntoView playing requestFullscreen\n// (",1),
    jsonld_check=False)['status'])                       # -> valid
PY
```
