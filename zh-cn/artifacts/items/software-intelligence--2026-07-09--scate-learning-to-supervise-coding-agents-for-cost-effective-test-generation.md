---
source: arxiv
url: https://arxiv.org/abs/2607.08983v1
published_at: '2026-07-09T23:13:46'
authors:
- Sijia Gu
- Noor Nashid
- Ali Mesbah
topics:
- coding-agents
- automated-test-generation
- code-coverage
- contextual-bandits
- program-analysis
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation

## Summary
## 摘要
Scate 在生成单元测试期间自动监督编码代理，使其将工作投入到难以覆盖的代码路径上，减少过早停止。它使用上下文老虎机，根据类的复杂度、当前覆盖率和生成成本，在常规生成、程序分析和终止之间进行选择。

## 问题
- 编码代理经常在覆盖简单路径后停止，导致复杂分支未被测试。论文报告了一个 Gemini CLI 示例，其行覆盖率约为 42%，分支覆盖率约为 31%。
- 目前仍需要人工监督来决定何时重试、添加分析或停止，这会增加人工成本，也可能浪费 API 令牌。
- 自动化监督可以改善测试覆盖率，而测试覆盖率会影响缺陷检测和生成测试的维护成本。

## 方法
- Scate 根据代码行数（LOC）、按权重计算的每类方法数、类的响应度、行覆盖率、分支覆盖率和未覆盖复杂度构建包含七个特征的上下文，另加一个截距项。
- 一个持久化的 LinUCB 上下文老虎机从三个动作中选择一个：默认生成、使用 Scate MCP 程序分析工具进行分析，或停止。
- 奖励结合了行覆盖率和分支覆盖率的相对增益、复杂未覆盖代码的进展、令牌成本，以及对未带来覆盖率增益的动作的惩罚。
- MCP 工具提取未覆盖的控制流路径和外部调用，然后向代理提供最多 10 个覆盖不足的方法，并附上经过优先级排序的路径和依赖信息。

## 结果
- 在基于 Defects4J 的数据集上，与无监督的纯代理基线相比，使用 Gemini CLI 的 Scate 将行覆盖率提高了 32.3%，将分支覆盖率提高了 30.9%。
- 使用 Claude Code 时，与相应的无监督基线相比，Scate 将行覆盖率提高了 6.0%，将分支覆盖率提高了 5.9%。
- 论文报告称，该框架在所有评估指标上都优于当前最先进的非代理测试生成方法。
- 摘录提供了相对覆盖率提升数据，但没有给出最终绝对覆盖率、令牌节省量、数据集规模或统计显著性数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08983v1](https://arxiv.org/abs/2607.08983v1)
