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
## 总结
这篇论文认为，验证器通过率对形式化规格合成来说是一个很弱的目标，并提出 VeriAct，用来生成可验证、正确且完整的 JML 规格。论文还提出了 Spec-Harness，一种评估方法，用来检查被验证器接受的规格是否真的捕捉了程序行为。

## 问题
- 任务是为 Java 方法自动合成形式化的 Java Modeling Language (JML) 规格。
- 现有系统通常用 OpenJML 是否接受规格来判断成功，但验证器会接受过弱、部分正确或错误的规格。
- 这很重要，因为过弱的规格会漏掉真实行为、拒绝有效输入，或允许无效输出，从而损害验证、测试和软件可靠性。

## 方法
- 作者先在两个基准上比较了经典方法（Daikon、Houdini）和基于提示的 LLM 方法（SpecGen、AutoSpec、FormalBench prompts）：SpecGenBench 和 FormalBench。
- 然后他们使用 GEPA 提示优化，把结构化的验证器反馈用于改进提示式合成，而不是只用简单的通过/失败奖励。
- 他们提出 **Spec-Harness**，这是一个自动化评估框架，通过符号验证，加上建立在霍尔三元组推理上的输入/输出变异式检查，来判断规格的正确性和完整性。
- 他们提出 **VeriAct**，一个有代理性的闭环系统：LLM 负责规划和编写规格，运行代码和验证工具，读取 Spec-Harness 的反馈，并迭代修复规格，直到它更符合方法行为。

## 结果
- 数据集规模：SpecGenBench 有 120 个任务，FormalBench 从 700 个任务中过滤后得到 662 个可用任务。
- 经典基线的验证器通过率：Houdini 在 SpecGenBench 上达到 **104/120 (86.7%)**，在 FormalBench 上达到 **359/662 (54.2%)**；Daikon 分别为 **22/120 (18.3%)** 和 **87/662 (13.1%)**。
- 最好的基于提示的方法在通过率上都低于 Houdini：SpecGen 为 **80/120 (66.7%)** 和 **200/659 (30.3%)**；AutoSpec 为 **70/120 (58.3%)** 和 **185/662 (27.9%)**；FormalBench prompts 为 **77/120 (64.2%)** 和 **238/662 (36.0%)**。
- 提示敏感性很强。对 SpecGen 而言，从最佳设置到平均设置，验证器通过率降到 SpecGenBench 上的 **43.1%**，FormalBench 上的 **20.1%**。
- 主要的定性结论是，很多被验证器接受的规格，包括经过提示优化的规格，在 Spec-Harness 检查下仍然是错误或不完整的。
- 摘要中还说，VeriAct 在两个基准上对正确性和完整性的表现都优于基于提示和经过提示优化的基线，但给出的文本里没有包含 VeriAct 最终的数值提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.00280v1](http://arxiv.org/abs/2604.00280v1)
