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
## 总结
MV-VDP 是一种机器人操作策略，同时预测未来的多视角视频和动作热图，因此模型能跟踪 3D 场景结构以及动作之后场景会如何变化。论文面向低数据量操作任务，并报告了在仿真和真实机器人上的结果，优于视频动作、3D 和视觉-语言-动作基线。

## 问题
- 许多机器人策略用 2D 图像学习，却在 3D 空间中执行动作，这会造成观测和控制之间的不匹配，并增加所需的机器人数据量。
- 许多策略复用在静态图文对上预训练的图像骨干网络，因此对场景动态和动作后果的建模较弱。
- 这在低数据量操作场景中最明显：论文关注每个任务只有 5 到 10 条演示的设置，而常见的行为克隆和 VLA 系统往往会失败。

## 方法
- 该方法将裁剪后的点云投影到三个固定的正交视图，生成多视角 RGB 图像和机器人末端执行器位姿的多视角热图。
- 它对适合预训练的视频输入和动作预测使用同一种表示类型：模型同时预测未来 RGB 视频和未来热图视频。
- 骨干网络是一个 5B 参数的 Wan2.2 视频扩散模型，并加入跨视角注意力，使不同相机视角的 token 在每个时间步交互。
- 从各视图预测得到的热图峰值会回投到 3D 末端执行器位置。另一个 1.7 亿参数的解码器使用去噪后的视频潜变量预测旋转和夹爪状态，然后把位置、旋转和夹爪输出合成为动作块。
- 训练同时使用视频序列和热图序列上的扩散损失，再加上 LoRA 微调和 SE(3) 增强。论文说完整微调没有提升性能。

## 结果
- **Meta-World，7 个任务，每个任务 5 条演示，每个任务 25 次试验：** MV-VDP 的平均成功率达到 **89.1%**，高于 **Track2Act 67.4%**、**DreamZero 61.1%**、**AVDC 58.9%**、**DP 37.7%**、**BC-R3M 35.4%**、**BC-Scratch 26.2%** 和 **UniPi 11.4%**。
- **Meta-World 单任务示例：** MV-VDP 在 D-Open、D-Close、Btn 和 Handle 上得到 **25/25**，在 Btn-Top 和 Fct-Open 上得到 **24/25**，在 Fct-Cls 上得到 **8/25**。
- **真实世界，每个任务约 10 条演示，每个任务 10 次试验：** 在基础任务上，MV-VDP 报告 Put Lion 为 **10/10**、Push-T 为 **4/10**、Scoop Tortilla 为 **7/10**。摘录中的基线更弱：**BridgeVLA 9/10, 0/10, 4/10**；**UVA 2/10, 0/10, 0/10**；**DP3 0/10, 0/10, 0/10**；**π0.5 1/10, 0/10, 0/10**。
- **真实世界未见变体：** 摘录报告 MV-VDP 在 Put-B 上为 **5/10**、在 Put-H 上为 **6/10**，说明它对背景和物体高度变化有一定迁移能力。表格被截断，所以其余未见任务数字和最终平均值在给出的文本中没有完整显示。
- 论文还声称对超参数有较强鲁棒性，包括只用 **1** 个扩散步也能保持较好性能，但摘录没有给出支撑表格或精确数字。
- 它还声称能预测逼真的未来视频并提供可解释的动作预览，但摘录没有给出定量的视频预测指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03181v1](http://arxiv.org/abs/2604.03181v1)
