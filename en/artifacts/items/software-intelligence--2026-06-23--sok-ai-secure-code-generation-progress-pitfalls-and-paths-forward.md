---
source: arxiv
url: https://arxiv.org/abs/2606.25195v1
published_at: '2026-06-23T21:39:05'
authors:
- Rupam Patir
- Keyan Guo
- Haipeng Cai
- Hongxin Hu
topics:
- secure-code-generation
- code-intelligence
- software-security
- coding-agents
- benchmarking
- llm-evaluation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# SoK: AI Secure Code Generation: Progress, Pitfalls, and Paths Forward

## Summary
The paper argues that AI secure code generation should be judged by whether models know secure coding principles and whether they turn that knowledge into working, exploit-resistant code. It introduces Kauge, an evaluation method that separates secure-coding knowledge, code actuation, and the gap between them.

## Problem
- Current secure-code-generation benchmarks often score only the generated program, so a pass/fail result can hide whether the model lacked the rule, applied it in the wrong place, or broke functionality while blocking an exploit.
- This matters because coding agents and LLMs now write and repair software at scale, and insecure generated code can reach real applications.
- Static-analysis-based checks can miss exploitable bugs or reward code that only satisfies a checker, so executable functionality and exploit tests give a stronger signal.

## Approach
- Kauge uses secure coding principles from OWASP and CERT as the unit of measurement, since these principles describe the defensive behavior code should implement.
- The method has 3 layers: Knowledge tests whether a model understands secure coding principles in natural language; Actuation tests whether generated code is functional and exploit-resistant; Gap checks whether the code implements the defensive mechanism tied to the relevant principle.
- The authors build an NLU benchmark with 6,382 verified fixed-answer questions derived from 456 source rules.
- The questions cover 4 reasoning dimensions: declarative, causal, procedural, and contextual reasoning.
- They also build an exploit-to-principle defense mapping and an SCP-compliance judge, then test models and coding agents on CWEval for function-level security and BaxBench for full web-application security.

## Results
- The excerpt gives no exact accuracy, correlation coefficient, p-value, or model-by-model table, so the claimed statistical result cannot be checked numerically from the provided text.
- The paper claims that secure-coding-principle understanding is a statistically strong predictor of 3 code outcomes: functional correctness, security, and joint functional-security correctness.
- The study reports a persistent knowledge-actuation gap: models often recognize the relevant secure coding principle but fail to implement the right defense at the right code boundary.
- At the Knowledge layer, current systems score far above chance across OWASP and CERT principles, with the main weakness in causal reasoning for lower-level CERT C/C++ rules; no exact scores are provided in the excerpt.
- At the Actuation layer, function-level failures split between nonfunctional code and functional but exploitable code, while application-level tasks often fail before security testing because the generated backend does not run.
- The paper identifies 4 gap cases: principled success, secure by other means, compliant but vulnerable, and direct actuation failure.

## Link
- [https://arxiv.org/abs/2606.25195v1](https://arxiv.org/abs/2606.25195v1)
