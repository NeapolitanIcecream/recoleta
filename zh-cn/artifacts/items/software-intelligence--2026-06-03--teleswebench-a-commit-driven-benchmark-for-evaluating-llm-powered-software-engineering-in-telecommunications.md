---
source: arxiv
url: https://arxiv.org/abs/2606.05001v1
published_at: '2026-06-03T15:19:40'
authors:
- Pranshav Gajjar
- Ali Mamaghani
- Dinesh Bharadia
- Vijay K Shah
topics:
- code-intelligence
- software-engineering-agents
- telecom-software
- benchmarking
- llm-as-judge
- srsran
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# TeleSWEBench: A Commit-Driven Benchmark for Evaluating LLM-Powered Software Engineering in Telecommunications

## Summary
## 摘要
TeleSWEBench 是一个包含 734 个任务的基准，用来测试 LLM 软件工程代理在真实 srsRAN 5G 提交上的表现。结果显示，当前代理在电信代码上仍然吃力：最强工具只能产出最多 25% 可交付的改动。

## 问题
- 电信网络现在依赖大型 C++ 无线协议栈；代码改动会影响 5G 协议行为、时序和状态机。
- SWE-bench、HumanEval 和 MBPP 这类通用编码基准不会测试 srsRAN 5G 这类系统中的仓库级 3GPP 逻辑。
- 现有的电信 LLM 评估主要关注问答或代码理解，没有直接测试电信仓库中的多文件代码生成。

## 方法
- 该基准从 2023-2025 年的 srsRAN 5G 仓库中挖掘真实开发者提交，起点超过 15,000 个提交。
- 它保留带有仓库原生测试的提交，并将其转成 734 个编码任务：142 个 Easy、279 个 Medium、313 个 Difficult。
- 难度控制提示中给出的定位细节量：Easy 包含准确文件和修改，Medium 给出受影响区域和事实，Difficult 只给高层目标。
- 评估分两阶段：先做文件定位，再只对完全文件匹配的补丁做功能正确性评估。
- 论文还提出 TeleJudge，一个分层 LLM 裁判，对文件级 diff 打分，并与可执行单元测试一起合成补丁判定。

## 结果
- TeleSWEBench 包含 734 个带可执行测试的问题，基于 srsRAN 5G 提交构建；任务范围从 1 个文件到 300 个文件不等。
- 在第 1 阶段定位中，QwenCoder-2.5 的 Easy 精确匹配率最好，达到 37.8%；在列出的模型中，Qwen3 的累计精确匹配率最好，为 14.0%。
- 难任务上的定位明显下降：QwenCoder-2.5 从 Easy 的 37.8% 精确匹配降到 Difficult 的 5.3%。
- 许多更大的模型经常不改代码：GLM-4.7 的累计 No Changes 率为 92.2%，Gemma4 为 86.8%。
- 摘要写到，表现最强的已评估 ASE 工具最多能产出 25% 可交付的改动。
- 评估的模型包括 Qwen3.5，参数量 397B，支持 1M token 上下文；Kimi K2.5，参数量 1T，支持 262K token 上下文；GPT-OSS，参数量 120B；Gemma 4，参数量 31B；以及 QwenCoder 2.5，参数量 1.5B。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05001v1](https://arxiv.org/abs/2606.05001v1)
