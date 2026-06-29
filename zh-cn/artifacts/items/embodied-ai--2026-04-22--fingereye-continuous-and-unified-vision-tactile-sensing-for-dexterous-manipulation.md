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
FingerEye 是一种低成本指尖传感器，在接触前、接触开始时和接触后都保持同一条视觉流持续工作。本文把这套硬件和模仿学习策略、仿真数字孪生结合起来，用于灵巧操作。

## 问题
- 灵巧操作需要覆盖整个交互过程的反馈：接近、首次接触，以及接触后的力控制。
- 常见触觉传感器如 GelSight 只在接触后才有用，而外部摄像头在接触区域附近往往会受到遮挡，线索也较弱。
- 这种缺口会让需要毫米级对齐和快速力调整的任务中接触起始变得不稳定，比如立起硬币或抓取薄物体。

## 方法
- FingerEye 把两个指尖 RGB 摄像头、一个柔性硅胶环和一个带有 35 个 AprilTag 的透明亚克力盖板组合在一起。接触前，摄像头观察物体；接触后，硅胶环变形会带动带标签的板块移动，同样的摄像头也能测到与触碰相关的变形。
- 两个摄像头的位置和焦距设置不同：尖端摄像头用于近距离变形感知，根部摄像头用于更宽的接触前场景可见性。这带来隐式的立体深度和连续感知，不需要切换模态。
- 接触力矩通过 AprilTag 布局的 6D 位姿变化推断。系统用多标签 PnP 加 Levenberg–Marquardt 精修估计板块位姿，并利用所有可见标签角点，在遮挡和变形条件下提高稳定性。
- 在控制方面，论文使用基于 Transformer 的模仿学习策略，融合多个 FingerEye 传感器和腕部摄像头的图像，以及机器人关节状态和最近的标签位姿历史，来预测未来一段动作块。
- 为了在真实数据有限时提高泛化能力，作者在 Isaac Lab 中构建了 FingerEye 数字孪生，并把真实示范与一个经过强视觉随机化的小规模仿真数据集混合起来。

## 结果
- 传感器硬件体积小、成本低：每个模块约 28.0 × 25.4 × 26.0 mm，由现成部件和 3D 打印部件组成，材料成本约 60 美元。
- 灵敏度分析报告的六个力/力矩轴上的最小可检测力矩为 [4.30, 4.22, 9.93, 0.32, 0.13, 8.55]^T，单位分别为 mN 和 mN·m。
- 在力-变形标定中，作者收集了 1,000 多组同步的力矩-位姿样本，覆盖全部 6 个维度，80% 用于训练、20% 用于测试，并在图 4 中报告了较高的测试 R^2 和较低的测试 RMSE。摘要片段没有给出各轴的具体数值。
- 在精细抓取中，装有 FingerEye 的 LEAP Hand 抓取了 9 个脆弱或可变形物体，并在指尖法向变形表明已接触时停止手指运动。论文称接触起始检测稳定，抬升过程没有造成损伤。
- 论文还称该系统在立硬币、捡薯片、取回字母和注射器操作等任务上实现了灵巧操作。
- 片段没有提供按任务划分的策略成功率、基线对比或仿真增强带来的提升，因此这里能直接看到的主要量化证据是传感器成本、尺寸、灵敏度，以及超过 1,000 组样本的力矩标定设置。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20689v2](http://arxiv.org/abs/2604.20689v2)
