---
source: arxiv
url: https://arxiv.org/abs/2607.15641v1
published_at: '2026-07-17T05:34:29'
authors:
- Anurag Maurya
- Sukhvansh Jain
- Prajwal Avhad
- Gautham Balachandran
- Ziyi Zhou
- Atharva Kshirsagar
- Satyam Singh
- Bowen Li. Rishabh Mukund
- Ritul Singh
- Jatin Vira
- Suvonil Chatterjee
- Devesh K. Jha
topics:
- robot-manipulation
- robot-foundation-model
- vision-language-action
- physical-reasoning
- robot-benchmark
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# IMBench: A Benchmark for Intuitive Robotic Manipulation

## Summary
## 摘要
IMBench 评估机器人系统能否将物理推理与可执行的操作结合起来。其包含 35 项任务的测试套件揭示了一个明显差距：系统能够识别约束、提出有效动作序列，并在闭环控制下完成任务，这三者之间并不等价。

## 问题
- 现有基准通常将物理推理与操作执行分开测量，因此无法检验模型能否将推断出的约束转化为可行的动作。
- 对于通用机器人策略而言，这一差距十分重要，因为涉及接触、工具使用、隐藏状态、时序和稳定性的任务，即使机器人理解目标，也可能执行失败。

## 方法
- IMBench 提供了 35 项 robosuite 任务，涵盖几何、动力学、因果动作、工具使用、隐藏状态、反应式重新规划和稳定性，并配有约 14,000 条筛选后的轨迹。
- 它将性能形式化为 Understand–Infer–Act 循环：识别任务约束，提出有序的子目标序列，并通过闭环交互执行。
- 该基准首先评估五个视觉语言模型对约束的理解和规划正确性，然后测试 GPT-5.5 以及包括 Diffusion Policy、π0.5 和 GR00T N 1.5 在内的端到端策略。
- 每个回合使用多视角 RGB、本体感知、夹爪状态和腕部力/力矩观测，并输出连续的 6 自由度末端执行器动作和夹爪动作；研究还在分布外物理变化下测试这些策略。

## 结果
- 最强的视觉语言模型在约束理解上的平均成功率约为 74%：Claude Sonnet 4.6 达到 74.5%，GPT-5.5 达到 74.1%；GPT-5.5 在高层规划正确性上的平均得分为 69.5%。
- 在闭环执行中，仅使用视觉输入时，GPT-5.5 在评估任务中的成功率为 11.3%；使用特权对象中心信息时为 18.8%。在两种设置下，精确对齐、时序、工具使用、隐藏状态推理和平衡任务的成功率均为 0%。
- 零样本视觉语言动作策略的平均成功率最高仅为 0.02；针对任务进行训练后，π0.5 的成功率提高到 0.15，GR00T N 1.5 提高到 0.02，Diffusion Policy 提高到 0.24。
- 分布外性能通常大幅下降：π0.5 在 balance-medium 任务上的成功率从分布内的 0.71 降至 0.12，在 keyboard-typing 任务上则从 0.13 降至 0.00；contact-tolerant domino-single 的表现相对更稳健。
- 该基准仅涵盖仿真环境、Franka 机器人、平行夹爪和吸盘夹爪，以及低到中等时域的任务。因此，报告结果并不能证明这些方法在真实机器人或灵巧手上的性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15641v1](https://arxiv.org/abs/2607.15641v1)
