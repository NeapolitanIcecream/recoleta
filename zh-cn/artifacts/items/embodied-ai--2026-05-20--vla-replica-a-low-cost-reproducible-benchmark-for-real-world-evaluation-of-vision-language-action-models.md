---
source: arxiv
url: https://arxiv.org/abs/2605.20774v1
published_at: '2026-05-20T06:15:30'
authors:
- Alex S. Huang
- Jiahui Zhang
- Shiqing Tang
- Yu Xiang
topics:
- vision-language-action
- real-world-evaluation
- robot-benchmark
- manipulation
- reproducibility
- vla-finetuning
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models

## Summary
## 总结
VLA-REPLICA 是一个低成本、可复现的真实世界基准，用来评估视觉-语言-动作机器人策略在可重复的操作任务上的表现。它面向本地实验室评估，而不是只做仿真测试或依赖集中式机器人评测服务。

## 问题
- VLA 模型需要真实世界评估，因为当接触、光照、相机位姿和物体摆放与模拟器不同，仿真会高估性能。
- 现有的真实世界基准往往需要昂贵硬件，或只覆盖很窄的任务类型，或要求远程评测，这会拖慢本地测试。
- 这篇论文要解决一个实际缺口：不同实验室需要一种方法，能在物理机器人上运行可比的 VLA 评估，而不用购买高端设备。

## 方法
- 这个基准使用现成硬件：一只 SO-101 6-DoF 机械臂、一台 Intel RealSense D455 顶置摄像头、一台腕部摄像头、一个 32 英寸灯箱和常见物体。
- 通过相机叠加工具、AprilTag 对齐、固定光照、参考图像和预设物体摆放，用户可以在不同实验室复现相同的测试场景。
- SO-101 的动作空间通过机械臂校准进行归一化，因此示范和策略动作可以在分别搭建的机械臂之间迁移。
- 任务集包含 10 个操作任务，覆盖抓取放置、折叠毛巾、打开烤箱、擦白板、倒水或摇动、抬起和按按钮。
- 数据集包含 500 条专家示范，每个任务 50 条示范；评估覆盖 50 个分布内场景和 40 个分布外场景。

## 结果
- 完整硬件成本约为 1050 美元，列出的部件包括约 200 美元的 SO-101 机械臂、约 425 美元的 RealSense D455、13.98 美元的网络摄像头、152.99 美元的灯箱和 215.99 美元的物体套件。
- 论文的可复现性检查显示，一名不了解该基准的用户在 1 小时内搭建完成了系统。
- 这个基准定义了 90 个测试场景：10 个任务上的 50 个分布内场景，以及 8 个任务上的 40 个分布外场景。
- 所有评估策略都使用同样的 500 条示范和 4 万步训练或微调。
- 在 10 个分布内任务上，平均成功率分别为：ACT 0.18、DiT-D 0.16、DiT-F 0.12、SmolVLA 0.26、X-VLA 0.14、π0 0.34、π0.5 0.54。
- π0.5 的分布内平均成功率最高，为 0.54；按任务看，它在折叠毛巾上得分 1.0，在把面包放到盘子上得分 0.8，在把碗放到杯垫上得分 0.8。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20774v1](https://arxiv.org/abs/2605.20774v1)
