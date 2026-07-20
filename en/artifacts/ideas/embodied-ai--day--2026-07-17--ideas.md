---
kind: ideas
granularity: day
period_start: '2026-07-17T00:00:00'
period_end: '2026-07-18T00:00:00'
run_id: a51a0ca0-07f5-4628-b5a8-ba7fcc6d6fc1
status: succeeded
topics:
- embodied AI
- robot control
- VLA models
- physical reasoning
- deployment efficiency
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robot-control
- topic/vla-models
- topic/physical-reasoning
- topic/deployment-efficiency
language_code: en
pass_output_id: 363
pass_kind: trend_ideas
upstream_pass_output_id: 362
upstream_pass_kind: trend_synthesis
---

# Closed-loop VLA training and evaluation changes

## Summary
Phase labels can govern both sensor access during manipulation and compute reuse during policy evaluation. The evidence supports narrower changes to training and test infrastructure rather than claims of general physical reliability, which remains limited by simulation-heavy evaluation and weak long-horizon safety results.

## Constraint-aware wrist-camera masking for compositional manipulation
VLA training teams should replace gripper-state-only wrist-camera masking with a gate that also considers the current sub-task and its physical constraints. AC-VLA’s closed-gripper masking discourages visual shortcuts and contributes to large LIBERO-OOD gains, but IMBench shows that alignment, tool use, hidden state, timing, and balancing remain execution bottlenecks even when models identify constraints. Those operations may require close-range or force-sensitive observations after the gripper closes, so one masking rule can trade trajectory memorization for sensor deprivation.

The concrete change is to attach constraint labels to AC-VLA’s automatically segmented sub-tasks: suppress the wrist view during transport when third-person geometry is sufficient, but preserve it for contact, alignment, tool, hidden-state, and stability phases. A useful first check is an inference-time occlusion ablation by phase on held-out LIBERO-OOD and IMBench episodes; if wrist removal disproportionately damages those constraint classes, the training gate should be conditioned on constraint type rather than gripper state alone.

### Sources
- [AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning](../Inbox/2026-07-17--ac-vla-robust-out-of-distribution-action-execution-via-compositional-learning.md): AC-VLA masks wrist-camera inputs during closed-gripper phases; with π₀.₅ it reports 64.2% Spatial-OOD and 73.3% Goal-OOD success, gains of 28.7 and 26.7 percentage points.
- [IMBench: A Benchmark for Intuitive Robotic Manipulation](../Inbox/2026-07-17--imbench-a-benchmark-for-intuitive-robotic-manipulation.md): IMBench reports only 11.3% vision-only and 18.8% privileged-state closed-loop success for GPT-5.5, with alignment, timing, tool-use, hidden-state, and balancing tasks at 0%.

## Forked closed-loop evaluation with shared slow-backbone prefixes
Teams comparing many action experts or tenant-specific VLA policies can reduce duplicated evaluation compute by forking simulator states from a common observation history. Compute the slow backbone and its cache once for the shared prefix, attach each isolated action expert to that cache, and branch the environments only when their actions diverge. JoyNexus already isolates tenant-specific modules and groups compatible workloads around a resident backbone; the fast-slow driving system shows that an action expert can consume a persistent backbone cache plus the current frame at control rate.

The evaluator must preserve closed-loop branching rather than score every expert on one fixed log: the driving study’s route completion rose from 82.1% at 10 Hz to 94.0% at 20 Hz with the same expert, showing that control cadence changes outcomes. The cheapest implementation check is to fork identical simulator snapshots, compare shared-prefix and independently computed caches for numerical and trajectory equivalence, then measure GPU time saved before branches diverge. JoyNexus does not report numerical efficiency gains, so that measurement is necessary before adopting the design.

### Sources
- [JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models](../Inbox/2026-07-17--joynexus-service-oriented-multi-tenant-post-training-for-vla-models.md): JoyNexus keeps a shared backbone resident, isolates tenant-specific action modules and policy state, and groups compatible samples for shared-backbone computation, but reports no numerical efficiency values.
- [Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving](../Inbox/2026-07-17--think-at-5-hz-act-at-20-hz-asynchronous-fast-slow-vision-language-action-inference-for-closed-loop-driving.md): A 337M action expert reads a persistent cache from a frozen 7B backbone and the current frame; increasing fresh control from 10 Hz to 20 Hz raised CARLA route completion from 82.1% to 94.0%.
