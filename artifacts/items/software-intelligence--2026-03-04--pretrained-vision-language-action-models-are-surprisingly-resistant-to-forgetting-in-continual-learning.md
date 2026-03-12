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
- continual-learning
- vision-language-action
- robot-learning
- experience-replay
- catastrophic-forgetting
relevance_score: 0.16
run_id: materialize-outputs
---

# Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning

## Summary
这篇论文研究大型预训练视觉-语言-动作模型（VLA）在机器人持续学习中是否会像传统小模型一样严重遗忘。作者发现，预训练VLA配合非常简单的经验回放就能显著抑制遗忘，甚至在小回放缓存下接近零遗忘。

## Problem
- 机器人持续学习需要按顺序学新任务，但常见策略模型在学习新任务时会**灾难性遗忘**旧任务。
- 现有结论多来自**从零训练的小型行为克隆模型**；对于现代**大规模预训练VLA**，其持续学习行为缺乏系统研究。
- 这个问题重要，因为若大模型本身更抗遗忘，就能让机器人以更简单的方法持续积累技能，而不必依赖复杂正则化或巨大回放缓存。

## Approach
- 在 **LIBERO-Spatial / Object / Goal / 10** 四个机器人持续学习基准上，比较两类预训练VLA（**Pi0、GR00T N1.5**）与多个非预训练小模型（如 **BC-Transformer、BC-ViT、BC-DP**）。
- 采用最简单的**Experience Replay (ER)**：顺序训练任务时，只保留每个旧任务的一小部分样本，与当前任务数据混合训练。
- 用 **Success Rate (SR)** 衡量整体任务成功率，用 **Negative Backward Transfer (NBT)** 衡量遗忘；NBT 越接近 0 越好，负值表示对旧任务还有正向回迁。
- 为分析预训练作用，固定 Pi0 架构，比较三种初始化：**VL+Action 预训练**、**仅VL预训练**、**从零训练**，并改变回放缓存大小（如 10 / 100 / 1000 样本）。
- 进一步通过**组件交换与恢复实验**分析“看似遗忘但知识仍保留”的现象：分别检查视觉语言骨干和动作头在继续学习后是否仍保存旧任务知识。

## Results
- 在 **20% 数据/任务（sample size=1000）** 设置下，预训练VLA明显优于非预训练模型：
  - **GR00T** 平均 **SR=0.919±0.011**, **NBT=0.027±0.021**；
  - **Pi0** 平均 **SR=0.768±0.017**, **NBT=-0.016±0.022**；
  - 对比 **BC-DP** 的 **SR=0.696±0.068, NBT=0.127±0.071**，**BC-T** 的 **SR=0.585±0.066, NBT=0.245±0.080**，说明VLA遗忘更少且成功率更高。
- 在 **LIBERO-Object** 与 **LIBERO-10** 上，ER远优于不回放方法：
  - **Pi0 + ER**：Object **SR=0.898, NBT=-0.007**；10 **SR=0.586, NBT=-0.070**。
  - **Pi0 Sequential**：Object **NBT=0.696**；10 **NBT=0.562**。
  - **GR00T + ER**：Object **SR=0.962, NBT=0.004**；而 **Sequential** 在 Object 上 **NBT=0.752**，**EWC** 为 **0.766**。
- 小缓存下预训练优势更明显：作者称在 **2% 回放数据（100样本/任务）** 时，预训练VLA的 **NBT 约 0.1–0.2**，而非预训练基线约 **0.4–0.5**，即后者遗忘大约 **2–4 倍**；有时VLA在该设置下可实现**零遗忘**。
- 预训练本身是关键因素。在相同 Pi0 架构下（sample size=1000）：
  - **Pi0 from VL+Action**：平均 **SR=0.863, NBT=-0.0322**；
  - **Pi0 from VL**：平均 **SR=0.899, NBT=0.0159**；
  - **Pi0 from scratch**：平均 **SR=0.655, NBT=-0.0393**；
  - **BC-Transformer**：平均 **SR=0.678, NBT=0.191**。
  这表明低遗忘不能单看 NBT；预训练同时提升**前向学习能力**与保持旧知识的能力。
- 论文还声称：即便某些旧任务性能下降，VLA内部仍保留相关知识，因而经过**少量微调步骤**即可快速恢复旧技能；摘录中未给出该恢复实验的明确数值，但这是作者关于“表面遗忘不等于知识彻底丢失”的核心结论。

## Link
- [http://arxiv.org/abs/2603.03818v1](http://arxiv.org/abs/2603.03818v1)
