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
## 摘要
Agent-CoEvo 将仓库级缺陷修复视为对代码补丁和测试补丁的联合搜索，而不是假设测试是固定且正确的。在 SWE-bench Lite 和 SWT-bench Lite 上，它报告的修复效果和测试生成效果都高于此前的基于智能体和无智能体系统。

## 问题
- 仓库级问题修复通常从不完整或错误的行为约束开始，因为测试可能遗漏某些假设，或没有准确表达这个缺陷。
- 大多数 LLM 修复系统会把测试固定下来，并把它们当作最后的筛选条件，这会奖励过拟合补丁，也会拒绝有效修复。
- 这很重要，因为真实的软件修复依赖于同时修改实现代码和定义预期行为的测试。

## 方法
- 论文提出了 **Agent-CoEvo**，这是一个多智能体协同进化系统，包含用于生成代码补丁的 `CodeAgent` 和用于生成测试补丁的 `TestAgent`。
- `LocationAgent` 先把问题描述转成复现脚本，运行该脚本，并定位可能有缺陷的文件和代码行。
- 系统维护代码补丁候选和测试补丁候选两个种群，然后让每个测试候选都对每个代码候选运行，以构建一个通过/失败执行矩阵。
- 代码适应度取决于它通过了多少测试，以及它的行为与其他代码候选有多一致；测试适应度取决于高适应度代码候选是否能通过该测试。
- 新候选通过基于 LLM 的语义交叉生成，精英候选会在迭代之间保留。测试候选会在早期被过滤，因此它们必须在有缺陷的仓库上失败。

## 结果
- 在 **SWE-bench Lite（300 个问题）** 上，Agent-CoEvo 报告 **41.33% resolved**，高于 **DARS: 37.00%**、**KGCompass: 36.67%**、**Moatless Tools (DeepSeek-V3): 30.67%** 和 **Agentless 1.5: 32.00%**。
- 在 **SWT-bench Lite（276 个问题）** 上，Agent-CoEvo 报告 **46.4% resolved**，高于 **AssertFlip: 38.0%**、**AEGIS: 36.0%**、**OpenHands setup: 28.3%** 和 **SWE-Agent+: 18.5%**。
- 在 **SWT-bench Lite** 的测试质量上，Agent-CoEvo 报告 **56.0% ΔC**，高于 **OpenHands setup: 52.4%**、**AssertFlip: 44.2%** 和 **AEGIS: 44.2%**。
- 该方法使用 **10 的种群规模** 和 **5 轮进化迭代**，骨干模型为 **DeepSeek-V3-0324**。
- 摘录声称它相对仅代码、仅测试和通用型智能体基线都有稳定提升，但给出的文本没有包含研究问题中提到的各个单独组件的消融实验数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04580v1](http://arxiv.org/abs/2604.04580v1)
