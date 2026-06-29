---
source: arxiv
url: https://arxiv.org/abs/2606.04463v1
published_at: '2026-06-03T05:16:41'
authors:
- Zhuoyuan Wu
- Jun Gao
topics:
- world-model
- vision-language-action
- robot-policy-evaluation
- cross-embodiment
- robot-data-scaling
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# OSCAR: Omni-Embodiment Skeleton-Conditioned World Action Model for Robotics

## Summary
## 总结
OSCAR 是一个 20 亿参数的动作条件视频世界模型，用于跨机械臂和人手的机器人策略评估。它把 2D 骨架渲染作为动作输入，让生成器获得空间运动线索，同时不把条件绑定到某一种机器人的外观上。

## 问题
- 在真实硬件上评估机器人策略速度慢、成本高，而且很难大规模重复，所以一个有用的视频世界模型可以在部署前筛选策略。
- 现有的动作条件视频模型往往无法精确遵循帧级和像素级动作，这削弱了它们作为评估代理的价值。
- 许多模型只在窄范围的机器人数据集上训练，或者使用只适用于特定本体的动作编码，这限制了它们在 Franka Panda、KUKA iiwa、AgiBot G1、Toyota HSR 和人手之间的迁移能力。

## 方法
- OSCAR 在一个初始 RGB 帧和完整的 2D 运动骨架渲染序列上微调 Cosmos-Predict2.5-2B。
- 骨架条件的构建方式是把机器人 URDF 连接点或 MANO 手部关节投影到相机视角中，再在黑色画布上画出连线和关节点。
- 骨架视频先通过 WAN 2.1 VAE 编码，变成 token，然后在去噪过程中加到扩散 Transformer 里的带噪视频 token 上。
- 训练流程会整理、过滤、去重并标注机器人和第一视角人类视频，最终从 2,165,359 个公开源 episode 中保留 180,657 个 episode。
- 训练分两阶段进行：先在四种机器人本体上迭代 15k 次，然后在混合的机器人和人类数据集上继续训练，使用单个 NVIDIA GH200 GPU。

## 结果
- 在一个覆盖四种本体的 200 段视频基准上，OSCAR 的 PSNR 达到 24.24，SSIM 达到 0.846，高于 Genie Envisioner 的 23.29 PSNR 和 0.838 SSIM。
- OSCAR 的 LPIPS 为 0.094，FVD 为 7.08，FID 为 15.07，latent L2 为 0.096；下一个最强的列出基线分别是 LPIPS 0.140、FVD 15.37、FID 22.92、latent L2 0.129。
- 在报告的 GH200 测试中，OSCAR 的速度为 2.214 FPS；Kinema4D 为 0.089 FPS，Genie Envisioner 为 1.382 FPS。
- 该模型参数量为 20 亿，在表格指标上优于 140 亿参数的 Kinema4D：PSNR 24.24 对 17.68，SSIM 0.846 对 0.741，FVD 7.08 对 17.07，FID 15.07 对 37.16。
- 消融结果显示，在仅机器人数据上使用骨架条件时，效果接近网格渲染：PSNR 23.48 对 23.11，SSIM 0.832 对 0.831，FVD 7.69 对 7.89。
- 在机器人-only 预热的基础上加入人类数据，会优于仅用机器人骨架训练：PSNR 24.24 对 23.48，SSIM 0.846 对 0.832，FVD 7.08 对 7.69，FID 15.07 对 16.37。摘要声称它与 RoboArena 的真实世界策略评估有很强相关性，但没有给出相关系数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04463v1](https://arxiv.org/abs/2606.04463v1)
