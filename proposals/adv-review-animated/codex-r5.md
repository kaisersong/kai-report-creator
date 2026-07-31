1) P0-1 仍可被 RCDATA 劫持：`<title><html data-render-mode="animated"></title><html data-render-mode="standard">`；浏览器把前者当 `title` 文本、真实根为 standard，但 `HTMLParser` 会触发前一个 `html` 的 `handle_starttag`，误判 animated。
2) P0-2 的 template 栈仍可被同类解析差异绕过：`<template><textarea></template><button id="play-btn"></textarea></template><template><textarea></template><nav id="nav-sections"></textarea></template>`；浏览器中两 ID 都只是 `textarea` 文本，`HTMLParser` 却提前弹栈并收集它们。

REJECT
