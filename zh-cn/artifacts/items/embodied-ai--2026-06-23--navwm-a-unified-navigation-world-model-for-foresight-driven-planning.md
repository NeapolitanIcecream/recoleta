---
source: arxiv
url: https://arxiv.org/abs/2606.24101v1
published_at: '2026-06-23T03:30:20'
authors:
- Yanghong Mei
- Longteng Guo
- Ming-Ming Yu
- Guiyu Zhao
- Xingjian He
- Jing Liu
topics:
- world-model
- visual-navigation
- robot-planning
- multimodal-trajectory-prediction
- visual-foresight
- image-goal-navigation
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# NavWM: A Unified Navigation World Model for Foresight-Driven Planning

## Summary
## 摘要
NavWM 是一种导航世界模型，使用预测的未来图像在多条候选机器人路径中做选择。论文报告称，相比先前的视觉导航和世界模型基线，它在轨迹预测、未来帧生成和图像目标导航上表现更好。

## 问题
- 视觉导航策略可能做出短视动作，因为它们把相机输入直接映射为动作，没有测试可能的未来状态。
- 现有导航世界模型常把感知、动作预测和未来图像生成拆成独立部分，可能浪费共享的空间和时间信息。
- 单轨迹动作预测可能收敛到一条路径，即使存在多条安全路线也如此；这对杂乱的室内和室外机器人导航很重要。

## 方法
- NavWM 输入过去的 RGB 帧、当前帧和目标图像，然后预测多条未来轨迹以及这些轨迹对应的未来观测。
- Bidirectional Mamba 主干在共享潜在空间中编码视觉历史和目标输入。
- 可学习的潜在世界 token 使用来自 Depth Anything V2 和 SAM 的伪标签训练，为模型提供用于规划的深度和语义线索。
- 基于锚点的轨迹头预测多个候选目标点和路点序列，而不是只预测一条路径。
- 带流匹配的 Conditional Diffusion Transformer 根据候选动作生成未来视觉观测，因此规划器可以通过视觉前瞻为路径打分。

## 结果
- 在 Go Stanford、SCAND、RECON 和 HuRoN 上的离线轨迹预测相比 UniWM 有提升：ATE 从 0.302 降至 0.207，RPE 从 0.116 降至 0.066，AOE 从 9.468 降至 8.152，MAOE 从 13.221 降至 12.855。
- 未来图像生成优于 NWM 和 UniWM：PSNR 达到 17.340，而 NWM 为 14.343，UniWM 为 14.172。
- NavWM 报告的 SSIM 为 0.507，LPIPS 为 0.243，DreamSim 为 0.084；列出的最接近基线分别是 UniWM 的 SSIM 0.435、UniWM 的 LPIPS 0.282，以及 NWM 的 DreamSim 0.091。
- 在图像目标导航 rollout 中，论文报告称已见环境中的成功率从 66% 升至 72%。
- 在未见环境的零样本推理中，包括把 TartanDrive 作为留出测试平台，论文报告的导航成功率为 44%。
- 默认模型有 1.5B 参数，使用 4 个过去帧预测接下来的 4 帧，并训练 100,000 个教师强制步骤，再在预测轨迹上进行 50,000 个微调步骤。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24101v1](https://arxiv.org/abs/2606.24101v1)
