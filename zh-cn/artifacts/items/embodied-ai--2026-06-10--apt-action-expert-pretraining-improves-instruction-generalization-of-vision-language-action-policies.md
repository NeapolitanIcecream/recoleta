---
source: arxiv
url: https://arxiv.org/abs/2606.12366v1
published_at: '2026-06-10T17:34:25'
authors:
- Kechun Xu
- Zhenjie Zhu
- Anzhe Chen
- Rong Xiong
- Yue Wang
topics:
- vision-language-action
- robot-foundation-model
- action-expert-pretraining
- instruction-generalization
- manipulation
- sim2real
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies

## Summary
## 总结
APT 在为视觉-语言-动作机器人策略加入语言条件之前，先对连续动作专家进行预训练。论文声称，这样能提升在模拟环境和真实机器人操作中的分布外指令跟随能力。

## 问题
- 连续动作 VLA 策略常常学到视觉捷径，因为每条轨迹里有很多视觉-动作帧，但只有一个语言指令。
- 随机初始化的动作专家会把噪声梯度传回预训练 VLM，从而削弱模型的语言行为。
- 这会影响机器人策略对改写表达、新物体名称和组合指令的跟随能力，而不是记住任务标签。

## 方法
- 该方法把策略分解为视觉-动作先验 π(a|v) 和语言条件化的 VLA 似然，因此动作模型先只从图像和动作中学习操作。
- 第 1 阶段冻结 VLM，在遮蔽语言的视觉-动作对上训练基于扩散的动作专家。
- 第 2 阶段注入语言 token，训练完整的 VLA 策略，让预训练的动作分布受指令引导。
- 动作专家使用 Transformer 自注意力，处理视觉、语言、本体感觉、动作历史和噪声动作 token。
- 分层门控融合把中间的 Qwen3-VL 特征加入动作专家层，学习到的门控控制有多少 VLM 信息进入。

## 结果
- 在 LIBERO-PRO 上，OpenVLA 和 π0 的平均成功率都是 0%，π0.5 为 11%，LangForce 为 14%，APT 为 19%，加入 VLM 微调后的 APT 为 27%。
- 在 LIBERO-PRO Spatial 上，加入 VLM 微调后的 APT 在 Pos 上达到 62%，在 Task 上达到 62%；π0.5 分别是 20% 和 1%。
- 在刚性物体抓取放置任务上，π0.5 的 SO、UO、UC 和 UOUE 分别为 84%、70%、86% 和 50%；加入两阶段训练和 VLM 微调后的 APT 分别为 98%、84%、92% 和 58%。
- 结合知识隔离和两阶段训练的 APT 变体在只使用 VLA 数据、且不进行 VL 推理共训练的情况下，SO、UO、UC 和 UOUE 分别为 96%、74%、90% 和 62%。
- 论文报告说，两阶段动作预训练能提升 π 风格和 GR00T 风格架构在几乎所有测试设置中的表现，但摘要里只在图中给出了详细数值。
- 真实世界实验中，每个策略都用每个任务 30 个示范进行微调，并包含单任务和组合泛化；摘要没有给出最终真实世界成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12366v1](https://arxiv.org/abs/2606.12366v1)
