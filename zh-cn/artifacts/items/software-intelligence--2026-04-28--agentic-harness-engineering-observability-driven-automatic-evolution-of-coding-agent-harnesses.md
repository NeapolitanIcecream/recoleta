---
source: arxiv
url: https://arxiv.org/abs/2604.25850v4
published_at: '2026-04-28T16:55:02'
authors:
- Jiahang Lin
- Shichun Liu
- Chengjun Pan
- Lizhi Lin
- Shihan Dou
- Zhiheng Xi
- Xuanjing Huang
- Hang Yan
- Zhenhua Han
- Tao Gui
- Yu-Gang Jiang
topics:
- coding-agents
- harness-optimization
- software-foundation-models
- code-intelligence
- agent-evaluation
- automated-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses

## Summary
## 摘要
AHE 是一个自动化循环，它使用结构化 rollout 证据和已测量的编辑结果来修改编码智能体的 harness。论文称，它将 Terminal-Bench 2 的 pass@1 从 69.7% 提高到 77.0%，并且无需重新演化即可迁移到 SWE-bench-verified 和其他模型系列。

## 问题
- 编码智能体的性能取决于模型周围的 harness：提示词、工具、中间件、记忆、技能和执行控制。
- Harness engineering 大多依赖人工；当基础模型、任务和工具需求变化时，这会拖慢适配。
- 自动化修改 harness 很难，因为原始轨迹规模大，可编辑部分类型不一，且通过率变化很难归因到某一次编辑。

## 方法
- AHE 在 NexAU 中将七类可编辑 harness 组件暴露为文件：系统提示词、工具描述、工具实现、中间件、技能、子智能体配置和长期记忆。
- 它运行任务 rollout，清理轨迹，并使用 Agent Debugger 将原始轨迹转成按任务划分的报告和一个基准级证据文件。
- Evolve Agent 读取这些证据，编辑 harness 文件，并为每项变更写入 manifest，其中包含失败证据、根因、修复、预期任务收益和回归风险。
- 下一轮迭代会用任务级结果检查这些预测，并在文件级回滚被拒绝的编辑。
- 种子 harness 被刻意设计得很小：一个 shell 工具，没有中间件，没有技能，没有子智能体。

## 结果
- 在 Terminal-Bench 2 上，10 轮 AHE 迭代将 NexAU₀ 的 pass@1 从 69.7% 提高到 77.0%，在 89 个任务上提升 +7.3 个百分点。
- 在 Terminal-Bench 2 总体 pass@1 上，AHE 超过 OpenCode 的 47.2%、Terminus-2 的 62.9%、Codex 的 71.9%、ACE 的 68.9% 和 Training-Free GRPO 的 72.3%。
- 按 Terminal-Bench 2 难度划分，AHE 在 Easy 上得分 100.0%，在 Medium 上得分 88.2%，在 Hard 上得分 53.3%；Codex 在 Hard 上更高，为 56.7%。
- 在 SWE-bench-verified 上，冻结的 AHE harness 在 500 个任务上达到 75.6% 的成功率，相比之下 NexAU₀ 为 75.2%，ACE 为 74.6%，TF-GRPO 为 74.2%。
- 在 SWE-bench-verified 的 token 使用量上，AHE 每次试验使用 461k tokens，NexAU₀ 为 526k，ACE 为 679k，TF-GRPO 为 582k。
- 跨模型的 Terminal-Bench 2 迁移对所有测试基础模型都是正向的，提升幅度为 +2.3 到 +10.1 个百分点；例子包括 deepseek-v4-flash 从 51.7% 提高到 61.8%，qwen-3.6-plus 从 56.2% 提高到 62.5%，gemini-3.1-flash-lite-preview 从 36.5% 提高到 41.6%。组件消融显示，收益主要来自记忆、工具和中间件：仅记忆达到 75.3%，仅工具达到 73.0%，仅中间件达到 71.9%，而仅系统提示词降至 67.4%，低于 69.7% 的种子。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25850v4](https://arxiv.org/abs/2604.25850v4)
