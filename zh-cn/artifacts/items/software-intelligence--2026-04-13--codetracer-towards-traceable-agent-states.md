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
## 摘要
CodeTracer 是一个面向代码智能体的追踪与诊断系统。它将智能体运行过程重建为状态转换树，并找出最早导致失败的阶段和步骤。论文还提出了 CodeTraceBench，这是一个大规模的已执行并带标注的代码智能体轨迹基准，用于失败定位。

## 问题
- 代码智能体现在会跨工具、文件、测试和环境执行长链条、多步骤工作流，因此一旦失败，很难判断运行最早是在哪里出错，以及后续哪些错误是由这一步引起的。
- 现有评估通常把整次运行压缩成单一的成功或失败标签，或者依赖小规模人工检查，这种方式无法扩展到真实的软件工程轨迹。
- 这会影响调试、智能体改进和恢复：如果系统无法定位失败起点，额外迭代常常会变成循环、浪费 token，并产生错误修改。

## 方法
- CodeTracer 通过一个可演化的提取器解析来自不同智能体框架的异构运行产物。这个提取器可以复用或生成特定格式的解析器，然后将运行过程规范化为带类型的步骤记录。
- 它构建分层追踪树：纯探索步骤保留在当前状态内，会改变状态的动作则创建子状态。这样更容易查看运行历史，也能把动作和上下文变化对应起来。
- 诊断模块会预测应对失败负责的阶段、该阶段内与错误相关的步骤，以及支持诊断的一组紧凑证据。
- 论文还基于已执行轨迹构建了 CodeTraceBench，覆盖 5 个基准、4 个智能体框架和 5 个模型骨干，并提供阶段标签和步骤级失败标注。该基准包含 3.32K 的完整划分和 1.06K 的验证划分。
- 标注采用从已观察到的失败向后追溯到最早因果责任步骤的方法。在一个 15% 的双重标注子集上，错误关键步骤标签的 Cohen's kappa 为 0.73。

## 结果
- 数据规模：作者收集了 7,936 条原始轨迹，筛选出 3,326 条用于分析，并报告更广泛基准源池中有 4,354 条已标准化且带步骤级标注的轨迹。
- CodeTraceBench 上的主要定位结果：在所有测试骨干模型上，CodeTracer 在步骤级失败定位任务中都优于 Bare LLM 和 Mini-CodeTracer。以 GPT-5 为例，F1 从 Bare LLM 的 18.78 和 Mini-CodeTracer 的 19.33 提升到 CodeTracer 的 48.02，同时 token 使用量从 58.5k 和 44.8k 降到 31.1k。
- 对 Claude-sonnet-4，CodeTracer 在 56.8k token 下达到 46.57 F1、40.47 precision 和 54.87 recall；相比之下，Bare LLM 在 105.1k token 下的 F1 为 16.22。
- 对 DeepSeek-V3.2，CodeTracer 在 44.6k token 下达到 46.14 F1；相比之下，Bare LLM 在 83.4k token 下为 16.33 F1。
- 在困难样本上，CodeTracer 仍保持明显优势：GPT-5 达到 40.14 F1，Claude-sonnet-4 为 38.67，DeepSeek-V3.2 为 38.72。
- 论文分析认为，额外迭代只有在一定范围内有帮助。例如 GPT-5 的 resolved rate 从 10 次迭代时的 38.69% 上升到 40 次时的 47.06%，但在 100 次和 >=150 次时仍停留在 47.06%，与此同时 token 从 106.19k 增加到 266.32k。
- 在他们的语料中，框架复杂度带来的成本增长大于成功率增长：MiniSWE-Agent 的成功率为 32.8%，token 为 44.6k；OpenHands 的成功率为 38.3%，token 为 91.4k；SWE-Agent 的成功率为 37.5%，token 为 86.7k。
- 他们的行为分析发现存在从证据到行动的落差：无效步骤在已解决运行中占 22%，在未解决运行中升到 40%；正确的状态变化则从 30% 降到 21%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11641v3](http://arxiv.org/abs/2604.11641v3)
