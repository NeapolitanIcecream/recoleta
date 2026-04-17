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
CLI-Tool-Bench 是一个基准，用来测试 LLM 智能体能否仅根据自然语言规格、在没有仓库脚手架的情况下，从零构建完整的 CLI 工具。论文表明，当前最强的模型在大多数任务上仍然失败，总体成功率低于 43%。

## 问题
- 现有代码基准主要测试函数补全、问题修复，或在预设仓库中的代码填充，因此遗漏了一项核心的 0 到 1 能力：规划并构建仓库本身。
- 许多基准使用与特定内部实现绑定的白盒单元测试，这与用户在实际中评判 CLI 工具的方式不一致；用户看的是命令行为、输出和文件系统效果。
- 这很重要，因为意图驱动的软件生成声称能够从零产出可运行的软件，而当前评测并不能很好地衡量这一点。

## 方法
- 论文提出了 **CLI-Tool-Bench**，这是一个包含 **100 个真实世界 CLI 仓库** 的基准，涵盖 **Python (38)**、**JavaScript (16)** 和 **Go (46)**，任务分为简单、中等和困难。
- 每个任务都给智能体提供一个**空工作区**，以及从原始项目 README 提取并去标识化的需求说明、完整的 `--help` 接口文档，以及每类命令的一个已验证示例。
- 该基准使用**LLM 引导的模式提取与模糊测试流水线**来构建端到端测试：先解析命令/子命令结构、标志、参数约束，再生成测试命令。
- 评估采用隔离 Docker 容器中的**黑盒差分测试**。生成的工具会与人工编写的 oracle 在 **return code**、**stdout** 和**文件系统副作用**上进行比较。
- 输出匹配使用多层级指标：**Exec**、**Exact Match**、阈值为 **0.8** 的归一化编辑距离 **Fuzzy Match**，以及由 GPT-5.4 判定的 **Semantic Match**。论文报告了对语义判定的人类验证：在 **1,000** 个采样输出对上，**Cohen's kappa > 0.9**。

## 结果
- 该基准包含 **100 个仓库**，覆盖 **9 个领域**，难度分布为 **42 个简单**、**24 个中等**、**34 个困难**任务。
- 每类命令有 **50 个端到端测试用例**，包括正例和反例。
- 论文在 **2 个智能体框架** 中评估了 **7 个 LLM**，总计 **14 种智能体配置**。
- 主要性能结论是，**顶级模型的总体成功率低于 43%**，作者据此认为 0 到 1 软件生成仍然很难。
- 论文还指出，**更高的 token 消耗不一定带来更好的表现**。
- 作者还报告了生成仓库中的一种行为模式：智能体经常产生**单体式代码结构**，并且可能陷入**无限生成循环**。这段摘录没有给出除 **<43%** 这一结论之外更完整的逐模型量化表格。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06742v1](http://arxiv.org/abs/2604.06742v1)
