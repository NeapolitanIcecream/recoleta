---
source: arxiv
url: https://arxiv.org/abs/2605.08658v1
published_at: '2026-05-09T03:54:51'
authors:
- Shan Jiang
- Zijian Yi
- Chenguang Zhu
topics:
- code-generation
- inference-time-scaling
- program-sketching
- code-intelligence
- execution-based-selection
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching

## Summary
SketchVerify is an inference-time method for code generation that spends extra compute on different algorithmic sketches before sampling implementations. Its strongest claim is a weak-model gain on hard HumanEval+ problems; stronger model greedy decoding can still be cheaper and more accurate.

## Problem
- Small code models often repeat the same wrong algorithm when sampled many times, so extra candidates may add cosmetic variation instead of new solution strategies.
- This matters when a practitioner must use a cheap or low-latency model tier and wants better pass@1 without switching models.
- Flat sampling gives no direct control over how many distinct algorithms the model tries.

## Approach
- The model first lists K different algorithmic strategies for a programming problem, such as hash map, sorting with two pointers, or dynamic programming.
- For each strategy, it writes a partial Python program sketch with ?? holes for expressions, conditions, or bounds while keeping the main control flow fixed.
- The model fills each sketch M times, producing K×M candidate programs.
- Candidates are compiled and run on generated tests; passing candidates are grouped by execution fingerprints, and the shortest program in the largest behavior cluster is selected.
- The method keeps the selector close to flat Semantic Voting, so the main change is candidate generation rather than a new voting rule.

## Results
- On 19 HumanEval+ problems where Gemini 3.1 Flash Lite greedy fails, Lite Sketch K=2,M=5 solved 11/19 problems, or 58%, versus flat N=10 solving 5/19, or 26%, a +32 pp gain at matched candidate count.
- On the same hard subset, Lite Sketch K=10,M=10 solved 15/19, or 79%, versus flat N=100 solving 10/19, or 53%, a +26 pp gain at matched candidate count.
- Lite Sketch K=2,M=5 cost $3.8e-4 per problem and beat flat N=50, which solved 9/19, or 47%, at $1.1e-3 per problem.
- On full HumanEval+, Lite Sketch K=10,M=10 reached 92.1% pass@1, compared with Lite greedy at 85.4% and flat Semantic Voting at 92.7%.
- On a 100-problem Lite scaling sweep, Sketch K=2,M=5 reached 91.0% at about 11.6K tokens, while flat N=10 reached 85.0% at about 8.0K tokens; Sketch K=10,M=10 reached 93.0% at about 88.4K tokens, while flat N=100 reached 89.0% at about 62.0K tokens.
- Cross-tier results weaken the deployment claim: on the hard subset, Flash greedy solved 17/19, or 89%, at $1.1e-4 per problem, beating Lite Sketch K=10,M=10 at 15/19, or 79%, and $2.8e-3 per problem.

## Link
- [https://arxiv.org/abs/2605.08658v1](https://arxiv.org/abs/2605.08658v1)
