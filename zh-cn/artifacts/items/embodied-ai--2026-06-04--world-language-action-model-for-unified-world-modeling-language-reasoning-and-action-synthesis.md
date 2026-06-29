---
source: arxiv
url: https://arxiv.org/abs/2606.05979v1
published_at: '2026-06-04T10:23:01'
authors:
- Yi Yang
- Zhihong Liu
- Siqi Kou
- Yiyang Chen
- Yanzhe Hu
- Jianbo Zhou
- Boyuan Zhao
- Zhijie Wei
- Xiao Xia
- Xueqi Li
- Pengfei Liu
- Zhijie Deng
topics:
- world-language-action
- robot-foundation-model
- world-model
- vision-language-action
- long-horizon-manipulation
- cross-embodiment-learning
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# World-Language-Action Model for Unified World Modeling, Language Reasoning, and Action Synthesis

## Summary
## 总结
WLA 提出了一种世界-语言-行动机器人模型，把文本子任务、未来视觉状态和动作放在同一策略里预测。文中报告的 WLA-0 原型在仿真和真实机器人环境中都取得了较强结果，推理时使用 20 亿活跃参数，在 NVIDIA RTX 5090 上延迟约 40 毫秒。

## 问题
- 现有的世界-行动模型主要预测未来图像，这能提供有用的物理监督，但对长时程任务的高层语言规划支持较弱。
- 现有的视觉-语言-行动模型可以执行语言指令，但往往缺少对物理动态的直接未来状态监督。
- 这很重要，因为长时程机器人操作需要语义进展跟踪、记忆，以及在视觉条件变化时快速生成动作。

## 方法
- WLA 以图像、文本指令和机器人状态为输入，然后预测文本子任务、紧凑的物理动态表示和一个动作块。
- 自回归 Transformer 主干生成语言子任务和编码物理转移的 meta-query 输出。
- World Expert 训练这些 meta-query 输出去预测未来视觉帧，Action Expert 则把同一个转移信号和本体感觉输入映射为可执行动作。
- 常规推理时可以移除 World Expert，因此动作生成保留了世界预测带来的训练收益，而在测试时不需要承担图像生成成本。
- 测试时缩放模式会采样多个动作块，为每个动作块预测未来帧，用价值模型对这些想象状态打分，然后执行得分最高的动作块。

## 结果
- WLA-0 总参数量为 34 亿，推理时使用约 20 亿活跃参数，并报告在 NVIDIA RTX 5090 上约 40 毫秒的推理延迟。
- 在 RoboTwin 2.0 上，WLA-0 在 Clean 上报告 92.94% 的成功率，在 Randomized 上报告 90.02%，且没有具身预训练；Lingbot-VA 分别为 92.90% 和 91.50%，Fast-WAM 分别为 91.88% 和 91.78%。
- 在 LIBERO 上，WLA-0 在 Spatial、Object、Goal 和 Long 四项上的平均成功率为 98.6%；测试时缩放使用 6 个候选和 horizon 2 后，平均值升至 98.9%。
- 去掉世界建模损失后，RoboTwin Clean 从 92.94% 降到 90.98%，LIBERO 平均值从 98.6% 降到 97.9%，这支持未来状态监督能提高动作学习。
- 在 RMBench 上，WLA-0 的平均成功率为 56.5%，对比 Mem-0 的 28.5%、Fast-WAM 的 13.3%、X-VLA 的 7.3% 和 pi-0.5 的 5.5%；去掉语言子任务损失后，WLA-0 降到 17.3%。
- 对于仅有视频数据的未见 RoboTwin 2.0 任务，摘要给出的相对已见动作基线的平均提升为：同具身视频达到 34.4 / 30.0，对比 13.0 / 11.6；跨具身视频达到 28.8 / 27.4。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05979v1](https://arxiv.org/abs/2606.05979v1)
