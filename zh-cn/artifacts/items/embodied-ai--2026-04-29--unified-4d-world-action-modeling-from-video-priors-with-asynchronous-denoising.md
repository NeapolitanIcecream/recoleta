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
X-WAM 是一个机器人世界-动作模型，把未来多视角 RGB-D 视频、3D 结构、机器人状态和动作放在一个扩散模型里预测。它的核心主张是，加入深度预测和异步去噪后，策略成功率和 4D 世界生成都会提升。

## 问题
- 现有统一的世界-动作模型大多只预测 2D 视频和动作，所以在操作和重建中缺少直接的 3D 几何信息。
- 高质量视频扩散需要很多去噪步数，而机器人动作可以用更少步数解码；两者共用同一调度会浪费控制时间。
- 这个问题重要，因为机器人策略需要快速动作来做闭环控制，也需要空间预测来支持接触丰富的操作。

## 方法
- X-WAM 在多视角机器人数据上微调了 Wan2.2-TI2V-5B，这是一种预训练的视频 Diffusion Transformer。
- 模型接收语言指令、初始 RGB 视图和本体感觉状态，然后预测 8 帧未来 RGB、8 个未来状态和 32 个未来动作。
- 深度分支复制了最后几层 DiT block，并通过 cross-attention 读取 RGB 特征，从而生成深度信息，而不会让 token 序列翻倍。
- 异步噪声采样在动作解码时使用比视频更少的去噪步数；训练时从耦合分布中采样视频和动作的噪声水平，让训练调度与推理一致。
- 模型在超过 5,800 小时的真实和仿真机器人数据上训练，使用统一的末端执行器位姿和夹爪动作格式。

## 结果
- 在 RoboCasa 上，X-WAM 报告 24 个任务的平均成功率为 79.2%，而 Cosmos Policy 为 67.1%，提升了 12.1 个百分点。
- 在 RoboTwin 2.0 Clean 上，它报告成功率为 89.8%，而 Motus 为 88.7%，提升了 1.1 个百分点。
- 在 RoboTwin 2.0 Randomized 上，它报告成功率为 90.7%，而 Motus 为 87.0%，提升了 3.7 个百分点。
- 在预测方面，论文评估了 PSNR、SSIM、LPIPS、AbsRel、δ1 和 Chamfer Distance，并声称在视觉和几何指标上优于现有方法；摘录里没有这些指标的具体数值。
- 论文还声称在双臂耳机包装任务上做了真实世界部署，但摘录里没有给出那项实验的成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26694v2](https://arxiv.org/abs/2604.26694v2)
