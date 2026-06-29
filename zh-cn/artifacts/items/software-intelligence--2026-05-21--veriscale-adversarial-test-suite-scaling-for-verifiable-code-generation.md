---
source: arxiv
url: https://arxiv.org/abs/2605.22368v1
published_at: '2026-05-21T12:00:45'
authors:
- Yifan Bai
- Xiaoyang Liu
- Zihao Mou
- Guihong Wang
- Jian Yu
- Shuhan Xie
- Yantao Li
- Yangyu Zhang
- Jingwei Liang
- Tao Luo
topics:
- verifiable-code-generation
- code-intelligence
- software-benchmarks
- lean
- adversarial-testing
- test-suite-generation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# VeriScale: Adversarial Test-Suite Scaling for Verifiable Code Generation

## Summary
## 摘要
VeriScale 通过扩展和压缩基于 Lean 的可验证代码生成测试集，让薄弱的规格和实现更难蒙混过关。它在 Verina 的基础上生成了 VerinaPlus 和 VerinaLite，并报告称，在更强的测试下，顶级 LLM 的得分大幅下降。

## 问题
- 现有的可验证代码生成基准中的正向和负向测试太少，LLM 可能在没有抓住预期行为的情况下也能通过。
- SpecGen 需要意外输入和意外输出，来检查生成的前置条件和后置条件是否会拒绝无效行为。
- 这个问题很重要，因为被抬高的基准分数会让生成的规格和代码看起来比实际更安全。

## 方法
- VeriScale 先用 LLM 生成种子输入，再用类型感知的变异，为每个任务生成大量候选输入。
- 它用 Lean 对照真实前置条件进行检查，把候选项分成预期输入和非预期输入。
- 对于预期输入，它运行参考实现来生成预期输出。
- 为了生成更难的非预期输出，它让更强的模型编写对抗性实现，输出会被生成的后置条件接受，但结果是错误的。
- 它用保留边界的选择方法压缩扩展后的测试集中的非预期输入，再用贪心集合覆盖步骤保留那些能击败许多对抗性实现的预期用例。

## 结果
- VerinaPlus 在整体上把 Verina 扩大了 83 倍以上；VerinaLite 是一个轻量的 14 倍版本。
- 预期输入输出用例的平均数量从 Verina 的 5.89 增加到 VerinaPlus 的 370.07，提升 62.83 倍；VerinaLite 保留 52.34，提升 8.89 倍。
- 非预期输出的平均数量从 12.69 增加到 VerinaPlus 的 1114.01，提升 87.79 倍；VerinaLite 保留 202.35，提升 15.95 倍。
- 非预期输入的平均数量从 0.65 增加到 VerinaPlus 的 119.00，提升 183.08 倍；VerinaLite 保留 15.80，提升 24.31 倍。
- 对于 GPT-5.5，SpecGen 在 Verina 上是 68.78%，在 VerinaPlus 上降到 44.44%；CodeGen 从 96.83% 降到 86.24%。
- 论文用 Lean v4.24.0 评估了 8 个 LLM，报告增强后的基准达到 100% 代码覆盖率，并称 VerinaLite 以更低的评估成本保留了与 VerinaPlus 相近的区分能力。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22368v1](https://arxiv.org/abs/2605.22368v1)
