---
kind: ideas
granularity: week
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-08T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- 3D grounding
- world models
- policy evaluation
- action representation
- robot adaptation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/3d-grounding
- topic/world-models
- topic/policy-evaluation
- topic/action-representation
- topic/robot-adaptation
language_code: zh-CN
---

# 机器人策略接口校准

## 摘要
机器人 VLA 团队可以通过调整现有策略周围的控制接口和评估流程取得进展。最实用的做法包括：用于低数据操作调优的体素热图动作头、用于 VLA checkpoint 筛选的闭环世界模型，以及在混合机器人数据集训练前进行 3D 坐标对齐。

## 用于低数据操作微调的体素热图动作头
微小的末端执行器误差仍会决定许多操作 rollout 的成败。ActionMap 给 VLA 团队提供了一个可测试的改造方案：把原生连续动作解码器换成覆盖平移、旋转和夹爪命令的体素热图头，再用 top-k soft argmax 解码连续动作。

这个改造范围很小，可以放进现有 OpenVLA-OFT 或 pi0.5 训练运行中做消融。保持 backbone 和数据集不变，用动作网格上的高斯 blob 训练热图头，并把抓取位置误差和任务成功率同当前的 L1 头或 flow-matching 头比较。ActionMap 的结果支持这项检查：在 LIBERO 上配合 OpenVLA-OFT、训练步数相同的情况下，平均成功率从 89.1% 升到 97.3%。只用 43 条 LIBERO-Spatial 演示时，它达到 93.2%，L1 头为 67.2%。在真实 Franka 任务中，它完成 30 次试验中的 20 次，回归头为 30 次中的 7 次。

这个方案最适合受限于演示稀缺，或在抓取、扫动和插入中遇到毫米级偏差的团队。低成本验证方式是在当前策略上按任务替换动作头，不改 backbone，并在真实机器人上同时报告成功率和末端执行器误差。

### 资料来源
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): 概述 ActionMap 的即插式体素热图头、LIBERO 增益、低数据结果和真实 Franka 试验次数。
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): 确认该热图头直接替换现有 VLA 动作解码器，并报告训练步数匹配的 LIBERO 改进。

## 用于 VLA checkpoint 筛选的闭环世界模型评估
机器人评估团队可以在为每个 VLA checkpoint 投入硬件时间之前，加入一个闭环想象 rollout 阶段。PiL-World 给出了具体流程：冻结 VLA 策略，让它预测一个动作 chunk，用世界模型生成下一段同步多视角观测，把生成的末端观测再输入策略，然后重复。

它的运行价值是筛选 checkpoint。真实 rollout 很慢，因为需要安全执行、场景重置和重复试验。PiL-World 在三个真实双臂任务上，把想象成功率与真实成功率的平均差距从 Ctrl-World 的 63.2% 降到 12.0%，并报告了任务-checkpoint 设置中真实成功率与想象成功率之间 0.94 的 Pearson 相关系数。对于 40k 步 checkpoint 的 Stack Bowls，真实成功率为 96.7%，PiL-World 估计为 92.5%。

可行的采用路径是用目标工作单元中少量真实成功和失败轨迹校准世界模型，再用想象 rollout 排序 checkpoint 和任务变体。发布仍应以硬件试验为准，但筛选预算可以集中到那些闭环 rollout 能保持场景状态、夹爪运动和多视角一致性的 checkpoint 上。

### 资料来源
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): 概述 PiL-World 的 policy-in-the-loop 方法、训练输入、真实-想象成功率差距和相关性结果。
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): 确认需要观测-动作闭环测试，以及真实机器人评估的成本限制。

## 用于混合机器人操作数据集的 3D 坐标对齐预处理
如果团队要跨摄像头、机械臂和数据集约定训练一个 VLA，应加入一个预处理层，把观测、本体感知和输出动作表示到共享 3D 坐标系中。Dex-BEV 是最清晰的模板：在可用时用相机标定和深度把像素提升到 3D，把多视角几何投影到规范鸟瞰视角坐标系中，并在同一坐标系中表示动作。

痛点很具体。混合机器人数据包含不同的相机位姿、基座坐标系、动作约定和执行速度。Dex-BEV 在修改过相机和位姿设置的 LIBERO 上报告 89.9% 的平均成功率，而列出的 2D baseline 低于 10%。在 RoboTwin 2.0 Clean 上，它达到 76.0%，高于 64.8% 的 2D 消融。GeoAlign 为几何敏感任务提供了更轻的 rollout 变体：用机器人 RGB-D 数据对 RGB 几何分支做后训练，丢弃深度头，并让本体感知状态在动作生成期间查询几何特征。在真实 ALOHA 任务上，GeoAlign 报告 78.8% 的平均成功率，RGB-only baseline 为 65.0%；透明瓶任务为 75.0%，RGB-only 为 35.0%。

直接测试方式是建立一个相机位姿扰动套件，并加入少量透明、薄片或插入类任务。如果成功率主要在视角变化或局部几何需求下下降，应该先把 3D 对齐放进数据管线，再增加更多演示。

### 资料来源
- [Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning](../Inbox/2026-06-01--dexterity-bev-aligning-3d-world-and-actions-for-generalizable-robot-policies-learning.md): 概述 Dex-BEV 的共享 3D 坐标系、BEV 预处理、修改版 LIBERO 泛化和 RoboTwin 结果。
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): 概述 GeoAlign 的 RGB 派生几何特征、本体感知查询、真实 ALOHA 增益和透明物体结果。
