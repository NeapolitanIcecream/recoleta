---
source: arxiv
url: https://arxiv.org/abs/2605.07001v2
published_at: '2026-05-07T22:33:32'
authors:
- Ion George Dinu
- "Marian Cristian Mih\u0103escu"
- Traian Rebedea
topics:
- llm-agents
- code-intelligence
- automated-refactoring
- software-architecture
- code-smells
- benchmark
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair

## Summary
SmellBench tests whether LLM coding agents can repair architectural code smells in a real Python codebase. The paper finds that agents can fix some true smells and identify many false positives, but aggressive repairs often make the codebase worse.

## Problem
- Architectural code smells affect maintainability across modules, so fixing them needs design-level reasoning instead of a local bug patch.
- Static detectors produce many false positives; in this benchmark, expert review found 41 of 65 detected hard smells were false positives, or 63.1%.
- Existing LLM repair benchmarks usually use failing tests as an oracle, while architectural smells need judgment about dependencies, APIs, and design intent.

## Approach
- The authors build SmellBench around 65 hard-severity PyExamine detections in scikit-learn v1.7.2, covering Scattered Functionality, Redundant Abstractions, Unstable Dependency, Improper API Usage, and God Object smells.
- Experts label each smell as False Positive, True Positive, or Partially Valid, then review agent changes across 715 agent-task outcomes.
- Each agent receives a task packet with the smell report, affected files, affected modules, a smell-specific playbook, and few-shot examples.
- Agents work through an MCP-based task loop: claim a task, inspect and edit code, run compilation and import checks, then report Done, Accepted, Need More Work, or Blocked.
- GEPA optimizes the smell-specific playbooks using easy and medium examples, while the hard-tier evaluation tasks stay unseen during prompt optimization.

## Results
- The benchmark contains 65 hard smells: 20 Scattered Functionality, 25 Redundant Abstractions, 14 Unstable Dependency, 4 Improper API Usage, and 2 God Object cases.
- Expert labels are 41 False Positive cases, 11 True Positive cases, and 13 Partially Valid cases; the overall false-positive rate is 63.1%.
- The best agent reaches a 47.7% resolution rate on the benchmark, based on re-running PyExamine after agent changes.
- Agents identify false positives with up to κ=0.94 agreement against expert judgment.
- Repair aggressiveness hurts net codebase quality: the most aggressive agent introduces 140 new smells.
- Expert-label reliability is reported as mean pairwise quadratic-weighted Cohen’s κ_w=0.67; when labels are collapsed into genuine versus not genuine, annotators agree on 81.5% of cases with Fleiss’ κ=0.45.

## Link
- [https://arxiv.org/abs/2605.07001v2](https://arxiv.org/abs/2605.07001v2)
