---
source: arxiv
url: http://arxiv.org/abs/2604.11641v3
published_at: '2026-04-13T15:52:03'
authors:
- Han Li
- Yifan Yao
- Letian Zhu
- Rili Feng
- Hongyi Ye
- Jiaming Wang
- Yancheng He
- Pengyu Zou
- Lehan Zhang
- Xinping Lei
- Haoyang Huang
- Ken Deng
- Ming Sun
- Zhaoxiang Zhang
- He Ye
- Jiaheng Liu
topics:
- code-agents
- agent-tracing
- failure-localization
- software-engineering-benchmark
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CodeTracer: Towards Traceable Agent States

## Summary
## 总结
CodeTracer 是一个面向代码代理的追踪与诊断系统，它把代理运行重建为状态转移树，并找出最早导致失败的阶段和步骤。论文还提出了 CodeTraceBench，这是一个包含已执行并带标注的代码代理轨迹的大型基准，用于失败定位。

## 问题
- 代码代理现在会在工具、文件、测试和环境之间执行很长的多步工作流，因此一旦失败，就很难看出运行最早在哪一步出错，以及后续错误中哪些来自那个失误。
- 现有评估通常把整次运行压缩成一个成功或失败标签，或者依赖少量人工检查，这种做法难以扩展到真实的软件工程轨迹。
- 这会影响调试、代理改进和恢复：如果系统无法定位失败起点，额外迭代往往只会变成循环、浪费 token 和错误修改。

## 方法
- CodeTracer 用一个可演化的提取器解析来自不同代理框架的异构运行工件，这个提取器可以复用或合成特定格式的解析器，然后把运行归一化为带类型的步骤记录。
- 它构建了一棵分层追踪树。纯探索步骤保留在当前状态内，会改变状态的动作则创建子状态。这样更容易浏览运行历史，也能把动作和上下文变化关联起来。
- 诊断模块会预测负责失败的阶段、该阶段内与错误相关的步骤，以及支持诊断的精简证据集。
- 论文还基于 5 个基准、4 个代理框架和 5 个模型骨干构建了 CodeTraceBench，带有阶段标签和步骤级失败标注。基准包含一个 3.32K 的完整划分和一个 1.06K 的验证划分。
- 标注过程使用从观察到的失败向后追踪到最早因果责任步骤的方法。在 15% 的双重标注子集上，错误关键步骤标签的 Cohen's kappa 为 0.73。

## 结果
- 数据规模：作者收集了 7,936 条原始轨迹，筛选后用于分析的轨迹为 3,326 条，并在更大的基准来源池中报告了 4,354 条标准化且带步骤级标注的轨迹。
- CodeTraceBench 上的主要定位结果：CodeTracer 在所有测试骨干上都优于 Bare LLM 和 Mini-CodeTracer 的步骤级失败定位。对 GPT-5，F1 从 18.78（Bare LLM）和 19.33（Mini-CodeTracer）提升到 48.02，同时 token 使用量从 58.5k 和 44.8k 降到 31.1k。
- 对 Claude-sonnet-4，CodeTracer 在 56.8k token 下达到 46.57 F1、40.47 precision 和 54.87 recall；Bare LLM 在 105.1k token 下的 F1 为 16.22。
- 对 DeepSeek-V3.2，CodeTracer 在 44.6k token 下达到 46.14 F1；Bare LLM 在 83.4k token 下的 F1 为 16.33。
- 在困难样本上，CodeTracer 仍保持明显优势：GPT-5 的 F1 为 40.14，Claude-sonnet-4 为 38.67，DeepSeek-V3.2 为 38.72。
- 分析表明，额外迭代只在一定范围内有效。例如，GPT-5 的解决率从 10 次迭代时的 38.69% 提升到 40 次迭代时的 47.06%，但在 100 次和 >=150 次迭代时仍保持 47.06%，而 token 从 106.19k 增加到 266.32k。
- 在他们的数据集中，框架复杂度带来的成本增长大于成功率增长：MiniSWE-Agent 的成功率为 32.8%，token 为 44.6k；OpenHands 的成功率为 38.3%，token 为 91.4k；SWE-Agent 的成功率为 37.5%，token 为 86.7k。
- 他们的行为分析发现了证据到动作之间的差距：无效步骤在已解决运行中从 22% 上升到未解决运行中的 40%，而正确的状态变化从 30% 降到 21%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11641v3](http://arxiv.org/abs/2604.11641v3)
