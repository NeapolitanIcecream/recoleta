---
source: arxiv
url: https://arxiv.org/abs/2605.27461v1
published_at: '2026-05-25T20:46:22'
authors:
- Brian Zhu
- Philipp Schmitt
- Philine Meister
- Lukas Gensler
- Momen Khalil
- Emmanuele Poggi
- Johannes Hechtl
- Carsten Braunroth
- Kai Wurm
- Gokul Narayanan
- Eugen Solowjow
- Georg von Wichert
- Andre Scholz
- Felix Albrecht
- Maxmillian Metzner
topics:
- vision-language-action
- robot-foundation-model
- industrial-robotics
- robot-data-scaling
- factory-deployment
- manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons

## Summary
## 摘要
这篇论文是一个工厂现场案例研究，内容是针对西门子的一项包装任务，对预训练的 Pi0.5 VLA 策略进行微调。它的主要价值在于记录了部署流程和失败分析，而不是提出新的模型架构。

## 问题
- 机器人必须从一堆杂乱的物料中抓取一个透明配件袋，把它放进纸盒的腔体里，并让袋内物品保持在盒盖闭合平面以下。
- 这个任务之所以重要，是因为生产场景需要在遮挡、紧张节拍、安全运动和严格的下游质量检查下保持稳定操作。
- 实验室里的 VLA 演示常常掩盖实际问题，比如遥操作延迟、相机视角差、透明物体，以及抓取失败后的恢复。

## 方法
- 团队通过反复的数据收集、人工审核、训练、评估和针对性的恢复数据，调整了一个预训练的 Pi0.5 策略，使其适配任务。
- 他们使用 UR7e 机械臂、Robotiq 2F-85 夹爪、腕部相机、底座相机、Meta Quest 3 遥操作设备和一台 RTX 5090 工业电脑，采集了 2,535 段工厂轨迹，约 10 小时。
- 一开始他们把任务简化为三个约束：袋内物品已沉降、无需重新摆放袋子、料箱中袋子更少。后续轮次逐步去掉这些约束。
- 前两轮训练使用 LoRA 微调，batch size 为 32，训练 30k 步；第三轮后改为全量微调，batch size 为 128，训练 60k 步，约 4 个 epoch。
- 执行方案利用重力让运输过程中袋内物品沉降，然后用第二只机械臂把伸出的物品推回纸盒腔体内。

## 结果
- 数据集包含 2,535 段轨迹：693 段受约束轨迹、199 段取消“无需重新摆放”约束的轨迹、1,401 段无约束轨迹、242 段恢复轨迹，以及大约 900 段更早的 mock-cell 轨迹，用来改进执行方案。
- 在微调前，人工审核删除了不到 5% 的采集轨迹。
- 论文要求在进入下一轮数据采集前，评估成功率至少达到 70%，但没有报告最后一轮训练后的总体最终成功率。
- 最终评估使用了模拟清空装有 30 个随机摆放袋子的料箱的测试，每个抓放回合限时 1 分钟。
- 在无约束的第 2 和第 3 次试验中，最常见的错误是袋内物品留在产品上方：失败回合中这一问题占 65%，其中第 2 次试验为 62%，第 3 次试验为 69%。
- 其他报告的失败率中，失败回合里多袋同时被抓起占 23%，袋子没有完全放入盒内占 15%，抓取不佳或抓取失败占 15%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27461v1](https://arxiv.org/abs/2605.27461v1)
