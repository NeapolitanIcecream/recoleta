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
## 摘要
本文测试带有 bash 访问能力的 LLM 智能体，能否像获得人工构建上下文的 LLM 一样，对软件仓库工件进行分类。在 4 个任务和 4943 次有效分类中，智能体达到相近准确率，同时避免了大型工件上的上下文窗口失败。

## 问题
- 软件仓库挖掘常常需要为提交、评审、代码行或整个仓库打标签，人工标注慢、成本高，而且结果不一致。
- 简单 LLM 分类器需要有人决定把哪些仓库上下文放进提示词，这个选择可能导致错误标签或上下文窗口溢出。
- 这个问题很重要，因为仓库挖掘研究依赖这些标签来分析缺陷、安全、维护和项目质量。

## 方法
- 研究比较了固定上下文 LLM 调用和基于相同 LLM 构建的智能体。
- 智能体从一个工件标识符开始，例如提交 SHA，然后在沙箱化 Docker 容器中用 bash 和 git 命令检查仓库。
- 评估覆盖 4 个分类任务：Munaiah 仓库分类（172 个仓库）、Herbold 缺陷修复代码行分类（212 行）、Härtel 安全评审分类（135 条评审）和 Levin 维护意图提交分类（129 个提交）。
- 研究测试了 Claude 3.7 Sonnet、Mistral Large 3 和 Llama 3.3 70B 上的 8 种方法配置，包括思维链、无思维链、记忆、原生工具调用和停止序列工具调用。
- 研究衡量准确率、token、时间、成本、失败、探索步骤，并人工检查 100 个分歧案例。

## 结果
- 实验产生 5184 次尝试；其中 212 次被排除，因为记忆方法不适用于 Herbold 代码行，另有 29 次是真实错误，剩下 4943 次有效分类。
- 提供的摘录没有给出各任务准确率数字。它称没有明确的准确率赢家，智能体虽然自行检索上下文，但相对简单 LLM 仍有竞争力。
- 智能体有 0 次上下文窗口溢出错误。简单 Llama 有 9 次，简单 Claude Sonnet 有 7 次，简单 Claude Sonnet no-CoT 有 6 次，简单 Mistral 有 3 次。
- 简单 LLM 每次运行使用约 5K–8K 个输入 token。Agent Mistral 平均使用 8.5K 个新输入 token 和 607 个输出 token；Agent Sonnet stop-sequence 平均使用 10.7K 个新输入 token、18.2K 个缓存读取 token、4.9K 个缓存写入 token 和 720 个输出 token；Agent Sonnet native 平均使用 14.2K 个新输入 token、18.5K 个缓存读取 token、5.3K 个缓存写入 token 和 1.1K 个输出 token。
- 智能体每次运行成本高出 1.2 到 3.2 倍，但其成本与工程化上下文大小的相关性接近 0；简单 LLM 的成本会随着大型提示词上升。
- 对 100 个分歧案例的人工诊断发现，有些真实标签或任务规范存在疑问，所以用原始标签衡量准确率，可能会低估拥有更广泛仓库访问能力的方法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04845v1](https://arxiv.org/abs/2605.04845v1)
