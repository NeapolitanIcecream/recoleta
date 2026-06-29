---
source: hn
url: https://www.normaltech.ai/p/did-googles-ai-agents-really-build
published_at: '2026-05-22T22:50:27'
authors:
- randomwalker
topics:
- coding-agents
- multi-agent-software-engineering
- open-world-evaluation
- software-engineering-ai
- agent-benchmarks
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Did Google's AI agents build an operating system for $916?

## Summary
## 摘要
文章认为，谷歌关于“由智能体构建操作系统”的说法，在没有提示词、代码、日志、重试次数和抄袭检查的情况下，证据并不充分。它把这次演示视为一个适合独立评估长时间运行的编码智能体的案例。

## 问题
- 谷歌称，智能体用一个提示词、花了大约 900 美元就构建了一个操作系统，但公开说明缺少判断这一说法所需的细节。
- 这个案例很重要，因为智能体厂商现在把长时间的软件任务当作能力证明，而标准基准很难很好地测试这类工作。
- 方法细节缺失，让人难以判断结果来自模型能力、重度提示词工程、针对任务的脚手架、重试，还是对公开代码的复制。

## 方法
- 作者审查的是谷歌公开的博客文章，而不是重新运行实验。
- 他们检查这篇说明是否定义了人工介入、报告了重试和 dry run、发布了产物，以及是否测试了复制或记忆化代码。
- 他们把模型和外围脚手架分开来看：专门角色、对子智能体的委派、工具访问、卡住的智能体重启，以及一个反作弊组件。
- 他们认为，面向开放世界的评估需要更强的规范：公开产物、更清晰的介入日志、成本报告，以及独立审查。

## 结果
- 谷歌报告最终 API 费用为 916.92 美元，总预算为 26 亿 token。
- 谷歌把任务描述为从一个提示词开始，但后来这个提示词变成了数千行；文章说，没有报告生成提示词的尝试次数。
- 谷歌说有几十个子智能体协同工作，并通过 Antigravity 2.0 这套设置分工和委派。
- 谷歌说最终运行不需要额外的人类指导或纠正，但文章说，这篇说明没有给出人工重启、审批、升级处理、dry run 或重试的明确次数。
- 谷歌没有发布独立审查所需的关键产物：长提示词、生成的源代码和智能体日志。
- 文章没有发现基准对照、相似性分析或日志分析，因此无法检验这些智能体是否复制或记住了已有的玩具操作系统代码。

## Problem

## Approach

## Results

## Link
- [https://www.normaltech.ai/p/did-googles-ai-agents-really-build](https://www.normaltech.ai/p/did-googles-ai-agents-really-build)
