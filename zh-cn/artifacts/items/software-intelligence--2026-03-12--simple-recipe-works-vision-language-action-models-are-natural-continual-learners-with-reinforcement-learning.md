---
source: arxiv
url: http://arxiv.org/abs/2603.11653v1
published_at: '2026-03-12T08:22:39'
authors:
- Jiaheng Hu
- Jay Shim
- Chen Tang
- Yoonchang Sung
- Bo Liu
- Peter Stone
- Roberto Martin-Martin
topics:
- continual-learning
- reinforcement-learning
- vision-language-action
- lora
- embodied-ai
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning

## Summary
这篇论文表明，对大型预训练视觉-语言-动作模型做**顺序微调（Sequential Fine-Tuning, Seq. FT）+ LoRA + on-policy RL**，在持续强化学习中竟然天然很稳，不仅几乎不遗忘，还常常优于更复杂的持续学习方法。

## Problem
- 论文要解决的是：**视觉-语言-动作（VLA）模型在不断到来的新任务上持续强化学习时，如何一边学新任务，一边不忘旧任务**。
- 这很重要，因为真实机器人/具身智能体处在**开放、变化的环境**中，需要持续自我改进，而不是只会离线一次性训练好的固定能力。
- 传统持续学习观点认为，直接顺序微调会导致**灾难性遗忘**，所以通常需要回放、正则化、参数隔离等复杂机制，但这些方法常牺牲新任务适应能力和训练成本。

## Approach
- 作者系统比较了**8类持续强化学习方法**，覆盖正则化、回放、参数隔离，以及面向大模型适配的方法，并与**顺序微调**和**多任务联合训练 oracle**对比。
- 实验统一采用**大型预训练 VLA + LoRA 参数高效微调 + GRPO on-policy 强化学习**的训练配方，以便公平研究“为什么简单方法就够强”。
- 在最核心机制上，方法其实很简单：**任务一个接一个来时，只在当前任务上继续训练同一个预训练 VLA，并只更新少量 LoRA 参数**；作者发现这样反而不会明显破坏旧知识。
- 作者进一步分析指出，稳定性的来源是三者协同：**大规模预训练模型**提供稳健表征，**LoRA**限制更新幅度/子空间，**on-policy RL**带来更受控的策略更新；去掉任一部分，遗忘都会显著增加。

## Results
- 在 **libero-spatial** 上，Seq. FT 达到 **AVG 81.2±0.4**，优于 EWC **66.1±0.9**、DER **73.4±1.3**、SLCA **69.9±0.7**、RETAIN **66.0±0.7**，接近 multitask oracle **85.8±0.2**；其遗忘 **NBT 0.3±0.5**，零样本成功率 **ZS 57.1±1.1**，还高于 oracle **51.2±0.7**。
- 在 **libero-object** 上，Seq. FT 达到 **AVG 93.2±0.7**，高于 EWC **82.6±1.2**、Expert Replay **88.8±0.2**、DER **89.1±0.2**、SLCA **84.1±0.7**、RETAIN **76.6±0.3**，接近 oracle **95.7±0.7**；遗忘仅 **NBT 1.0±0.7**，并有 **FWT 7.1±0.8**、**ZS 25.4±0.2**。
- 在 **libero-long-horizon** 上，Seq. FT 达到 **AVG 89.8±0.9**，接近 oracle **90.5±0.8**，优于 EWC **86.6±0.3**、DER **87.6±0.4**、RETAIN **86.2±0.9**；其 **NBT -2.4±1.0**，意味着几乎无遗忘甚至旧任务还有提升，**ZS 86.6±0.2** 也很强。
- 综合三大 benchmark，作者声称 Seq. FT 的遗忘通常**低于 2%**，有时还是负遗忘；相比之下，很多复杂 CRL 方法因约束更新而降低 plasticity，回放法还要求额外存储和旧数据访问，却**没有带来更好结果**。
- 论文还声称，这种现象在**多种受控扰动**（环境参数变化、不同模型/物理域、任务顺序变化）下依然保持，但在当前摘录中未给出这些扩展实验的完整数值。

## Link
- [http://arxiv.org/abs/2603.11653v1](http://arxiv.org/abs/2603.11653v1)
