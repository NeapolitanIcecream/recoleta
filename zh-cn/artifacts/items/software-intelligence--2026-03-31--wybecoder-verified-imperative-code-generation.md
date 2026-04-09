---
source: arxiv
url: http://arxiv.org/abs/2603.29088v1
published_at: '2026-03-31T00:06:44'
authors:
- Fabian Gloeckle
- Mantas Baksys
- Darius Feher
- Kunhao Zheng
- Amaury Hayat
- Sean B. Holden
- Gabriel Synnaeve
- Peter O'Hearn
topics:
- formal-verification
- imperative-code-generation
- lean-theorem-proving
- multi-agent-systems
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# WybeCoder: Verified Imperative Code Generation

## Summary
## 摘要
WybeCoder 是一个用于生成并形式化验证命令式程序的混合智能体系统。它把基于 SMT 的验证与 Lean 中的交互式证明结合起来，并且在这一设定下报告的求解率明显高于早期的已验证代码基准。

## 问题
- LLM 在代码生成和定理证明上已有进展，但对生成软件的形式化验证仍然落后，尤其是涉及可变状态和循环的命令式代码。
- 现有工作通常只处理定理证明器中的函数式程序，或处理 Dafny 这类 auto-active 系统中的命令式程序；两者都只覆盖了问题的一部分。
- 这很重要，因为生成的代码仍然需要代价高昂的人工审查，而测试或模糊测试也无法给出完整的正确性保证。

## 方法
- 该系统采用 prove-as-you-generate 循环：生成命令式代码、生成不变式、运行 verification condition generation，把常规证明义务交给 CVC5，把剩余的困难部分交给 Lean。
- 它使用两种智能体形式：一种是顺序细化智能体，另一种是按子目标分解的多智能体系统，后者会提取证明义务、并行求解，并重建完整证明。
- 当某个证明子目标失败时，智能体可以请求对代码或不变式做有针对性的修改。具名不变式和确定性的目标名称让系统可以在版本修订之间复用已解决的子证明。
- 作者将 Verina 和 Clever 这两个函数式验证基准转换为等价的命令式 Velvet/Lean 任务，用来评估这一设定。
- 为了减少规格泄漏和用函数式实现规避要求的情况，他们允许使用函数式规格，但要求命令式实现，然后用基于 LLM 的命令式判别器进行过滤。

## 结果
- Verina 的最佳报告结果：使用 **Claude 4.5 Opus**、采用 **sequential agent**、配置为 **32 turns × 16 agents**，达到 **74.1% solve rate**。
- Clever-Loom 的最佳报告结果：使用 **Claude 4.5 Opus**、采用 **sequential agent**、配置为 **32 turns × 16 agents**，达到 **62.1% solve rate**。
- 在 Verina 上，sequential-agent 的成绩分别是 **64.6% (GPT-5)**、**55.6% (Gemini 3 Pro)**、**63.3% (Claude 4.5 Sonnet)** 和 **74.1% (Claude 4.5 Opus)**。文中列出的基线是 **DS Prover V2 7B** 的 **20.0%**。
- 在 Clever-Loom 上，sequential-agent 的成绩分别是 **53.8% (GPT-5)**、**32.8% (Gemini 3 Pro)**、**59.6% (Claude 4.5 Sonnet)** 和 **62.1% (Claude 4.5 Opus)**，相比之下 **COPRA** 基线是 **8.7%**。
- 论文指出，在 Verina 上，低预算设置的结果从此前报告的 **18%** 提高到他们方案的 **55%**，并给出小预算设定下混合验证从 **15% 到 55%** 的提升。
- 他们的泄漏控制影响很大：在 Verina 上，GPT-5 的一个子目标分解设定在没有命令式约束时是 **75.1%**，加入约束后降到 **51.9%**。作者认为后者更能真实反映命令式已验证代码生成的水平。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29088v1](http://arxiv.org/abs/2603.29088v1)
