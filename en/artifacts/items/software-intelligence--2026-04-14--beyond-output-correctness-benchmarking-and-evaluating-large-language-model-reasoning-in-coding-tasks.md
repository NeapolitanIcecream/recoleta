---
source: arxiv
url: http://arxiv.org/abs/2604.12379v1
published_at: '2026-04-14T07:12:46'
authors:
- Yuangang Li
- Justin Tian Jin Chen
- Ethan Yu
- David Hong
- Iftekhar Ahmed
topics:
- code-reasoning-evaluation
- benchmarking
- llm-judge
- code-intelligence
- reasoning-quality
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks

## Summary
This paper argues that checking only final code outputs misses whether an LLM reasoned correctly. It introduces CodeRQ-Bench, a benchmark for reasoning quality in coding tasks, and VERA, an evaluator that checks reasoning against evidence and adjusts for task ambiguity.

## Problem
- Current coding benchmarks such as HumanEval and SWE-bench score final outputs, so a model can get the right answer with flawed reasoning or fail with reasoning that is partly sound.
- Existing reasoning evaluators such as ReCEval, SocREval, and CaSE were built for general NLP tasks, not coding tasks with program semantics, repository context, APIs, and execution behavior.
- There was no benchmark covering reasoning quality across the main coding task types: generation, summarization, and classification.

## Approach
- The paper builds **CodeRQ-Bench**, a reasoning-quality benchmark with 4 datasets and 732 total instances: CoderEval-RE (230), SWEbench-RE (111), ClassEval-RE (139), and DebugBench-RE (252).
- Two new parts of the benchmark are added for broader task coverage: ClassEval-RE for code summarization and DebugBench-RE for bug detection / classification. Each instance gets a consensus label from 3 expert annotators.
- Annotation quality is strong on the new datasets: Fleiss' kappa is 0.91 for ClassEval-RE and 0.95 for DebugBench-RE, with adjudication rates of 4.32% and 3.57%.
- The authors analyze 1,069 evaluator mismatch cases and identify 5 recurring failure modes, including lack of evidence grounding, poor ambiguity handling, bad score aggregation, self-generated reference bias, and weak code awareness.
- They propose **VERA**, a 2-stage evaluator: first, an LLM judge scores reasoning with search-based evidence checking; second, another judge estimates task ambiguity and penalizes reasoning that handles ambiguity poorly. The final score is `max(p + δ, 0)`.

## Results
- On **CoderEval-RE**, VERA reaches **AUCROC 0.6905** and **AUPRC 0.4615**, beating the best listed baselines at **0.5700 AUCROC** and **0.3516 AUPRC**.
- On **SWEbench-RE**, VERA reaches **AUCROC 0.6399** and **AUPRC 0.3058**, above the best listed baselines at **0.5778 AUCROC** and **0.2165 AUPRC**.
- On **ClassEval-RE**, VERA reaches **AUCROC 0.7090** and **AUPRC 0.8869**, above the best listed baselines at **0.6250 AUCROC** and **0.8502 AUPRC**.
- On **DebugBench-RE**, VERA reaches **AUCROC 0.7176** and **AUPRC 0.7939**, above the best listed baselines at **0.6769 AUCROC** and **0.7431 AUPRC**.
- The abstract states the largest gains over prior methods are **up to +0.26 AUCROC** and **+0.21 AUPRC** across the four datasets.
- Existing evaluators often perform near random on coding reasoning. In the mismatch analysis, the authors collect **1,069** errors, including **709 missed errors** and **360 false alarms**, which they use to motivate VERA's design.

## Link
- [http://arxiv.org/abs/2604.12379v1](http://arxiv.org/abs/2604.12379v1)
