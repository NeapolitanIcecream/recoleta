---
source: arxiv
url: https://arxiv.org/abs/2606.29908v1
published_at: '2026-06-29T07:43:47'
authors:
- Hong Chen
- Daqi Liu
- Zehan Zhang
- Haiguang Wang
- Tianhao Lu
- Longfei Yan
- Haiyang Sun
- Fangzhen Li
- Hongwei Xie
- Bing Wang
- Guang Chen
- Hangjun Ye
- Yihua Tan
topics:
- embodied-navigation
- world-action-model
- visual-navigation
- diffusion-world-model
- goal-conditioned-navigation
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Pondering the Way: Spatial-perceiving World Action Model for Embodied Navigation

## Summary
## 摘要
SWAM 是一种目标条件导航模型，可从起点和目标 RGB 图像出发，在一次扩散过程中同时预测路径和视觉路线。它降低了候选轨迹展开成本，并在 RECON、SCAND 和 TartanDrive 上提高了轨迹准确性。

## 问题
- 视觉导航需要让动作同时匹配目标图像和可通行空间；错误可能让机器人走向不可行路径。
- 两阶段世界模型规划器会采样候选动作、渲染展开轨迹并排序，因此质量取决于候选覆盖范围，运行时间也会随样本数量增加而增长。
- 仅用 RGB 进行预测可能遗漏几何信息，导致视角跳变、尺度漂移和最终位置准确性较弱。

## 方法
- SWAM 微调 CogVideoX Diffusion Transformer，对一个组合 token 序列进行去噪，该序列包含未来 RGB 潜变量、深度潜变量和 2D 动作 token。
- 模型以起点和目标观测为条件。DepthAnything v3 在训练期间提供深度伪标签；推理时只需要单目 RGB。
- Visual-Guided Action Refinement 在解码动作前，使用从生成的 RGB-D token 到动作 token 的交叉注意力。
- Trajectory-Scale Regularization 监督积分后的终点位移，减少不同路径长度下的长时域漂移。

## 结果
- 在 RECON 上，ATE 从 NWM+NoMaD x16 的 1.53 降至 0.93，降低 39.2%；RPE 为 0.43，而对方为 0.49。
- 在 SCAND 上，ATE 从 NWM+NoMaD x16 的 2.18 降至 1.15，降低 47.2%；RPE 为 0.34，而对方为 0.46。
- 在 TartanDrive 上，ATE 从 NWM+NoMaD x16 的 6.23 降至 1.55，降低 75.1%；RPE 为 0.68，而对方为 1.30。
- SWAM 每个 episode 用时 16.91 秒，NWM+NoMaD x16 为 245.98 秒；直接策略更快，GNM 为 0.12 秒，NoMaD 为 0.21 秒，但轨迹误差更高。
- 在 RECON 的 success@0.25 指标上，SWAM 报告的成功率为 NWM+NoMaD x16 的 2.1 倍；摘录未提供绝对成功率数值。
- 在 TartanDrive 的视频生成任务上，SWAM 报告 PSNR 为 18.11，SSIM 为 0.532；摘录称其在所评估数据集上结果最佳，但完整对比表已被截断。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.29908v1](https://arxiv.org/abs/2606.29908v1)
