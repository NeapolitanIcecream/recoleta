---
source: arxiv
url: http://arxiv.org/abs/2603.05839v1
published_at: '2026-03-06T02:49:49'
authors:
- Anushka Debnath
- Stephen Cranefield
- Bastin Tony Roy Savarimuthu
- Emiliano Lorini
topics:
- llm-interpretability
- trust-modeling
- white-box-analysis
- activation-space
- human-ai-interaction
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating LLM Alignment With Human Trust Models

## Summary
本文研究大语言模型内部是否真的“理解”人类信任理论，而不只是在输出上表现得像会谈论信任。作者对白盒分析 GPT-J-6B 的激活空间，发现其内部“trust”表征最接近 Castelfranchi 的社会认知信任模型，其次是 Marsh 模型。

## Problem
- 论文要解决的问题是：LLM 内部究竟如何表示“信任”，以及这种表示是否与已有的人类信任理论一致。
- 这很重要，因为信任是人机协作、多智能体合作与决策中的核心因素；如果模型内部信任表征偏差很大，系统设计和行为解释都会受影响。
- 以往研究多是黑盒地看输入输出，缺少对白盒内部激活和概念结构的直接检验。

## Approach
- 选用可访问层级激活的开源模型 **EleutherAI/gpt-j-6B**，对白盒分析其“trust”相关内部表示。
- 从 5 个经典人类信任模型中整理信任相关概念，再用**对比提示**为每个概念构造“正例故事 vs 反例故事”，生成概念方向向量。
- 在固定的软件工程同事情境中，针对双向关系生成概念：如 Katherine→Alice 与 Alice→Katherine；每个概念用 **100** 条正向和 **100** 条负向一行故事构造。
- 对 GPT-J-6B 的 **28 层**隐藏状态提取表示；每层每个 token 为 **4096 维**，先做 token 平均、再做样本平均，最后用“正均值 - 负均值”得到概念向量，并跨层平均成单一概念嵌入。
- 先对 **30 个情绪/关系概念**扩展成双向 **60 个概念**，计算两两余弦相似度分布，取 **80 分位数**对应的 **0.6** 作为“显著对齐”阈值；再比较 trust 与各信任模型概念的相似度均值和超阈值数量。

## Results
- 在 60 个一般概念的两两相似度分析中，作者设定 **0.6** 为显著对齐阈值，对应所有概念对余弦相似度分布的**前 20%**。
- 五个信任模型中，**Castelfranchi 模型**与 trust1 的平均相似度最高，为 **0.7303**，且有 **8** 个概念超过阈值；是论文的主结论。
- **Marsh 模型**排名第二，平均相似度 **0.6973**，有 **7** 个概念超过阈值；其后依次是 **McAllister 0.6704（4 个）**、**McKnight 0.6640（5 个）**、**Mayer 0.4530（5 个）**。
- Castelfranchi 模型中与 trust1 最接近的概念包括：**confidence1 0.9225**、**reputation1 0.8963**、**willingness2 0.8858**、**competence2 0.8504**、**commitment2 0.8450**、**security1 0.8089**。
- 论文还发现少数“理论上应正相关”的概念在模型内部却为负相关：例如 Mayer 模型里的 **risk1 = -0.8462**、**benevolence2 = -0.1434**；作者据此认为 LLM 的内部表征并不完全遵循传统理论定义。
- 没有与其他 LLM、其他白盒方法或下游任务精度的直接 baseline 对比；核心突破是首次用白盒激活相似度框架，对 LLM 内部“信任”概念与人类信任模型做定量对齐分析。

## Link
- [http://arxiv.org/abs/2603.05839v1](http://arxiv.org/abs/2603.05839v1)
