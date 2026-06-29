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
GS-Playground 是一个模拟器，用于以高速训练基于视觉的机器人策略，输入是基于 3D Gaussian Splatting 的照片级真实图像。它面向视觉强化学习、Real2Sim 场景构建、接触丰富的操作、导航和运动控制。

## 问题
- 基于视觉的机器人强化学习需要大量并行仿真步数，但高分辨率的照片级真实渲染会耗尽 GPU 内存并拖慢训练。
- 从真实采集构建可用于仿真的场景仍然需要人工工作，因为视觉资产、碰撞几何、位姿、尺度和物理一致性都必须对齐。
- 这个问题之所以重要，是因为接触丰富的机器人技能通常需要仿真规模，而视觉策略又需要接近真实相机输入的图像，才能完成 sim-to-real 迁移。

## 方法
- 该系统把自定义并行物理引擎和批量 3D Gaussian Splatting 渲染器结合起来，让物理状态和渲染图像在多个环境中同步更新。
- 物理解算器使用速度-冲量接触形式、Projected Gauss-Seidel 求解、约束岛和 warm-starting 来处理刚体接触和摩擦。
- 渲染器会裁剪 3DGS 点并批量处理多个场景，从而降低内存占用，同时把视觉质量保持在接近原始重建的水平。
- Rigid-Link Gaussian Kinematics 将高斯簇绑定到仿真的刚体上，因此在接触和运动过程中，渲染物体会随物理刚体一起移动。
- Real2Sim 流水线使用 Grounding DINO、SAM/SAM2、LaMa、SAM-3D、AnySplat 和 Speedy-splat，把 RGB 采集转换为 3DGS 资产、网格、深度、位姿、尺度和可用于碰撞的场景元素。

## 结果
- 论文声称在 NVIDIA RTX 4090 和 Intel i9-14900K 上，640×480 分辨率下 3DGS 渲染速度约为 10,000 FPS；对比表中，DISCOVERSE 约为 650 FPS，GS-Playground 约为 10k FPS。
- 批量渲染器支持最多 2048 个 640×480 场景，总吞吐量最高可达 10,000 FPS。
- 3DGS 裁剪步骤移除了超过 90% 的高斯点，同时把 PSNR 损失控制在 0.05 以下。
- 对比表显示该模拟器最多支持 4096 个 3DGS 环境，在环境数量上与 GaussGym 持平，同时增加了动态 3DGS 场景。
- 在稳定堆叠任务中，warm-starting 将 Projected Gauss-Seidel 迭代次数从 50 多次降到 10 次以下。
- 物理基准包括 10 ms 步长的 Boston Dynamics Spot 稳定性测试和 Newton's Cradle 接触测试；文中称其能量流失低于 MuJoCo，并且在所展示的接触案例中稳定性更好。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25459v1](https://arxiv.org/abs/2604.25459v1)
