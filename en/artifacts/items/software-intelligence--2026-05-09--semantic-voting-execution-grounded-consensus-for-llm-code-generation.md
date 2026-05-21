---
source: arxiv
url: https://arxiv.org/abs/2605.08680v1
published_at: '2026-05-09T04:33:39'
authors:
- Shan Jiang
- Zijian Yi
- Chenguang Zhu
topics:
- code-generation
- execution-based-selection
- llm-code-evaluation
- consensus-voting
- test-input-generation
- software-foundation-models
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Semantic Voting: Execution-Grounded Consensus for LLM Code Generation

## Summary
Semantic Voting studies how to select one program from many LLM-generated code candidates when no full test oracle is available. Its main claim is that execution traces from good generated inputs matter more than the specific consensus rule.

## Problem
- LLM code pipelines often sample many candidates, then need to choose one final answer without complete tests.
- Output-pattern majority voting discards candidates that fail on any generated input, so one bad probe can remove a correct program.
- Better selection matters because pass@1 depends on choosing the correct candidate from a pool where correct code may already exist.

## Approach
- SemanticVote samples N candidate programs, filters syntax errors, and generates test inputs with sketches.
- Sketch-based input generation asks an LLM for K abstract input categories, then instantiates each M times; the default is K=10, M=5, D=50 inputs.
- Each candidate runs on all generated inputs in a sandbox with a 5-second timeout, producing an execution fingerprint of outputs, exception types, or timeouts.
- Candidates with identical fingerprints form clusters; the method picks the shortest program from the largest all-success cluster, or the largest cluster if none fully succeed.
- The paper compares SemanticVote with output-pattern majority voting, AST-normalized majority voting, weighted voting, and MBR-Exec across Gemini models and benchmarks.

## Results
- Across 18 configurations on HumanEval+ and MBPP+, the best execution-based selector beats output-pattern majority voting by 19–52 percentage points; every execution-based selector beats it by at least 18 points.
- On HumanEval+ with N=50, output-pattern majority voting scores 43.9–77.4% pass@1, while weighted voting, MBR-Exec, and SemanticVote score 92.1–98.8% depending on model and thinking level.
- On MBPP+ with N=50, output-pattern majority voting scores 39.4–77.2%, while the execution-based methods score 90.7–97.4%.
- SemanticVote, weighted voting, and MBR-Exec are statistically tied in all 18 configurations; paired bootstrap tests report p>0.05, and SemanticVote differs from weighted voting by -0.79 to +0.61 percentage points.
- Sketch-based inputs are the strongest input source in the ablation, beating direct LLM concrete inputs by 0.6–2.1 points and beating random fuzzing or example-only inputs by up to 11.3 points.
- Oracle-gap analysis finds generation failures average 2.8% on HumanEval+ and 3.9% on MBPP+, while selection failures average 1.5–2.7%; this limits the room for one execution-based aggregator to beat another.

## Link
- [https://arxiv.org/abs/2605.08680v1](https://arxiv.org/abs/2605.08680v1)
