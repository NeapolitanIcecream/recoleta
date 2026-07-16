---
kind: trend
trend_doc_id: 13
granularity: day
period_start: '2026-03-31T00:00:00'
period_end: '2026-04-01T00:00:00'
topics:
- robotics
- world-models
- vision-language-action
- object-centric-learning
- data-efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-13
tags:
- recoleta/trend
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/object-centric-learning
- topic/data-efficiency
language_code: zh-CN
---

# 机器人世界模型正进入动作闭环，结果比结构更强

## 概览
这一天讲的是世界模型正在变成机器人控制面的组成部分。DIAL 通过潜在未来状态把 VLM 接到动作上，并宣称在 VLA 训练里带来很大的数据效率提升。HCLSM 直接用 slot、层次结构和因果边处理场景结构，但它自己的结果也说明，稳定的对象中心世界建模仍然很难。

## 研究发现

### 潜在意图成了 VLA 设计的重点
DIAL 把未来视觉特征当作控制接口。视觉-语言模型（VLM）在 horizon 16 处预测一个潜在未来，另一个策略把这个预测和当前观测一起变成一个 16 步动作块。直接的收益是数据效率：论文在 RoboCasa GR1 Tabletop 上报告了 state-of-the-art 结果，使用 2,400 条轨迹，而之前的全量数据运行用了 24,000 条。它还把这套方法扩展到一个机器人设置之外，使用 27,419 条 EgoDex 人类轨迹做 zero-shot 泛化测试，并在 IRON-R01-1.11 类人机器人上报告了真实世界迁移。

#### 资料来源
- [DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA](../Inbox/2026-03-31--dial-decoupling-intent-and-action-via-latent-world-modeling-for-end-to-end-vla.md): 总结抓住了潜在意图瓶颈、两阶段训练、基准范围，以及少 10 倍示范的主张。

### 对象中心世界模型变得更明确了，但仍然脆弱
HCLSM 把世界建模推进到对象和事件结构上，但证据并不一致。模型把场景拆成多个 slot，分别对连续运动、事件帧和更高层目标建模，并在对象之间加入学习到的交互边。它的两阶段训练很关键：先强制 slot 专门化，再打开未来预测。 在 PushT 上，分阶段方法报告的下一状态预测误差是 0.008，吞吐量达到每秒 2.9 步。论文也展示了当前的限制。slot 仍然很分散，学到的因果图没有变得有用，而且因为 bf16 NaN 不稳定性，4 次运行里只有 2 次完成。

#### 资料来源
- [HCLSM: Hierarchical Causal Latent State Machines for Object-Centric World Modeling](../Inbox/2026-03-31--hclsm-hierarchical-causal-latent-state-machines-for-object-centric-world-modeling.md): 总结给出了分阶段训练主张、PushT 指标、吞吐量、较弱的分解、失败的因果图和稳定性细节。
