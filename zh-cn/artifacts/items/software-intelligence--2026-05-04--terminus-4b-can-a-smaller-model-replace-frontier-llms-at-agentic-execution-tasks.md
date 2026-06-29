---
source: arxiv
url: https://arxiv.org/abs/2605.03195v1
published_at: '2026-05-04T22:24:24'
authors:
- Spandan Garg
- Vikram Nitin
- Yufan Huang
topics:
- code-agents
- software-foundation-models
- terminal-execution
- small-language-models
- multi-agent-software-engineering
- context-management
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?

## Summary
## 摘要
Terminus-4B 是一个基于 Qwen3-4B 训练的模型，用作编码代理中的终端执行子代理。论文声称，它可以替代这一狭窄子任务中的前沿大模型，同时把主代理的 token 用量最多降低约 30%。

## 问题
- 编码代理常把构建、测试、安装和诊断放在主代理上下文里运行。每个命令可能带来数万 token 的终端输出。
- 这会挤占代码、计划和之前修改的上下文，也会提高成本，缩短可用于解决问题的有效轨迹。
- 现有的子代理设置通常给终端工作分配前沿模型，但这个任务很窄：运行命令、读取输出，并返回简洁且准确的摘要。

## 方法
- 论文给编码代理加入了一个 Execution Subagent 工具。主代理发送自然语言查询，子代理在自己的上下文里运行终端命令。
- 子代理只有一个工具，Terminal。它每轮运行一个同步命令，使用明确的超时，默认最多 10 轮，并返回带有每个命令摘要的结构化 `<final_answer>`。
- Terminus-4B 以 Qwen3-4B 为起点，先用专家子代理轨迹做监督微调，再用 GRPO 强化学习完成后训练。
- RL rollout 与主代理隔离：一个轻量的 Qwen3-4B Instruct 模型把固定查询转发给子代理，因此训练重点放在终端执行行为上。
- 奖励使用 LLM judge 和评分标准，把候选 rollout 与参考轨迹在质量和失败维度上进行比较。

## 结果
- 摘要声称，与 No Subagent 基线相比，主代理 token 用量最多减少约 30%，而在 SWE-Bench Pro 和内部的 SWE-Bench C# 基准上没有报告性能损失。
- 论文声称，Terminus-4B 作为 Execution Subagent 时缩小了与 Claude Sonnet、Claude Opus 和 GPT-5.3-Codex 的差距，而且经常超过它们，但这段摘录没有给出完整基准表或准确的解决率数字。
- 在 Serilog 示例中，基线用了 246 万主代理 token、40 轮和 18 次直接终端调用。使用 Terminus-4B 作为子代理时，运行用了 74 万主代理 token 和 32 轮，而子代理内部运行了 9 个命令。
- 在同一个示例中，子代理返回了大约 200 token 的摘要，而不是原始日志，其中包括 `dotnet build` 成功、9 个警告和 0 个错误、769 个单元测试通过，以及 1 个审批测试失败和可能的修复方向。
- 训练语料从大约 10k 个可构建实例开始，覆盖 2,144 个仓库和 5 种语言，生成了来自 730 个仓库的 3,009 次唯一 Execution Subagent 调用。
- 收集集中的任务标签包括 2,692 个测试执行任务、2,166 个错误诊断任务、969 个构建/编译任务和 106 个依赖任务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03195v1](https://arxiv.org/abs/2605.03195v1)
