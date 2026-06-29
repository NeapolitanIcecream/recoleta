---
source: arxiv
url: http://arxiv.org/abs/2604.06742v1
published_at: '2026-04-08T07:09:10'
authors:
- Ruida Hu
- Xinchen Wang
- Chao Peng
- Cuiyun Gao
- David Lo
topics:
- llm-agents
- software-generation
- benchmarking
- cli-tools
- black-box-testing
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios

## Summary
## 摘要
CLI-Tool-Bench 是一个基准，用来测试 LLM 代理能否只根据自然语言规格、在没有仓库脚手架的情况下，从零开始构建完整的 CLI 工具。论文显示，当前最强模型在大多数任务上仍然失败，总体成功率低于 43%。

## 问题
- 现有代码基准大多测试函数补全、问题修复，或在预设仓库内填代码，因此看不到一个核心的 0 到 1 能力：规划并搭建仓库本身。
- 许多基准使用绑定到特定内部实现的白盒单元测试，这和用户在实际中判断 CLI 工具的方式不一致。用户看的是命令行为、输出和文件系统效果。
- 这很重要，因为意图驱动的软件生成声称可以从零开始产出可运行软件，而现有评估并没有很好地衡量这一点。

## 方法
- 论文提出 **CLI-Tool-Bench**，这是一个包含 **100 个真实世界 CLI 仓库** 的基准，覆盖 **Python（38）**、**JavaScript（16）** 和 **Go（46）**，任务难度分为简单、中等和困难。
- 每个任务都会给代理一个 **空工作区**，以及从原始项目 README 中整理出的去标识化需求、完整的 `--help` 接口文档，以及每类命令的一个已验证示例。
- 基准通过一个 **LLM 引导的模式提取和 fuzzing 流水线** 生成端到端测试：先解析命令/子命令结构、标志和参数约束，再生成测试命令。
- 评估采用在隔离 Docker 容器中的 **黑盒差分测试**。生成的工具会与人工编写的 oracle 在 **返回码**、**stdout** 和 **文件系统副作用** 上进行比较。
- 输出匹配使用多层指标：**Exec**、**Exact Match**、基于归一化编辑距离阈值 **0.8** 的 **Fuzzy Match**，以及由 GPT-5.4 判定的 **Semantic Match**。论文还报告了语义判定的人类验证结果：在 **1,000** 对抽样输出上，**Cohen's kappa > 0.9**。

## 结果
- 这个基准包含 **100 个仓库**，覆盖 **9 个领域**，难度分布为 **42 个简单任务**、**24 个中等任务** 和 **34 个困难任务**。
- 每类命令都有 **50 个端到端测试用例**，包括正例和负例。
- 论文在 **2 个代理框架** 中评估了 **7 个 LLM**，总计 **14 种代理配置**。
- 核心结果是：**最强模型的总体成功率低于 43%**，作者用这一点说明 0 到 1 的软件生成仍然很难。
- 论文还指出，**更高的 token 消耗不一定带来更好的性能**。
- 作者报告了生成仓库中的一种行为模式：代理经常产出 **单体化代码结构**，还会陷入 **无限生成循环**。摘录没有提供超出 **<43%** 这一结论之外的完整逐模型量化表格。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06742v1](http://arxiv.org/abs/2604.06742v1)
