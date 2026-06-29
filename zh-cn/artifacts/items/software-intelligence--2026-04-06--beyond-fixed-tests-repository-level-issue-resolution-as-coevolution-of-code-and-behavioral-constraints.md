---
source: arxiv
url: http://arxiv.org/abs/2604.04580v1
published_at: '2026-04-06T10:26:46'
authors:
- Kefan Li
- Yuan Yuan
- Mengfei Wang
- Shihao Zheng
- Wei Wang
- Ping Yang
- Mu Li
- Weifeng Lv
topics:
- program-repair
- multi-agent-systems
- test-generation
- repository-level-reasoning
- swe-bench
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints

## Summary
## 总结
Agent-CoEvo 把仓库级 bug 修复看作代码补丁和测试补丁的联合搜索，而不是假设测试是固定且正确的。在 SWE-bench Lite 和 SWT-bench Lite 上，它报告的修复率和测试生成性能都高于先前的基于智能体和无智能体系统。

## 问题
- 仓库级问题修复常常从不完整或错误的行为约束开始，因为测试可能遗漏假设，或者把 bug 表达得不好。
- 大多数基于 LLM 的修复系统保持测试不变，并把它们当作最终过滤器，这会奖励过拟合补丁，并拒绝有效修复。
- 这很重要，因为真实的软件修复依赖于同时修改实现和定义预期行为的测试。

## 方法
- 论文提出 **Agent-CoEvo**，一种多智能体共进化系统，包含用于代码补丁的 `CodeAgent` 和用于测试补丁的 `TestAgent`。
- `LocationAgent` 先把问题描述转成复现脚本，运行脚本，并定位可能有缺陷的文件和行。
- 系统维护候选代码补丁和测试补丁的种群，然后让每个测试候选与每个代码候选运行，构建通过/失败执行矩阵。
- 代码适应度取决于它通过了多少测试，以及它的行为与其他代码候选的一致程度；测试适应度取决于高适应度代码候选是否会把它通过。
- 新候选由基于 LLM 的语义交叉生成，优秀候选会在迭代中保留。测试候选会提前筛选，必须在有 bug 的仓库上失败。

## 结果
- 在 **SWE-bench Lite（300 个问题）** 上，Agent-CoEvo 报告 **41.33% resolved**，高于 **DARS: 37.00%**、**KGCompass: 36.67%**、**Moatless Tools (DeepSeek-V3): 30.67%** 和 **Agentless 1.5: 32.00%**。
- 在 **SWT-bench Lite（276 个问题）** 上，Agent-CoEvo 报告 **46.4% resolved**，高于 **AssertFlip: 38.0%**、**AEGIS: 36.0%**、**OpenHands setup: 28.3%** 和 **SWE-Agent+: 18.5%**。
- 在 **SWT-bench Lite** 的测试质量上，Agent-CoEvo 报告 **56.0% ΔC**，高于 **OpenHands setup: 52.4%**、**AssertFlip: 44.2%** 和 **AEGIS: 44.2%**。
- 该方法使用 **population size 10** 和 **5 evolutionary iterations**，并以 **DeepSeek-V3-0324** 作为骨干模型。
- 摘要声称它在仅代码、仅测试和通用智能体基线之上都有稳定提升，但所给文本没有包含研究问题中讨论的各个组件的消融数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04580v1](http://arxiv.org/abs/2604.04580v1)
