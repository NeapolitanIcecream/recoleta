---
kind: trend
trend_doc_id: 76
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
topics:
- embodied-ai
- world-models
- model-based-rl
- retrieval
- safety
run_id: materialize-outputs
aliases:
- recoleta-trend-76
tags:
- recoleta/trend
- topic/embodied-ai
- topic/world-models
- topic/model-based-rl
- topic/retrieval
- topic/safety
language_code: zh-CN
---

# 具身控制研究集中在有依据的决策机制上

## Overview
这一天的内容不多，但方向很清楚。两篇论文都在处理更贴近真实约束的具身决策回路。一篇用基于事件编码情境的记忆检索来做 UAV 控制。另一篇用 grounded imagination 来减少基于模型的强化学习中的 rollout 漂移。它们共同强调的是：当时域变长或环境更复杂时，动作选择仍然要快、可检查、而且稳定。

## Clusters

### 基于检索的世界模型，用于可检查的动作选择
在当天这篇具身控制论文里，记忆是最具体的核心机制。该 UAV 系统先把场景转成语义事件，再从知识库中检索相似的过往情境，然后从最匹配的机动簇中选择动作。论文的主张很务实：在让控制回路足够快、能够部署的同时，也保留动作为何被选中的线索。按论文报告，在其自身设定内结果很强，控制间隔为 20–50 ms，检索延迟低于 1 ms，并且在五个对抗式课程回合中实现了 100% 成功率和零碰撞。和一篇以基准测试为主的机器人论文相比，这里的证据范围更窄，因为摘录没有给出外部基线或大范围消融。

#### Evidence
- [Event-Centric World Modeling with Memory-Augmented Retrieval for Embodied Decision-Making](../Inbox/2026-04-08--event-centric-world-modeling-with-memory-augmented-retrieval-for-embodied-decision-making.md): 摘要给出了以事件为中心的检索设计和报告的 UAV 结果。

### 模型强化学习中的 grounded imagination
这篇强化学习论文的重点是让想象出的轨迹在长时域内保持贴近真实。GIRL 引入了来自视觉模型 DINOv2 的 grounding 信号，并用一个会根据不确定性和真实转移反馈调整的自适应 trust-region bottleneck 替代固定的 KL 项。论文报告的提升比较全面：在 DeepMind Control 上，IQM 达到 0.81，而 DreamerV3 为 0.67、TD-MPC2 为 0.71；同时漂移分数更低，在干扰任务和操作任务上的结果也更好。一个蒸馏变体还把 grounding 带来的墙钟时间开销从 22% 降到 4% 以下，这对方法在训练速度上保持竞争力很重要。

#### Evidence
- [GIRL: Generative Imagination Reinforcement Learning via Information-Theoretic Hallucination Control](../Inbox/2026-04-08--girl-generative-imagination-reinforcement-learning-via-information-theoretic-hallucination-control.md): 摘要给出了方法、基准对比、漂移降低情况和计算说明。
