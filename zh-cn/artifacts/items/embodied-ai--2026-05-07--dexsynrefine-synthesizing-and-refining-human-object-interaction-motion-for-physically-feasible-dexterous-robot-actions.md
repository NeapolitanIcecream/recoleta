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
## 摘要
DexSynRefine 将少量人-物交互录像转成可执行的灵巧机器人动作。它把动作生成、残差强化学习和接触/动力学自适应结合起来，用于五项操作任务。

## 问题
- 灵巧遥操作数据集采集成本高，而人-物交互录像更容易扩展。
- HOI 数据提供腕部、手部和物体运动，但不提供机器人执行所需的接触力和动力学；人手和机器人手在形状与驱动方式上也不同。
- 稀疏的 HOI 示范常常没有适配新初始物体姿态的参考，原始重定向在未记录过的情况外会失效。

## 方法
- 该方法在五项任务上每项收集 7 条 HOI 示范，并用以物体为中心的 SE(2) 增强扩展到每项约 300 条轨迹，每条轨迹的时域长度为 T=220。
- HOI-MMFP 先用 Transformer 自编码器学习潜在运动流形，再用条件 flow matching，根据任务文本嵌入和初始物体姿态生成腕部、手关键点和物体轨迹。
- PPO 教师策略学习加到生成的腕部和指尖目标上的任务空间残差；逆运动学把这些目标转换成 7 自由度机械臂和 16 自由度手部指令，频率为 120 Hz。
- 可部署的学生策略使用 30 步本体感觉历史，结合 GRU 接触估计器和动力学潜变量预测器，替代特权仿真状态。

## 结果
- 在初始姿态扰动为 ±20 cm 的 x/y 位移和 ±30° 偏航时，HOI-MMFP 的首帧腕部误差为 0.015 m / 2.50°，DiT-Full 为 0.018 m / 2.65°，TC-VAE 为 0.121 m / 12.88°。
- HOI-MMFP 的腕部抖动更低：29.83±4.78 m/s^3 和 101.08±17.12 rad/s^3；TC-VAE 为 37.00±8.52 / 139.14±45.21，DiT-Full 为 41.03±8.23 / 189.52±33.82。
- 在 Pick Up 和 Hammer 上，以 HOI-MMFP 作为参考时，仿真成功率为 52.6±3.04%，DiT-Full 为 49.10±4.12%；物体平移误差为 0.041 m 对 0.057 m，物体朝向误差为 46.29° 对 51.42°。
- 任务空间残差动作在五项任务上的平均仿真成功率最高，为 68.1%。各任务成功率分别为 Pringles 71.5%、Watering Can 52.4%、Bowl 94.8%、Hammer 60.3% 和 Book 61.6%；运动学重定向保持在 0.0-5.8%。
- 完整学生策略优于自适应消融：在 Hammer 上，成功率为 44.3%，没有接触模块时为 17.2%，没有动力学模块时为 7.5%；在 Watering Can 上，分别为 51.8%、0.0% 和 4.4%。
- 摘要称，真实机器人在五项任务上都完成了迁移，相比运动学重定向提升了 50-70 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05925v1](https://arxiv.org/abs/2605.05925v1)
