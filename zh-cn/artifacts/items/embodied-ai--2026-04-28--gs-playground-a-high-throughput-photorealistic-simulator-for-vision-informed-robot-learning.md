---
source: arxiv
url: https://arxiv.org/abs/2604.25459v1
published_at: '2026-04-28T10:05:39'
authors:
- Yufei Jia
- Heng Zhang
- Ziheng Zhang
- Junzhe Wu
- Mingrui Yu
- Zifan Wang
- Dixuan Jiang
- Zheng Li
- Chenyu Cao
- Zhuoyuan Yu
- Xun Yang
- Haizhou Ge
- Yuchi Zhang
- Jiayuan Zhang
- Zhenbiao Huang
- Tianle Liu
- Shenyu Chen
- Jiacheng Wang
- Bin Xie
- Xuran Yao
- Xiwa Deng
- Guangyu Wang
- Jinzhi Zhang
- Lei Hao
- Zhixing Chen
- Yuxiang Chen
- Anqi Wang
- Hongyun Tian
- Yiyi Yan
- Zhanxiang Cao
- Yizhou Jiang
- Hanyang Shao
- Yue Li
- Lu Shi
- Bokui Chen
- Wei Sui
- Hanqing Cui
- Yusen Qin
- Ruqi Huang
- Lei Han
- Tiancai Wang
- Guyue Zhou
topics:
- robot-simulation
- vision-based-rl
- gaussian-splatting
- sim2real
- robot-data-scaling
- contact-rich-manipulation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning

## Summary
## 摘要
GS-Playground 是一个仿真器，用于高速生成照片级真实感 3D Gaussian Splatting 图像，训练基于视觉的机器人策略。它面向视觉强化学习、真实到仿真的场景创建、富接触操作、导航和运动控制。

## 问题
- 基于视觉的机器人强化学习需要大量并行仿真步骤，但高分辨率照片级真实感渲染会耗尽 GPU 内存并拖慢训练。
- 从真实采集数据构建可用于仿真的场景仍需要人工处理，因为视觉资产、碰撞几何、位姿、尺度和物理一致性必须对齐。
- 这个问题很重要，因为富接触机器人技能通常需要大规模仿真，而视觉策略需要足够接近真实相机输入的图像，才能完成从仿真到真实的迁移。

## 方法
- 该系统把自定义并行物理引擎与批处理 3D Gaussian Splatting 渲染器结合起来，使多个环境中的物理状态和渲染图像同步更新。
- 物理解算器使用速度-冲量接触形式、Projected Gauss-Seidel 求解、约束岛和热启动来处理刚体接触和摩擦。
- 渲染器会剪枝 3DGS 点并批处理多个场景，在保持接近原始重建视觉质量的同时降低内存使用。
- Rigid-Link Gaussian Kinematics 将高斯簇绑定到仿真的刚体上，使渲染对象在接触和运动过程中随物理刚体移动。
- Real2Sim 流程使用 Grounding DINO、SAM/SAM2、LaMa、SAM-3D、AnySplat 和 Speedy-splat，将 RGB 采集数据转换为 3DGS 资产、网格、深度、位姿、尺度和可用于碰撞的场景元素。

## 结果
- 论文声称，在 NVIDIA RTX 4090 和 Intel i9-14900K 上，640×480 分辨率的 3DGS 渲染约为 10,000 FPS；对比表列出 DISCOVERSE 约为 650 FPS，GS-Playground 约为 10k FPS。
- 批处理渲染器在 640×480 分辨率下最多支持 2048 个场景，总吞吐量最高可达 10,000 FPS。
- 3DGS 剪枝步骤移除了超过 90% 的高斯，同时将 PSNR 损失控制在 0.05 以下。
- 对比表显示，该仿真器最多支持 4096 个 3DGS 环境，在环境数量上与 GaussGym 相同，同时增加了动态 3DGS 场景。
- 在稳定堆叠任务中，热启动将 Projected Gauss-Seidel 迭代次数从超过 50 次降到少于 10 次。
- 物理基准包括 10 ms 时间步长的 Boston Dynamics Spot 稳定性测试和 Newton’s Cradle 接触测试；论文声称，在展示的接触案例中，它比 MuJoCo 的能量耗散更低，稳定性更好。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25459v1](https://arxiv.org/abs/2604.25459v1)
