---
source: arxiv
url: http://arxiv.org/abs/2604.19092v1
published_at: '2026-04-21T05:09:56'
authors:
- Feng Jiang
- Yang Chen
- Kyle Xu
- Yuchen Liu
- Haifeng Wang
- Zhenhao Shen
- Jasper Lu
- Shengze Huang
- Yuanfei Wang
- Chen Xie
- Ruihai Wu
topics:
- world-model-benchmark
- robotic-manipulation
- embodied-evaluation
- video-world-models
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation

## Summary
## 概要
RoboWM-Bench 是一个基准，用来测试世界模型生成的机器人操作视频能否转成可执行动作，并且真正完成任务。论文表明，视频生成在视觉上表现很强，但并不能稳定地产生在物理上可执行的操作行为。

## 问题
- 现有视频世界模型基准主要关注视觉真实性、语义一致性或用于诊断的物理合理性，但不会直接测试生成的操作行为是否能由机器人执行。
- 这一点很重要，因为机器人从想象或生成视频中学习，只有在预测行为符合真实动力学、接触关系和任务约束时才有效。
- 真实机器人评测成本高，也很难复现，所以论文的目标是构建一个可扩展、可重复、以具身执行为依据的基准。

## 方法
- 该基准从初始场景观测和任务描述出发，让世界模型生成未来的操作视频，再将该视频转换为机器人动作，并在仿真中执行。
- 对于人手操作视频，方法使用 HaMeR 估计 3D 手部姿态，并将其重定向为机器人末端执行器运动；同时采用修改后的位姿/朝向表示和夹爪信号，以获得更稳定的接触几何。
- 对于机器人视频，方法使用一个逆动力学模型，从连续帧中恢复关节动作。该模型先在仿真中训练，再用少量真实 Franka 数据微调。
- 它在基于 LeHome 的高保真 real-to-sim 设置中重建真实场景，然后同时检查接触、抬起等步骤级节点，以及最终任务是否成功。
- 任务集合覆盖刚体、关节体、可变形物体、长时程和双手操作场景。

## 结果
- 在人工任务级评测中，Wan 2.6 是已报告模型里表现最强的：Pick Object 为 83%，Push Button 为 100%，Pour Water 为 80%，Open Drawer 为 80%，Put in Drawer 为 80%，Fold Towel 为 40%。较弱模型常在更难任务上完全失败，例如 Cosmos 在 Pour Water 和 Fold Towel 上都是 0%。
- 人工步骤级结果显示，早期接触远比完整执行容易。以 Put on Plate 为例，多个模型的接触率达到 100%，但最终放置成功率分别降到：Cosmos 15%、Wan 2.2 55%、Wan 2.6 70%、Veo 3.1 30%、LVP 70%。
- 在机器人任务级评测中，成功率低得多。在不做任务特定微调时，已报告的最好结果来自 Wan 2.6：Close Drawer 为 50%，Push Object 为 40%，Push Button 为 40%，Pick Object 和 Put on Plate 都为 20%，Pull Object 和 Put in Drawer 都为 0%。
- 微调有帮助，但没有解决问题。Cosmos-FT 在 Close Drawer 上达到 90%，Push Button 60%，Pick Object 和 Push Object 都为 50%，Put on Plate 和 Pull Object 都为 40%，Discard Trash 为 30%，Put in Drawer 为 20%。
- 机器人步骤级结果揭示了失败发生的位置。在 Put in Drawer 中，Cosmos-FT 的接触率为 60%，但 lift、above drawer、in drawer 和 close drawer 都只有 20%；而未微调的基线通常在第一步之后就经常降到 0%。
- 论文的核心经验结论是，视觉真实性与可执行性并不一致：当前视频世界模型即使经过操作数据微调，仍然会在空间推理、接触稳定性、长时程执行和可变形物体动力学上失败。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19092v1](http://arxiv.org/abs/2604.19092v1)
