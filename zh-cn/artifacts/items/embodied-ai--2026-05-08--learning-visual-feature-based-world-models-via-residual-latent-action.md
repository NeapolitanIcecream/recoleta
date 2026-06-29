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
## 总结
RLA-WM 通过生成紧凑的残差潜在动作，再用当前 DINO 特征解码未来的机器人视觉特征。论文称，它在预测精度上优于 DINO token 回归、直接特征空间生成和视频扩散，同时计算量远低于视频扩散。

## 问题
- 机器人世界模型常直接预测视频像素，这种做法代价高，而且可能生成视觉上清晰但物理上错误的未来画面。
- DINO-WM 这类基于特征的世界模型计算更便宜，但在复杂的三维操作中，直接回归会让预测变模糊或塌缩。
- 这个问题很关键，因为有用的机器人世界模型应当支持从离线机器人视频中学习策略，包括没有动作标注的视频。

## 方法
- 该方法把两个 DINO token 状态之间的残差 `s_{t+h} - s_t` 编码成一个紧凑潜在向量，称为 Residual Latent Action，简称 RLA。
- RLA 解码器在一次前向传播中，用当前 token `s_t` 和潜变量 `z` 重建未来的 DINO token `s_{t+h}`。
- RLA-WM 在当前 DINO token 和一个动作块条件下，用 flow matching 预测 `z`，再把预测出的潜变量解码成未来的 DINO token。
- 该模型把迭代式生成步骤放在较小的 RLA 空间里，而不是更大的 DINO token 空间。论文给了一个规模例子：512×512 图像大约有 16k 个 Stable Diffusion VAE 潜在维度，而 DINOv3-L token 大约有 100 万维度。
- 论文还把 RLA 用在两种策略学习设置中：一种是部分使用无动作视频训练的轻量级 world action model，另一种是在离线训练的 RLA-WM 内部完成的视觉强化学习。

## 结果
- 在 ManiSkill 的未来帧预测上，RLA-WM 报告 LPIPS 0.071、SSIM 0.931、DINO L1 0.030。列表中的最强基线是 FM-WM，LPIPS 0.127、SSIM 0.890、DINO L1 0.063；DINO-WM 为 0.156、0.865、0.078。
- 在真实世界的 IWS 数据集上，RLA-WM 报告 LPIPS 0.196、SSIM 0.847、DINO L1 0.053。DINO-WM 报告 0.223、0.825、0.058，FM-WM 报告 0.360、0.741、0.119。
- 单次推理的计算量分别为：RLA-WM 3.5T FLOPs，DINO-WM 2.1T，RAE 和 FM-WM 14.3T，Vid2World 1.1P。
- 在无动作视频模仿学习中，RLA world action model 在 5 个 ManiSkill 任务上的平均成功率为 35.6%，BC-ResNet 为 27.2%，DINO CLS 为 27.4%，UniVLA 为 28.7%，AdaWorld 为 33.7%。
- 在同一设置下的 PushT 上，RLA 的成功率为 15.2%，BC-ResNet 为 3.6%，AdaWorld 为 9.2%。
- 论文中用于预测的训练数据包括：每个 ManiSkill 任务 1,000 个成功 episode 和 500 个失败 episode、每个机器人 3,000 个 play video，以及每个选定的 IWS 任务超过 600 个人工遥操作 demo。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07079v1](https://arxiv.org/abs/2605.07079v1)
