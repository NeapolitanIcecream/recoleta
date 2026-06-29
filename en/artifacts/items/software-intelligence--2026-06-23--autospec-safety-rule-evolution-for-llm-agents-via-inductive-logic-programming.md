---
source: arxiv
url: https://arxiv.org/abs/2606.24245v2
published_at: '2026-06-23T07:31:03'
authors:
- Pingchuan Ma
- Zhaoyu Wang
- Zimo Ji
- Yuguang Zhou
- Zhantong Xue
- Zongjie Li
- Shuai Wang
- Xiaoqin Zhang
topics:
- llm-agent-safety
- symbolic-rules
- inductive-logic-programming
- counterexample-guided-synthesis
- code-execution-safety
- human-feedback
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# AutoSpec: Safety Rule Evolution for LLM Agents via Inductive Logic Programming

## Summary
AutoSpec updates symbolic safety rules for LLM agents using labeled execution traces. It keeps rules readable while improving precision and recall on code-execution and embodied-agent safety tasks.

## Problem
- LLM agents can delete files, leak credentials, send unsafe network calls, or violate physical-world constraints through tool use.
- Hand-written safety rules are auditable, but they drift as models, tools, prompts, and workloads change.
- Neural safety classifiers can adapt, but they do not give the clear rule logic needed for review in safety-sensitive deployments.

## Approach
- AutoSpec starts with an expert rule set, a predicate library, and traces labeled safe or unsafe by users or reviewers.
- It runs the current rules on the traces, then collects false positives and false negatives as counterexamples.
- Inductive Logic Programming, implemented with ILASP, finds predicates that separate missed unsafe traces from wrongly blocked safe traces.
- The system turns those predicates into rule edits such as adding an exception, adding a conjunct, relaxing a condition, or adding a disjunctive branch.
- A verifier scores candidate rule sets on the labeled traces and keeps an edit only when it improves the score.

## Results
- The evaluation uses 291 execution traces across code-execution and embodied-agent domains.
- AutoSpec reports F1 scores of 0.98 in one domain and 0.93 in the other.
- It claims up to 94% false-positive reduction while maintaining high recall.
- The ILP-guided version reaches up to 4.8x higher F1 than heuristic CEGIS.
- The rule evolution loop converges in 4 to 5 iterations.
- The predicate libraries used in the evaluation contain 16 to 24 predicates per domain.

## Link
- [https://arxiv.org/abs/2606.24245v2](https://arxiv.org/abs/2606.24245v2)
