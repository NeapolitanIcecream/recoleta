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
## 总结
VeriContest 是一个包含 946 个问题的 Rust/Verus 基准，用来测试模型是否能生成带形式化规格和机器检查证明的代码。结果显示，普通代码测试通过率和生成完整可验证程序之间有很大差距。

## 问题
- LLM 生成的代码可能通过可见测试，但仍然有功能错误或安全缺陷，因为测试只能抽样行为，不能证明正确性。
- 现有的可验证代码基准通常规模较小，缺少真实证明，只测试流水线中的一个阶段，或使用与常规软件开发相距很远的设置。
- 这篇论文把竞争编程任务作为目标，因为这类任务需要具体的算法推理，包括贪心方法、动态规划、二分查找和滑动窗口。

## 方法
- 该基准包含 946 个任务：690 个来自 LeetCode，256 个来自 Codeforces。每个任务都包含自然语言提示、专家验证的 Verus 规格、评测通过的 Rust 代码、经过 Verus 检查的证明，以及正负测试集。
- 构建从 91 个手工验证的种子题开始，再用 Copilot/GPT-5.3-Codex 代理结合人工审查扩展，并且只保留符合 Verus 支持的 Rust 子集的任务。
- 人类专家检查在线评测通过情况、规格的合理性与完整性，以及带 `--no-cheating` 的 Verus 证明有效性。
- 作者从已验证程序生成正样本测试，再通过语义、语法和直接输出变异生成负样本测试。
- Post2Exe 把受支持的 Verus 后置条件转换成可执行的 Rust 检查，这样负样本测试就能暴露不完整的规格。

## 结果
- VeriContest 有 946 个任务。任务中位数规模是：描述 188 个词，代码 32 行，规格 23 行，证明 83 行，循环不变式 11.5 个，断言 14 个，正样本测试 276 个，负样本测试 2,670 个。
- 平均测试生成结果是每个任务 252.7 个正样本测试和 2,315.6 个负样本测试，已验证代码的行覆盖率为 99.66%。
- Post2Exe 转换了基准中 83% 的后置条件，并发现 60 个需要修改的不完整后置条件。
- 在 pass@1 上，GPT-5.5 在自然语言到代码生成上达到 92.18%，但在规格生成上只有 48.31%，在证明生成上只有 13.95%，端到端可验证生成上只有 5.29%。
- 所有评测模型的端到端得分都低于 6%。Claude Opus 4.7 达到 2.22%，Claude Sonnet 4.6 达到 2.85%，Gemini 3.1 Pro 达到 2.64%，Qwen 3.6 达到 0.21%。
- 在代码生成中加入形式化规格并不能解决这个任务：GPT-5.5 在 spec-to-code 上得分 67.65%，在自然语言加规格到代码上得分 74.52%，都低于它在自然语言到代码上的 92.18%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08553v1](https://arxiv.org/abs/2605.08553v1)
