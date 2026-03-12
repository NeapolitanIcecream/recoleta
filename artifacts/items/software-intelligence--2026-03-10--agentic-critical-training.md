---
source: hf_daily
url: https://huggingface.co/papers/2603.08706
published_at: null
authors: []
topics:
- llm-agents
- reinforcement-learning
- self-reflection
- agent-training
- ood-generalization
relevance_score: 0.87
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# Agentic Critical Training

## Summary
- TL;DR: ACT 用强化学习直接训练语言模型代理去判断两个行动哪个更好，从而学会“为什么这样做更优”的自我反思能力，并在多个代理基准上稳定优于单纯模仿学习、常规强化学习和反思蒸馏方法。
- Problem:
  - 现有代理训练通常从模仿学习开始，只教模型“做什么”，却不教它“为什么这个动作更好”，因此缺乏对行动质量的内在判断能力。
  - 一些方法通过加入由专家/候选动作对比生成的“反思文本”来补救，但本质仍是让模型模仿现成反思，而不是自己学会评判优劣。
  - 对自主代理而言，能否识别更优动作直接影响规划、纠错、泛化和复杂任务表现，因此这个问题很重要。
- Approach:
  - 提出 **Agentic Critical Training (ACT)**：把训练目标从模仿动作/模仿反思，改为“在备选动作中判断哪个更好”。
  - 用强化学习按“判断是否正确”给予奖励；模型若能选对更优动作，就得到正反馈。
  - 这种机制迫使模型自己形成关于行动质量的推理，而不是复述预先构造好的反思语句。
  - ACT 可与不同的后训练方法结合使用，作为提升代理反思与决策能力的通用训练范式。
- Results:
  - 在 **3 个具有挑战性的 agent benchmark** 上，ACT 与不同后训练方法结合时都能持续提升代理性能。
  - 相比 **imitation learning**，平均提升 **5.07 points**。
  - 相比已有 **reinforcement learning** 方法，平均提升 **4.62 points**。
  - 相比通过知识蒸馏注入反思能力的方法，平均提升 **2.42 points**。
  - 论文还声称 ACT 具有**强的分布外泛化能力**，并且在**没有任何推理专项训练数据**的情况下提升一般推理基准表现。
  - 摘要未给出具体 benchmark 名称、绝对分数或更细粒度指标，因此目前可确认的定量结果主要是上述平均点数提升。

## Links
- Canonical: https://huggingface.co/papers/2603.08706
