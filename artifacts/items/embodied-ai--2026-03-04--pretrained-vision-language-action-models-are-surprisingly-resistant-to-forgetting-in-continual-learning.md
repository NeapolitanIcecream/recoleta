---
source: arxiv
url: http://arxiv.org/abs/2603.03818v1
published_at: '2026-03-04T08:03:13'
authors:
- Huihan Liu
- Changyeon Kim
- Bo Liu
- Minghuan Liu
- Yuke Zhu
topics:
- vision-language-action
- continual-learning
- experience-replay
- catastrophic-forgetting
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
---

# Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning

## Summary
本文研究大规模预训练视觉-语言-动作（VLA）模型在机器人持续学习中的遗忘问题，发现它们比从零训练的小模型更不容易灾难性遗忘。核心结论是：对VLA来说，简单的经验回放就常常足够，且预训练显著改变了持续学习的动态。

## Problem
- 机器人策略需要按时间顺序持续学习新任务，但通常会**灾难性遗忘**旧任务，导致顺序微调几乎不可用。
- 以往结论主要来自**小型、从零训练的行为克隆模型**；这些结论是否适用于现代**预训练VLA**仍不清楚。
- 这个问题重要，因为若VLA天然更抗遗忘，就能用更简单的方法持续扩展机器人技能库，而不必依赖很大的回放缓存或复杂正则化。

## Approach
- 在 **LIBERO-Spatial / Object / Goal / 10** 四个持续学习基准上，比较两类预训练VLA（**Pi0、GR00T N1.5**）与多种非预训练小模型（如 **BC-Transformer、BC-ViT、BC-Diffusion Policy**）。
- 使用最简单的**Experience Replay (ER)**：学习新任务时，混合当前任务数据和少量旧任务回放样本；用**平均成功率（SR）**和**Negative Backward Transfer（NBT，越低越好）**评估遗忘。
- 做受控消融来隔离**预训练的作用**：比较同一Pi0架构的三种初始化——**VL+Action预训练、仅VL预训练、从零训练**，并扫描不同回放缓存大小（0.2%、2%、20%）。
- 进一步通过**模块交换与再微调恢复实验**分析“表面遗忘”是否等于“知识彻底消失”，区分VL骨干和动作头中的知识保留情况。

## Results
- 在 **sample size=1000（每任务约20%数据）** 下，预训练VLA + ER显著优于小模型：**GR00T** 在四个LIBERO套件平均 **SR=0.919±0.011, NBT=0.027±0.021**；**Pi0** 平均 **SR=0.768±0.017, NBT=-0.016±0.022**。对比 **BC-Transformer** 平均 **SR=0.585±0.066, NBT=0.245±0.080**，**BC-ViT** 平均 **SR=0.508±0.142, NBT=0.193±0.082**。这表明VLA遗忘接近零，甚至出现**正向后向迁移**（负NBT）。
- 在更具体任务上，**GR00T** 于 **LIBERO-Object** 达到 **SR=0.975±0.004, NBT=0.019±0.013**，于 **LIBERO-10** 达到 **SR=0.820±0.017, NBT=0.059±0.035**；而 **BC-Transformer** 在相同两项仅有 **0.595±0.112 / 0.132±0.120** 和 **0.376±0.034 / 0.192±0.019**。
- 与非ER基线相比，**ER对VLA特别有效**。例如在 **GR00T, LIBERO-Object** 上：**Sequential** 的 **NBT=0.752**，**EWC=0.766**，而 **ER=0.004**；在 **Pi0, LIBERO-10** 上：**Sequential=0.562**，**EWC=0.543**，而 **ER=-0.070**。说明少量显式回放远胜仅靠顺序训练或参数正则化。
- 在**小回放缓存**下，VLA仍明显更抗遗忘：当 buffer size 为 **2%（每任务100样本）** 时，文中称 **Pi0/GR00T 的 NBT 约 0.1–0.2**，而非预训练基线约 **0.4–0.5**，即后者遗忘高出约 **2–4倍**；小模型通常需要 **>20%** 的回放数据才接近VLA表现。
- 预训练本身是关键因素。Pi0受控比较中，**Pi0 from VL+Action** 平均 **SR=0.863, NBT=-0.0322**；**Pi0 from VL** 平均 **SR=0.899, NBT=0.0159**；**Pi0 from scratch** 平均 **SR=0.655, NBT=-0.0393**；**BC-Transformer** 平均 **SR=0.678, NBT=0.191**。作者据此认为，预训练不仅降低遗忘，还保持更强的**前向学习能力**；从零训练时，低遗忘有时只是因为新任务也没学好。
- 论文还声称：即便旧任务性能在持续学习中下降，**VLA内部仍保留相关知识**，因为只需**少量finetuning steps**就能快速恢复旧任务表现；摘录中未给出这一恢复实验的具体数值，但这是其关于“表面遗忘不等于知识消失”的最强具体主张。

## Link
- [http://arxiv.org/abs/2603.03818v1](http://arxiv.org/abs/2603.03818v1)
