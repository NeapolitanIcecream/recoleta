---
source: arxiv
url: https://arxiv.org/abs/2605.07079v1
published_at: '2026-05-08T00:58:16'
authors:
- Xinyu Zhang
- Zhengtong Xu
- Yutian Tao
- Yeping Wang
- Yu She
- Abdeslam Boularias
topics:
- robot-world-model
- visual-feature-prediction
- latent-action
- flow-matching
- actionless-video-learning
- offline-robot-rl
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Visual Feature-Based World Models via Residual Latent Action

## Summary
## 摘要
RLA-WM 通过生成紧凑的残差潜在动作来预测机器人未来的视觉特征，然后用当前 DINO 特征对其解码。论文称，相比 DINO-token 回归、直接特征空间生成和视频扩散，该方法预测精度更高，计算量也远低于视频扩散。

## 问题
- 机器人世界模型常预测视频像素，这种方式成本高，并且可能生成视觉上清晰但物理上错误的未来状态。
- DINO-WM 等基于特征的世界模型成本更低，但直接回归在复杂 3D 操作中可能使预测变模糊或坍缩。
- 这个问题重要，因为有用的机器人世界模型应能支持从离线机器人视频中学习策略，包括没有动作标签的视频。

## 方法
- 该方法把两个 DINO token 状态之间的残差 `s_{t+h} - s_t` 编码成一个紧凑的潜在向量，称为 Residual Latent Action，即 RLA。
- RLA 解码器用当前 token `s_t` 和潜变量 `z`，通过一次前向传播重建未来 DINO token `s_{t+h}`。
- RLA-WM 在当前 DINO token 和一个动作块的条件下，用流匹配预测 `z`，然后把预测出的潜变量解码为未来 DINO token。
- 模型在较小的 RLA 空间中运行迭代生成步骤，而不是在大得多的 DINO token 空间中运行。论文给出一个规模示例：一张 512×512 图像约有 16k 个 Stable Diffusion VAE 潜在维度，而 DINOv3-L token 约有 1M 个维度。
- 论文还把 RLA 用于两个策略学习设置：一个部分使用无动作视频训练的轻量级世界动作模型，以及在离线训练的 RLA-WM 内进行的视觉 RL。

## 结果
- 在 ManiSkill 未来帧预测上，RLA-WM 报告的 LPIPS 为 0.071，SSIM 为 0.931，DINO L1 为 0.030。列出的最强基线为 FM-WM，其 LPIPS 为 0.127，SSIM 为 0.890，DINO L1 为 0.063；以及 DINO-WM，其三项数值为 0.156、0.865、0.078。
- 在真实世界 IWS 数据集上，RLA-WM 报告的 LPIPS 为 0.196，SSIM 为 0.847，DINO L1 为 0.053。DINO-WM 报告的三项数值为 0.223、0.825、0.058，FM-WM 报告的三项数值为 0.360、0.741、0.119。
- 每次推理的计算量为：RLA-WM 3.5T FLOPs，DINO-WM 2.1T，RAE 和 FM-WM 14.3T，Vid2World 1.1P。
- 在无动作视频模仿学习中，RLA 世界动作模型在 5 个 ManiSkill 任务上的平均成功率达到 35.6%，相比之下 BC-ResNet 为 27.2%，DINO CLS 为 27.4%，UniVLA 为 28.7%，AdaWorld 为 33.7%。
- 在相同设置下的 PushT 上，RLA 达到 15.2% 成功率，BC-ResNet 为 3.6%，AdaWorld 为 9.2%。
- 论文描述的预测训练数据包括每个 ManiSkill 任务 1,000 条成功 episode 和 500 条失败 episode、每个机器人 3,000 段 play 视频，以及每个选定 IWS 任务超过 600 条人类遥操作演示。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07079v1](https://arxiv.org/abs/2605.07079v1)
