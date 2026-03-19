---
source: arxiv
url: http://arxiv.org/abs/2603.03406v1
published_at: '2026-03-03T16:57:14'
authors:
- Jan Miller
topics:
- code-synthesis
- multi-model-collaboration
- code-review
- llm-agents
- benchmarking
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Review Beats Planning: Dual-Model Interaction Patterns for Code Synthesis

## Summary
本文研究两种模型如何协作生成更好的代码，核心结论是“先审查再修复”明显优于常见的“先规划再编码”。在开源量化模型和普通GPU上，该模式在 HumanEval+ 上达到 90.2% pass@1，超过若干更大或专有模型。

## Problem
- 论文要解决的问题是：**两个语言模型应该如何交互，才能比单个模型生成更可靠的代码**，这对低成本、本地部署的代码生成系统很重要。
- 常见做法是让推理模型先做计划、代码模型再实现，但作者发现这种“plan-then-code”在代码任务上可能**反而把正确解带偏**。
- 这很重要，因为很多软件智能体、多模型编程系统默认采用“规划→执行”范式；如果交互方向错了，系统复杂度增加却可能降性能。

## Approach
- 使用两个不同角色的模型：**代码专长模型** Qwen2.5-Coder-14B-Instruct 和 **推理通才模型** Qwen3-32B，均为 AWQ 4-bit 量化，运行在两张 A10G 上。
- 对比三种双模型模式：**plan-then-code**（先规划后编码）、**review-then-fix**（先编码后审查修复）、**adversarial dual-generation**（两者独立生成再交叉验证）。
- 核心方法是 **review-then-fix**：先让代码模型自由写代码，再让推理模型按题目规格检查 bug，最后让代码模型根据具体反馈修复。简单说，就是**不要先告诉程序员怎么写，而是在写完后指出哪里错了**。
- 作者还加入一个可选 **retry** 变体：利用题面可见 doctest/示例做编译与执行检查，失败后把错误反馈给模型，最多重试 3 次；并强调不会使用隐藏测试，避免泄漏。
- 进一步用 HumanEval+（规格丰富）和 MBPP+（规格精简）比较，分析一个关键调节因素：**规格越详细，审查越有效**。

## Results
- 在 **HumanEval+** 上，单独代码模型 **78.0%**，单独推理模型 **84.1%**；而 **plan-then-code 只有 75.6%**，比代码模型基线**低 2.4 个百分点**。
- **review-then-fix（无 retry）** 在 HumanEval+ 达到 **87.8%**，相对代码模型基线提升 **+9.8pp**；加入 retry 后达到 **90.2%**，相对基线提升 **+12.2pp**。
- 在 **HumanEval** 上，review-then-fix + retry 达到 **93.3%**；adversarial debate 在 HumanEval+ 为 **86.6%**，优于基线但低于 review-then-fix。
- 与公开参考结果比较：作者系统在 **HumanEval+ 90.2%**，高于 **GPT-4o 87.2%**、**O1 Preview 89.0%**、**Qwen2.5-Coder-32B FP16 87.2%**；硬件成本约 **$2/小时**（2×A10G）。
- 跨 **542 道题**（HumanEval+ 164 + MBPP+ 378）验证发现，审查效果受规格丰富度显著影响：在 **HumanEval+** 上提升 **+9.8pp**，在 **MBPP+** 上仅 **+2.3pp**，前者约为后者 **4 倍**，但两者都仍是净正收益。
- 失败分析显示，plan-then-code 在 164 题中造成 **15 个退化**、仅带来 **14 个改进**；主要退化原因包括 **缺失导入 7 例**、**算法翻译失误 5 例**、**过度工程 2 例**、**变量名“纠正”错误 1 例**。

## Link
- [http://arxiv.org/abs/2603.03406v1](http://arxiv.org/abs/2603.03406v1)
