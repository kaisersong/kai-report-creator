1) P0-2 的正则仍不能证明 ID 属于真实 DOM 元素：`<script>const x='<button id="play-btn"><nav id="nav-sections">';</script>` 在剥离注释后仍同时命中，空白页仍可绕过；需用 HTML parser/tokenizer 排除 script/style/template 内容。
2) P1-1 的 SRI/身份校验仍不成立：`integrity="sha512-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"` 会通过 `{40,}`，但不是 64-byte SHA-512；`https://cdnjs.cloudflare.com/ajax/libs/evil/1/gsap.min.js` 也可冒充文件名。需按算法解码校验长度，并固定三组 URL/哈希对。
REJECT
