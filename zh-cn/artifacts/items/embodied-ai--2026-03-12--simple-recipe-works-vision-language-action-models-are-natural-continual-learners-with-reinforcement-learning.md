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
- vision-language-action
- continual-reinforcement-learning
- lora
- robot-foundation-model
- on-policy-rl
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning

## Summary
本文系统研究了大型预训练视觉-语言-动作（VLA）模型在持续强化学习中的表现，核心结论是：看似朴素的顺序微调（Sequential Fine-Tuning, Seq. FT）配合 LoRA 和 on-policy RL，往往已经足够稳定、可扩展，并且比更复杂的持续学习方法更强。它挑战了“顺序训练必然灾难性遗忘”的常识，对构建可持续自我改进的机器人基础模型很重要。

## Problem
- 论文要解决的问题是：**VLA 模型在任务持续到来时，能否一边学新任务、一边保住旧能力与零样本泛化，而不发生灾难性遗忘**。
- 这很重要，因为真实机器人环境是开放且不断变化的，机器人基础模型若不能持续适应，就难以成为真正长期可用的 embodied agent。
- 传统持续学习通常认为直接顺序微调会严重遗忘，因此需要回放、正则化、参数隔离等复杂机制；作者质疑这一点在“大型预训练 VLA + RL 后训练”场景下是否仍然成立。

## Approach
- 作者对 **3 个不同 VLA 模型、5 个持续 RL 基准**进行系统比较，评估 8 类方法：Seq. FT、多任务 oracle、EWC、Expert Replay、Dark Experience Replay、Dynamic Weight Expansion、SLCA、RETAIN。
- 基础训练配方很简单：**冻结大部分预训练骨干，仅用 LoRA 做参数高效适配，并使用 on-policy 的 GRPO 进行 RL 后训练**。
- 评估指标包括：训练任务平均成功率 **AVG**、遗忘程度 **NBT**、前向迁移 **FWT**，以及专门衡量保留预训练泛化能力的 **ZS（zero-shot success）**。
- 作者进一步做机制分析，主张性能来自三者协同：**大规模预训练提供强初始表示，LoRA 限制更新幅度减少干扰，on-policy RL 让更新更稳定**；去掉任一要素都会显著加剧遗忘。

## Results
- 在 **libero-spatial** 上，Seq. FT 达到 **AVG 81.2±0.4%**、**NBT 0.3±0.5**、**FWT 3.9±1.5**、**ZS 57.1±1.1%**；相比 EWC 的 **66.1% AVG**、RETAIN 的 **66.0% AVG** 明显更好，接近 multitask oracle 的 **85.8% AVG**，且 **ZS 甚至高于 oracle（57.1% vs 51.2%）**。
- 在 **libero-object** 上，Seq. FT 达到 **AVG 93.2±0.7%**、**NBT 1.0±0.7**、**FWT 7.1±0.8**、**ZS 25.4±0.2%**；优于 EWC **82.6%**、SLCA **84.1%**、RETAIN **76.6%**，接近 oracle **95.7%**。Expert Replay 的 ZS 略高（**26.7%**），但 AVG 仍低于 Seq. FT（**88.8% vs 93.2%**）。
- 在 **libero-long-horizon** 上，Seq. FT 达到 **AVG 89.8±0.9%**、**NBT -2.4±1.0**、**FWT 0.5±0.1**、**ZS 86.6±0.2%**；与 oracle **90.5% AVG** 几乎持平，并表现出**负遗忘**（旧任务反而提升）。
- 总体上，作者声称 Seq. FT 的遗忘非常小，**NBT 在多个基准上都低于约 2% 且有时为负**，与“顺序微调会严重灾难性遗忘”的经典结论相反。
- 与复杂 CRL 方法相比，作者认为它们往往引入稳定性约束却损害可塑性：例如 EWC、SLCA、RETAIN 在多个基准上 AVG 明显更低；DWE 虽几乎不忘（如 **NBT 0.0**），但前向迁移为 **0.0**，说明难以利用跨任务正迁移；回放法还依赖额外存储和旧数据。
- 文本还提到作者在环境扰动、不同模型/物理引擎、任务顺序变化下观察到类似趋势，但给定摘录中**完整数值结果未全部提供**；最强具体主张是：**大型预训练 VLA + LoRA + on-policy RL 的组合，使简单顺序微调成为一种天然的持续学习器**。

## Link
- [http://arxiv.org/abs/2603.11653v1](http://arxiv.org/abs/2603.11653v1)
