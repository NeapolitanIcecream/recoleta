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
WybeCoder 是一个混合代理系统，用于生成并形式化验证命令式程序。它把基于 SMT 的验证和 Lean 的交互式证明工作结合起来，并报告了相较于这一场景下更早的已验证代码基准更高的通过率。

## 问题
- LLM 在代码生成和定理证明上都有进展，但生成软件的形式化验证仍然落后，尤其是带有可变状态和循环的命令式代码。
- 现有工作通常只处理定理证明器中的函数式程序，或者自动活性系统如 Dafny 中的命令式程序；两者都没有覆盖问题的全部。
- 这很重要，因为生成的代码仍然需要昂贵的人工审查，而且测试或模糊测试不能给出完整的正确性保证。

## 方法
- 系统采用 prove-as-you-generate 循环：生成命令式代码，生成不变式，运行验证条件生成，把常规义务发送给 CVC5，把困难的剩余部分发送给 Lean。
- 它使用两种代理风格：一个顺序细化代理，以及一个子目标分解的多代理系统，后者提取证明义务、并行求解，然后重建完整证明。
- 当某个证明子目标失败时，代理可以请求有针对性的代码或不变式修改。命名的不变式和确定性的目标名称让系统可以在修订之间迁移已解决的子证明。
- 作者把 Verina 和 Clever 这两个函数式验证基准翻译成命令式的 Velvet/Lean 任务来评估这套设置。
- 为了减少规格泄漏和函数式作弊，他们允许函数式规格，但要求命令式实现，然后用基于 LLM 的命令式判定器进行过滤。

## 结果
- 报告的最佳 Verina 结果：**74.1%** 通过率，使用 **Claude 4.5 Opus**、**顺序代理**、**32 轮 × 16 个代理**。
- 报告的最佳 Clever-Loom 结果：**62.1%** 通过率，使用 **Claude 4.5 Opus**、**顺序代理**、**32 轮 × 16 个代理**。
- 在 Verina 上，顺序代理得分为 **64.6%（GPT-5）**、**55.6%（Gemini 3 Pro）**、**63.3%（Claude 4.5 Sonnet）** 和 **74.1%（Claude 4.5 Opus）**。列出的基线是 **DS Prover V2 7B** 的 **20.0%**。
- 在 Clever-Loom 上，顺序代理得分为 **53.8%（GPT-5）**、**32.8%（Gemini 3 Pro）**、**59.6%（Claude 4.5 Sonnet）** 和 **62.1%（Claude 4.5 Opus）**，而 **COPRA** 基线是 **8.7%**。
- 论文强调了 Verina 上的低预算提升，从先前报告结果的 **18%** 提升到他们设置下的 **55%**，并且引用了小预算场景下混合验证从 **15% 到 55%** 的改进。
- 他们的泄漏控制影响很大：Verina 上一个 GPT-5 子目标分解设置在没有命令式约束时是 **75.1%**，加入该约束后降到 **51.9%**。作者把这视为对命令式已验证代码生成更诚实的度量。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29088v1](http://arxiv.org/abs/2603.29088v1)
