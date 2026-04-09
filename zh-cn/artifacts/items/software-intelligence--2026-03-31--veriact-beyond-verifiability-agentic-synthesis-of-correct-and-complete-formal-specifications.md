---
source: arxiv
url: http://arxiv.org/abs/2604.00280v1
published_at: '2026-03-31T22:12:15'
authors:
- Md Rakib Hossain Misu
- Iris Ma
- Cristina V. Lopes
topics:
- formal-specification-synthesis
- program-verification
- jml
- llm-agents
- benchmark-evaluation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# VeriAct: Beyond Verifiability -- Agentic Synthesis of Correct and Complete Formal Specifications

## Summary
## 概要
本文认为，把验证器通过率当作形式化规格合成的目标过于薄弱，并提出 VeriAct 来生成可验证、正确且完整的 JML 规格。论文还提出了 Spec-Harness，这是一种评估方法，用来检查被验证器接受的规格是否真正刻画了程序行为。

## 问题
- 任务是为 Java 方法自动合成形式化的 Java Modeling Language（JML）规格。
- 现有系统通常用 OpenJML 是否接受该规格来判断是否成功，但验证器也可能接受过弱、不完整或错误的规格。
- 这很重要，因为薄弱的规格会漏掉真实行为、拒绝有效输入，或允许无效输出，从而损害验证、测试和软件可靠性。

## 方法
- 作者先比较了经典方法（Daikon、Houdini）和基于提示的 LLM 方法（SpecGen、AutoSpec、FormalBench prompts），使用两个基准：SpecGenBench 和 FormalBench。
- 然后，他们应用 GEPA 提示优化，用结构化的验证器反馈而不是简单的通过/失败奖励，来提升基于提示的合成效果。
- 他们提出了 **Spec-Harness**，这是一个自动化评估框架，通过符号验证以及基于 Hoare 三元组推理、类似输入/输出变异检查的方法，来检验规格的正确性和完整性。
- 他们提出了 **VeriAct**，这是一个 agentic 闭环系统：LLM 负责规划并编写规格，运行代码和验证工具，读取 Spec-Harness 的反馈，并反复修复规格，直到它更符合方法行为。

## 结果
- 数据集规模：SpecGenBench 有 120 个任务；FormalBench 从 700 个任务中过滤后，有 662 个可用任务。
- 经典基线在验证器通过率上的结果：Houdini 在 SpecGenBench 上达到 **104/120 (86.7%)**，在 FormalBench 上达到 **359/662 (54.2%)**；Daikon 分别达到 **22/120 (18.3%)** 和 **87/662 (13.1%)**。
- 最好的基于提示的方法在验证器通过率上仍低于 Houdini：SpecGen 为 **80/120 (66.7%)** 和 **200/659 (30.3%)**；AutoSpec 为 **70/120 (58.3%)** 和 **185/662 (27.9%)**；FormalBench prompts 为 **77/120 (64.2%)** 和 **238/662 (36.0%)**。
- 提示敏感性很大。对 SpecGen 来说，平均验证器通过率从最佳设置下降到 SpecGenBench 上的 **43.1%**，以及 FormalBench 上的 **20.1%**。
- 主要的定性结论是，许多被验证器接受的规格，包括经过提示优化的规格，在用 Spec-Harness 检查时仍然是错误的或不完整的。
- 摘要指出，VeriAct 在两个基准上的正确性和完整性方面都优于基于提示和经过提示优化的基线，但所给文本没有提供 VeriAct 最终提升的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.00280v1](http://arxiv.org/abs/2604.00280v1)
