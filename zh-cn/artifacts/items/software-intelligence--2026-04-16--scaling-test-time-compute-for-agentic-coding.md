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
## 摘要
这篇论文通过把测试时算力用于多次完整的 agent rollout，并选择和复用这些尝试中的有用部分，提升了 agentic coding 的效果。核心思路是用简短的结构化摘要替代冗长且嘈杂的轨迹，从而同时改进选择和后续细化。

## 问题
- Agentic coding 任务会在许多终端步骤中产生很长的动作-观察轨迹，因此数学推理或单次代码生成中的标准 test-time scaling 方法很难直接迁移过来。
- 原始轨迹难以比较，也难以复用，因为其中混杂了有用线索、重复日志、错误和走不通的尝试。
- 这很重要，因为 SWE-Bench Verified 和 Terminal-Bench v2.0 这类基准依赖长程调试和编辑，更有效地使用推理算力可以在不改变基础模型的情况下提高通过率。

## 方法
- 该方法把每次 rollout 转成紧凑的结构化摘要，记录关键诊断、尝试过的修复、进展和失败模式。
- 对于并行扩展，它使用 **Recursive Tournament Voting (RTV)**：运行 **N=16** 个 rollout，对它们做摘要，在小组内比较这些摘要，并重复这一过程直到只剩下一个 rollout。默认设置使用两两分组（**G=2**）和 **V=8** 次比较投票。
- 对于顺序扩展，它把 **Parallel-Distill-Refine (PDR)** 适配到 agentic coding：用前一轮中 **K=4** 个摘要构造细化上下文，然后在重置后的环境中、基于这些摘要启动一次全新的 rollout。
- 完整流程是：第 0 轮 rollouts，**RTV** 选出 top-**K**，第 1 轮细化 rollouts，然后再做最终的 **RTV** 选择。
- 消融实验显示，结构化摘要比完整轨迹更适合做选择；递归的两两比较比一次性多路比较效果更好；基于多个先前摘要做细化比只基于一个摘要更好。

## 结果
- **SWE-Bench Verified** 上完整流程的主要提升：Claude-4.5-Opus **70.94% → 77.60%**（+6.66），Gemini-3.1-Pro **72.25% → 76.60%**（+4.35），Claude-4.5-Sonnet **67.41% → 75.60%**（+8.19），Gemini-3-Flash **70.79% → 76.00%**（+5.21），GPT-5-0825 **61.41% → 69.80%**（+8.39）。
- **Terminal-Bench v2.0** 上完整流程的主要提升：Claude-4.5-Opus **46.95% → 59.09%**（+12.14），Gemini-3.1-Pro **52.49% → 64.77%**（+12.28），Claude-4.5-Sonnet **40.62% → 56.82%**（+16.20），Gemini-3-Flash **37.93% → 48.86%**（+10.93），GPT-5-0825 **31.32% → 38.64%**（+7.32）。
- 单独使用 **RTV** 也有帮助。例如，Claude-4.5-Sonnet 在 SWE-Bench Verified 上从 **67.4% 提升到 73.6%**，在 Terminal-Bench v2.0 上从 **40.6% 提升到 54.6%**，设置为 **N=16, G=2, V=8**。
- 在对 100 个抽样 SWE-Bench Verified 任务进行顺序细化时，Gemini-3.1-Pro 从 **72.69% 提升到 73.75%**（单次 rollout 细化），用 random-**K** 细化时从 **72.69% 提升到 76.94%**，用 **RTV** 选出的 **K=4** 个摘要细化时从 **72.69% 提升到 79.25%**。Claude-4.5-Sonnet 在 select-**K** 细化下达到 **78.06%**。
- 上下文质量可以预测下一轮是否成功。当选出的先前 **K=4** 个 rollout 中有 **4/4** 个通过时，第 1 轮通过率会上升到约 **97.3%**（Claude-4.5-Sonnet）和 **99.7%**（Gemini-3.1-Pro）。
- 顺序细化还把 Table 4 中的平均 agent 步数降到约一半，同时提升了 pass@1。论文还指出，这个方法解决了部分任务，而最初的 **16** 个 rollout 没有一个解出这些任务。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16529v1](http://arxiv.org/abs/2604.16529v1)
