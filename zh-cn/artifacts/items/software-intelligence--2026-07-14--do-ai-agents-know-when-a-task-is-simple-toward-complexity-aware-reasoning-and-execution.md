---
source: arxiv
url: https://arxiv.org/abs/2607.13034v1
published_at: '2026-07-14T17:59:31'
authors:
- Junjie Yin
- Xinyu Feng
topics:
- software-agents
- code-intelligence
- adaptive-computation
- tool-use
- execution-efficiency
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution

## Summary
## 摘要
E3 帮助软件代理估计任务所需的执行范围，从最小可行路径开始，并仅在验证失败时扩大范围。在受控基准测试中，它保持了成功率，同时大幅降低了成本、令牌使用量和文件检查量。

## 问题
- LLM 代理经常采用“最大上下文优先”策略，即使面对局部编辑，也会反复读取文件和依赖项；这很重要，因为不必要的上下文会增加延迟、令牌消耗、工具调用次数和工程成本，却不会提高正确性。
- 论文针对的是一种缺失能力：代理在执行任务前，估计任务难度、所需信息以及最短的可靠执行路径。

## 方法
- E3（Estimate、Execute、Expand，即估计、执行、扩展）首先根据任务以及至多一次低成本的环境探测，预测难度、范围、风险和置信度。
- 它执行一条最小可行路径：对简单任务进行局部编辑；只有在估计范围更大时，才扩大文件检查范围或追踪依赖关系。
- 它验证结果，并在验证失败或置信度较低时逐步扩大范围，同时复用缓存的搜索结果，而不是重新开始。
- 论文形式化了“最小充分执行”和代理认知冗余比（Agent Cognitive Redundancy Ratio，ACRR）；后者衡量实际成本相对于由预言机定义的最小成本的比例。

## 结果
- 在包含 121 项编辑的确定性基准 MSE-Bench 上，E3 在成功率达到 100% 的同时，达到了最强基线的表现，并将总成本降低了 85%、令牌使用量降低了 91%、检查文件数降低了 92%。
- 在成功率相当的情况下，E3 的成本也比强大的自适应检索基线低 16%，这表明其收益并不局限于与“最大上下文优先”策略进行比较。
- 在留出的指令措辞下，E3 仍保持 100% 的成功率，并且在几乎所有测试过的成本权重下，仍是成本最低的完全成功策略。
- 在 LLM-Case 真实模型测试框架中，负责编辑开源库的实时 gpt-4o 代理表现出程度较轻但可测量的过度读取；在任务成功率相当的情况下，E3 是范围最精简、速度最快的策略。其唯一报告的不足由服务提供商的速率限制导致，而不是错误编辑。
- 证据对能力受控的模拟器和所报告的测试框架案例支持最强；这些结果并不能证明 E3 在一般已部署代理上的表现。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13034v1](https://arxiv.org/abs/2607.13034v1)
