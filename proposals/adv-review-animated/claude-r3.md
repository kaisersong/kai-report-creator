# 自评 r3（对修复方案 v3）— 含原型实证

## 方法

不停留在纸面：把 v3 的两处关键加固（P0-2 HTMLParser、P1-1 完整对白名单）
写成原型，直接拿 codex 第三轮的反例打。

## 实证结果

```
== P0-2 (HTMLParser 收集真实标签 id) ==
  codex反例: <script>const x='<button id="play-btn">'   → BLOCKED ✅
  注释内伪标签 <!-- <button id="play-btn"> -->          → BLOCKED ✅
  真实元素 <button id="play-btn">                       → PASS   ✅
== P1-1 (三组 (src,integrity) 完整对白名单) ==
  codex反例: 伪 hash sha512-+40个A                      → BLOCKED ✅
  codex反例: 冒充文件名 .../libs/evil/1/gsap.min.js     → BLOCKED ✅
  F12: 无引号 <script src=https://evil...>              → BLOCKED ✅
```

三个此前能绕过的反例全部被拦，且真实元素不误杀。

## 附带发现（可简化实现）

`HTMLParser` 对注释**天然免疫**（注释不触发 `handle_starttag`），因此 P0-2/P1-1
改用 parser 后并不依赖 P0-0 的注释剥离。P0-0 仍应保留，但其价值已收窄为
**标准轨**那些 `f'id="{id}" not in html'` 子串判定（kiro 指出的同类弱点）——
实现时按此定位，不要把 P0-0 描述成 animated 检查的前提（v3 文中 P0-1 仍需要它，
因为根元素匹配用的是正则）。

## 阻塞问题

无。

## 结论

**ACCEPT**。v3 的每条修复都对应一个可复现的反例，且验收清单（9 项假阳性拦截）
与「明确不承诺静态判定编造数字」的能力边界一致，不再超卖。
