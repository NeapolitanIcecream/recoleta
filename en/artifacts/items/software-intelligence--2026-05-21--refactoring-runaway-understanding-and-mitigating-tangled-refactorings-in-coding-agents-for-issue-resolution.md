---
source: arxiv
url: https://arxiv.org/abs/2605.22526v1
published_at: '2026-05-21T14:18:29'
authors:
- Zhao Tian
- Zifan Zhang
- Tao Xiao
- Dong Wang
- Masanari Kondo
- Junjie Chen
- Yasutaka Kamei
topics:
- coding-agents
- automated-software-engineering
- issue-resolution
- refactoring
- patch-quality
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# "Refactoring Runaway": Understanding and Mitigating Tangled Refactorings in Coding Agents for Issue Resolution

## Summary
The paper studies unrequested refactorings in coding-agent patches for Java issue resolution and shows that these changes often hurt compilation. It introduces RefUntangle, a refinement step that checks whether refactorings are needed and safe, then removes or repairs risky ones.

## Problem
- Coding agents sometimes expand small bug fixes or feature changes into large structural edits, which increases review cost and can break builds.
- Existing SWE-bench-style evaluations mostly measure whether tests pass, so they miss structural patch quality and refactoring side effects.
- The paper asks how agent refactorings differ from human developer refactorings and whether they affect compilability or issue-resolution success.

## Approach
- The study uses the Java part of Multi-SWE-bench: 128 human golden patches and 4,608 patches produced by 3 agent systems using 12 LLMs.
- After patch filtering and removal of 2 abnormal rollback patches, the analysis covers 3,691 valid agent patches.
- RefactoringMiner 3.0 detects tangled refactorings in both human and agent patches.
- The authors compare refactoring frequency, density, and type diversity across agents, models, and human patches.
- RefUntangle uses an LLM-based assessment to judge whether each refactoring is necessary and safe, then selectively removes or repairs problematic operations.

## Results
- Agent patches contain tangled refactorings less often than human patches: 21.43% of agent patches, 791/3,691, versus 36.72% of human patches, 47/128.
- Agent patches have lower refactoring density than human patches: 0.66 refactorings per patch, 2,429/3,691, versus 1.75 per patch, 224/128.
- Agents cover more refactoring types: 73 distinct types versus 46 in human patches.
- Across agent systems, SWE-agent has the highest tangled-refactoring ratio at 25.85%, 371/1,435, while OpenHands has the lowest at 14.68%, 154/1,049.
- Logistic regression finds that tangled refactorings are associated with lower compilability, with no statistically significant link to functional correctness.
- RefUntangle raises average compilation success from 19.34% to 38.33% and makes 2.79% of previously unresolved patches pass all tests.

## Link
- [https://arxiv.org/abs/2605.22526v1](https://arxiv.org/abs/2605.22526v1)
