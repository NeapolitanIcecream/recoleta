---
source: arxiv
url: https://arxiv.org/abs/2606.17937v1
published_at: '2026-06-16T13:45:17'
authors:
- Tianyi Lu
- Hui Zhang
- Zijie Diao
- Junke Wang
- Shengqi Xu
- Xingyao Lin
- Guojin Zhong
- Ziyi Ye
- Peng Wang
- Zuxuan Wu
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- world-model
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ThinkingVLA: Interleaved Vision and Language Reasoning for Robotic Manipulation

## Summary
## 摘要
ThinkingVLA 是一种 VLA 策略，在一个自回归序列中依次生成文本子目标、未来图像、面向动作的文本理由，然后生成机器人动作。它面向长时程操作任务；在这类任务中，直接从观测到动作的策略容易丢失任务结构和空间依据。

## 问题
- 大多数 VLA 策略把当前图像和指令直接映射为动作，这会削弱子目标规划、未来状态检查和长时程执行能力。
- 纯文本 CoT 缺少空间精度，纯视觉预测缺少任务分解，解耦的文本/图像推理也无法让每一步基于前一个已生成模态进行条件生成。
- 更好的长时程机器人控制很重要，因为做早餐或组装物体等任务既需要预测下一场景，也需要推断达到该场景所需的动作。

## 方法
- 该策略把每次决策分解为正向 CoT、预测的未来图像、逆向 CoT 和动作：p(r_fwd, o_hat_{t+1}, r_inv, a_t | o_t, l)。
- thinking expert 使用 PaliGemma 文本分词、SigLIP 观测编码和 Cosmos 图像分词，在一个因果序列中生成文本 token 和离散图像 token。
- 预测图像成为逆向 CoT 的目标状态；逆向 CoT 在生成动作前推理物体位置、夹爪意图和动作方向。
- 一个单独的 300M 参数 action expert 使用 flow matching，并通过共享的 Mixture-of-Transformers 注意力关注完整推理前缀。
- 训练分三阶段：在 Open X-Embodiment 上进行推理/图像预训练，端到端动作学习，然后在 RoboTwin 和 ALOHA 演示上进行目标微调。

## 结果
- 在 RoboTwin 2.0 Easy 上，ThinkingVLA 在 20 个任务上的平均成功率达到 77.9%，高于 BagelVLA 的 73.4%、XVLA 的 69.2%、UP-VLA 的 51.2% 和 π0 的 49.8%。
- 在 RoboTwin 2.0 Hard 上，它的平均成功率达到 29.3%；XVLA 更高，为 35.4%，而 BagelVLA 为 16.8%，π0 为 17.2%，UP-VLA 为 13.3%。
- 在更长的仿真任务上，增益更大：Horizon=2 Easy/Hard 为 71.0%/26.6%，BagelVLA 为 55.8%/7.0%；Horizon=3 为 60.0%/23.6%，BagelVLA 为 55.8%/6.8%。
- 在五个真实 ALOHA 任务上，每个任务使用 50 个演示和 20 次试验，完整模型报告的成功率为 90%、90%、85%、70% 和 90%，并在 Make Breakfast 和 Assemble Equation 上比 π0.5 高 10 个百分点。
- 消融实验显示，逆向 CoT 的贡献最大：移除它会使真实世界平均成功率从 85.0% 降至 70.0%；移除正向 CoT 会使成功率下降 6 个百分点。
- 与跳过 Stage 2 相比，Stage 2 端到端预训练使 50-demo 设置下的成功率在 Hang Cup 上提高 5 个百分点，在 Place Cubes 上提高 25 个百分点，在 Assemble Equation 上提高 50 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17937v1](https://arxiv.org/abs/2606.17937v1)
