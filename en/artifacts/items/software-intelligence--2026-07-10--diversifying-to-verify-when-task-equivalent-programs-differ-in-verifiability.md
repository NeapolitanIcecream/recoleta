---
source: arxiv
url: https://arxiv.org/abs/2607.09366v1
published_at: '2026-07-10T12:44:08'
authors:
- Shirley Yu
- Ruben Martins
topics:
- code-verification
- llm-code-generation
- program-synthesis
- formal-methods
- automated-software-production
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability

## Summary
Diversify2Verify tests whether different implementations of the same programming task are easier or harder for automated deductive verification. Across 73 tasks and 292 Why3 artifacts, generating array/list and recursive/imperative variants increased artifact verification to 52.7% and task coverage to 67.1%.

## Problem
- Fully verified software requires a correct implementation, a formal contract, and proof guidance such as invariants and termination arguments.
- Equivalent implementations can create different proof obligations, so a failed verification attempt may reflect implementation structure or missing annotations rather than incorrect task behavior.
- This matters for LLM-based software production because executable tests do not establish correctness, while one-shot generation often mixes specification, implementation, and proof repair.

## Approach
- The pipeline has three stages: infer and validate a representation-specific Why3 contract, generate executable implementations, and add proof annotations for full verification.
- For each task, it generates four families: array-recursive, array-imperative, list-recursive, and list-imperative.
- After the contract is accepted, it is frozen. Later repairs can change code or proof annotations within the assigned family but cannot weaken the semantic target or switch representation or control structure.
- Why3 checks contracts, test lemmas, executable behavior, safety, termination, and functional correctness. The pipeline uses bounded repair, with up to five implementation attempts and two final verification repair passes.

## Results
- The benchmark contains 73 tasks and 292 implementation artifacts covering integers, arrays, and lists.
- 96 artifacts verified initially, giving a 32.9% artifact-level rate; two repair passes raised this to 154 artifacts, or 52.7%.
- At least one variant verified for 49 of 73 tasks, producing a 67.1% task-level success rate.
- The strongest single implementation family verified 44 tasks, so combining families improved task coverage beyond any one family.
- The study reports that representation and control structure materially change verification outcomes, although it does not prove that the array and list contracts are formally equivalent beyond targeting the same benchmark-level task.

## Link
- [https://arxiv.org/abs/2607.09366v1](https://arxiv.org/abs/2607.09366v1)
