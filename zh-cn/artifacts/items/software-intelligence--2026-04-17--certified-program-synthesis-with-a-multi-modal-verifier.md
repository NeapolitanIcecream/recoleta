---
source: arxiv
url: http://arxiv.org/abs/2604.16584v1
published_at: '2026-04-17T14:56:45'
authors:
- Yueyang Feng
- Dipesh Kafle
- Vladimir Gladshtein
- Vitaly Kurin
- "George P\xEErlea"
- Qiyuan Zhao
- "Peter M\xFCller"
- Ilya Sergey
topics:
- program-synthesis
- formal-verification
- lean-theorem-prover
- property-based-testing
- code-generation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Certified Program Synthesis with a Multi-Modal Verifier

## Summary
## 摘要
本文介绍了 LeetProof。这是一条经过认证的程序合成流水线，在 Lean 中用同一个验证器完成测试、自动证明和交互式证明。论文的主要结论是，这种分阶段的多模态设计能更早发现有问题的规格，并且在相同预算下，比仅使用 Lean 的单模式基线产出更多完全认证的程序。

## 问题
- 经过认证的程序合成需要从自然语言生成代码、形式化规格和机器可检查的证明，但生成出的规格常常有误：要么过弱，无法排除错误程序；要么过强，导致任何有效实现都无法满足。
- 现有 vericoding 系统通常绑定在一种验证风格上，例如依赖 SMT 的 auto-active 工具或交互式证明器，这限制了方法在不同任务和工具之间的迁移。
- 论文报告称，VERINA 和 CLEVER 基准中大约 **10%** 的参考规格有缺陷，因此如果规格检查不严格，评测结果和训练目标都会受到影响。

## 方法
- 系统 LeetProof 构建在 Lean 中的 Velvet 之上。Velvet 在同一环境中支持三种模式：基于性质的测试、由 SMT 支持的验证条件求解，以及交互式 Lean 证明脚本。
- 这条流水线按阶段运行：先从自然语言任务生成形式化规格，再用生成的测试和随机化的基于性质测试验证该规格，然后合成 Velvet 程序和循环不变式，最后证明剩余的验证条件。
- 在规格验证阶段，系统会在测试用例上检查三件事：输入满足前置条件，期望输出满足后置条件，以及其他候选输出不会同样满足后置条件。这可以捕获规格不足的问题，例如把 `result = true <-> P` 错写成 `result = true -> P`。
- 在程序和不变式合成阶段，LLM 提出代码和不变式，随后验证器生成验证条件，尝试自动化策略，并在投入证明工作之前，用基于性质的测试为错误不变式或有缺陷的代码寻找反例。
- 自动化无法解决的剩余证明义务会交给 AI 辅助的 Lean 证明工具处理，这些工具可以访问 Mathlib 搜索和辅助引理，也可以委托给更强的外部 AI 证明器，例如 Aristotle。

## 结果
- 在规格推断任务上，论文声称其基于性质测试的规格生成器在 VERINA 上达到 **97.4% 语义准确率**。
- 随机化规格测试在 **VERINA** 和 **CLEVER** 中发现，大约 **10%** 的已发布参考规格存在缺陷。
- 作者引入了一个新的基准，包含 **50 个命令式风格的 LeetCode 题目**，并带有复杂度标注。
- 论文称，LeetProof 在 **相同固定预算** 下，达到的 **完全认证解比例显著高于** **单模式 Lean 基线**，而且这一结果在 **两个前沿 LLM 后端** 上都成立。当前摘录没有给出确切的完全认证解数量或百分比。
- 在一个示例中，自动化策略解决了 **18 个** 验证条件中的 **14 个**，剩下 **4 个** 需要交互式或 AI 辅助证明。
- 摘录没有提供完整的端到端基准表，因此这里能得到的最强定量结论是：**97.4%** 的规格准确率、约 **10%** 的基准缺陷率、**50 题**的基准规模，以及示例中的 **14/18 VC** 自动化结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16584v1](http://arxiv.org/abs/2604.16584v1)
