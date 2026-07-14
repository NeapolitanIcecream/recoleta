---
source: arxiv
url: https://arxiv.org/abs/2607.11167v1
published_at: '2026-07-13T07:03:29'
authors:
- Haojie Huang
- Linfeng Zhao
- Haotian Liu
- Zhang Ye
- Si-Yuan Huang
- Mingxi Jia
- Boce Hu
- Fangzhou Lin
- Yu Qi
- Dian Wang
- Robin Walters
- Robert Platt
topics:
- robot-manipulation
- imitation-learning
- image-space-actions
- equivariant-augmentation
- multi-view-diffusion
- sim-to-real
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation

## Summary
## 摘要
Pix2Act通过预测配对相机视图中的连续二维夹爪关键点轨迹来学习机器人操作策略，再通过三角测量恢复三维动作。它的等变数据增强和多视图扩散架构提高了模拟操作成功率，并增强了对相机变换的鲁棒性。

## 问题
- 传统策略直接根据图像预测三维平移和旋转，使观测与动作之间的几何联系保持隐式。这会增加歧义和过拟合，也使精确操作更难学习。
- 早期的图像-动作方法使用离散像素或对每个视图分别进行预测，导致精度损失、轨迹超出画面、三角测量误差和轨迹不一致。
- 这个问题影响需要精确操作的任务，因为这类任务中的动作会随空间位置变化，并且需要适应不同的相机姿态和物体配置。

## 方法
- 用四个三维关键点表示每个夹爪姿态，并将这些关键点投影到两台手部相机成像平面上的连续、无界坐标中。三角测量恢复三维关键点轨迹，再重建平移和旋转。
- 训练扩散策略生成图像空间中的关键点轨迹，而不是直接生成三维姿态。模型使用两个手部相机视图和一个头戴式相机视图，分别获取局部操作细节和全局上下文。
- 对每个相机图像及其对应的动作轨迹分别施加平面旋转和平移。这会约束每台相机的等变性，同时使恢复出的三维动作不受这些变换影响。
- 使用 Diffusion X-Net。该模型结合每个视图的视觉编码器、多视图 Transformer 和共享的逐视图扩散头，在融合相机信息的同时支持相机置换等变性。

## 结果
- 在 10 个 MimicGen 模拟任务上，每个任务使用 100 个示范进行训练，并在每个任务的 50 次未见测试中评估，Pix2Act 的平均成功率达到 75.2%。
- Pix2Act 在 10 个任务中的 9 个任务上取得最高成绩，比报告结果中最强的基线 EquiDiff-Voxel 高 12.1 个百分点，平均成功率为 75.2%，而该基线为 63.1%。
- 它比最强的图像基线 EquiDiff-Img 高 21.6 个百分点，平均成功率为 75.2%，而该基线为 53.6%。
- 各任务成功率介于 Square 的 50% 和 StackThree 的 94% 之间；在两个高精度任务 Threading 和 NutAssembly 上，Pix2Act 的成功率分别为 52% 和 90%。
- 摘录指出，Pix2Act 在真实世界任务中也优于各项基线，并且在相机受到扰动时保持稳健，但没有提供相应的真实世界数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11167v1](https://arxiv.org/abs/2607.11167v1)
