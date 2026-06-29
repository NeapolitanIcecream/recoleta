---
source: arxiv
url: http://arxiv.org/abs/2604.05399v2
published_at: '2026-04-07T03:49:12'
authors:
- Youngjoo Ahn
- Sangyeop Yeo
- Gijung Im
- Jongmin Lee
- Jinyoung Yeo
- Jieung Kim
topics:
- formal-verification
- automated-theorem-proving
- proof-search
- llm-for-code
- interactive-theorem-proving
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# PROMISE: Proof Automation as Structural Imitation of Human Reasoning

## Summary
PROMISE targets automated proof generation for large formal verification projects, where current LLM-based methods lose accuracy on long, interdependent proofs. It guides proof search with structurally similar proof-state transitions instead of relying on surface text matches to prior lemmas or scripts.

## Problem
- Formal verification can give machine-checked correctness guarantees for safety-critical software, but proof construction is still expensive and requires expert interactive theorem proving.
- Existing LLM-based proof systems often treat proving as single-shot generation, next-tactic prediction, or text-based retrieval over lemmas and proofs; these methods struggle when proofs have deep dependencies across modules and files.
- On system-scale benchmarks such as seL4 or FSCQ, the paper states that proof coverage for mid-level lemmas often stays below 30% for prior methods, which limits practical use on verified systems software.

## Approach
- PROMISE models a proof as a sequence of proof states and tactic-induced transitions, then searches for prior transitions that evolve in a similar way to the current proof state.
- It retrieves structurally compatible proof fragments based on proof-state evolution patterns, not just lexical similarity between theorem statements or proof text.
- It combines this structural retrieval with context-aware lemma retrieval from the active proof environment, using available lemmas whose roles fit the current goal state.
- The system runs as an iterative, stateful proof search loop that proposes short tactic continuations, checks them with the proof assistant, and expands the search using retrieved transition traces.
- The method is model-agnostic and uses off-the-shelf LLMs without extra training; the paper evaluates it with GPT-3.5-Turbo, Qwen2.5-Coder-7B-Instruct, and also discusses GPT-4.1 settings.

## Results
- On the seL4 microkernel verification benchmark, PROMISE reports improvements of up to **+26 percentage points**, which the paper describes as a **186% relative gain**, over prior LLM-based proof automation approaches.
- The paper compares against **Selene** and **Rango** and says PROMISE outperforms prior approaches in the **majority of settings** under the same query budget.
- In the single exception named in the excerpt, **GPT-4.1/P2**, PROMISE remains competitive with the strongest baseline rather than leading it.
- PROMISE keeps performance strong across different model sizes and capabilities; the excerpt says the gap between **Qwen2.5-Coder-7B-Instruct** and **GPT-3.5-Turbo** is small within PROMISE, while other methods show larger model sensitivity.
- The excerpt does not provide the full result table, exact success-rate values for each model, or per-benchmark breakdown beyond the headline **+26-point / 186%** improvement claim.

## Link
- [http://arxiv.org/abs/2604.05399v2](http://arxiv.org/abs/2604.05399v2)
