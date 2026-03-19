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
- activation-space
- contrastive-prompting
- white-box-analysis
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating LLM Alignment With Human Trust Models

## Summary
本文研究大语言模型内部是否以接近人类信任理论的方式表示“信任”。作者对白盒分析 GPT-J-6B 的激活空间，发现其内部“信任”表征最接近 Castelfranchi 的社会认知信任模型，其次是 Marsh 模型。

## Problem
- 现有关于 LLM 信任推理的研究多是黑盒的，只看输入输出，几乎不知道模型**内部**如何表示“信任”。
- 如果不知道 LLM 的内部信任概念与哪些人类信任理论对齐，就难以判断其社会推理是否可靠，也难以为人机协作系统设计可解释的信任机制。
- 信任对协作、多智能体系统和人机交互很重要，因此理解 LLM 如何编码信任具有实际意义。

## Approach
- 选用可访问层级激活的开源模型 **EleutherAI/gpt-j-6B**，对白盒分析其隐藏表示。
- 基于 5 个经典人类信任模型提取信任相关概念，并把双人关系设为有方向的二元关系（如 Katherine→Alice 与 Alice→Katherine）。
- 用**对比提示**为每个概念生成正反两类 100 条一句话故事；对 GPT-J-6B 的 28 层隐藏状态做 token 平均、样本平均，并取“正例均值 - 反例均值”得到概念向量，最终跨层平均成单个概念嵌入。
- 先对 30 个情绪/关系概念扩展成 60 个方向化概念，计算两两余弦相似度分布，并把 **0.6**（前 20% 相似度）设为“显著对齐”阈值。
- 再计算 trust1 与各信任模型相关概念的余弦相似度，用两种指标比较模型：**平均相似度**与**超过 0.6 阈值的概念数**。

## Results
- 在 60 个一般概念的两两比较中，作者将 **余弦相似度 0.6** 设为显著对齐阈值，对应整体分布的**前 20%**。
- 按**平均余弦相似度**，5 个信任模型与 trust1 的对齐从高到低为：**Castelfranchi 0.7303** > **Marsh 0.6973** > **McAllister 0.6704** > **McKnight 0.6640** > **Mayer 0.4530**。
- 按**超过阈值的概念数**，结果为：**Castelfranchi 8** > **Marsh 7** > **Mayer 5** = **McKnight 5** > **McAllister 4**。
- Castelfranchi 模型中与 trust1 高度接近的概念包括：confidence1 **0.9225**、reputation1 **0.8963**、willingness2 **0.8858**、competence2 **0.8504**、commitment2 **0.8450**、security1 **0.8089**、reliability2 **0.7667**、predictable2 **0.7141**。
- 论文还指出一些与理论不一致的负相似度：在 Mayer 模型中，**risk1 = -0.8462**、**benevolence2 = -0.1434**；在 McKnight 模型中，**benevolence2 = -0.1434**。这表明 GPT-J-6B 内部未必按这些理论假设来编码“风险”或“仁善”与信任的关系。
- 核心结论是：GPT-J-6B 的内部信任表征更像**社会认知式**的信任观，而不是纯粹的组织行为或初始信任框架；作者将其视为 LLM 激活空间可用于比较社会认知理论的证据。

## Link
- [http://arxiv.org/abs/2603.05839v1](http://arxiv.org/abs/2603.05839v1)
