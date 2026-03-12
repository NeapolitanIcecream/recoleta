---
source: arxiv
url: http://arxiv.org/abs/2603.04819v1
published_at: '2026-03-05T05:10:47'
authors:
- Pradyumna Tambwekar
- Andrew Silva
- Deepak Gopinath
- Jonathan DeCastro
- Xiongyi Cui
- Guy Rosman
topics:
- embodied-ai
- synthetic-data
- open-set-assistance
- multimodal-learning
- robotics
- overcooked
relevance_score: 0.38
run_id: materialize-outputs
---

# On the Strengths and Weaknesses of Data for Open-set Embodied Assistance

## Summary
本文研究开放集具身辅助中的“数据到底该怎么构造”问题：仅靠合成交互数据，模型能否理解长时序用户行为，并对从未见过的缺陷或新任务给出纠正动作或文字指导。作者在 Overcooked 中构建多模态合成数据并微调 Llama-based 模型，发现精心设计的数据能显著提升开放集辅助泛化，但任务泛化仍然更难。

## Problem
- 现有辅助式具身模型通常假设**封闭的纠正类别**，或依赖**外部规划器**，难以应对真实场景中开放、多样、未预定义的用户错误行为。
- 长时序、多模态的人机交互数据昂贵且噪声大，导致很难系统评估：模型是否能对**未见过的行为缺陷**和**新任务配置**进行泛化。
- 这很重要，因为机器人/自动驾驶等交互式系统若不能给新用户、新任务提供可靠辅助，就难以安全、有效地落地部署。

## Approach
- 定义**Open-Set Corrective Assistance**：模型读取用户的多模态轨迹（图像状态+动作文本），生成两类辅助之一：**纠正动作**或**自然语言反馈**，且不提供固定标签集合。
- 在 Overcooked 中用合成用户生成数据：设计 **5** 种启发式策略、**17** 类缺陷（含 no defect）、**450** 个程序化地图，并在 rollout 中加入 **20%** 随机动作噪声，制造丰富而分层的行为分布。
- 构建两大类训练数据：一类是 grounding 数据（Image-QA **55k**、Trajectory-QA **54k**、Video-QA **55k**），提升空间/时序理解；另一类是任务数据（Coaching **26k**、Corrections **27k**、Defect-Delineation **20k**）。
- 模型结构采用 **Llama-3 + ViT-base** 的投影式多模态架构，图像轨迹编码后与动作文本交织输入，统一用文本解码输出反馈或动作。
- 纠正动作由“去除缺陷后的启发式下一步动作”生成，文字反馈与 reasoning traces 则由 **GPT-4o** 合成，用于蒸馏辅助能力与行为分析能力。

## Results
- 在**未见缺陷泛化**上，作者的 **8B** 模型取得最佳 coaching：**77.80**，高于 Behavior Critic (**21.00**) 和 Behavior Critic + Summaries (**55.70**)。
- 在**未见缺陷的纠正动作**上，作者的 **1B** 模型最好：**55.70**，优于 Behavior Critic (**20.40**) 与 Behavior Critic + Summaries (**19.80**)；**8B** 为 **54.60**，接近 1B，说明该能力在 **1B** 左右已趋于饱和。
- 在**新任务/新菜谱泛化**上，作者的 **8B** 模型显著领先：coaching **85.96**，高于 Behavior Critic (**34.21**) 和 Behavior Critic + Summaries (**71.05**)。
- 在**新任务的纠正动作**上，作者的 **8B** 达到 **56.67**，优于 **1B** 的 **50.83**、Behavior Critic 的 **9.17** 和 +Summaries 的 **15.83**；表明任务泛化更依赖更强的多模态 grounding 与模型规模。
- 作者的核心结论是：有效的开放集辅助需要覆盖**多模态 grounding、缺陷推断、场景多样性**的数据；但即便如此，开放任务组合泛化仍然是困难问题。

## Link
- [http://arxiv.org/abs/2603.04819v1](http://arxiv.org/abs/2603.04819v1)
