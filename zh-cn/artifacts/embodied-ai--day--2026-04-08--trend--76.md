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

# 具身控制工作集中在有约束的决策机制上

## 概览
这一天的内容不多，但很清楚。两篇论文都在处理更贴近现实约束的具身决策循环。一篇用事件编码情境上的记忆检索来做 UAV 控制。另一篇用有约束的想象来减少模型式强化学习里的 rollout 漂移。它们共同强调的是，在时间跨度变长或环境更复杂时，动作选择仍然要快、可检查、稳定。

## 研究发现

### 用于可检查动作选择的基于检索的世界模型
记忆是当天具身控制论文里最具体的机制。该 UAV 系统把场景转成语义事件，从知识库中检索相似的过往情境，再从最匹配的机动簇里选取动作。论文的主张很实际：让控制环路保持足够快以便部署，同时保留动作为何被选中的痕迹。结果只在作者自己的设置里很强，控制间隔为 20–50 ms，检索低于毫秒级，在五个对抗式课程回合中达到 100% 成功率且零碰撞。证据范围比重基准的机器人论文更窄，因为摘录里没有外部基线或大规模消融。

#### 资料来源
- [Event-Centric World Modeling with Memory-Augmented Retrieval for Embodied Decision-Making](../Inbox/2026-04-08--event-centric-world-modeling-with-memory-augmented-retrieval-for-embodied-decision-making.md): Summary gives the event-centric retrieval design and reported UAV results.

### 模型式强化学习中的有约束想象
这篇强化学习论文的重点是让想象轨迹在长时间跨度内保持接近现实。GIRL 从视觉模型 DINOv2 加入一个 grounding 信号，并用一个自适应信任域瓶颈替换固定的 KL 项，这个瓶颈会根据不确定性和真实转移反馈调整。报告的提升范围很广：DeepMind Control 上的 IQM 为 0.81，DreamerV3 为 0.67，TD-MPC2 为 0.71，同时漂移分数更低，在干扰物和操作任务上也更好。一个蒸馏版本还把 grounding 开销从总运行时间的 22% 降到 4% 以下，这对它能否在训练速度上保持竞争力很重要。

#### 资料来源
- [GIRL: Generative Imagination Reinforcement Learning via Information-Theoretic Hallucination Control](../Inbox/2026-04-08--girl-generative-imagination-reinforcement-learning-via-information-theoretic-hallucination-control.md): Summary gives the method, benchmark comparisons, drift reductions, and compute note.
