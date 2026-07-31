先对照代码与 v2 方案核对关键假设（契约变量、装配顺序、overrides 能力），再给出可执行性结论。发现关键点：`.kpi-value` 实际用的是 `--text` 而非 `--primary`。继续核对现有主题与 overrides 契约。## 1) 仍然致命的问题

无。

## 2) 非致命但应在动工前修的问题

1. **§4-3 / spike 的「KPI 命中 `#0b6b55`」与管线默认冲突**  
   `shared.css` 明确把 `.kpi-value` 设为中性色 `var(--report-text, var(--text))`（forest 下是 `#17211c`），不是 `--primary`。  
   反例：只写 `:root { --primary: #0b6b55 }`、不在 POST-SHARED 覆写 `.kpi-value`，硬检查永远失败；或误把 `--text` 改成绿，正文也变绿。动工前二选一：POST-SHARED 显式覆写 KPI 色，或改查 `.kpi-card` 顶边/`--primary` 消费点。

2. **radar 预设交付物超卖了 `theme_overrides` 能力**  
   §1/§6 写「accent + 状态三色 + 底色微调」，但装配只映射 `primary_color` → `--primary` 与 `font_family`（见 `toc-and-template.md`）。  
   反例：用户照 YAML 只改 `primary_color`，success/warning/danger 与底色仍是 dark-board 原值。动工前把示例与边界说明收成「仅 `primary_color`」，删掉管线做不到的字段承诺。

## 3) 结论

**ACCEPT**（可动工；上述两点是验收措辞/文档对齐，不挡 spike）。
