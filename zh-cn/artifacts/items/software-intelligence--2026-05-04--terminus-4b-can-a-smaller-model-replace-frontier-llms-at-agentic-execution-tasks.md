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
Terminus-4B 是一个 Qwen3-4B 模型，训练目标是在编码智能体内部充当终端执行子智能体。论文称，在这个范围很窄的子任务上，它可以替代前沿 LLM，同时把主智能体的 token 用量最多降低约 30%。

## 问题
- 编码智能体经常在主智能体上下文中运行构建、测试、安装和诊断命令。每条命令可能加入数万枚终端输出 token。
- 这会挤占代码、计划和先前编辑的上下文空间，增加成本，并缩短有效的问题求解轨迹。
- 现有子智能体设置通常用前沿模型处理终端工作，尽管该任务范围很窄：运行命令、读取输出，并返回简洁、准确的摘要。

## 方法
- 论文向编码智能体加入了一个 Execution Subagent 工具。主智能体发送自然语言查询，子智能体在自己的上下文中运行终端命令。
- 子智能体只有一个工具：Terminal。它每轮运行一条同步命令，使用显式超时，默认限制为 10 轮，并返回结构化的 `<final_answer>`，其中包含每条命令的摘要。
- Terminus-4B 以 Qwen3-4B 为起点，先用专家子智能体轨迹进行监督微调，再用 GRPO 强化学习针对该任务做后训练。
- RL rollout 与主智能体隔离：一个轻量级 Qwen3-4B Instruct 模型把固定查询转发给子智能体，因此训练集中在终端执行行为上。
- 奖励使用 LLM judge 和评分细则，在质量维度和失败维度上把候选 rollout 与参考轨迹进行比较。

## 结果
- 摘要称，相比 No Subagent 基线，主智能体 token 用量最多降低约 30%，并且在 SWE-Bench Pro 和一个内部 SWE-Bench C# 基准上没有报告性能损失。
- 论文称，作为 Execution Subagent，Terminus-4B 缩小了与 Claude Sonnet、Claude Opus 和 GPT-5.3-Codex 的差距，并且经常超过它们，但摘录没有包含完整基准表或精确的解决率数字。
- 在 Serilog 示例中，基线使用了 2.46M 个主智能体 token、40 轮和 18 次直接终端调用。使用 Terminus-4B 作为子智能体后，该运行使用了 740k 个主智能体 token 和 32 轮，子智能体在内部运行了 9 条命令。
- 在同一示例中，子智能体返回了约 200 个 token 的摘要，而非原始日志；摘要包括 `dotnet build` 成功，含 9 个警告和 0 个错误，769 个单元测试通过，以及 1 个 approval test 失败和可能的修复方式。
- 训练语料起始于约 10k 个可构建实例，覆盖 2,144 个代码库和 5 种语言，最终在 730 个代码库中产生了 3,009 次唯一的 Execution Subagent 调用。
- 收集集合中的任务标签包括 2,692 个测试执行任务、2,166 个错误诊断任务、969 个构建/编译任务和 106 个依赖任务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03195v1](https://arxiv.org/abs/2605.03195v1)
