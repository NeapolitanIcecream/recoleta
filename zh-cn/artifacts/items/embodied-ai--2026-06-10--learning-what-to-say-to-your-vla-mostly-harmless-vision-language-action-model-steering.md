---
source: arxiv
url: https://arxiv.org/abs/2606.12299v1
published_at: '2026-06-10T16:34:49'
authors:
- Hyun Joe Jeong
- Gokul Swamy
- Andrea Bajcsy
topics:
- vision-language-action
- robot-policy-steering
- language-feedback
- conformal-prediction
- robot-data-scaling
- closed-loop-control
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering

## Summary
## 摘要
本文训练了一个语言反馈策略，在每个重规划步骤改变输入给冻结 VLA 模型的语言，从而引导模型执行任务。论文声称，这种方法在使用 conformal prediction 门控避免可能有害的引导时，能显著提高成功率。

## 问题
- VLA 模型对意思几乎相同的指令可能表现出很不一样的反应，因此用户和零样本语言模型都难以可靠地选出能让机器人完成任务的提示词。
- 有些任务无法通过语言改进，因为基础 VLA 可能忽略语言，或者缺少所需的低层行为。
- 这很重要，因为错误的引导提示词会让任务成功率低于直接给出原始指令。

## 方法
- 该方法保持 VLA 冻结，只在闭环执行过程中改变传给它的语言输入。
- 它先用 VLM 给机器人行为视频生成描述，然后微调 Qwen3-VL-4B-Instruct 作为语言反馈策略，提出与任务相关的子任务指令。
- 它使用 GPT-5.4 为每个候选序列生成 16 个轨迹级语言扰动，在这些序列上运行冻结的 VLA，并估计哪些序列相比原始任务指令能提高成功率。
- 它对语言反馈策略进行 rejection fine-tuning，保留带来正向提升的最佳序列。
- 它训练一个 improvement head 来预测何时引导会有帮助，然后用按类别条件的 conformal prediction 校准阈值；当预测收益太低时，策略会拒绝执行并回退到原始指令。

## 结果
- 根据摘要，在见过的环境中，这个经过 conformal 校准的语言反馈策略在仿真中把基础 VLA 性能提高了 24.7%，在 Franka 硬件上提高了 65.0%。
- 仿真设置使用 pi0.5-LIBERO 在 LIBERO-OOD 上测试，包括 LIBERO-10 风格的长时程任务、每个视觉环境 5 个语义扰动，以及 200 个视觉-语义评估组合。
- 硬件设置使用 pi0.5-DROID 在 Franka 机器人上做 zero-shot 测试，包含 4 个训练任务、视觉和语义扰动，以及 2 个未见过的任务，用于 zero-shot LFP 泛化。
- 训练时，每个任务使用 50 个机器人视频做叙述，并且每个交互式搜索种子对应 16 个语言序列扰动。
- 在校准数据和测试数据满足可交换性的前提下，这个 conformal 门控给出了文中所述的假阳性保证 P(steer | steering harms) <= alpha。
- 论文声称，闭环语言反馈产生了开环提示改写没有表现出的恢复行为，但摘录没有给出这组比较的精确成功率数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12299v1](https://arxiv.org/abs/2606.12299v1)
