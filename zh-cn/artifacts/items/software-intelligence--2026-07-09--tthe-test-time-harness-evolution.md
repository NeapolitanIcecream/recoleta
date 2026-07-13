---
source: arxiv
url: https://arxiv.org/abs/2607.08124v1
published_at: '2026-07-09T05:53:39'
authors:
- Jun Nie
- Yonggang Zhang
- Jun Song
- Qianshu Cai
- Dahai Yu
- Yike Guo
- Xinmei Tian
- Bo Han
topics:
- test-time-adaptation
- llm-agents
- code-intelligence
- automated-software-production
- agent-harnesses
- multi-agent-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# TTHE: Test-Time Harness Evolution

## Summary
## 摘要
TTHE 在评估过程中改写并选择可执行的 harness 程序，根据无标签执行轨迹调整 LLM agent 的 harness。在代码、SQL、软件工程和数据科学任务上，它在不改变模型权重、适配过程中不使用金标准标签的情况下，改进了固定的 ReAct 风格 harness。

## 问题
- LLM agent 通常使用固定的控制程序来构建上下文、调用工具、验证结果和恢复故障，因此当测试阶段的失败模式不同于开发阶段时，无法进行调整。
- 现有的提示词、工作流和模型适配方法通常在评估前运行，或更新模型参数、修改单次响应，或要求带标签的反馈。
- 执行轨迹包含运行时错误、测试结果、工具输出和格式错误的中间产物等有用信号，但这些信号无法直接说明任务是否正确，因此这个问题很重要。

## 方法
- TTHE 将 harness 而非模型权重作为适配状态。harness 是运行在冻结 LLM 外部的可执行 Python 代码。
- 对于每个无标签测试批次，TTHE 创建多个 harness 分支并运行这些分支，记录提示词、补全内容、工具调用、输出、错误、产物和运行时状态。
- agentic proposer 根据这些轨迹以及执行健康度、往返一致性和公开测试通过率等代理信号，修改各自的分支。
- agentic judge 在看不到金标准答案、隐藏测试或参考输出的情况下，选择一个最终分支。选定的 harness 会保留到下一个批次。
- 求解、提议和评判使用同一个冻结的骨干模型，因此适配通过代码变更完成，不涉及权重更新，也不需要单独训练的适配模型。

## 结果
- 在 DeepSeek-V4-Flash 上，相对于固定的 ReAct 风格基线，TTHE 将 BIRD 从 12.0% 提升到 50.0%，将 LiveCodeBench 从 30.0% 提升到 38.3%，将 SWE-bench Verified 从 20.0% 提升到 35.0%，并将 DS-1000 从 38.0% 提升到 44.0%。
- 在 BIRD 上，该方法将 MiMo V2.5 从 32.0% 提升到 52.0%，将 Kimi K2.5 从 28.0% 提升到 48.0%。
- 实验覆盖五个以执行为依据的领域，包括文本到 SQL、竞赛编程、软件工程、数据科学编程和 agentic 工具使用；摘录为其中四个领域提供了确切的主要结果数据。
- 这些增益具有传导性：每个批次都使用根据该批次无标签轨迹选出的 harness 进行测量，而金标准标签只用于选择后的评估。
- 消融实验和轨迹审计发现，搜索预算的效果并非单调变化、候选覆盖有限、选择遗憾，以及不完善的执行代理信号导致的 judge 错误，是该方法的主要局限。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08124v1](https://arxiv.org/abs/2607.08124v1)
