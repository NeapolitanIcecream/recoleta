---
source: arxiv
url: https://arxiv.org/abs/2604.26694v2
published_at: '2026-04-29T14:01:54'
authors:
- Jun Guo
- Qiwei Li
- Peiyan Li
- Zilong Chen
- Nan Sun
- Yifei Su
- Heyun Wang
- Yuan Zhang
- Xinghang Li
- Huaping Liu
topics:
- world-action-model
- robot-foundation-model
- vision-language-action
- 4d-reconstruction
- asynchronous-denoising
- robot-data-scaling
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising

## Summary
## 摘要
X-WAM 是一个机器人世界-动作模型，用一个扩散模型预测未来多视角 RGB-D 视频、3D 结构、机器人状态和动作。它的主要主张是，加入深度预测和异步去噪可以同时提高策略成功率和 4D 世界生成质量。

## 问题
- 现有统一世界-动作模型大多预测 2D 视频和动作，因此缺少可用于操作和重建的直接 3D 几何信息。
- 高质量视频扩散需要很多去噪步，而机器人动作可以用更少步数解码；使用同一调度会浪费控制时间。
- 这个问题重要，因为机器人策略需要快速动作来进行闭环控制，也需要空间预测来处理接触密集型操作。

## 方法
- X-WAM 在多视角机器人数据上微调 Wan2.2-TI2V-5B，这是一个预训练视频 Diffusion Transformer。
- 模型接收语言指令、初始 RGB 视图和本体感知状态，然后预测 8 个未来 RGB 帧、8 个未来状态和 32 个未来动作。
- 深度分支复制最后几个 DiT 块，并通过交叉注意力读取 RGB 特征，在不把 token 序列加倍的情况下生成深度。
- Asynchronous Noise Sampling 用比视频更少的去噪步解码动作；训练时从耦合分布中采样视频和动作噪声水平，使训练调度与推理匹配。
- 模型使用超过 5,800 小时的真实和仿真机器人数据训练，采用共享的末端执行器位姿和夹爪动作格式。

## 结果
- 在 RoboCasa 上，X-WAM 报告了 24 个任务的平均成功率为 79.2%，Cosmos Policy 为 67.1%，提升 12.1 个百分点。
- 在 RoboTwin 2.0 Clean 上，它报告的成功率为 89.8%，Motus 为 88.7%，提升 1.1 个百分点。
- 在 RoboTwin 2.0 Randomized 上，它报告的成功率为 90.7%，Motus 为 87.0%，提升 3.7 个百分点。
- 在预测方面，论文评估了 PSNR、SSIM、LPIPS、AbsRel、δ1 和 Chamfer Distance，并称其视觉和几何指标优于现有方法；摘录中未包含这些指标值。
- 论文还称在双臂耳机包装任务上进行了真实世界部署，但摘录没有提供该实验的成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26694v2](https://arxiv.org/abs/2604.26694v2)
