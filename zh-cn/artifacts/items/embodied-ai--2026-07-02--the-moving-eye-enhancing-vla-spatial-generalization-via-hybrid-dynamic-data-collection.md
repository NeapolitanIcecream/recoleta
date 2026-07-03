---
source: arxiv
url: https://arxiv.org/abs/2607.02322v1
published_at: '2026-07-02T15:30:26'
authors:
- Jincheng Tang
- Yilong Zhu
- Zhengyuan Xie
- Jiang-Jiang Liu
- Jiaxing Zhang
topics:
- vision-language-action
- robot-data-collection
- spatial-generalization
- dynamic-camera
- manipulation
- shortcut-learning
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# The Moving Eye: Enhancing VLA Spatial Generalization via Hybrid Dynamic Data Collection

## Summary
## 摘要
论文认为，VLA 策略在相机和物体发生位置变化时失效，是因为训练数据把相机位姿、机器人基座和物体位置绑定在一起。论文测试了一个真实的双臂采集设置，将移动相机 episode 与静态多视角 episode 混合使用，并发现 Gr00t 在笔任务上的最佳混合比例为 Moving:Multi-Fixed = 1:3。

## 问题
- 研究目标是 VLA 操作在相机位姿或物体布局变化时的空间泛化能力不足。
- 作者指出了三类捷径来源：相机-基座耦合、相机-物体耦合、物体-位置耦合。
- 这对真实机器人很重要，因为固定相机可能发生移动，不同数据集的相机支架会不同，移动视角或手持视角也会在任务执行期间变化。

## 方法
- 双臂设置使用一只 So-101 机械臂执行操作，另一只 Airbot 机械臂作为可移动环境相机。
- 论文比较了 Fixed View、Multi-Fixed View 和 Moving View 数据。Moving View 在与 Multi-Fixed View 相同的有界区域内使用连续相机轨迹。
- 训练数据按 Moving:Multi-Fixed = 1:k 混合 Moving 和 Multi-Fixed episode；对于 Gr00t n1，报告的笔任务最佳比例为 1:3。
- 采集过程还会随机化目标和容器位置，以减少物体-位置捷径。
- 策略把腕部相机和环境相机观测以及语言映射为动作，然后在留出的相机位姿、移动相机轨迹和偏移后的物体配置上测试。

## 结果
- 在使用 2400 个样本的笔任务中，Fixed View 训练在固定 ID 测试上达到 85.0% 成功率，但在移动相机 OOD 测试上只有 43.0%。Mixed Data 达到 86.0% ID 和 83.0% OOD。
- 在物体-位置耦合测试中，Multi-Fixed 基线在笔筒位于训练位置时得分为 95.0 ± 3.5%，在笔筒移动一个直径后得分为 71.9 ± 5.2%。Mixed 1:3 的得分为 91.9 ± 2.4% 和 90.6 ± 6.3%。
- 在 Gr00t 的移动相机笔测试中，按 Moving:Multi-Fixed 比例划分的成功率为：1:0 时 54.8 ± 10.7%，1:1 时 83.3 ± 7.1%，1:3 时 89.0 ± 5.7%，0:1 时 80.5 ± 6.1%。
- 评估使用了 400 个笔任务 episode、40 条移动相机轨迹、40 个静态相机位姿、5 个目标-容器相对位置和 8 个笔朝向。
- 摘录称该数据策略对 ACT、Diffusion、Pi0 和 Gr00t 有帮助，但提供的文本没有包含跨架构数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02322v1](https://arxiv.org/abs/2607.02322v1)
