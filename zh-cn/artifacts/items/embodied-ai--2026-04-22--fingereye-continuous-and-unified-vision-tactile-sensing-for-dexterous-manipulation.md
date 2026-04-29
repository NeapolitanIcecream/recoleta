---
source: arxiv
url: http://arxiv.org/abs/2604.20689v2
published_at: '2026-04-22T15:37:34'
authors:
- Zhixuan Xu
- Yichen Li
- Xuanye Wu
- Tianyu Qiu
- Lin Shao
topics:
- vision-tactile-sensing
- dexterous-manipulation
- imitation-learning
- sim2real
- robot-sensing
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# FingerEye: Continuous and Unified Vision-Tactile Sensing for Dexterous Manipulation

## Summary
## 摘要
FingerEye 是一种低成本指尖传感器，在接触前、接触开始时和接触后都保持同一视觉流工作。论文将这套硬件与一个模仿学习策略以及一个用于灵巧操作的仿真数字孪生配合使用。

## 问题
- 灵巧操作需要贯穿整个交互过程的反馈：接近、首次接触，以及接触后的力调节。
- GelSight 等常见触觉传感器只有在接触后才有用，而外部相机在接触区域附近提供的线索较弱，或者容易被遮挡。
- 这个缺口会让接触建立在需要毫米级对齐和快速力调整的任务中变得不稳定，例如立硬币或抓取薄物体。

## 方法
- FingerEye 将两个指尖 RGB 相机、一个柔性硅胶环和一个带有 35 个 AprilTags 的透明亚克力盖板结合起来。接触前，相机看到的是物体；接触后，环的形变会带动带标签的板移动，因此同一组相机也能测量与触觉相关的形变。
- 两个相机的位置和焦距设置不同：一个位于指尖，用于近距离形变感知；另一个位于指根，用于在接触前提供更宽的场景视野。这样可以得到隐式双目深度，并在不切换模态的情况下实现连续感知。
- 接触 wrench 由 AprilTag 布局的 6D 位姿变化推断得到。系统使用多标签 PnP 加 Levenberg–Marquardt 精化来估计板的位姿，并使用所有可见标签角点，以便在遮挡和形变情况下获得更稳定的结果。
- 在控制方面，论文使用一种 transformer 模仿学习策略，融合多个 FingerEye 传感器和一个腕部相机的图像，以及机器人关节状态和最近的标签位姿历史，用来预测未来动作块。
- 为了在真实数据有限的情况下提高泛化能力，作者在 Isaac Lab 中构建了 FingerEye 数字孪生，并将真实示范与一个规模更小但进行了大量视觉随机化的仿真数据集混合使用。

## 结果
- 传感器硬件紧凑且便宜：每个模块约 28.0 × 25.4 × 26.0 mm，由现成部件和 3D 打印部件构成，材料成本约 $60。
- 灵敏度分析报告六个力/力矩轴上的最小可检测 wrench 为 [4.30, 4.22, 9.93, 0.32, 0.13, 8.55]^T，单位为 mN 和 mN·m。
- 在力–形变标定中，作者收集了覆盖全部 6 个维度的 1,000 多组同步 wrench–位姿样本，使用其中 80% 训练、20% 测试，并在 Fig. 4 中报告了较高的测试 R^2 和较低的测试 RMSE。当前摘录未给出各轴的具体数值。
- 在精细抓取实验中，配备 FingerEye 的 LEAP Hand 抓取了 9 种易碎或可变形物体，并在指尖法向形变表明发生接触时停止手指运动。论文称其能够稳定检测接触开始，并在不损伤物体的情况下完成提起。
- 论文称其在立硬币、抓取芯片、取信件和操作注射器等任务上成功实现了灵巧操作。
- 当前摘录没有给出任务级策略成功率、基线对比或仿真增强带来的收益，因此这里可用的主要定量证据是传感器的成本、尺寸、灵敏度，以及超过 1,000 个样本的 wrench 标定设置。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20689v2](http://arxiv.org/abs/2604.20689v2)
