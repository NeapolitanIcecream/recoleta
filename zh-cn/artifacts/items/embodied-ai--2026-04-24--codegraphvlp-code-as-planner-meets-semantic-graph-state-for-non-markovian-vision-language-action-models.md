---
source: arxiv
url: http://arxiv.org/abs/2604.22238v1
published_at: '2026-04-24T05:27:27'
authors:
- Khoa Vo
- Sieu Tran
- Taisei Hanyu
- Yuki Ikebe
- Duy Nguyen
- Bui Duy Quoc Nghi
- Minh Vu
- Anthony Gunderman
- Chase Rainwater
- Anh Nguyen
- Ngan Le
topics:
- vision-language-action
- long-horizon-manipulation
- non-markovian-planning
- semantic-graph-state
- code-as-planner
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models

## Summary
## 摘要
CodeGraphVLP 面向长时程机器人操作任务，这类任务的下一步动作取决于更早的观测，而不只是当前相机画面。它把持久化语义图、一次性生成的代码规划器和面向对象的提示结合起来，用于 VLA 策略。

## 问题
- 标准的视觉-语言-动作模型通常只根据最新观测来执行，在非马尔可夫任务上会失效，因为关键证据可能被遮挡，或者只在更早的轨迹中出现。
- 基于历史的扩展可能会错过过去稀疏出现的证据，或者在上下文窗口变大时带来延迟和计算开销。
- 带有 VLM 参与的分层规划器能改善长时程推理，但反复调用模型很慢，而且只用语言描述子任务，在杂乱场景里仍然容易出现视觉对齐不稳的问题。

## 方法
- 系统通过分割、相关性过滤、跨视角关联、跟踪和基于规则的关系归纳，持续构建和更新一个包含任务相关对象、属性和关系的持久语义图。
- 在任务开始时调用一次 LLM，写出一个任务特定的 Python 规划器。它读取语义图，用简单谓词检查进度，保存轻量级任务记忆，并输出下一步子任务和相关对象。
- 执行器 VLA 不会看到完整的杂乱场景。它接收一条简短的子任务指令，以及只保留规划器选中对象的掩膜图像。
- 训练方式与部署方式一致：录制的演示被转换为带子任务条件、带掩膜的观测，随后 VLA 在这些输入上用模仿学习进行微调。

## 结果
- 在三个真实世界桌面任务上，CodeGraphVLP 的平均成功率为 **81.7%**，高于 **Gr00T N1.5 + Multi-frame: 56.7%**、**Gr00T N1.5: 31.7%**、**π0: 30.0%**、**π0.5: 5.0%** 和 **π0 FAST: 0.0%**。
- 在 **Pick-and-Place Twice** 上，CodeGraphVLP 的完整成功率为 **80%**，中间指标 "PnP Once" 为 **100%**；对比之下，**Gr00T N1.5 + Multi-frame** 为 **75% / 100%**，**Gr00T N1.5** 为 **35% / 50%**。
- 在 **Place-and-Stack** 上，CodeGraphVLP 的成功率为 **80%**，中间指标 "Drop Cube" 为 **95%**；对比之下，**Gr00T N1.5 + Multi-frame** 为 **50% / 50%**，**Gr00T N1.5** 为 **40% / 40%**。
- 在 **Swap Cups** 上，CodeGraphVLP 的成功率为 **85%**，中间指标 "Stage Cup" 为 **100%**；对比之下，**Gr00T N1.5 + Multi-frame** 为 **45% / 90%**，**Gr00T N1.5** 为 **20% / 70%**。
- 论文还声称，与 VLM-in-the-loop 规划相比，它的规划延迟明显更低，但这段摘要没有给出具体延迟数值。
- 真实世界设置中的训练数据规模为：**Pick-and-Place Twice** 100 个演示，**Place-and-Stack** 100 个演示，**Swap Cups** 200 个演示。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22238v1](http://arxiv.org/abs/2604.22238v1)
