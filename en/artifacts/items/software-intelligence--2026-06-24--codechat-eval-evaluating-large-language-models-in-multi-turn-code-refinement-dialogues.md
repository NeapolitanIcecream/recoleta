---
source: arxiv
url: https://arxiv.org/abs/2606.25747v1
published_at: '2026-06-24T12:16:04'
authors:
- Guoxiang
- Guo
- Kla Tantithamthavorn
- Neelofar Neelofar
- Yuanyuan Qi
- Aldeida Aleti
topics:
- code-intelligence
- software-foundation-models
- code-generation
- multi-turn-evaluation
- llm-benchmarks
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues

## Summary
CodeChat-Eval tests whether code LLMs keep already-correct code correct across developer follow-up edits. The paper finds large correctness regressions in 10-turn code refinement dialogues.

## Problem
- Existing coding benchmarks such as HumanEval, MBPP, SWE-Bench, and BigCodeBench mostly test a single request, so they miss regressions caused by later refinement instructions.
- The setting matters because developers often ask for follow-up edits such as style cleanup, refactoring, or a different implementation strategy while expecting the original behavior to stay unchanged.
- The paper measures both whether the refined code still passes the original tests and whether the model followed the edit instruction.

## Approach
- CodeChat-Eval starts from 542 programming tasks: 164 from HumanEval and 378 from MBPP.
- Each evaluation session has 10 turns: 1 initial code-generation turn and 9 follow-up refinement turns.
- Refinement instructions come from CodeAlignBench. The authors curate 169 raw instructions, filter out 11 that alter functionality or break the test harness, and classify the rest by scope and change operation.
- Scope categories are cosmetic, structural, and semantic. Change operations are add, remove, and modify.
- An agenda-guided dynamic instruction selection algorithm chooses an applicable instruction for the current code at each turn, then tests the new code with the original test suite and checks instruction adherence with an LLM judge.

## Results
- The study evaluates 8 open-weight and proprietary LLMs from the Llama, Qwen, DeepSeek, and GPT families.
- Functional correctness drops by 19.2% for GPT-5 Nano and by 69.2% for Llama 3.1 8B after multi-turn refinement, compared with the earlier correct state.
- The paper reports statistically significant correctness declines across all evaluated LLMs.
- Semantic refinement instructions have the largest scope-level effect, with a 21% correctness decrease.
- Additive change requests have the largest operation-level effect, with a 17% correctness decrease.
- The 10-turn setup is chosen to cover 95% of real-world dialogue lengths cited by the authors.

## Link
- [https://arxiv.org/abs/2606.25747v1](https://arxiv.org/abs/2606.25747v1)
