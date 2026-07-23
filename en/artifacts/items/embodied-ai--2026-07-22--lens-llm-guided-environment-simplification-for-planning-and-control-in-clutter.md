---
source: arxiv
url: https://arxiv.org/abs/2607.19633v1
published_at: '2026-07-22T00:05:00'
authors:
- Aileen Liao
- Rachel Holladay
- Dinesh Jayaraman
- Michael Posa
topics:
- robot-manipulation
- scene-abstraction
- llm-guided-planning
- vision-language-action
- cluttered-environments
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# LENS: LLM-guided Environment Simplification for Planning and Control in Clutter

## Summary
LENS uses an LLM-guided, closed-loop abstraction layer to remove or combine task-irrelevant objects before planning or control in cluttered manipulation scenes. The paper reports improved success and scalability for TAMP, contact-implicit model-based control, and the π0.5 vision-language-action model, although the provided excerpt omits some hardware and VLA result details.

## Problem
- Clutter increases the number of objects, contacts, collision constraints, decision branches, and visual distractors, making classical planners and learned robot policies slower and less reliable.
- Existing scene abstractions often require task-specific manual heuristics, which are costly to create and difficult to adapt across tasks and layouts.
- This matters for deployment because downstream systems inherit the full complexity of unstructured real-world scenes even when most objects are irrelevant to the task.

## Approach
- Given a task description and scene representation, GPT-4o identifies relevant objects and groups objects that can be treated as one entity.
- LENS prunes irrelevant objects and merges functionally or dynamically coupled objects into composite bodies while preserving a conservative physical representation.
- The reduced scene is passed unchanged into a TAMP system, the C3+ contact-implicit controller, or the π0.5 VLA model; for the VLA, pruning produces an inpainted image with distractors removed.
- If execution times out or fails, LENS re-queries the VLM with failure feedback and revises the abstraction, with up to two feedback iterations in the reported TAMP experiments.

## Results
- The VLM query took an average of 1.76 seconds and was reported as negligible relative to execution time; the paper excludes it from runtime comparisons.
- In model-based control, LENS-C3+ succeeded in 39 of 45 trials, compared with 17 of 30 for the full-scene baseline.
- With 6 objects, the baseline C3+ controller exceeded LENS runtime by roughly an order of magnitude, at approximately 1,000 seconds; with 7 objects, the baseline exceeded 4,000 seconds, while LENS remained in the approximately 40–135 second range.
- TAMP was evaluated over 50 episodes in light-clutter, heavy-clutter, and clutter-with-stack environments. LENS had limited benefit in light clutter but outperformed the baseline in heavier clutter, where the baseline often timed out; exact success-rate values are not available in the provided text because the figure data are not reproduced.
- The paper states that LENS improved the π0.5 VLA in both simulation and hardware, but the excerpt does not include the corresponding table values or hardware success rates.
- The reported results support improved scalability and robustness in the tested tabletop tasks, but they do not establish performance across broader robot embodiments, environments, or tasks beyond those experiments.

## Link
- [https://arxiv.org/abs/2607.19633v1](https://arxiv.org/abs/2607.19633v1)
