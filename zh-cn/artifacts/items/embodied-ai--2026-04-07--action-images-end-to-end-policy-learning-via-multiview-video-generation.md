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
## 总结
Action Images 通过把每个 7-DoF 动作转成多视角像素空间视频，并训练一个视频模型同时生成未来观测和动作，来学习机器人控制。论文声称，这样可以不再需要单独的 policy head，并提升零样本机器人控制能力，尤其是在新视角和真实环境变化下。

## 问题
- 视频世界模型可以预测未来帧，但这不一定会得到能在新环境里选对动作的策略。
- 许多已有方法把动作放在单独模块里，或者放进和图像像素没有直接对应关系的潜变量 token 里，所以预训练视频知识很难顺畅迁移到控制任务。
- 单一相机视角会让 3D 机器人运动产生歧义，这会影响从图像中恢复动作。

## 方法
- 将每个机器人动作 \((x,y,z,\text{orientation},\text{gripper})\) 转成三个语义 3D 点：末端执行器位置、up point 和 normal point。
- 把这些点投影到每个相机视角中，并渲染成 RGB 高斯热图。蓝色通道还在低响应区域存储夹爪开合状态。这样得到与 RGB 机器人视频对齐的多视角动作视频。
- 在打包后的观测视频和动作视频 token 上训练一个单一的预训练视频生成骨干网络（Wan 2.2），并用掩码支持联合视频-动作生成、按动作条件的视频生成、视频到动作标注，以及仅视频生成。
- 将生成的动作图像解码回连续 7-DoF 控制：从蓝色通道读取夹爪状态，通过侧视图匹配把主视图中的热图峰值提升到 3D，再用恢复出的三个 3D 点重建位姿。
- 在 RLBench、DROID 和 BridgeV2 上训练，使用相机条件和掩码潜变量 token 上的 flow-matching 损失。

## 结果
- 在零样本 RLBench 任务上，方法报告的成功率为：pick cup 30%，reach target 60%，close drawer 50%，close laptop 15%。
- 在零样本真实世界任务上，面对未见过的物体、环境和 xArm 机器人配置，报告的成功率为：Place Cup 40%，Pick Unseen Toy 20%，Pick Tissue 15%，Close Drawer 45%，Close Box 10%。
- 与表 2 中复现的基线相比，它在大多数列出的任务上超过了 MV-Policy、pi_0.5、MolmoAct、TesserAct 和 Cosmos-Policy。例子包括：RLBench reach target 为 60%，而 pi_0.5 和 Cosmos-Policy 都是 5%；真实环境 Close Drawer 为 45%，而 MolmoAct 是 5%，其他方法都是 0%。
- 摘要还声称，它的零样本成功率和视频-动作联合生成质量都优于此前的 video-space world models，但摘录没有给出联合生成指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06168v2](http://arxiv.org/abs/2604.06168v2)
