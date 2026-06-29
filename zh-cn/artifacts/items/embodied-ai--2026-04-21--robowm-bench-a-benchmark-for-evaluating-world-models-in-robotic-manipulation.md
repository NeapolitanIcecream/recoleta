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
## 摘要
RoboWM-Bench 是一个基准，用来测试世界模型生成的机器人操控视频能否转成可执行动作，并且真的完成任务。论文表明，强的视觉视频生成并不能稳定地产生可物理执行的操控行为。

## 问题
- 现有的视频世界模型基准主要关注视觉真实感、语义，或诊断性的物理合理性，但它们不会直接测试生成的操控行为能否被机器人执行。
- 这很重要，因为机器人只会从想象或生成的视频里学到东西，前提是预测行为和真实动力学、接触关系、任务约束一致。
- 真实机器人评测成本高，也难以复现，所以论文想做一个可扩展、可重复的具身评测基准。

## 方法
- 这个基准先给出初始场景观测和任务描述，让世界模型生成未来的操控视频，再把视频转成机器人动作并在仿真中执行。
- 对于人手视频，它用 HaMeR 估计三维手部姿态，并把这些姿态重定向到机器人的末端执行器动作，还改了姿态和朝向的表示，并加入夹爪信号，以便更稳定地处理接触几何。
- 对于机器人视频，它使用逆动力学模型，先在仿真中训练，再用少量真实 Franka 数据微调，从连续帧中恢复关节动作。
- 它在基于 LeHome 构建的高保真真机到仿真系统里重建真实场景，然后检查接触、抬起这类步级节点，以及最终任务是否成功。
- 任务集合覆盖刚性、可动、可变形、长时程和双手操控场景。

## 结果
- 在人手任务级评测中，Wan 2.6 是表现最强的报告模型：Pick Object 为 83%，Push Button 为 100%，Pour Water 为 80%，Open Drawer 为 80%，Put in Drawer 为 80%，Fold Towel 为 40%。较弱的模型在更难任务上经常崩溃，比如 Cosmos 在 Pour Water 和 Fold Towel 上都是 0%。
- 人手步级结果显示，早期接触比完整执行容易得多。对于 Put on Plate，几种模型都能达到 100% 接触，但最终放置成功率下降到 Cosmos 的 15%、Wan 2.2 的 55%、Wan 2.6 的 70%、Veo 3.1 的 30% 和 LVP 的 70%。
- 在机器人任务级评测中，成功率低得多。在没有任务特定微调的情况下，最好成绩是 Wan 2.6：Close Drawer 50%，Push Object 40%，Push Button 40%，Pick Object 和 Put on Plate 都是 20%，Pull Object 和 Put in Drawer 都是 0%。
- 微调有帮助，但不能解决问题。Cosmos-FT 在 Close Drawer 上达到 90%，在 Push Button 上达到 60%，在 Pick Object 和 Push Object 上达到 50%，在 Put on Plate 和 Pull Object 上达到 40%，在 Discard Trash 上达到 30%，在 Put in Drawer 上达到 20%。
- 机器人步级结果暴露了失败发生的位置。在 Put in Drawer 中，Cosmos-FT 的接触率是 60%，但在 lift、above drawer、in drawer 和 close drawer 上都只有 20%；而未微调的基线在第一步之后常常就是 0%。
- 论文的主要经验结论是，视觉真实感和可执行性会分开：当前视频世界模型在空间推理、接触稳定性、长时程执行和可变形物体动力学上仍然会失败，即使做了操控微调也是如此。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19092v1](http://arxiv.org/abs/2604.19092v1)
