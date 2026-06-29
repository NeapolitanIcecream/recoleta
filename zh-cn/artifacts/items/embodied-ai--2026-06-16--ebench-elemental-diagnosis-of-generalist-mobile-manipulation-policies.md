---
source: arxiv
url: https://arxiv.org/abs/2606.18239v1
published_at: '2026-06-16T17:58:22'
authors:
- Ning Gao
- Jinliang Zheng
- Xing Gao
- Haoxiang Ma
- Hanqing Wang
- Yukai Wang
- Jiantong Chen
- Zanxin Chen
- Shujie Zhang
- Mingda Jia
- Xuekun Jiang
- Zihou Zhu
- Xinyu Li
- Shuai Wang
- Hao Li
- Wenzhe Cai
- Yuqiang Yang
- Xudong Xu
- Zhaoyang Lyu
- Yao Mu
- Tai Wang
- Jiangmiao Pang
- Jia Zeng
- Weinan Zhang
- Chunhua Shen
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- mobile-manipulation
- robot-benchmark
- robot-data-scaling
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# EBench: Elemental Diagnosis of Generalist Mobile Manipulation Policies

## Summary
## 摘要
EBench 是一个仿真基准，用于诊断通用移动操作策略在移动、长时程和灵巧任务中的表现。它表明，相近的总体成功率可能掩盖技能、精度、任务时程和分布外行为上的明显差异。

## 问题
- 当前机器人操作基准常把性能压缩成一个成功率数字，这会隐藏通用策略在哪些地方成功或失败。
- 许多套件只覆盖较窄的场景，例如桌面抓取放置、移动重排，或某一项孤立能力，因此会遗漏移动、长时程和高精度操作的组合能力。
- 这一点很重要，因为具身基础模型和视觉-语言-动作策略在真实机器人部署前需要能解释失败模式的诊断信号。

## 方法
- EBench 定义了 26 个仿真任务：10 个移动抓取放置任务、9 个移动长时程任务，以及 7 个固定基座的灵巧且精确的任务。
- 每个任务沿 5 个能力轴标注：场景类型、原子技能、时间时程、精度和操作模式。
- 该基准测试 4 类泛化偏移：未见过的背景、未见过的物体、改写后的指令，以及它们的混合，同时保持训练/测试资产池相互分离。
- 数据采集对 7 个灵巧任务使用遥操作，对 19 个移动或长时程任务使用关键帧位姿加 cuRobo 运动规划。
- 数据集包含 6,600 个演示 episode 和 91.4 小时演示，并使用二值成功率和分阶段部分进度分数进行评估。

## 结果
- 在 π0、π0.5、XVLA 和 InternVLA-A1 中，总体测试成功率接近，范围为 24.4% 到 29.5%，但能力画像差异很大。
- π0.5 的总体测试结果最好：SR 为 29.5%，Score 为 45.6%，从 Val-Train 到 Test 的保持率为 SR 0.92、Score 0.95。
- InternVLA-A1 的测试 SR 达到 27.6%，在移动操作上表现较好，SR 约为 34.7%，但在灵巧固定基座任务上降至 5.8% SR，差距为 29 个百分点。
- π0 在亚厘米级高精度任务上领先，SR 为 13.8%；π0.5 在低精度任务上领先，SR 为 44.2%。
- 组合偏移下的泛化最难：Background 和 Instruction 变体的 SR 为 27% 到 35%，Object 替换使 SR 降至 21% 到 29%，Mix 降至 18% 到 23%。
- 预训练在 EBench 上带来的提升大于在 LIBERO 或 RoboTwin 2.0 Hard 上的提升：π0 的 SR 从 11.2% 提高到 24.4%，π0.5 从 8.5% 提高到 29.5%，XVLA 从 15.7% 提高到 24.7%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18239v1](https://arxiv.org/abs/2606.18239v1)
