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
本文测试 Claude Code 和 Codex 能否把混乱的神经科学数据集转换成用于神经解码的共享格式。主要发现是，智能体经常能完成单个转换步骤，但完整、无错误的数据集复用仍需要人工审查。

## 问题
- 神经科学数据集分散在不同实验室、文件格式、API 和实验设计中，复用这些数据可能需要大量人工工作。
- NWB 等标准让文件更容易加载，但字段含义和分析选择常常仍不清楚。
- 这会影响跨数据集分析和脑-行为基础模型，因为数据准备可能成为瓶颈。

## 方法
- 该基准使用 8 篇近期小鼠神经群体记录论文，这些论文共享了数据和代码，数据形式包括 NWB 文件、IBL 和 Allen Brain Observatory 等联盟 API、Python 文件和 MATLAB 文件。
- 每个智能体收到论文、方法文本、发布的代码和原始数据，然后编写 `convert_data.py`，按指定的 subject/session/trial 格式生成 `converted_data.pkl`。
- 目标任务在所有数据集中保持一致：训练一个从神经活动预测任务变量或行为变量的线性解码器。
- 评估使用结果指标，例如数据集统计和解码器 balanced accuracy，并结合人工流程评分，评分项包括数据加载、trial 构建、神经预处理、变量构建、缺失数据处理和代码效率。
- 研究对每个数据集运行 Claude Code Opus 4.6 和 Codex GPT 5.4 各三次，共 48 次智能体运行。

## 结果
- 48 次运行全部生成了所需格式的转换数据，并产出了解码器性能值。
- 在有人工参考的监督数据集上，智能体通过了许多结果检查，例如 Allen2P 格式检查中 Claude Code 为 11/12，Codex 为 9/12；Lee2025 检查中两个智能体均为 15/15。
- 完整端到端成功很少见：按表中的端到端标准，Allen2P 中 Claude Code 成功运行数为 0/3，Codex 为 0/3；Lee2025 中两个智能体均达到 3/3。
- 人工流程分数按评分至少为 ok 的子任务比例计算，Claude Code 在各数据集上的范围为 0.813 到 0.938，Codex 为 0.885 到 1.000。
- 论文报告了每个智能体 169 个不正确或令人担忧的 trial 子任务案例用于错误分析，许多错误与筛选选择、时间分辨率、处理决策、根据变量名作出的假设以及语义不明确有关。
- agents-as-judges 并不可靠，尤其是在没有 ground-truth references 时。因此，作者主张在科学数据复用中加入交互式人工审查。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12808v2](https://arxiv.org/abs/2605.12808v2)
