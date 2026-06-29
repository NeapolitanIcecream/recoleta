---
kind: trend
trend_doc_id: 553
granularity: week
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-08T00:00:00'
topics:
- robotics
- vision-language-action
- 3D grounding
- world models
- policy evaluation
- action representation
- robot adaptation
run_id: materialize-outputs
aliases:
- recoleta-trend-553
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/3d-grounding
- topic/world-models
- topic/policy-evaluation
- topic/action-representation
- topic/robot-adaptation
language_code: zh-CN
---

# 机器人 VLA 进展正由可执行控制来衡量

## Overview
本周，机器人 Vision-Language-Action (VLA) 工作按可执行控制来评判。最有力的证据把性能收益与 3D 锚定、闭环世界模型，以及能降低真实机器人误差的动作头联系起来。Dex-BEV、PiL-World 和 ActionMap 在基准和硬件上都显示了这一模式。

## Clusters

### VLA 操作中的 3D 锚定
空间对齐是主要的性能杠杆。Dex-BEV 将视觉几何、本体感知和输出动作放入共享的鸟瞰视角坐标系。它在官方 LIBERO 上报告 97.8% 的平均成功率，在 RoboTwin 2.0 Clean 上为 76.0%，在修改了相机和姿态设置的 LIBERO 上为 89.9%，而列出的 2D 基线低于 10%。

GeoAlign 加入由 RGB 推导的几何特征，并由机器人状态进行查询。收益在几何敏感任务上最清楚：真实 ALOHA 的平均成功率为 78.8%，RGB-only 基线为 65.0%；透明瓶任务成功率为 75.0%，RGB-only 为 35.0%。3DThinkVLA 采用更轻的部署路线。它训练潜在 3D 感知和推理适配器，推理时仍使用 2D 图像，同时在 LIBERO 上达到 98.7%，在 LIBERO-PLUS 上达到 81.0%。

#### Evidence
- [Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning](../Inbox/2026-06-01--dexterity-bev-aligning-3d-world-and-actions-for-generalizable-robot-policies-learning.md): Dex-BEV 结果以及共享 3D/BEV 对齐设计。
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): GeoAlign 的几何条件 VLA 设计，以及 LIBERO、SimplerEnv、真实 ALOHA 结果。
- [3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training](../Inbox/2026-06-03--3dthinkvla-endowing-vision-language-action-models-with-latent-3d-priors-via-3d-thinking-guided-co-training.md): 3DThinkVLA 的潜在 3D 训练方法以及 LIBERO/LIBERO-PLUS 结果。

### 用于控制和策略评估的世界模型
World Action Models (WAMs) 正通过其对动作选择、延迟和真实 rollout 一致性的影响来测试。GeoSem-WAM 训练未来 RGB、几何和语义预测头，然后在部署时移除这些头。报告的结果有实际意义：在 LIBERO 上平均成功率为 98.55%，在真实 Franka 任务上平均成功率为 95.4%，Fast-WAM 为 88.9%。

PiL-World 使用策略在环设置。冻结的 VLA 预测一个动作块，世界模型预测下一步多视角观测，生成的观测再作为下一次策略输入。在三个真实双臂任务中，它将真实成功率与想象成功率之间的平均差距降至 12.0%，Ctrl-World 为 63.2%；它还报告真实成功率和想象成功率之间的 Pearson 相关系数为 0.94。

#### Evidence
- [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](../Inbox/2026-06-02--geosem-wam-geometry-and-semantic-aware-world-action-models.md): GeoSem-WAM 的结构化未来预测目标、部署设计以及 LIBERO/Franka 结果。
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): PiL-World 的闭环想象 rollout 方法，以及真实成功率与想象成功率的一致性。

### 动作头和适配器作为部署杠杆
几篇论文通过改变动作接口或适配路线来改善策略行为，同时基本保持主 VLA 不变。ActionMap 用覆盖平移、旋转和夹爪命令的体素热力图替代单点动作解码。在使用 OpenVLA-OFT 的 LIBERO 上，在相同训练步数下，它达到 97.3% 的平均成功率，L1 回归为 89.1%。在真实 Franka 任务上，它在 30 次试验中成功 20 次，回归头为 30 次中成功 7 次。

WIZARD 面向任务适配。它根据语言指令和一段短演示视频预测任务特定的 LoRA 权重，然后用生成的适配器运行冻结的 VLA。在留出的 LIBERO-Spatial 上，它达到 0.40 的平均成功率，列出的最强多任务 VLA 基线为 0.19，最近邻适配器检索为 0.02。它与任务特定专家之间仍有较大差距，但证据显示，适配速度和数据需求已经成为控制性能评估的一部分。

#### Evidence
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): ActionMap 的体素热力图动作头、LIBERO 收益、低数据结果和真实 Franka 试验。
- [Robotic Policy Adaptation via Weight-Space Meta-Learning](../Inbox/2026-06-05--robotic-policy-adaptation-via-weight-space-meta-learning.md): WIZARD 生成 LoRA 的适配方法以及留出 LIBERO 结果。
