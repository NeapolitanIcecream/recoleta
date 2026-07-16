---
kind: ideas
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
run_id: c9eca421-8667-4075-8f9f-f78f90cc9cfb
status: succeeded
topics:
- robotics
- vision-language-action models
- behavior cloning
- test-time scaling
- robot safety
- contact-rich manipulation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/behavior-cloning
- topic/test-time-scaling
- topic/robot-safety
- topic/contact-rich-manipulation
language_code: en
pass_output_id: 313
pass_kind: trend_ideas
upstream_pass_output_id: 312
upstream_pass_kind: trend_synthesis
---

# Robot Rollout Decision Checks

## Summary
Robot teams can now make deployment decisions with more than aggregate task success. The practical changes are specific: use commissioning rollouts to choose among frozen experts, wrap VLA execution with candidate scoring and physical-feasibility checks, and add unsafe-success metrics to rollout reviews.

## Pre-deployment smoke-test routing for frozen VLA experts
Robot teams that already run smoke tests before deployment can keep those rollouts as selection data for each task and perturbation. RouterVLA shows a simple probe-success rule selecting among frozen experts reached 0.6149 held-out success on LIBERO-Plus, compared with 0.4686 for the global best expert. The result is useful because learned scorers added little over the simple rule, while same-trial reuse inflated measured gains.

A practical version would store each candidate checkpoint’s probe outcomes, rollout length, duration, termination behavior, and missing-statistic flags, then choose a policy for the target condition with a trial-disjoint validation rule. The cheap check is to replay the lab’s existing commissioning logs through this rule and compare against the single-checkpoint choice on held-out rollouts.

### Sources
- [RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection](../Inbox/2026-06-25--routervla-turning-smoke-tests-into-supervision-for-heterogeneous-vla-selection.md): RouterVLA reports trial-disjoint smoke-test routing, the 0.6149 versus 0.4686 success comparison, learned-scorer results, and same-trial inflation.
- [RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection](../Inbox/2026-06-25--routervla-turning-smoke-tests-into-supervision-for-heterogeneous-vla-selection.md): The paper abstract states that recorded probes build profiles for frozen experts and separate trials score the selected expert.

## Runtime candidate scoring for VLA action execution
Latency-tolerant manipulation tasks can add an execution wrapper that samples several reasoning-action or action-segment candidates, scores them before execution, and checks whether the observed state matches the predicted state after execution. E-TTS gives one version with reasoning-action joint sampling, vision-language verifiers, a history buffer, and feedback when a batch is rejected. PhysReflect-VLA gives a physical version with forward and inverse models that score candidate transitions and a reflector that issues corrective guidance after state mismatch.

This is a concrete adoption path for teams with a trained VLA policy that fails through bad contact, geometry violations, or accumulated action error. A first test can run the wrapper only on slow object rearrangement or insertion subtasks, then compare success, rejection rate, added latency, and recovery after mismatch against the base policy.

### Sources
- [E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation](../Inbox/2026-06-25--e-tts-a-new-embodied-test-time-scaling-framework-for-robotic-manipulation.md): E-TTS describes reasoning-action candidate sampling, verifier scoring, history-aware feedback, and average reported simulated gains.
- [PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies](../Inbox/2026-06-25--physreflect-vla-physical-feasibility-and-self-reflective-regulation-for-reliable-vision-language-action-policies.md): PhysReflect-VLA describes physical-feasibility scoring, predicted-versus-observed state checks, corrective guidance, and real-robot success gains.

## Unsafe-success tracking in robot rollout reviews
Robot evaluation should separate a clean completion from a completion that includes collisions, unsafe proximity, bad sequencing, or constraint violations. ForesightSafety-VLA scores each rollout as safe success, unsafe success, safe failure, or unsafe failure, then adds cumulative safety cost, risk exposure time, and safety-adjusted success rate. Its reported baselines show why the split matters: OpenVLA-oft had the best listed safety-adjusted success rate at 0.35, while unsafe success still appeared at 0.06.

A deployment review can add this as a gate on top of task success. Annotators or automated monitors would tag hazards during the whole trajectory, then report unsafe success as its own line item. The first useful check is small: rescore recent successful rollouts for contact, clearance, hot-zone, spill, and temporal-precondition violations, then see how many “successful” runs would fail a safety-adjusted review.

### Sources
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA defines the four rollout outcomes, 13 safety categories, process metrics, scenario design, and unsafe-success baseline results.
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): The abstract states that safety is the primary evaluation target and that controlled variations diagnose failure sources.
