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
SWE-Cycle 是一个包含 489 个实例的基准，用来测试代码代理能否端到端解决真实的 GitHub issue：搭建环境、修改代码，并编写验证测试。它的评估器 SWE-Judge 结合代码审查和执行结果，在抽样案例中与人工标注的匹配率超过 95%。

## 问题
- 现有的 SWE-bench 风格评估会给代理预先搭好的环境和固定测试，因此看不到依赖安装和测试设计中的失败。
- 静态解析器和固定的单元测试脚本会拒绝有效补丁、接受浅层的测试投机做法，并且在自主代理轨迹上出错。
- 这很重要，因为有用的编码代理必须能接手一个原始仓库，完成修复，并在没有人工搭建的情况下验证结果。

## 方法
- 作者基于 SWE-bench Verified、SWE-bench Pro 和 SWE-bench Multilingual 构建 SWE-Cycle，在经过污染、复杂度和测试可靠性过滤后，把 1,531 个初始实例缩减到 489 个。
- 每个实例都有三个独立任务：环境重建、代码实现和验证测试生成。
- FullCycle 任务只给代理一个原始仓库和 issue 描述，然后要求它在一次自主运行中完成全部三个阶段。
- SWE-Judge 用静态审查加动态执行来评分，分数为 0-2，并归一化到 0-1。
- 在 FullCycle 评估中，SWE-Judge 先检查环境，再评估生成的测试，必要时修正质量较差的测试，然后测试提交的实现。

## 结果
- SWE-Judge 与人工标注的一致率在 Env（N=143）上为 99.3%，在 Impl（N=113）上为 95.6%，在 TestGen（N=201）上为 99.5%，在 FullCycle（N=489）上为 96.9%。
- 在独立任务上，已报告的最高解决率分别是 Env 的 78.12%、Impl 的 40.08% 和 TestGen 的 67.28%，都来自 Claude-Sonnet-4.6。
- 在文段所示的结果里，FullCycle 的解决率对每个模型都低于 14%；GLM-5.1 达到 13.50%，Claude-Sonnet-4.6 达到 12.27%。
- 文段中的 FullCycle 平均分里，GLM-5.1 为 81.49，Claude-Sonnet-4.6 为 80.52，但严格解决率低得多，说明部分进展并不能转化为完整的问题修复。
- 该基准评估了六个基于 LLM 的代理：GPT-5.4、Claude-Sonnet-4.6、Qwen-3.5、GLM-5.1、Kimi-K2.5 和 MiniMax-M2.7。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13139v1](https://arxiv.org/abs/2605.13139v1)
