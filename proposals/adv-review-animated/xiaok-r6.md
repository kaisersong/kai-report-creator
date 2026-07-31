**对威胁模型边界的判断：**

1. **边界站得住**。gate 是自检工具而非安全边界，HTML 由本 skill 自身 agent 生成、无可信输入源——这一前提使「对抗构造免疫」不在合理需求范围内。v5 已用 HTMLParser 堵住全部 12 个实证绕过（覆盖 AI 偷懒的全部真实形态），剩余缺口仅对刻意构造的解析歧义开放，这类输入在正常生成路径中不会出现。

2. **双标论证成立**。标准轨 `f'id="{id}" not in html'` 纯子串判定比 animated 轨的 HTMLParser 严格更弱，却从未被要求对抗免疫。要求 animated 轨单独达标缺乏一致性依据。

3. **zero-dependency 约束合理**。引入 html5lib/lxml 仅为防御一个自产工具不会产生的输入，成本收益不匹配。Playwright 读真实 DOM 作为 backlog 升级路径方向正确。

**ACCEPT**
