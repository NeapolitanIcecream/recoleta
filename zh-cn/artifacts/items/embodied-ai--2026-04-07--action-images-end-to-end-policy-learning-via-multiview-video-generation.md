---
source: arxiv
url: http://arxiv.org/abs/2604.06168v2
published_at: '2026-04-07T17:59:30'
authors:
- Haoyu Zhen
- Zixian Gao
- Qiao Sun
- Yilin Zhao
- Yuncong Yang
- Yilun Du
- Pengsheng Guo
- Tsun-Hsuan Wang
- Yi-Ling Qiao
- Chuang Gan
topics:
- robot-policy-learning
- world-action-model
- multiview-video-generation
- pixel-grounded-actions
- zero-shot-robotics
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Action Images: End-to-End Policy Learning via Multiview Video Generation

## Summary
## 摘要
Action Images 将每个 7-DoF 动作转换为多视角像素空间视频，并训练一个视频模型同时生成未来观测和动作来学习机器人控制。论文称，这种方法不需要单独的 policy head，并能提升零样本机器人控制表现，尤其是在新视角和真实世界分布变化下。

## 问题
- 视频世界模型可以预测未来帧，但这并不能稳定地产生一种策略，使机器人在新环境中选择正确动作。
- 许多先前方法把动作放在单独模块中，或编码为与图像像素无关的潜在 token，因此预训练视频模型中的知识无法直接迁移到控制任务。
- 单一相机视角会让机器人的 3D 运动变得有歧义，从而影响从图像中恢复动作。

## 方法
- 将每个机器人动作 \((x,y,z,\text{orientation},\text{gripper})\) 转换为三个语义 3D 点：末端执行器位置、一个上方向点和一个法向点。
- 将这些点投影到每个相机视角，并渲染为 RGB 高斯热力图。蓝色通道还在低响应区域存储夹爪张开程度。这样得到一个与 RGB 机器人视频对齐的多视角动作视频。
- 在打包后的观测视频和动作视频 token 上训练一个预训练视频生成骨干网络（Wan 2.2），并用掩码支持视频-动作联合生成、动作条件视频生成、视频到动作标注和仅视频生成。
- 通过读取蓝色通道中的夹爪状态、将主视角中的热力图峰值结合侧视角匹配提升到 3D，并从恢复出的三个 3D 点重建位姿，将生成的动作图像解码回连续的 7-DoF 控制。
- 在 RLBench、DROID 和 BridgeV2 上训练，并使用相机条件和针对掩码潜在 token 的 flow-matching loss。

## 结果
- 在 RLBench 零样本任务上，该方法报告的成功率为：pick cup 30%、reach target 60%、close drawer 50%、close laptop 15%。
- 在真实世界零样本任务中，面对未见过的物体、环境和 xArm 机器人设置，该方法报告的结果为：Place Cup 40%、Pick Unseen Toy 20%、Pick Tissue 15%、Close Drawer 45%、Close Box 10%。
- 与表 2 中复现的基线相比，它在大多数列出的任务上优于 MV-Policy、pi_0.5、MolmoAct、TesserAct 和 Cosmos-Policy。例子包括：RLBench reach target 为 60%，而 pi_0.5 为 5%，Cosmos-Policy 也为 5%；真实场景 Close Drawer 为 45%，而 MolmoAct 为 5%，其余方法为 0%。
- 摘要还称，该方法在零样本成功率和视频-动作联合生成质量上优于先前的视频空间世界模型，但摘录中没有给出联合生成指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06168v2](http://arxiv.org/abs/2604.06168v2)
