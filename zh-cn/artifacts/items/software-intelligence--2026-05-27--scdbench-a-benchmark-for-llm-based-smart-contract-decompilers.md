---
source: arxiv
url: https://arxiv.org/abs/2605.29059v1
published_at: '2026-05-27T20:08:47'
authors:
- Kaihua Qin
- Dawn Song
- Arthur Gervais
topics:
- smart-contract-decompilation
- code-intelligence
- llm-evaluation
- software-benchmark
- semantic-testing
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# SCDBench: A Benchmark for LLM-Based Smart Contract Decompilers

## Summary
## 摘要
SCDBench 是一个基准，用来测试 LLM 能否把以太坊字节码反编译成能编译、且行为与原始合约一致的 Solidity。表现最好的模型也只在 600 个合约中有 42 个达到完整的语义正确性。

## 问题
- 智能合约源代码常常不可用：论文指出，超过 99% 的以太坊合约没有验证，而智能合约保护着超过 1600 亿美元的资产。
- LLM 反编译器会生成看起来合理、也能编译的 Solidity，但会改变行为，这让只看可读性的评估不适合审计和安全工作。
- 以往的反编译评估使用的数据集范围窄、采样方式私有或不清楚，而且指标不一致，所以结果很难复现，也很难比较。

## 方法
- SCDBench 包含 600 个真实 Solidity 合约，这些合约从 772,736 个按精确字节码唯一且已验证的以太坊合约中抽样得到，分成 200 个简单样本、200 个中等样本和 200 个困难样本。
- 每个任务都提供 EVM 字节码作为输入，并以真实 Solidity 源码作为参考输出。
- 这个基准用四个累积阶段评估输出：格式完整性、可编译性、ABI 恢复和语义一致性。
- 语义检查会把固定测试用例分别在原始合约和反编译合约上回放，并比较返回数据、revert 状态、发出的日志和触及的存储槽。
- 作者还测试了一个同模型修复步骤：如果生成的 Solidity 格式正确但编译失败，模型会收到编译器错误，并有一次机会修复。

## 结果
- 数据集包含 227,383 个具体语义测试用例，覆盖 14,553 个公共函数，平均代码覆盖率为 77.8%。
- GPT-5.3-Codex 的格式完整性最好：564/600 个合约，或 94.0%。Opus 4.7 达到 435/600，GLM-5 达到 520/600，GLM-5 instruct 达到 540/600。
- GPT-5.3-Codex 在未修复情况下的编译成功率最好，达到 421/600 个合约，或 70.2%。经过一次修复后，GPT-5.3-Codex 提升到 542/600，或 90.3%。
- 修复对每个测试模型都有提升：Opus 4.7 从 341/600 提升到 415/600 个可编译合约，GLM-5 从 221/600 提升到 403/600，GLM-5 instruct 从 144/600 提升到 386/600。
- 带修复的 GPT-5.3-Codex 在 ABI 恢复上的 F1 最好：总分 0.896，简单合约 0.942，中等合约 0.928，困难合约 0.861。
- 语义正确性仍然很低：按基准的语义回放检查，表现最好的模型也只完整反编译了 42/600 个合约。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29059v1](https://arxiv.org/abs/2605.29059v1)
