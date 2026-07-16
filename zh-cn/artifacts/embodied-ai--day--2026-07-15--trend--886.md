---
kind: trend
trend_doc_id: 886
granularity: day
period_start: '2026-07-15T00:00:00'
period_end: '2026-07-16T00:00:00'
topics:
- robot learning
- VLA fine-tuning
- representation anchoring
- execution recovery
- world action models
- human-in-the-loop autonomy
run_id: materialize-outputs
aliases:
- recoleta-trend-886
tags:
- recoleta/trend
- topic/robot-learning
- topic/vla-fine-tuning
- topic/representation-anchoring
- topic/execution-recovery
- topic/world-action-models
- topic/human-in-the-loop-autonomy
language_code: zh-CN
---

# 机器人策略保留预训练知识，并将恢复任务交给轻量级控制层

## 概览
今天的证据进一步支持近期对部署的关注，并指向一种更具体的设计模式：保留有用结构，而不是端到端地重新学习所有内容。两项研究在视觉—语言—动作（VLA）微调期间保护预训练语义，另一些研究则将预测训练、运行时恢复和人工纠正与已部署的动作策略分离。结果令人鼓舞，但大多仍局限于单项基准测试和小规模真实机器人研究。

## 研究发现

### VLA 微调期间的语义保留
两种独立方法都将行为克隆微调期间的表征损失视为泛化失败。Semantic Anchoring 将共享动作通道对齐到冻结的文本流形，并发现这种对齐程度与分布外成功率相关，Spearman ρ=0.964。Anchor-Align 则蒸馏冻结视觉语言模型的隐状态，并在机器人观测上增加运动方向预测。在 LIBERO-PRO 上，它达到 71.9%，而其 VLA-Adapter 基线为 61.0%。这些研究共同支持保留预训练概念，同时为执行特定特征留出空间。

#### 资料来源
- [Semantic Anchoring for Robotic Action Representations](../Inbox/2026-07-15--semantic-anchoring-for-robotic-action-representations.md): 报告语义侵蚀、其与分布外成功率的相关性，以及通过锚定动作特征带来的提升。
- [Generalizable VLA Finetuning via Representation Anchoring and Language-Action Alignment](../Inbox/2026-07-15--generalizable-vla-finetuning-via-representation-anchoring-and-language-action-alignment.md): 报告分层锚定、语言—动作对齐，以及基准测试和真实机器人性能的提升。

### 训练时增加能力，部署时不增加开销
GigaWorld-Policy-0.5 从未来视觉动态中学习，但通过分离的视觉专家和动作专家，在部署时跳过视频生成；其纯动作路径在 RTX 4090 上的运行时间约为 85 ms。一个互补的执行管理器保持底层操作策略冻结，并在执行、重试、修复和重置模式之间进行选择。在注入干扰的情况下，它使 LIBERO 各套件的成功率提升了 25.7 至 39.2 个百分点。这两种设计都将成本高昂的预测或恢复逻辑与核心动作生成器分离，而不是扩展每一步推理。

#### 资料来源
- [GigaWorld-Policy-0.5: A Faster and Stronger WAM Empowered by AutoResearch](../Inbox/2026-07-15--gigaworld-policy-0-5-a-faster-and-stronger-wam-empowered-by-autoresearch.md): 在训练期间使用未来场景监督，同时报告 85 ms 的纯动作推理时间和真实机器人任务性能提升。
- [Learning Robust Execution in Robotic Manipulation with Agentic Reinforcement Learning](../Inbox/2026-07-15--learning-robust-execution-in-robotic-manipulation-with-agentic-reinforcement-learning.md): 在冻结的低层策略外围增加高层恢复策略，并报告其在 LIBERO 各套件中的干扰条件性能提升。

### 操作知识转化为可复用监督
PhysClaw-0 将自然语言纠正保存为可复用规则，因此反复出现的数据采集失败不再需要操作员重复干预。它用 4.8 分钟的人工作业时间采集了 50 条有效示范，而遥操作需要 30 分钟，同时下游策略的成功率均为 80%。Industrial Dexterity Benchmark 展示了更丰富传感的类似价值：在电缆抓取并插入任务中，多模态模仿学习达到 78%，而单摄像头 RGB 仅为 36%。这些评估范围有限，但表明持久化纠正和任务特定传感能够减少对单一整体策略的依赖。

#### 资料来源
- [PhysClaw-0: A Symbiotic Agentic System for Robot Autonomy via Language Corrections](../Inbox/2026-07-15--physclaw-0-a-symbiotic-agentic-system-for-robot-autonomy-via-language-corrections.md): 量化了操作员时间的减少、持久化纠正记忆，以及在一项真实机器人任务中相当的下游部署成功率。
- [Industrial Dexterity Benchmark: A Hardware-Software Benchmarking Platform for Industrial Dexterous Manipulation](../Inbox/2026-07-15--industrial-dexterity-benchmark-a-hardware-software-benchmarking-platform-for-industrial-dexterous-manipulation.md): 报告了多模态工业基准的设置，以及电缆任务中 78% 对比 36% 的结果。
