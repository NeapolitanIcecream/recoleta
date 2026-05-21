---
source: arxiv
url: https://arxiv.org/abs/2605.01394v1
published_at: '2026-05-02T11:31:33'
authors:
- Dong Xu
- Jialun Cao
- Guozhao Mo
- Junjie Hu
- Cheng Wen
- Hongyu Lin
- Xianpei Han
- Shengchao Qin
- Cong Tian
- Shing-Chi Cheung
- Le Sun
- Yaojie Lu
topics:
- formal-specification
- code-intelligence
- llm-evaluation
- agentic-workflows
- program-verification
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation

## Summary
LiveFMBench evaluates how well LLMs and agentic pipelines generate ACSL formal specifications for C programs. The paper claims current systems improve with sampling, reasoning mode, and agent workflows, but their measured accuracy is inflated unless unfaithful outputs are filtered.

## Problem
- Writing correct formal specifications for C programs is expensive and requires expertise in contracts, preconditions, postconditions, and loop invariants.
- Prior LLM evaluations may include data leakage from GitHub or older benchmarks, so reported accuracy can mix real capability with memorization.
- Automated provers can be fooled when a model changes the program or assertion instead of adding valid specifications, which makes naive pass rates too high.

## Approach
- The authors build LiveFMBench with 630 ACSL-annotated C programs: 270 pre-2025 programs and 360 newly collected SV-COMP 2025 programs to reduce contamination risk.
- They evaluate 15 open-source LLMs under direct prompting, reasoning-enabled thinking mode, and an AutoSpec-style agentic pipeline.
- They use Frama-C v27.1 with Alt-Ergo and Z3 to check whether generated ACSL specifications prove the target assertions.
- They measure pass@1, pass@5, and pass@32, then filter outputs for faithfulness by checking AST equivalence and preserving the original assertion expressions.
- They label failures by type, including missing specifications, incorrect pre/postconditions, flawed loop invariants, and verifier misuse.

## Results
- Naive evaluation overestimates direct-prompting performance: after filtering unfaithful outputs, true specification generation accuracy drops by about 20%.
- More samples help: pass@5 is about 2× pass@1 on average, and pass@32 is about 3× pass@1 on average.
- Thinking mode improves success rates by 19.40% to 2465.52% relative, depending on the model and setting.
- Qwen3-32B gains strongly from thinking mode, with pass@5 rising from 6.33 to 27.44.
- The agentic pipeline helps most under low sampling budgets and on harder datasets, while its edge shrinks as sampling increases.
- Failure analysis finds incorrect loop invariants are the most common error type; the agentic pipeline reduces assertion errors, though the excerpt does not give the exact reduction size.

## Link
- [https://arxiv.org/abs/2605.01394v1](https://arxiv.org/abs/2605.01394v1)
