---
source: arxiv
url: https://arxiv.org/abs/2605.04845v1
published_at: '2026-05-06T12:43:46'
authors:
- "Johannes H\xE4rtel"
topics:
- llm-agents
- repository-mining
- code-intelligence
- software-classification
- dynamic-context-retrieval
- tool-use
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Repository Mining: A Multi-Task Evaluation

## Summary
## 总结
这篇论文测试了带有 bash 访问权限的 LLM 智能体，能否像给定人工构建上下文的 LLM 一样对软件仓库工件进行分类。在 4 个任务和 4943 次有效分类中，智能体的准确率接近，同时避免了大工件上的上下文窗口失败。

## 问题
- 软件仓库挖掘经常需要为提交、评审、代码行或整个仓库打标签，而人工标注耗时、成本高，而且结果不一致。
- 简单的 LLM 分类器需要有人决定把哪些仓库上下文放进提示词里，这个选择可能导致标签错误或上下文窗口溢出。
- 这个问题很重要，因为仓库挖掘研究依赖这些标签来分析缺陷、安全、维护和项目质量。

## 方法
- 这项研究比较了固定上下文的 LLM 调用和基于同一批 LLM 构建的智能体。
- 智能体从一个工件标识符开始，比如 commit SHA，然后在沙箱化的 Docker 容器里用 bash 和 git 命令检查仓库。
- 评估覆盖 4 个分类任务：Munaiah 仓库分类（172 个仓库）、Herbold 缺陷修复代码行分类（212 行）、Härtel 安全评审分类（135 条评审），以及 Levin 维护意图提交分类（129 次提交）。
- 研究测试了 8 种方法配置，使用 Claude 3.7 Sonnet、Mistral Large 3 和 Llama 3.3 70B，包括 chain-of-thought、no-chain-of-thought、memorization、native tool calling 和 stop-sequence tool calling。
- 研究测量了准确率、token、时间、成本、失败、探索步骤，以及 100 个人工检查的分歧案例。

## 结果
- 实验共进行了 5184 次尝试；其中 212 次因 memorization 不适用于 Herbold 行而被排除，29 次是真实错误，最后留下 4943 次有效分类。
- 提供的摘录没有给出按任务划分的准确率数字。它声称没有明显的准确率赢家，智能体虽然自己检索上下文，但表现与简单 LLM 相当。
- 智能体没有出现上下文窗口溢出错误。简单版 Llama 有 9 次，简单版 Claude Sonnet 有 7 次，简单版 Claude Sonnet no-CoT 有 6 次，简单版 Mistral 有 3 次。
- 简单 LLM 每次运行大约使用 5K–8K 个输入 token。Agent Mistral 平均使用 8.5K 个新增输入 token 和 607 个输出 token；Agent Sonnet stop-sequence 平均使用 10.7K 个新增输入 token、18.2K 个 cache-read、4.9K 个 cache-write 和 720 个输出 token；Agent Sonnet native 平均使用 14.2K 个新增输入 token、18.5K 个 cache-read、5.3K 个 cache-write 和 1.1K 个输出 token。
- 智能体每次运行的成本高出 1.2 到 3.2 倍，但它们的成本与人工构建上下文的大小几乎没有相关性，而简单 LLM 的成本会随着大提示词上升。
- 对 100 个分歧案例的人工诊断发现，一些 ground-truth 标签或任务规范本身就有疑问，所以与原始标签相比的准确率可能低估了那些能访问更广仓库上下文的方法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04845v1](https://arxiv.org/abs/2605.04845v1)
