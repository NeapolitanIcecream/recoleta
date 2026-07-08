---
source: arxiv
url: https://arxiv.org/abs/2607.06341v1
published_at: '2026-07-07T14:39:59'
authors:
- Shuangxiang Kan
- Shuanglong Kan
- Sebastian Ertel
topics:
- automated-formal-verification
- code-agents
- coq
- lean4
- software-verification
- llm-proof-generation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Harnessing Code Agents for Automatic Software Verification

## Summary
Aria pairs a general LLM code agent with a verification harness to write machine-checked Coq and Lean proofs automatically. The paper claims full success on all targeted lemmas, including Iris separation-logic proofs and Rust library verification built on Iris.

## Problem
- Formal software verification gives strong correctness guarantees, but Coq and Lean proofs require expert labor and often take hours or days per hard lemma.
- Prior LLM proof systems use fixed proof strategies such as tactic prediction, premise retrieval, repair loops, or divide-and-conquer, and reported Coq success rates are about 12% to 48% on their benchmarks.
- The hard target is concurrent, shared-memory software verification in Iris, where proofs involve separation logic, ghost resources, and many possible thread interleavings.

## Approach
- Aria gives a whole lemma to an off-the-shelf code agent, mainly Claude Code with Claude Opus 4.7, and lets the agent choose the proof strategy.
- A harness checks every candidate proof with the Coq kernel or Lean, rejects unsound outputs, and returns the failing step, error message, and open goal.
- The system retries each lemma up to 30 times, feeding verifier errors back to the agent until the proof is accepted or the budget is exhausted.
- The harness blocks `admit` and `Admitted`, checks that target lemmas were not dropped or altered, applies timeouts for divergent tactics, runs an Iris linter, and screens shell commands.
- HHL, the Harness Hook Language, defines hooks, workspaces, and workflows so the same harness policy can drive different code agents.

## Results
- On Iris core modules `algebra`, `bi`, `base_logic`, and `program_logic`, Aria proves 4,257 of 4,257 lemmas: 100% coverage, 0 failures, and 0 Coq expert interventions.
- On RustBelt-style Rust standard-library proofs built on Iris, including Arc, Mutex, RwLock, RefCell, Rc, Weak, and Cell, it proves 217 of 217 lemmas: 100% coverage.
- On `reglang`, it proves 318 of 318 Coq theorems. The paper says prior LLM provers proved about 1 in 8 on this benchmark.
- On `iris-lean`, an unfinished Lean 4 port of Iris, it proves 72 of 72 not-yet-ported lemmas.
- Reported prior Coq systems include PALM at 40.4% on 10,842 CoqGym theorems, Rango at 32.0% on 10,396 CoqStoq theorems, and COPRA at 48.3% on a 118-theorem CompCert subset.
- The Iris campaign ran for about 380 hours of model time, about 16 days, with the only stated human action being launch.

## Link
- [https://arxiv.org/abs/2607.06341v1](https://arxiv.org/abs/2607.06341v1)
