---
source: arxiv
url: https://arxiv.org/abs/2605.18073v1
published_at: '2026-05-18T08:55:30'
authors:
- Anika Tabassum
- Md Sifat Hossain
- Md. Fahim Arefin
- Tariqul Islam
- Tarannum Shaila Zaman
topics:
- code-generation
- autonomous-programming
- multi-model-feedback
- llm-debugging
- competitive-programming
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback

## Summary
A-ProS is an autonomous programming system that improves competitive-programming solutions by pairing GPT-4 or GPT-5 code generators with separate LLM debugging critics and live judge feedback. On 367 ICPC and Codeforces problems, the paper reports large gains after three repair rounds, especially for GPT-5 workflows.

## Problem
- Single-shot LLM code generation often fails on algorithmic tasks because the model cannot use compiler, runtime, or judge feedback to repair a wrong solution.
- Competitive programming matters as a testbed because each task has strict correctness, time, and memory checks, so partial or plausible code receives no credit.
- Prior work gives limited controlled evidence on which parts of iterative code repair help: persistent context, repeated sampling, or a separate critic model.

## Approach
- A-ProS uses GPT-4 and GPT-5 as solution generators and three critic models for debugging feedback: Codestral-2508, Llama-3.3-70B, and DeepSeek-R1.
- The design tests 6 workflows from a 2 × 3 pairing of generators and critics.
- Each problem starts with one generated C++ solution, then allows up to 3 repair rounds after Codeforces returns a verdict such as Accepted, Wrong Answer, Runtime Error, or Time Limit Exceeded.
- The system keeps the conversation history across repair rounds, so the generator and critic can use earlier failures instead of starting each attempt with a blank prompt.
- The evaluation covers 367 problems: 167 ICPC World Finals problems from 2011–2024 and 200 Codeforces problems rated 1200–1800.

## Results
- GPT-5 workflows rise from 39 accepted initial solutions to 85–90 accepted solutions after 3 refinement rounds on the 367-problem set.
- GPT-4 workflows rise from 15 accepted initial solutions to 31–38 accepted solutions after 3 refinement rounds on the same set.
- In a paired ablation on 47 problems, stateful refinement beats stateless refinement by 8.5–10.6 percentage points at Itr3 acceptance.
- Stateful refinement reduces repeated failures by 2.9×–3.5× compared with stateless refinement.
- A-ProS reports gains 2.2×–2.3× larger than multi-round stateless refinement baselines.
- The ablation reports bootstrap 95% confidence intervals of [0.00, +0.15] for GPT-5 and [0.00, +0.11] for GPT-4, with GPT-5 exact McNemar p ≈ 0.063.

## Link
- [https://arxiv.org/abs/2605.18073v1](https://arxiv.org/abs/2605.18073v1)
