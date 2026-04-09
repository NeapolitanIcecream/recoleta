---
source: arxiv
url: http://arxiv.org/abs/2604.03181v1
published_at: '2026-04-03T16:57:06'
authors:
- Peiyan Li
- Yixiang Chen
- Yuan Xu
- Jiabing Yang
- Xiangnan Wu
- Jun Guo
- Nan Sun
- Long Qian
- Xinghang Li
- Xin Xiao
- Jing Liu
- Nianfeng Liu
- Tao Kong
- Yan Huang
- Liang Wang
- Tieniu Tan
topics:
- robot-manipulation
- video-diffusion-policy
- multi-view-3d
- vision-language-action
- data-efficient-learning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-View Video Diffusion Policy: A 3D Spatio-Temporal-Aware Video Action Model

## Summary
## 概要
MV-VDP 是一种机器人操作策略，会同时预测未来的多视角视频和动作热力图，因此模型既能跟踪 3D 场景结构，也能跟踪动作之后场景会如何变化。论文面向低数据操作场景，并报告称其在仿真和真实机器人上都明显优于基于视频动作、基于 3D 以及视觉-语言-动作的基线方法。

## 问题
- 许多机器人策略从 2D 图像学习，却要在 3D 空间中执行动作，这会造成观测与控制之间的不匹配，并提高对机器人数据量的需求。
- 许多策略复用在静态图像上训练的图文骨干网络，因此在建模场景动态和动作随时间产生的后果方面表现较差。
- 这一点在低数据操作中最明显：论文聚焦于每个任务只有 5 到 10 条演示的设置，在这种情况下，常见的行为克隆和 VLA 系统往往会失败。

## 方法
- 该方法将裁剪后的点云投影到三个固定的正交视角中，生成多视角 RGB 图像以及表示机器人末端执行器位姿的多视角热力图。
- 它对可兼容预训练的视频输入和动作预测使用同一种表示类型：模型会联合预测未来 RGB 视频和未来热力图视频。
- 骨干网络是一个 5B 的 Wan2.2 视频扩散模型，并加入了跨视角注意力，使不同相机视角的 token 能在每个时间步相互交互。
- 来自各视角的预测热力图峰值会被反投影为 3D 末端执行器位置。一个单独的 170M 解码器使用去噪后的视频潜变量来预测旋转和夹爪状态，然后将位置、旋转和夹爪输出组合成动作块。
- 训练同时对视频序列和热力图序列使用扩散损失，并结合 LoRA 微调和 SE(3) 增强。论文称完整微调没有带来性能提升。

## 结果
- **Meta-World，7 个任务，每个任务 5 条演示，每个任务 25 次试验：** MV-VDP 的平均成功率达到 **89.1%**，高于 **Track2Act 67.4%**、**DreamZero 61.1%**、**AVDC 58.9%**、**DP 37.7%**、**BC-R3M 35.4%**、**BC-Scratch 26.2%** 和 **UniPi 11.4%**。
- **Meta-World 各任务示例：** MV-VDP 在 D-Open、D-Close、Btn 和 Handle 上取得 **25/25**，在 Btn-Top 和 Fct-Open 上取得 **24/25**，在 Fct-Cls 上取得 **8/25**。
- **真实世界，每个任务约 10 条演示，每个任务 10 次试验：** 在基础任务上，MV-VDP 报告 Put Lion **10/10**、Push-T **4/10**、Scoop Tortilla **7/10**。摘录中给出的基线更弱：**BridgeVLA 9/10、0/10、4/10**；**UVA 2/10、0/10、0/10**；**DP3 0/10、0/10、0/10**；**π0.5 1/10、0/10、0/10**。
- **真实世界未见变体：** 摘录显示 MV-VDP 在 Put-B 上为 **5/10**，在 Put-H 上为 **6/10**，说明它对背景变化和物体高度变化有一定迁移能力。由于表格被截断，提供文本中看不到其余未见任务的数字和最终平均值。
- 论文还称其对超参数有较强鲁棒性，包括在仅用 **1 个 diffusion step** 时仍能保持较好性能，但摘录没有给出支持该说法的表格或具体数字。
- 论文称其未来视频预测更真实，动作预览也更容易解释，但摘录没有给出定量的视频预测指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03181v1](http://arxiv.org/abs/2604.03181v1)
