---
source: arxiv
url: https://arxiv.org/abs/2605.22175v1
published_at: '2026-05-21T08:45:50'
authors:
- Yuxuan Sun
- Yuze Zhao
- Yufeng Wang
- Yao Du
- Zhiyuan Ma
- Jinbo Wang
- Mengdi Zhang
- Kai Zhang
- Zhenya Huang
topics:
- test-generation
- mutation-testing
- software-engineering-agents
- code-intelligence
- benchmarking
- llm-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?

## Summary
## 摘要
SWE-Mutation 是一个基准，用来测试 LLM 能否写出能捕捉真实软件 bug 的测试套件。它使用由 agent 生成的 SWE-bench 变异体，并显示当前模型常常能生成可运行的测试，但抓不住目标 bug，也抓不住细微的错误变体。

## 问题
- LLM 软件 agent 需要高质量测试套件，用于 issue 验证、修复轨迹生成和强化学习反馈。
- 现有生成的测试往往很浅，常见的变异方法也会造出很容易发现的 bug，从而高估测试质量。
- 仓库级和多语言的测试套件评估仍然有限，尤其是那些需要项目上下文的缺陷。

## 方法
- 这个基准有两个任务：从零生成测试，以及修复一个不完整或较弱的测试套件。
- 每个样本把一个真实仓库 issue 和 3-5 个从 golden fix 派生的 mutant 配对；好的测试应当在原始 bug 上失败，在 golden fix 上通过，并杀死这些 mutant。
- mutant 生成器分四步：定位改动文件和失败轨迹，注入语义上合理的 bug，检查语法并用 Fail-to-Pass 测试验证失败，再挑选能躲过模型生成测试的 mutant。
- 数据集包含 2,636 个 mutant，来自 800 个样本：其中 1,664 个 mutant 来自 500 个 SWE-bench Verified Python 样本，972 个 mutant 来自 9 种语言的 300 个多语言样本。
- 评估使用 Pass@1 衡量可用的测试补丁，VRR 衡量能复现 issue 且在修复后通过的测试，RDR 衡量生成测试检测到的存活 mutant 比例。

## 结果
- 在用 Claude Code 做 Python 测试修复时，Claude Sonnet 4.5 达到 99.80% Pass@1、59.20% VRR 和 81.15% RDR，是表 2 中报告的最佳结果。
- 在用 Claude Code 做 Python 测试生成时，Claude Sonnet 4.5 达到 98.00% Pass@1、40.40% VRR 和 71.71% RDR；在 Mini-Swe-Agent 下达到 96.20%、29.80% 和 63.70%。
- DeepSeek-V3.1 在 Mini-Swe-Agent 下做 Python 测试生成时达到 88.20% Pass@1、10.20% VRR 和 36.15% RDR。这说明可执行测试和有用测试之间差距很大。
- agent 生成的 mutant 让基准比传统 mutant 更难：平均 RDR 从 71.04% 降到 39.81%。
- 在用 Mini-Swe-Agent 做 9 语言测试修复子集时，Claude Sonnet 4.5 的平均值是 91.33% Pass@1、33.33% VRR 和 58.33% RDR；DeepSeek-V3.1 的平均值是 86.00%、20.33% 和 36.67%。
- 把 Claude Sonnet 4 的 mutant 生成器换成 DeepSeek-V3.1 或 Qwen3-Coder 后，RDR 的变化都在 1.5 个百分点以内，评估器的排序相关系数分别是 0.96 和 0.93。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22175v1](https://arxiv.org/abs/2605.22175v1)
