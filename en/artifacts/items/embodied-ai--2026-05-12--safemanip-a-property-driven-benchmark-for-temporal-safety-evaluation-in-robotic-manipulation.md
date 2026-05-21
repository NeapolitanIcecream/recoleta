---
source: arxiv
url: https://arxiv.org/abs/2605.12386v1
published_at: '2026-05-12T16:49:28'
authors:
- Chengyue Huang
- Khang Vo Huynh
- Sebastian Elbaum
- Zsolt Kira
- Lu Feng
topics:
- robot-safety
- vision-language-action
- robot-manipulation
- temporal-logic
- benchmarking
- robocasa
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation

## Summary
SafeManip is a benchmark for checking temporal safety in robotic manipulation rollouts, using LTL_f monitors instead of only task success. It shows that current VLA policies can finish tasks while still violating safety rules during execution.

## Problem
- Standard manipulation benchmarks score task completion, so they can miss unsafe execution that happens before the final state.
- Many failures depend on event order: contamination before clean contact, release before an object is inside a fixture, or failure to recover after hitting a mechanism.
- This matters for household and kitchen robots because a successful final state can still include unsafe contact, spills, unstable placement, or hygiene violations.

## Approach
- SafeManip defines reusable temporal safety templates in Linear Temporal Logic over finite traces, written over predicates such as `Collision`, `StableGrasp`, `Sanitized`, `Contained`, and `FixOpen`.
- It maps each rollout to a symbolic predicate trace using simulator state, object poses, contacts, gripper state, fixture state, and task action signals.
- Each task binds the generic templates to concrete objects, fixtures, regions, and skills, then checks the rollout with LTL_f monitors compiled to finite automata.
- The property suite covers 8 safety categories with 10 templates: collision/contact, grasp stability, release stability, cross-contamination, action onset, mechanism recovery, containment, and enclosure/access.
- The benchmark reports task success separately from safety violation rate, success-and-safe, success-but-unsafe, fail-but-safe, fail-and-unsafe, and unsafe-state exposure.

## Results
- The evaluation uses 50 RoboCasa365 tasks, 6 VLA policies or variants, and 50 rollouts per task.
- The tested policies include `pi_0`, `pi_0.5`, GR00T N1.5, and 3 GR00T N1.5 training variants.
- `pi_0.5` raises task success over `pi_0` from 8.1% to 9.3%, while safety violation rate also rises from 69.7% to 82.8%.
- The paper reports that GR00T-tpt has higher task success than the other GR00T variants, but still has a high violation rate; the excerpt does not give the exact GR00T numbers.
- Category results in the excerpt identify collision/contact and release stability as dominant failure sources; release stability also has high unsafe-state exposure because failed placements can remain unsettled for many timesteps.
- Low containment and enclosure/access violation rates are partly tied to monitor activation: containment is checked after detected transfer, and enclosure/access often triggers only during reach-in or internal-fixture access events.

## Link
- [https://arxiv.org/abs/2605.12386v1](https://arxiv.org/abs/2605.12386v1)
