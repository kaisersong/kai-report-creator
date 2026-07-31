1) P0-1 仍用正则寻找首个 `<html>`，可被 `script` 文本劫持：`<script>const x='<html data-render-mode="animated">'</script><html data-render-mode="standard">…` 会被误判为 animated；应由 `HTMLParser` 提取真实根标签属性。
2) `_IdCollector._skip` 会被不匹配的结束标签错误减零：`<template></style><button id="play-btn"></button><div id="nav-sections"></div></template>` 可让模板内惰性元素冒充两个必需 ID；需按标签栈或独立 template 深度处理。
REJECT
