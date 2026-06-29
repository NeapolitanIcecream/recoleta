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
ABTest 是一个面向 AI 编码代理的行为驱动模糊测试系统。它把真实用户的失败报告转成可执行测试，在真实仓库上运行，找出很多普通代码基准测试会漏掉的新代理行为故障。

## 问题
- 现有的编码代理基准测试主要关注受控任务中的最终任务正确性，因此会漏掉过程级故障，例如改错文件、留下部分状态，或对工作区状态做出错误说明。
- 这些故障很重要，因为 Claude Code、Codex CLI 和 Gemini CLI 这类工具可以直接修改仓库、运行命令，并在日常开发中影响软件正确性和安全性。
- 论文关注多步交互过程中的行为鲁棒性，使用真实报告的失败，而不是合成的基准提示词。

## 方法
- ABTest 从 GitHub issues 中挖掘了 400 条由用户报告、开发者确认的编码代理失败，并将它们抽象为 47 个可复用的 **Interaction Patterns** 和 128 个 **Action Types**。
- 它把兼容的模式和动作配对组合成 647 个模糊测试种子模板，其中模式描述用户工作流，动作描述具体受压操作，例如文件移动、回滚、打补丁或执行命令。
- 它把每个种子实例化为真实仓库中的、以仓库为基础的多步测试用例，在隔离工作区中运行，并明确预期产物、文件状态和验证步骤。
- 它把这些用例运行到编码代理上，记录提示词、命令轨迹、文件差异、输出和其他产物，然后用自动检查加人工验证来检测行为异常。
- 核心机制很直接：从真实漏洞报告出发，抽象出重复出现的工作流和动作结构，生成大量相似的可执行用例，再检查代理行为是否偏离请求的工作流或仓库状态。

## 结果
- 来源数据：从 Claude Code、OpenAI Codex CLI 和 Gemini CLI 的 issue tracker 中挖掘出的 400 条真实失败报告。
- 模式库：47 个 Interaction Patterns 和 128 个 Action Types，组合成 647 个可执行的、以仓库为基础的模糊测试用例。
- 在每个评估配置下对 647 个用例包运行一次后，ABTest 标记出 1,573 个行为异常；其中 642 个经人工确认是新的真实异常，检测精度为 40.8%。
- Claude Code：使用 Claude 4.5 Haiku 检出 119 个新异常，使用 Claude 3.5 Haiku 检出 87 个。
- Codex CLI：使用 GPT-5.1-Codex-Mini 检出 166 个新异常，使用 GPT-4o-mini 检出 95 个。
- Gemini CLI：使用 Gemini 2.5 Flash-Lite 检出 175 个新异常。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03362v1](http://arxiv.org/abs/2604.03362v1)
