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
AHE 是一个自动循环，它用结构化的 rollout 证据和已测量的编辑结果来修改编码代理的 harness。论文声称，它把 Terminal-Bench 2 的 pass@1 从 69.7% 提高到 77.0%，并且无需重新进化就能迁移到 SWE-bench-verified 和其他模型家族。

## 问题
- 编码代理的表现取决于模型外部的 harness：提示词、工具、中间件、记忆、技能和执行控制。
- harness 工程主要靠手工完成，这会减慢基础模型、任务和工具需求变化时的适配速度。
- 自动化 harness 编辑很难，因为原始轨迹很大，可编辑部分彼此不同，而 pass 率变化也很难归因到某一次编辑。

## 方法
- AHE 在 NexAU 中把七类可编辑的 harness 组件作为文件暴露出来：系统提示词、工具说明、工具实现、中间件、技能、子代理配置和长期记忆。
- 它运行任务 rollout，清理轨迹，并用 Agent Debugger 把原始轨迹整理成按任务的报告和一个基准级证据文件。
- Evolve Agent 读取这些证据，编辑 harness 文件，并为每次变更写一份清单，其中包含失败证据、根因、修复、预期任务收益和回归风险。
- 下一轮会用任务级结果检查这些预测，并在文件级回滚被拒绝的编辑。
- 初始 harness 刻意做得很小：只有一个 shell 工具，没有中间件，没有技能，没有子代理。

## 结果
- 在 Terminal-Bench 2 上，10 轮 AHE 迭代把 NexAU₀ 的 pass@1 从 69.7% 提高到 77.0%，在 89 个任务上提升了 7.3 个百分点。
- 在 Terminal-Bench 2 的整体 pass@1 上，AHE 优于 OpenCode 的 47.2%、Terminus-2 的 62.9%、Codex 的 71.9%、ACE 的 68.9% 和 Training-Free GRPO 的 72.3%。
- 按 Terminal-Bench 2 难度分组，AHE 在 Easy 上得分 100.0%，Medium 上得分 88.2%，Hard 上得分 53.3%；Codex 在 Hard 上更高，为 56.7%。
- 在 SWE-bench-verified 上，冻结后的 AHE harness 在 500 个任务上的成功率达到 75.6%，而 NexAU₀ 为 75.2%，ACE 为 74.6%，TF-GRPO 为 74.2%。
- 在 SWE-bench-verified 的 token 使用上，AHE 每次试验用 461k tokens，而 NexAU₀ 为 526k，ACE 为 679k，TF-GRPO 为 582k。
- Terminal-Bench 2 的跨模型迁移对所有测试基础模型都是正向的，提升幅度从 +2.3 到 +10.1 个百分点；例如，deepseek-v4-flash 从 51.7% 提升到 61.8%，qwen-3.6-plus 从 56.2% 提升到 62.5%，gemini-3.1-flash-lite-preview 从 36.5% 提升到 41.6%。组件消融显示，提升主要来自记忆、工具和中间件：只保留记忆时达到 75.3%，只保留工具时达到 73.0%，只保留中间件时达到 71.9%；只保留系统提示词时则降到 67.4%，低于 69.7% 的初始值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25850v4](https://arxiv.org/abs/2604.25850v4)
