---
source: arxiv
url: https://arxiv.org/abs/2605.12808v2
published_at: '2026-05-12T23:00:18'
authors:
- Ling-Qi Zhang
- Kristin Branson
topics:
- agentic-ai
- code-intelligence
- scientific-data-reuse
- neuroscience-data
- human-ai-interaction
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Neurodata Without Boredom: Benchmarking Agentic AI for Data Reuse

## Summary
## 摘要
这篇论文测试 Claude Code 和 Codex 能否把杂乱的神经科学数据集转换成神经解码用的共享格式。主要结论是，代理模型常能完成单个转换步骤，但要实现完整、无错误的数据复用，仍然需要人工审查。

## 问题
- 神经科学数据分散在不同实验室、文件格式、API 和实验设计中，所以复用时常常需要大量人工工作。
- NWB 这类标准让文件更容易读取，但字段含义和分析选择往往仍然不清楚。
- 这会影响跨数据集分析和脑行为基础模型，因为数据准备很容易变成瓶颈。

## 方法
- 这个基准选取了 8 篇近期的小鼠神经群体记录论文，这些论文共享数据和代码，数据形式包括 NWB 文件、IBL 和 Allen Brain Observatory 这类联盟 API、Python 文件和 MATLAB 文件。
- 每个代理都拿到论文、方法部分、公开代码和原始数据，然后编写 `convert_data.py`，把数据整理成规定的 subject/session/trial 格式，并输出为 `converted_data.pkl`。
- 所有数据集的目标任务都一样：从神经活动训练线性解码器，预测任务变量或行为变量。
- 评估使用了结果指标，比如数据集统计量和解码器 balanced accuracy，也用了人工过程评分，覆盖数据加载、trial 构建、神经预处理、变量构建、缺失数据处理和代码效率。
- 研究对 Claude Code Opus 4.6 和 Codex GPT 5.4 在每个数据集上各运行 3 次，共 48 次代理运行。

## 结果
- 48 次运行都生成了符合要求格式的转换数据，并得到了解码器性能数值。
- 在有人工参考的监督数据集上，代理通过了很多结果检查。例如 Allen2P 的格式检查中，Claude Code 为 11/12，Codex 为 9/12；Lee2025 的检查中，两者都是 15/15。
- 端到端成功很少见：按表中的端到端标准，Allen2P 的 Claude Code 和 Codex 运行都没有一次成功，都是 0/3；Lee2025 上两者都达到了 3/3。
- 人工过程评分按被评为至少 ok 的子任务比例计算，Claude Code 在不同数据集上的范围是 0.813 到 0.938，Codex 的范围是 0.885 到 1.000。
- 论文报告了每个代理 169 个错误或值得关注的 trial 子任务案例用于错误分析，很多错误与过滤选择、时间分辨率、处理决策、从变量名推断的假设以及语义含糊有关。
- 代理作为评审也不可靠，尤其是在没有真实参考的情况下，所以作者主张在科学数据复用中保留交互式人工审查。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12808v2](https://arxiv.org/abs/2605.12808v2)
