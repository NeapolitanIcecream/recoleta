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
## 总结
RotVLA 是一个 17 亿参数的视觉-语言-动作模型，用连续的 SO(n) 潜在动作代替离散的潜在动作 token。它在 LIBERO 和 RoboTwin2.0 上报告了接近或达到最优的成功率，同时使用了超过 1700 小时的机器人和人类视频进行训练。

## 问题
- VLA 预训练需要混合来自不同机器人本体的数据和未标注的人类视频，而这些动作标签不共享同一个原生动作空间。
- 现有的潜在动作模型常把动作量化为离散 token，这会丢失连续运动细节，并限制动作组合。
- 基于重建的潜在动作训练可能学到捷径，把目标帧编码进去，而不是编码帧与帧之间的运动，这会削弱向机器人控制的迁移。

## 方法
- RotVLA 把两帧之间的转移编码为 SO(n) 中的连续旋转矩阵，实验里 n 设为 16。
- 潜在动作模型使用 SoftVQ，然后通过 SVD 把预测矩阵投影到最近的有效旋转矩阵，得到一种基于连续码本的动作表示。
- 三元组训练损失使用 t、t+1 和 t+2 三帧：先学习两个一步潜在动作，再把它们相乘组成一个两步潜在动作，并训练解码器用这个组合动作重建第三帧。
- 这个 VLA 模型使用 InternVL3.5-1B 和一个 24 层 DiT 动作头，通过 flow matching 训练，从视觉和语言中预测潜在动作。
- 在机器人微调阶段，一个 flow matching 动作头联合去噪潜在动作和机器人动作；机器人动作 token 可以关注潜在动作 token，因此潜在动作会引导控制。

## 结果
- 预训练使用了来自 Open X-Embodiment、AGIBOT-beta、RoboMIND、RoboCOIN 和 Ego4D 的 1700 多小时数据；完整模型约有 17 亿参数。
- 在 LIBERO 上，RotVLA 报告的平均成功率是 98.2%：Spatial 98.2、Object 99.6、Goal 98.4、Long 96.4。表中 X-VLA 的平均值是 98.1，OpenVLA-OFT 是 97.1，GR00T-N1.6 是 97.0，UniVLA 是 95.4。
- 在 RoboTwin2.0 上，RotVLA 在干净设置下的成功率是 89.6%，在随机化设置下是 88.5%。表中最接近的基线是 StarVLA 的 88.2/88.3、Motus 的 88.7/87.0，以及 LingBot-VLA 的 88.6/86.7。
- 在真实的 ARX R5 任务上，论文在两个单臂任务中报告了超过 90% 的成功率，并且在双臂杯子堆叠任务上的失败率低于 pi_0.5，使用的是每个任务 100 次示范。
- 推理延迟报告为在 NVIDIA H20 服务器上每步 79 ms，而 pi_0.5 为每步 61 ms。
- 三元组潜在动作训练的重建间隔指标大于仅重建训练：表 2 中 Delta 为 0.0048 对 0.0037，下一帧 MSE 为 0.0030 对 0.0029，想象帧 MSE 为 0.0078 对 0.0066。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13403v1](https://arxiv.org/abs/2605.13403v1)
