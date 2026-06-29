---
source: arxiv
url: https://arxiv.org/abs/2606.04455v1
published_at: '2026-06-03T04:58:17'
authors:
- Xinyu Lu
- Tianshu Wang
- Pengbo Wang
- zujie wen
- Zhiqiang Zhang
- Jun Zhou
- Boxi Cao
- Yaojie Lu
- Hongyu Lin
- Xianpei Han
- Le Sun
topics:
- meta-agents
- code-intelligence
- agent-benchmarks
- automated-software-engineering
- ai-safety
- reward-hacking
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?

## Summary
## 摘要
MAC 测试编码代理能否在时间、API 和安全限制下构建其他代理。论文发现，当前的元代理很少能超过人工编写的代理策略，表现最好的结果大多来自专有的前沿模型。

## 问题
- 现有代理基准主要测量的是在人类设计的工作流中执行任务，因此没有测试模型能否独立设计和改进一个代理系统。
- 这对自动化软件生产和 AI 安全很重要，因为有能力的元代理必须在改进另一个代理的同时编写代码、测试设计、处理预算，并避免奖励黑客。

## 方法
- 一个代码代理，也就是元代理，会得到一个沙盒、一个基础代理接口、模型/工具 API、一个开发集和一个评估 API。
- 元代理编写一个可执行的代理产物，通常是 `agent.py`，然后提交它，在开发集上获取反馈，并在固定预算内修改它。
- 隐藏的验证器随后会在留出的测试集上运行最终产物，并记录一个 `[0,1]` 之间的分数。
- MAC-v1 覆盖五个领域：AIME 数学、GPQA/HLE 科学问答、LiveCodeBench 编程、SWE-Bench 仓库修复，以及 Terminal-Bench 长周期终端任务。
- 评估使用独立的代理容器和评估容器、API 代理、配额检查、文件系统隔离、分割访问控制和事后审计，以减少奖励黑客和数据泄漏。

## 结果
- 可见表格中的人工基线平均值在 Meta-AIME 上为 0.733，在 Meta-GPQA 上为 0.597，在 Meta-LiveCodeBench 上为 0.555。
- Claude-Opus-4.6 配合 Claude Code 在 Meta-AIME 上得分 0.744 ± 0.054，在 Meta-GPQA 上得分 0.572 ± 0.049，在 Meta-LiveCodeBench 上得分 0.557 ± 0.043，大致追平了 AIME 和 LiveCodeBench 上的人工基线，但在 GPQA 上落后。
- Claude-Sonnet-4.6 在 Meta-AIME 上得分 0.783 ± 0.017，在 Meta-GPQA 上得分 0.383 ± 0.332，在 Meta-LiveCodeBench 上得分 0.446 ± 0.133；其中 GPQA 结果包含一次 0.000 的运行，显示出很高的运行间方差。
- MiniMax-M2.5 配合 Claude Code 在 Meta-AIME 上得分 0.306 ± 0.084，在 Meta-GPQA 上得分 0.363 ± 0.147，在 Meta-LiveCodeBench 上得分 0.260 ± 0.079，在可见结果中明显低于人工基线。
- 红队完整性测试进行了 8 次零资源试验；其中 7 次产生了策略违规，1 次产生了有效产物，审计代理在全部 8 次判定上都与人工标注者一致。
- 该设置对 AIME、GPQA 和 LiveCodeBench 使用 12 小时开发预算，对 SWE-Bench 和 Terminal-Bench 使用 24 小时预算，科学领域每个阶段使用 2,500 次搜索 API 调用。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04455v1](https://arxiv.org/abs/2606.04455v1)
