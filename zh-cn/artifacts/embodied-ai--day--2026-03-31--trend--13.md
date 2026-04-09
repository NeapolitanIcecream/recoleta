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

# 机器人世界模型正在进入动作回路，结果进展快于结构进展

## Overview
这一天的重点是，世界模型正在成为机器人控制的直接接口。DIAL通过潜在未来状态把VLM和动作连接起来，并声称在VLA训练中带来了很大的数据效率提升。HCLSM则用槽位、层级和因果边直接处理场景结构，但它自己的结果也说明，稳定的对象中心世界建模仍然很难。

## Clusters

### 潜在意图成为VLA设计的主要切入点
DIAL把未来视觉特征当作控制接口。视觉语言模型（VLM）预测16步时域上的潜在未来状态，另一个策略再把这个预测和当前观测一起转换成一个16步动作块。直接收益是数据效率：论文在RoboCasa GR1 Tabletop上用2,400条轨迹取得了最先进结果，而此前使用完整数据的实验用了24,000条。它还把这套方法扩展到单一机器人配置之外，使用27,419条EgoDex人类轨迹做零样本泛化测试，并报告了在IRON-R01-1.11人形机器人上的真实世界迁移结果。

#### Evidence
- [DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA](../Inbox/2026-03-31--dial-decoupling-intent-and-action-via-latent-world-modeling-for-end-to-end-vla.md): 摘要涵盖了潜在意图瓶颈、两阶段训练、基准范围，以及演示数据减少10倍的说法。

### 以对象为中心的世界模型变得更明确了，但仍然脆弱
HCLSM把世界模型推进到面向对象和事件结构的方向，但证据有好有坏。该模型把场景拆成多个槽位，为连续运动、事件帧和更高层目标分别建模动态，并加入对象之间学习得到的交互边。它的两阶段训练很关键：先让槽位形成专门分工，再开启未来预测。在PushT上，分阶段方法报告的下一状态预测误差是0.008，吞吐量达到每秒2.9步。论文也展示了当前的限制。槽位仍然分散，学到的因果图没有变得有用，而且4次运行里只有2次完成，因为bf16出现了NaN。

#### Evidence
- [HCLSM: Hierarchical Causal Latent State Machines for Object-Centric World Modeling](../Inbox/2026-03-31--hclsm-hierarchical-causal-latent-state-machines-for-object-centric-world-modeling.md): 摘要提供了分阶段训练的说法、PushT指标、吞吐量、分解较弱、因果图失效，以及稳定性问题的细节。
