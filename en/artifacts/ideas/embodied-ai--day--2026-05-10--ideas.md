---
kind: ideas
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: f40d46be-2529-4f2c-99da-f007c65c42b3
status: succeeded
topics:
- robotics
- VLA
- failure recovery
- long-horizon planning
- world models
- sim-to-real
- embodied datasets
tags:
- recoleta/ideas
- topic/robotics
- topic/vla
- topic/failure-recovery
- topic/long-horizon-planning
- topic/world-models
- topic/sim-to-real
- topic/embodied-datasets
language_code: en
pass_output_id: 143
pass_kind: trend_ideas
upstream_pass_output_id: 142
upstream_pass_kind: trend_synthesis
---

# Robot Policy Reliability

## Summary
Robotics teams can test reliability work with concrete artifacts: recovery-labeled rollouts for contact drift, entropy-gated search for long-horizon VLA inference, store video converted into robot action streams for retail adaptation, and action-conditioned world models for deformable objects.

## Recovery-labeled rollout buffers for contact-rich VLA tasks
VLA teams working on bimanual or contact-heavy manipulation should add failure and recovery episodes to the training buffer with separate labels, then evaluate policies with injected grasp errors. RePO-VLA gives a clear template: slice recovery segments out of full episodes, reset observation history for those segments, keep useful prefixes from failed rollouts with reliability decay, and assign low value to terminal drift. The deployment path is also practical because the reported policy uses a fixed high value condition, without an online failure detector or a hand-coded retry rule.

The first cheap test is a small adversarial suite around the failure modes that already break the robot: premature close, grasp slip, grasp position offset, and grasp orientation mismatch. RePO-VLA reports average adversarial success rising from 20% to 75%, and its FRBench-Sim data includes 23,453 bimanual episodes across 46 tasks, including 6,392 verified failure-recovery episodes. That scale is larger than most labs will copy at first, but the workflow is clear enough to pilot on a few high-value tasks before expanding collection.

### Sources
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): Documents RePO-VLA's success, failure, and recovery labeling workflow, FRBench-Sim scale, injected error types, and reported adversarial success gain.
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): Confirms deployment with a fixed high value condition and no online failure detector or heuristic retry rule.

## Entropy-triggered action-chunk search for long-horizon VLA inference
Robot deployment teams can add an inference-time gate that spends extra compute only when the VLA policy becomes uncertain. CAPS keeps the base policy unchanged, computes contextual SNR from action entropy, and runs Metropolis-Hastings search over future action chunks when entropy crosses a threshold. When uncertainty stays low, it uses greedy execution.

This is a fit for long-horizon tasks where a single locally plausible action can lose the instruction goal. The validation path is direct: log entropy during rollouts, replay high-entropy windows with action-chunk search, and compare task success and latency against the base policy. CAPS reports 47.4% average success on RoboTwin 1.0 with π0, compared with 32.2% for π0 and 41.3% for π0 plus TACO. On Simpler-WindowX, it reports 60.5% average success, ahead of π0 at 48.0% and π0 plus TACO at 55.5%.

### Sources
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): Summarizes CAPS's entropy/SNR trigger, Metropolis-Hastings action-chunk search, and reported success rates on RoboTwin and Simpler-WindowX.
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): Confirms CAPS as a training-free inference-time method for long-horizon VLA instruction drift.

## Retail video capture pipelines that produce robot action streams
Retail robotics groups can start with in-store human activity capture before expensive robot teleoperation. SABER shows a concrete data workflow: record natural grocery-store work with egocentric and fixed 360° cameras, estimate hand and body motion, manually correct pose estimates, and retarget the result into robot-compatible action targets. The resulting streams cover latent-action sequences, dexterous hand-pose trajectories, and whole-body motion for a humanoid.

This directly addresses the adoption blocker in store robots: general VLA training data often misses shelf picking, fridge opening, basket loading, floor retrieval, occlusion, lighting, and varied packaging. SABER reports 44.8K training samples from about 100 hours of real store capture and post-trains GR00T N1.6 to 29.3% mean success across 10 RoboBenchMart tasks, compared with 13.4% for simulation-only fine-tuning. A practical pilot would capture one aisle, convert a small set of worker actions into the same three supervision streams, and test whether task success improves on the store-specific actions that fail most often.

### Sources
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): Documents SABER's store-capture workflow, dataset composition, GR00T N1.6 post-training setup, and reported RoboBenchMart improvement.
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): Confirms the data gap for retail robotics and the use of real in-store capture without teleoperation overhead.
