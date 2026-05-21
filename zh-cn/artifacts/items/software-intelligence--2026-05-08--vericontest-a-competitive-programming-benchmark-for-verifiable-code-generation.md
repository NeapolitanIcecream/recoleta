---
source: arxiv
url: https://arxiv.org/abs/2605.08553v1
published_at: '2026-05-08T23:25:05'
authors:
- Zichen Xie
- Mrigank Pawagi
- Yuxin Liu
- Aaditi Rai
- Lize Shao
- John Berberian
- Sicong Che
- Wenxi Wang
topics:
- verifiable-code-generation
- code-generation-benchmark
- formal-verification
- rust-verus
- proof-generation
- specification-generation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation

## Summary
## 摘要
VeriContest 是一个包含 946 道题的 Rust/Verus 基准，用于测试模型能否生成带有形式化规约和机器检查证明的代码。报告结果显示，通过普通代码测试和生成完全验证程序之间存在很大差距。

## 问题
- LLM 生成的代码可能通过可见测试，但仍有功能错误或安全缺陷，因为测试只是抽样检查行为，不能证明正确性。
- 现有可验证代码基准通常规模较小，缺少真实证明，只测试一个阶段，或使用的场景与常规软件开发相距较远。
- 论文选择竞技编程任务，因为这些任务需要具体的算法推理，包括贪心方法、动态规划、二分搜索和滑动窗口。

## 方法
- 该基准包含 946 个任务：690 个来自 LeetCode，256 个来自 Codeforces。每个任务都包含自然语言提示、经专家验证的 Verus 规约、在线评测接受的 Rust 代码、Verus 检查过的证明，以及正向和负向测试。
- 构建过程从 91 个手工验证的种子问题开始，随后用 Copilot/GPT-5.3-Codex 代理加人工审查扩展，并且只保留符合 Verus 支持的 Rust 子集的任务。
- 人类专家检查在线评测接受情况、规约的可靠性和完整性，以及使用 `--no-cheating` 的 Verus 证明有效性。
- 作者从已验证程序生成正向测试，并通过语义、语法和直接输出变异生成负向测试。
- Post2Exe 将受支持的 Verus 后置条件转换为可执行的 Rust 检查，使负向测试能够暴露不完整规约。

## 结果
- VeriContest 有 946 个任务。任务规模中位数为：描述 188 个词、代码 32 行、规约 23 行、证明 83 行、循环不变量 11.5 个、断言 14 个、正向测试 276 个、负向测试 2,670 个。
- 平均每个任务的测试生成结果为 252.7 个正向测试和 2,315.6 个负向测试，对已验证代码的行覆盖率为 99.66%。
- Post2Exe 转换了基准中 83% 的后置条件，并发现 60 个需要修订的不完整后置条件。
- 在 pass@1 上，GPT-5.5 的自然语言到代码生成达到 92.18%，但规约生成只有 48.31%，证明生成只有 13.95%，端到端验证生成只有 5.29%。
- 所有评估模型的端到端得分都低于 6%。Claude Opus 4.7 达到 2.22%，Claude Sonnet 4.6 达到 2.85%，Gemini 3.1 Pro 达到 2.64%，Qwen 3.6 达到 0.21%。
- 向代码生成加入形式化规约不能解决该任务：GPT-5.5 在规约到代码上得分为 67.65%，在自然语言加规约到代码上得分为 74.52%，两者都低于其 92.18% 的自然语言到代码得分。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08553v1](https://arxiv.org/abs/2605.08553v1)
