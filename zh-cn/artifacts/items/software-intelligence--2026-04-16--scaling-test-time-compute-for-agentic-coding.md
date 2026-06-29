---
source: arxiv
url: http://arxiv.org/abs/2604.16529v1
published_at: '2026-04-16T17:39:33'
authors:
- Joongwon Kim
- Wannan Yang
- Kelvin Niu
- Hongming Zhang
- Yun Zhu
- Eryk Helenowski
- Ruan Silva
- Zhengxing Chen
- Srinivasan Iyer
- Manzil Zaheer
- Daniel Fried
- Hannaneh Hajishirzi
- Sanjeev Arora
- Gabriel Synnaeve
- Ruslan Salakhutdinov
- Anirudh Goyal
topics:
- agentic-coding
- test-time-scaling
- code-intelligence
- multi-agent-software-engineering
- swe-bench
- terminal-bench
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Scaling Test-Time Compute for Agentic Coding

## Summary
## 总结
本文通过在测试时计算上运行多个完整的智能体轨迹，再挑选并复用这些尝试中的有效部分，来改进智能体编码。核心思路是把冗长、噪声较多的轨迹替换成简短、结构化的摘要，从而同时提升筛选和后续改进效果。

## 问题
- 智能体编码任务会在多个终端步骤中产生很长的动作-观察轨迹，因此来自数学推理或单次代码生成的标准测试时缩放方法不太适用。
- 原始轨迹很难比较，也很难复用，因为其中混杂了有用线索、重复日志、错误和死胡同。
- 这很重要，因为 SWE-Bench Verified 和 Terminal-Bench v2.0 这类基准依赖长程调试和编辑，而更好的推理计算分配方式可以在不改变基础模型的情况下提高通过率。

## 方法
- 该方法把每次 rollout 转成一份紧凑的结构化摘要，记录关键诊断、尝试过的修复、进展和失败模式。
- 对于并行缩放，它使用 **Recursive Tournament Voting (RTV)**：运行 **N=16** 次 rollout，对它们做摘要，小组内比较摘要，并重复这一过程直到只剩一个 rollout。默认设置使用成对分组（**G=2**）和 **V=8** 次比较投票。
- 对于顺序缩放，它把 **Parallel-Distill-Refine (PDR)** 改造成适用于智能体编码：用上一轮的 **K=4** 个摘要构建一个精炼上下文，然后在重置后的环境中，基于这些摘要启动一次新的 rollout。
- 完整流程是：第 0 轮 rollout、用 **RTV** 选出前 **K** 个、第 1 轮精炼 rollout，然后进行最终的 **RTV** 选择。
- 消融实验表明，用结构化摘要做筛选比用完整轨迹更好，成对的递归比较比平铺式的多路比较更好，而基于多个先前摘要进行精炼也比只用一个摘要更好。

## 结果
- 在 **SWE-Bench Verified** 上，完整流程的主要提升为：Claude-4.5-Opus **70.94% → 77.60%**（+6.66），Gemini-3.1-Pro **72.25% → 76.60%**（+4.35），Claude-4.5-Sonnet **67.41% → 75.60%**（+8.19），Gemini-3-Flash **70.79% → 76.00%**（+5.21），GPT-5-0825 **61.41% → 69.80%**（+8.39）。
- 在 **Terminal-Bench v2.0** 上，完整流程的主要提升为：Claude-4.5-Opus **46.95% → 59.09%**（+12.14），Gemini-3.1-Pro **52.49% → 64.77%**（+12.28），Claude-4.5-Sonnet **40.62% → 56.82%**（+16.20），Gemini-3-Flash **37.93% → 48.86%**（+10.93），GPT-5-0825 **31.32% → 38.64%**（+7.32）。
- **RTV** 本身就有效。比如在 **N=16, G=2, V=8** 的设置下，Claude-4.5-Sonnet 在 SWE-Bench Verified 上从 **67.4%** 提升到 **73.6%**，在 Terminal-Bench v2.0 上从 **40.6%** 提升到 **54.6%**。
- 在对 100 个 SWE-Bench Verified 任务做顺序精炼时，Gemini-3.1-Pro 用单次 rollout 精炼时从 **72.69% → 73.75%**，用随机 **K** 精炼时从 **72.69% → 76.94%**，用 **RTV** 选出的 **K=4** 摘要时从 **72.69% → 79.25%**。Claude-4.5-Sonnet 用 select-**K** 精炼时达到 **78.06%**。
- 上下文质量能预测下一轮成功率。当精炼上下文包含 **4/4** 个通过的 rollout 时，使用 **K=4** 个筛选后的先前 rollout，下一轮通过率会上升到约 Claude-4.5-Sonnet 的 **97.3%** 和 Gemini-3.1-Pro 的 **99.7%**。
- 顺序精炼在提高 pass@1 的同时，也把 Table 4 中的平均智能体步骤数减少了约一半，论文还指出，该方法解决了一些初始 **16** 次 rollout 都没解决的任务。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16529v1](http://arxiv.org/abs/2604.16529v1)
