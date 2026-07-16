---
kind: trend
trend_doc_id: 259
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
topics:
- vision-language-action
- robot manipulation
- test-time compute
- error recovery
- real-time control
run_id: materialize-outputs
aliases:
- recoleta-trend-259
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/test-time-compute
- topic/error-recovery
- topic/real-time-control
language_code: en
pass_output_id: 126
pass_kind: trend_synthesis
---

# Robot VLA policies are adding execution-time judgment

## Overview
This period’s robotics papers concentrate on execution-time judgment for Vision-Language-Action (VLA) policies. VLA-ATTC spends extra inference under action uncertainty. Sentinel-VLA monitors task state and triggers planning or recovery when execution goes wrong. Both papers tie added reasoning to latency budgets on simulated and real-robot manipulation tasks.

## Findings

### Adaptive test-time action selection
VLA-ATTC adds a decision gate to VLA robot policies. It samples two action chunks, measures their Dynamic Time Warping distance, and treats high distance as action uncertainty. Low-uncertainty steps execute directly. High-uncertainty steps sample candidate action chunks after a shared vision-language prefill, then a Relative Action Critic picks the preferred action through pairwise comparisons.

The reported gains are largest where one bad action can spoil a long task. On LIBERO-LONG, PI0 improves from 82.8% to 90.6% average success with the adaptive setting. PI0.5 improves from 90.6% to 94.0%, and the full deliberation setting cuts PI0.5 failure rate by 51.1%. On real Agilex Piper tasks, PI0 rises from 46.0% to 58.7% with adaptive VLA-ATTC. The paper also reports 20.8 Hz control, which matters because candidate search can break robot timing if applied too broadly.

#### Sources
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): Summary chunk gives the uncertainty gate, Relative Action Critic, LIBERO-LONG results, real-robot results, and 20.8 Hz control figure.

### Status monitoring for recovery during manipulation
Sentinel-VLA adds a Status Monitor expert to a PI0-based policy. A learned monitor query reads the vision-language model cache and predicts whether the robot is at the initial step, running normally, entering a new subtask, or in error. The policy keeps a memory of the plan, current subtask, and error reflections. It updates that memory when status changes, then conditions the action expert on the image, instruction, status, and memory.

The evidence points to recovery as a measurable control feature. Sentinel-VLA reaches 54.7% average success on disturbed RLBench tasks, compared with 46.0% for PI0 and 48.4% for OneTwoVLA. On unseen RLBench tasks it reports 51.3%, ahead of PI0 at 42.0%. On real Agilex Piper tasks it reaches 60.0% average success across Stack cube, Pour water, and Sweep rubbish. The latency claim is also concrete: 13 ms per action on an RTX4090, with error detection at 97.4% on RLBench and 90.6% on a real-world error set.

#### Sources
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): Summary chunk covers the monitor states, thought memory, training data, benchmark results, latency, and error-detection rates.
