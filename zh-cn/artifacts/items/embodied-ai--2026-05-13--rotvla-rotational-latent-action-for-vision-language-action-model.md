---
source: arxiv
url: https://arxiv.org/abs/2605.13403v1
published_at: '2026-05-13T11:58:02'
authors:
- Qiwei Li
- Xicheng Gong
- Xinghang Li
- Peiyan Li
- Quanyun Zhou
- Hangjun Ye
- Jiahuan Zhou
- Yadong Mu
topics:
- vision-language-action
- latent-actions
- robot-foundation-model
- cross-embodiment-learning
- flow-matching
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# RotVLA: Rotational Latent Action for Vision-Language-Action Model

## Summary
## 摘要
RotVLA 是一个 1.7B 参数的视觉-语言-动作模型，使用连续的 SO(n) 潜在动作，而不是离散的潜在动作 token。它在 LIBERO 和 RoboTwin2.0 上报告了最高或接近最高的成功率，训练数据超过 1700 小时，来自机器人和人类视频。

## 问题
- VLA 预训练需要混合不同本体的机器人数据集和无标注人类视频，而这些动作标签没有共享的原生动作空间。
- 现有潜在动作模型常把动作量化为离散 token，这可能丢失连续运动细节，并限制动作组合能力。
- 基于重建的潜在动作训练可能学到捷径，编码目标帧而非帧间运动，从而削弱向机器人控制的迁移能力。

## 方法
- RotVLA 将两帧之间的转变编码为 SO(n) 中的连续旋转矩阵，实验中 n 设为 16。
- 潜在动作模型使用 SoftVQ，然后用 SVD 将预测矩阵投影到最近的有效旋转矩阵，得到基于连续码本的动作表示。
- 三元组训练损失使用 t、t+1 和 t+2 三帧：模型学习两个单步潜在动作，将它们相乘形成两步潜在动作，并训练解码器用组合后的动作重建第三帧。
- VLA 模型使用 InternVL3.5-1B 加一个 24 层 DiT 动作头，并用流匹配训练，使其根据视觉和语言预测潜在动作。
- 在机器人微调期间，一个流匹配动作头联合去噪潜在动作和机器人动作；机器人动作 token 可以关注潜在动作 token，因此潜在动作会引导控制。

## 结果
- 预训练使用来自 Open X-Embodiment、AGIBOT-beta、RoboMIND、RoboCOIN 和 Ego4D 的超过 1700 小时数据；完整模型约有 1.7B 参数。
- 在 LIBERO 上，RotVLA 报告的平均成功率为 98.2%：Spatial 98.2、Object 99.6、Goal 98.4、Long 96.4。表中 X-VLA 的平均值为 98.1，OpenVLA-OFT 为 97.1，GR00T-N1.6 为 97.0，UniVLA 为 95.4。
- 在 RoboTwin2.0 上，RotVLA 在 clean 设置中报告 89.6% 成功率，在 randomized 设置中报告 88.5%。表中最接近的基线是 StarVLA 的 88.2/88.3、Motus 的 88.7/87.0，以及 LingBot-VLA 的 88.6/86.7。
- 在真实 ARX R5 任务上，论文报告两个单臂任务的成功率超过 90%，并且在双臂叠杯任务上的失败次数低于 pi_0.5；每个任务使用 100 个演示。
- 推理延迟报告为在 NVIDIA H20 服务器上每步 79 ms，相比之下 pi_0.5 为每步 61 ms。
- 三元组潜在动作训练的重建差距指标大于仅重建训练：表 2 中 Delta 为 0.0048 对 0.0037，下一帧 MSE 为 0.0030 对 0.0029，想象帧 MSE 为 0.0078 对 0.0066。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13403v1](https://arxiv.org/abs/2605.13403v1)
