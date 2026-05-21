---
source: arxiv
url: https://arxiv.org/abs/2605.05925v1
published_at: '2026-05-07T09:31:43'
authors:
- Hyesung Lee
- Hyunwoo Jung
- Si-Hwan Heo
- Sungwook Yang
topics:
- dexterous-manipulation
- human-object-interaction
- residual-rl
- sim-to-real
- motion-synthesis
- contact-adaptation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# DexSynRefine: Synthesizing and Refining Human-Object Interaction Motion for Physically Feasible Dexterous Robot Actions

## Summary
## 概要
DexSynRefine 将少量人-物交互记录转成可执行的灵巧机器人动作。它在五个操作任务中结合了运动合成、残差强化学习以及接触/动力学适配。

## 问题
- 灵巧遥操作数据集采集成本高，而人-物交互记录更容易扩展。
- HOI 数据提供手腕、手和物体运动，但缺少机器人执行所需的接触力和动力学信息；人手和机器人手在形状和驱动方式上也不同。
- 稀疏 HOI 演示通常没有与新物体初始位姿匹配的参考，因此原始重定向在记录案例之外会失败。

## 方法
- 该方法在五个任务中每个任务采集 7 个 HOI 演示，并用以物体为中心的 SE(2) 增强扩展到每个任务约 300 条轨迹，每条轨迹的时域长度为 T=220。
- HOI-MMFP 用 Transformer 自编码器学习潜在运动流形，然后用条件流匹配，根据任务文本嵌入和物体初始位姿生成手腕、手部关键点和物体轨迹。
- PPO 教师策略学习任务空间残差，并将其加到生成的手腕和指尖目标上；逆运动学把这些目标转换为 7-DoF 机械臂和 16-DoF 手部命令，频率为 120 Hz。
- 可部署的学生策略使用 30 步本体感受历史，并通过 GRU 接触估计器和动力学潜变量预测器替代仿真中的特权状态。

## 结果
- 在初始位姿受到 ±20 cm x/y 和 ±30° yaw 扰动时，HOI-MMFP 的首帧手腕误差为 0.015 m / 2.50°，相比之下 DiT-Full 为 0.018 m / 2.65°，TC-VAE 为 0.121 m / 12.88°。
- HOI-MMFP 的手腕 jerk 更低：29.83±4.78 m/s^3 和 101.08±17.12 rad/s^3；相比之下，TC-VAE 为 37.00±8.52 / 139.14±45.21，DiT-Full 为 41.03±8.23 / 189.52±33.82。
- 在 Pick Up 和 Hammer 上，以 HOI-MMFP 作为参考得到 52.6±3.04% 的仿真成功率，DiT-Full 为 49.10±4.12%；物体平移误差为 0.041 m 对 0.057 m，物体朝向误差为 46.29° 对 51.42°。
- 任务空间残差动作在五个任务上的平均仿真成功率最高：68.1%。各任务成功率为 Pringles 71.5%、Watering Can 52.4%、Bowl 94.8%、Hammer 60.3%、Book 61.6%；运动学重定向保持在 0.0-5.8%。
- 完整学生策略优于适配消融版本：在 Hammer 上，成功率为 44.3%，无接触版本为 17.2%，无动力学版本为 7.5%；在 Watering Can 上，分别为 51.8%、0.0% 和 4.4%。
- 摘要称，该方法在全部五个任务上实现了真实机器人迁移，相比运动学重定向提高 50-70 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05925v1](https://arxiv.org/abs/2605.05925v1)
