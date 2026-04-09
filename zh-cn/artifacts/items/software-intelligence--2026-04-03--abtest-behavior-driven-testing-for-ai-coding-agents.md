---
source: arxiv
url: http://arxiv.org/abs/2604.03362v1
published_at: '2026-04-03T17:52:37'
authors:
- Wuyang Dai
- Moses Openja
- Hung Viet Pham
- Gias Uddin
- Jinqiu Yang
- Song Wang
topics:
- ai-coding-agents
- behavioral-testing
- fuzzing
- code-intelligence
- repository-grounded-evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ABTest: Behavior-Driven Testing for AI Coding Agents

## Summary
## 摘要
ABTest 是一个面向 AI 编码代理的行为驱动模糊测试系统。它把真实用户故障报告转成在真实代码仓库上可执行的测试，并发现了许多常规代码基准测不出的代理行为故障。

## 问题
- 现有编码代理基准主要关注受控任务中的最终任务正确性，因此会漏掉过程层面的故障，例如修改了错误文件、留下不完整状态，或对工作区状态做出错误声明。
- 这些故障很重要，因为 Claude Code、Codex CLI 和 Gemini CLI 这类工具可以直接修改代码仓库、运行命令，并在日常开发中影响软件正确性和安全性。
- 论文关注多步交互中的行为鲁棒性，使用真实上报的故障，而不是合成的基准提示。

## 方法
- ABTest 从 GitHub issues 中挖掘了 400 个用户上报、开发者确认的编码代理故障，并将其抽象为 47 个可复用的 **Interaction Patterns** 和 128 个 **Action Types**。
- 它将兼容的 pattern-action 对组合成 647 个模糊测试种子模板，其中 pattern 表示用户工作流，action 表示被施压的具体操作，例如文件移动、回滚、补丁应用或命令执行。
- 它把每个种子实例化为真实代码仓库中、隔离工作区内、基于仓库上下文的多步测试用例，并明确期望产物、文件状态和验证步骤。
- 它用这些用例测试编码代理，记录提示词、命令轨迹、文件 diff、输出和其他产物，再通过自动检查和人工验证检测行为异常。
- 核心机制很直接：从真实缺陷报告出发，抽象其中重复出现的工作流和动作结构，生成大量相似的可执行用例，并检查代理行为是否偏离请求的工作流或代码仓库状态。

## 结果
- 数据来源：从 Claude Code、OpenAI Codex CLI 和 Gemini CLI 的 issue tracker 中挖掘出的 400 个真实故障报告。
- 模式库：47 个 Interaction Patterns 和 128 个 Action Types，组合成 647 个可执行的、基于真实代码仓库的模糊测试用例。
- 对每个评估配置执行一次 647 用例集合后，ABTest 标记出 1,573 个行为异常；其中 642 个经人工确认为新的真实异常，检测精度为 40.8%。
- Claude Code：Claude 4.5 Haiku 发现 119 个新异常，Claude 3.5 Haiku 发现 87 个。
- Codex CLI：GPT-5.1-Codex-Mini 发现 166 个新异常，GPT-4o-mini 发现 95 个。
- Gemini CLI：Gemini 2.5 Flash-Lite 发现 175 个新异常。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03362v1](http://arxiv.org/abs/2604.03362v1)
