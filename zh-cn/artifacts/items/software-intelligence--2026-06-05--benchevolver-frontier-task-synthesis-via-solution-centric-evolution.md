---
source: hn
url: https://benchevolver.github.io/
published_at: '2026-06-05T23:39:52'
authors:
- matt_d
topics:
- code-benchmarking
- code-intelligence
- software-foundation-models
- automated-evaluation
- rl-training
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# BenchEvolver: Frontier Task Synthesis via Solution-Centric Evolution

## Summary
## 概要
BenchEvolver 先改参考解，再围绕这个可执行解写题目和测试，从而生成更难、可验证的编程任务。它针对代码评测里基准饱和的问题，因为当前模型在较容易的 LiveCodeBench 切分上已经接近满分。

## 问题
- 现有编程基准已经接近饱和：前沿模型在 LiveCodeBench easy 上的 Pass@1 超过 99%，平均也超过 90%，因此这些测试已经很难把强模型区分开。
- 手工构建更难的编程数据集速度慢、成本高，这限制了对代码模型进展的测量。
- 许多生成式任务只改写措辞或表面故事，推理方式却很相近，因此没有带来足够新的算法需求。

## 方法
- BenchEvolver 先改动参考解，让它需要更强的算法，再基于这个可执行解派生题面、示例和隐藏测试。
- Proposer 生成演化后的解和题目文本；Evaluator 检查正确性并测量难度；Memory 把已接受的谱系和过去的失败结果带入后续搜索。
- 验证阶段会交叉比对演化后的参考解、暴力求解器和只看题面就能判断的 oracle，然后在出现不一致时做有界修复。
- 只有当目标模型组在新任务上的失败率高于种子任务时，任务才会被接受，所以难度是通过真实模型表现来测量的。
- 示例提升包括把数组差分的区间交集问题改成 XOR 约束下的数位 DP，以及把 RK4 积分改成带高斯-牛顿法的非线性参数和初始状态估计。

## 结果
- 在 LiveCodeBench 上，论文报告前沿模型在最新 easy 切分上的 Pass@1 超过 99%，平均超过 90%，这推动了更难的评测需求。
- 作者构建了一个 91 题基准，来自 64 个经过人工审核的演化任务和 27 个困难的原始 LCB-v6 任务；每道题都通过了正确性、至少 3/5 的质量评分，以及难度范围门槛。
- 在这个基准上，前沿模型的 Pass@1 介于 27.5% 到 62.6% 之间，比已经饱和的 easy 切分更能拉开强模型差距。
- 在评测模型的平均结果上，Hard 切分从 87.0% 降到 45.7% Pass@1，绝对下降 41.3 个百分点。
- 6 位竞赛编程专家审查了 72 个种子上的 207 个演化问题，认为这些任务比种子题更新颖、难得多、算法覆盖更广，而且更清晰。
- 以 gpt-oss-20b 同时作为演化器和目标模型时，在演化任务上做 RL 训练，比只用原始种子训练更能提升留出集上的代码表现；摘录没有给出这个结果的具体提升幅度。

## Problem

## Approach

## Results

## Link
- [https://benchevolver.github.io/](https://benchevolver.github.io/)
