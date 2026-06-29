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
本文介绍了 LeetProof，这是一条认证程序合成流水线，在 Lean 中用同一个验证器完成测试、自动证明和交互式证明。核心主张是，这种分阶段、多模态设计能更早发现错误规格，并在相同预算下，比仅用 Lean 的单一模式基线产出更多完全认证的程序。

## 问题
- 认证程序合成必须从自然语言生成代码、形式规格和机器可检查的证明，但生成出来的规格常常有问题：要么太弱，挡不住错误程序，要么太强，没有任何有效程序能满足。
- 现有 vericoding 系统绑定在一种验证风格上，比如依赖 SMT 的 auto-active 工具或交互式证明器，这限制了它们在不同任务和工具之间的迁移。
- 论文报告说，VERINA 和 CLEVER 基准中的参考规格大约有 10% 有缺陷，所以如果规格检查不严，评测和训练目标都会被污染。

## 方法
- 系统 LeetProof 构建在 Lean 中的 Velvet 之上。Velvet 在同一个环境里支持三种模式：基于属性的测试、由 SMT 支持的验证条件消解，以及交互式 Lean 证明脚本。
- 流水线分阶段运行：先从自然语言任务生成形式规格，再用生成的测试和随机属性测试验证该规格，然后合成带循环不变式的 Velvet 程序，最后证明剩余的验证条件。
- 在规格验证中，它会在测试用例上检查三件事：输入是否满足前置条件，期望输出是否满足后置条件，以及其他输出是否也满足后置条件。这样可以发现规格不足的情况，比如把 `result = true -> P` 写成了 `result = true <-> P` 之外的弱形式。
- 在程序和不变式合成中，LLM 先提出代码和不变式，然后验证器生成验证条件，尝试自动战术，并用基于属性的测试在证明投入之前找出坏不变式或有 bug 的代码对应的反例。
- 自动化无法解决的剩余证明义务会交给 AI 辅助的 Lean 证明工具，这些工具可以访问 Mathlib 搜索和辅助引理，也可以转交给更强的外部 AI 证明器，比如 Aristotle。

## 结果
- 在规格推断上，论文声称其基于属性测试的规格生成器在 VERINA 上达到 **97.4% 的语义准确率**。
- 随机规格测试在 **VERINA** 和 **CLEVER** 中发现了大约 **10%** 的已发表参考规格有缺陷。
- 作者提出了一个新的基准，包含 **50 个命令式风格的 LeetCode 题目**，并附有复杂度标注。
- 论文说明，在 **相同固定预算** 下，LeetProof 相比 **单一模式的 Lean 基线**，能显著提高**完全认证解**的比例，而且这一结果在 **两个前沿 LLM 后端** 上都成立。摘要没有给出具体的认证解数量或百分比。
- 在一个示例中，自动战术解决了 **18 个验证条件中的 14 个**，剩下 **4 个** 需要交互式或 AI 辅助证明。
- 这段摘要没有给出端到端基准结果的完整表格，所以这里最强的定量结论是 **97.4%** 的规格准确率、基准中约 **10%** 的缺陷率、**50 题** 的基准规模，以及示例里 **14/18 VC** 的自动化结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16584v1](http://arxiv.org/abs/2604.16584v1)
