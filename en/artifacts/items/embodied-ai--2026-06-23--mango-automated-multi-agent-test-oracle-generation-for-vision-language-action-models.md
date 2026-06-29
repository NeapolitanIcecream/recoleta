---
source: arxiv
url: https://arxiv.org/abs/2606.24815v1
published_at: '2026-06-23T17:00:06'
authors:
- Pablo Valle
- Shaukat Ali
- Aitor Arrieta
- Lionel Briand
topics:
- vision-language-action
- robot-evaluation
- test-oracles
- failure-localization
- multi-agent-generation
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models

## Summary
MANGO automatically generates fine-grained test oracles for VLA robot tasks from natural-language instructions. It improves evaluation and debugging by checking ordered atomic steps such as open, pick, place, and close, rather than only the final simulator state.

## Problem
- VLA robot benchmarks often use hand-written symbolic oracles that check only the final state, such as whether an object is inside a container at the end of execution.
- These oracles require domain effort, depend on benchmark-specific formats such as Python or .bddl files, and give weak debugging signal for long-horizon manipulation tasks.
- A robot may fail by missing an intermediate step, dropping an object, or doing steps in the wrong order; a final-state oracle usually reports only task failure.

## Approach
- MANGO builds a reusable atomic task library from complex natural-language tasks, with parameterized actions such as `Open(fridge)`, `Pick(bottle)`, `Place(bottle, fridge)`, and `Close(fridge)`.
- It maps each atomic task to simulator checks using available simulator functions, such as open state, holding state, contact, and spatial relations.
- For each full instruction, it decomposes the instruction into an ordered or partially ordered sequence of atomic tasks and attaches the matching oracle to each step.
- Three agent roles run iterative checks: the Generator creates candidate task libraries and oracles, Assessor agents check logic, object grounding, function use, and execution reliability, and the Judge accepts the candidate or sends correction instructions.
- Each generation loop can stop when accepted or after 10 iterations.

## Results
- The paper evaluates MANGO on 2 benchmarks: LIBERO_10 and RoboCasa Humanoid Tabletop.
- The authors claim MANGO generates executable fine-grained oracles that detect a similar number of failures as hand-written symbolic oracles.
- The generated oracles also localize failures by identifying the failed atomic step and order violations in the task sequence.
- The paper reports ablation studies on component contributions and on reducing the initial task set while keeping oracle quality, but this excerpt gives no quantitative ablation values.
- The provided excerpt does not include exact success rates, failure counts, precision, recall, runtime, or baseline numbers beyond the 2 named benchmarks and the 10-iteration cap.

## Link
- [https://arxiv.org/abs/2606.24815v1](https://arxiv.org/abs/2606.24815v1)
