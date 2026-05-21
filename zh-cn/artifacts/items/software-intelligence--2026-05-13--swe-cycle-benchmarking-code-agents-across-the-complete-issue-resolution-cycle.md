---
source: arxiv
url: https://arxiv.org/abs/2605.13139v1
published_at: '2026-05-13T08:05:16'
authors:
- Hao Guan
- Lingyue Fu
- Shao Zhang
- Yaoming Zhu
- Kangning Zhang
- Lin Qiu
- Xunliang Cai
- Xuezhi Cao
- Weiwen Liu
- Weinan Zhang
- Yong Yu
topics:
- code-agents
- software-benchmarks
- issue-resolution
- agent-evaluation
- test-generation
- environment-reconstruction
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle

## Summary
## 摘要
SWE-Cycle 是一个包含 489 个实例的基准，用来测试代码代理能否端到端解决真实 GitHub issue：搭建环境、修改代码，并编写验证测试。它的评估器 SWE-Judge 将代码审查与执行结合，在抽样案例中与人工标签的一致率超过 95%。

## 问题
- 现有 SWE-bench 式评估为代理提供预建环境和固定测试，因此会漏掉依赖搭建和测试设计中的失败。
- 静态解析器和固定单元测试脚本可能拒绝有效补丁，接受浅层测试投机，并且无法处理自主代理轨迹。
- 这一点很关键，因为有用的编码代理必须能接手一个原始仓库、实现修复，并在没有人工设置的情况下验证结果。

## 方法
- 作者基于 SWE-bench Verified、SWE-bench Pro 和 SWE-bench Multilingual 构建 SWE-Cycle，经过污染、复杂度和测试可靠性过滤后，将 1,531 个初始实例减少到 489 个。
- 每个实例包含三个隔离任务：环境重建、代码实现和验证测试生成。
- FullCycle 任务只给代理一个原始仓库和 issue 描述，然后要求它在一次自主运行中完成全部三个阶段。
- SWE-Judge 用静态审查加动态执行为输出打分，使用 0-2 分并归一化到 0-1。
- 在 FullCycle 评估中，SWE-Judge 先检查环境，再评估生成的测试，在需要时改进较差的测试，然后测试提交的实现。

## 结果
- SWE-Judge 与人工标注的一致率为：Env 99.3%（N=143）、Impl 95.6%（N=113）、TestGen 99.5%（N=201）、FullCycle 96.9%（N=489）。
- 在隔离任务上，报告的最佳解决率分别是 Env 78.12%、Impl 40.08%、TestGen 67.28%，均由 Claude-Sonnet-4.6 取得。
- 摘录中每个模型的 FullCycle 解决率都低于 14%；GLM-5.1 达到 13.50%，Claude-Sonnet-4.6 达到 12.27%。
- 摘录中的 FullCycle 平均分为 GLM-5.1 的 81.49 和 Claude-Sonnet-4.6 的 80.52，而严格解决率低得多，说明局部进展不能转化为完整的 issue 解决。
- 该基准评估六个由 LLM 支持的代理：GPT-5.4、Claude-Sonnet-4.6、Qwen-3.5、GLM-5.1、Kimi-K2.5 和 MiniMax-M2.7。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13139v1](https://arxiv.org/abs/2605.13139v1)
