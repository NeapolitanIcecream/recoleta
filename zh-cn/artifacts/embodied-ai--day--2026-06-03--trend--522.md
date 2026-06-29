---
kind: trend
trend_doc_id: 522
granularity: day
period_start: '2026-06-03T00:00:00'
period_end: '2026-06-04T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- 3D geometry
- tactile sensing
- quadrotor navigation
run_id: materialize-outputs
aliases:
- recoleta-trend-522
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/3d-geometry
- topic/tactile-sensing
- topic/quadrotor-navigation
language_code: zh-CN
---

# 机器人策略工作正在接受几何、接触和真实执行的检验

## Overview
机器人占据了当天的主要内容，策略质量被当作执行问题来检验。最强的论文在部署前加入几何、物理验证、成功评分或空间记忆。OSCAR、3DThinkVLA 和 MAD 提供了最清楚的证据。

## Clusters

### Geometry-guided VLA policies
视觉-语言-动作（VLA）论文围绕那些让动作具有物理意义的信号展开。3DThinkVLA 将 Qwen3-VL 的视觉特征与 VGGT 3D 特征对齐，并把一个空间推理锚点蒸馏到普通动作提示中。它在 LIBERO 上的平均成功率为 98.7%，在 LIBERO-PLUS 上为 81.0%，推理时只用 2D 图像。

VISTA 处理的是同一问题的数据侧。它通过在 800 万样本的鱼眼 VQA 集上训练，并按完整性、连续性、自碰撞风险和执行保真度筛选轨迹，来适配 Universal Manipulation Interface（UMI）演示数据。ForesightFlow 提供了一条更轻的策略改进路径：每个动作块都带有生成的成功潜力分数，从而可以直接做 best-of-K 选择，不需要单独的 critic。它在真实世界双臂任务上的成功率是 35.4%，高于 IDQL 的 32.6%，训练计算量从 287 个 GPU 小时降到 178 个 GPU 小时。

#### Evidence
- [3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training](../Inbox/2026-06-03--3dthinkvla-endowing-vision-language-action-models-with-latent-3d-priors-via-3d-thinking-guided-co-training.md): 3DThinkVLA method and LIBERO/LIBERO-PLUS results.
- [VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training](../Inbox/2026-06-03--vista-vision-grounded-and-physics-validated-adaptation-of-umi-data-for-vla-training.md): VISTA fisheye VQA data, physical validation, and UMI adaptation.
- [Potential-Guided Flow Matching for Vision-Language-Action Policy Improvement](../Inbox/2026-06-03--potential-guided-flow-matching-for-vision-language-action-policy-improvement.md): ForesightFlow success-potential scoring, real-world results, and compute comparison.

### World models for policy evaluation and spatial memory
世界模型工作和可衡量的控制结果直接相关。OSCAR 把 2D 运动骨架视频当作动作条件，用在一个 20 亿参数的视频世界模型上，覆盖机器人机械臂和人手。在一个 200 个片段的基准上，它的 PSNR 达到 24.24，SSIM 达到 0.846，在报告的 GH200 测试中运行速度为 2.214 FPS。

MAD 把类似的预测思路用于四旋翼，训练一个 DreamerV3 风格的循环模型来预测局部占用图和可见性图。学到的策略在仿真中达到 9.66 m/s，在真实森林飞行中达到 5.05 m/s。另一项四旋翼研究给出一个警示：仿真策略分数最高的模型在真实平台上失败了，而其他模型通过狭窄缝隙到达了目标。作者认为，跨环境重建质量比单纯的仿真胜率更能反映真实迁移效果。

#### Evidence
- [OSCAR: Omni-Embodiment Skeleton-Conditioned World Action Model for Robotics](../Inbox/2026-06-03--oscar-omni-embodiment-skeleton-conditioned-world-action-model-for-robotics.md): OSCAR skeleton-conditioned world model, benchmark metrics, speed, and embodiment coverage.
- [MAD: Mapping-Aware World Models for Agile Quadrotor Flight](../Inbox/2026-06-03--mad-mapping-aware-world-models-for-agile-quadrotor-flight.md): MAD mapping-aware world model and quadrotor deployment results.
- [Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation](../Inbox/2026-06-03--generalization-of-world-models-under-environmental-variability-for-vision-based-quadrotor-navigation.md): Quadrotor world-model generalization study and simulation-to-real findings.

### Contact-rich data exposes limits of vision-only manipulation
HapTile 把触觉和操作者反馈加入 VLA 数据混合中。这个数据集包含 1,726 次演示，覆盖 38 个任务和 9 种技能，包含语言、第三人称 RGB、腕部 RGB、指尖触觉图像、机器人状态、7D 动作、时间戳，以及 15 Hz 的触觉反馈。最明显的提升出现在接触决定成败的任务上：在 π0 上，插销插入从只用视觉输入时的 0% 升到用原始触觉图像时的 90%；白板擦拭在加入触觉标记特征后从 50% 升到 100%。

结果并不完全一致。报告中的基线在加入触觉标记特征后，倒液性能变差。这让这个数据集更像一个诊断工具：触觉对一些重接触任务有帮助，但策略架构仍然需要更好的方式把触觉信号和视觉、语言输入结合起来。

#### Evidence
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](../Inbox/2026-06-03--haptile-a-haptic-informed-vision-tactile-language-action-dataset-for-contact-rich-imitation-learning.md): HapTile dataset contents, scale, tactile setup, and benchmark results.
