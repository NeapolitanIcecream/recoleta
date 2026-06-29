---
kind: ideas
granularity: day
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-19T00:00:00'
run_id: bfdb3bae-77e6-44b1-88f2-6274001cf2f7
status: succeeded
topics:
- embodied AI
- robot manipulation
- VLA models
- dexterous robotics
- world models
- robot benchmarks
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robot-manipulation
- topic/vla-models
- topic/dexterous-robotics
- topic/world-models
- topic/robot-benchmarks
language_code: en
pass_output_id: 185
pass_kind: trend_ideas
upstream_pass_output_id: 184
upstream_pass_kind: trend_synthesis
---

# Physical Rollout Evaluation for Robot Policies

## Summary
Real-robot rollout metrics are becoming the useful filter for VLA and world-model work. The clearest moves are to add quality scoring to teleoperated dexterous data, test VLA policies under camera corruption before deployment, and score tabletop policies on scene preservation and contact utility alongside task completion.

## Clip-quality scoring for noisy dexterous teleoperation datasets
Robot labs collecting bimanual dexterous demonstrations should add a clip-level quality score before training policies. Dexora shows a concrete version: two 6-DoF arms, two 12-DoF hands, four RGB views, joint states at 20 Hz, a matched MuJoCo twin, and a diffusion policy whose loss is weighted by an offline discriminator that down-weights poor demonstrations.

The pain is operational. High-DoF teleoperation data includes operator variation, tracking errors, occlusion, and latency. Throwing all episodes into training treats unstable clips as useful supervision. A small discriminator or evaluator that scores completion, contact stability, object pose drift, and hand-tracking confidence can turn an ordinary data lake into a trainable corpus.

A cheap first test is to rescore an existing teleoperation set, train the same policy with and without quality weights, and compare physical rollouts on tasks that need finger articulation, such as cap twisting, pen use, book retrieval, or dough handling. Dexora’s reported gap on dexterous tasks, 66.7% average success versus 51.7% for GR00T N1 and 6.7% for Diffusion Policy, gives this workflow enough signal to try on smaller local rigs.

### Evidence
- [Dexora: Open-source VLA for High-DoF Bimanual Dexterity](../Inbox/2026-05-18--dexora-open-source-vla-for-high-dof-bimanual-dexterity.md): Dexora combines a 36-DoF dual-arm dual-hand robot, matched MuJoCo twin, 100K simulated trajectories, 10K real teleoperated episodes, and quality-weighted diffusion policy training.
- [Dexora: Open-source VLA for High-DoF Bimanual Dexterity](../Inbox/2026-05-18--dexora-open-source-vla-for-high-dof-bimanual-dexterity.md): The paper abstract describes the hybrid teleoperation interface, synthetic and real datasets, and the offline discriminator for down-weighting low-quality demonstrations.

## Camera-corruption regression tests for VLA robot policies
VLA deployment teams should add a camera-corruption regression suite before physical trials. StableVLA documents the failure mode clearly: policies that work under clean camera inputs can break under blur, noise, weather-like effects, and digital artifacts that were absent during training.

The practical build is small. Take the team’s normal validation clips or simulation rollouts, apply fixed severity levels for common visual corruptions, and report success by task family. For policies using a VLA-Adapter-style bridge between the vision encoder and the language-policy stack, test a replacement visual projector based on StableVLA’s Information Bottleneck Adapter. Its design filters noisy feature channels while preserving spatial detail through a parallel path, with fewer than 10M added parameters and no extra robot data.

The acceptance test should include the policy’s normal clean score, its worst corruption cases, and at least one real robot trial with induced camera degradation. StableVLA reports LIBERO severity-5 gains such as Object at 70.2% versus 29.3% and Long at 45.3% versus 26.2%, plus a real Pack Doll result of 50% success versus 20% for VLA-Adapter-0.5B.

### Evidence
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): StableVLA identifies visual corruptions as a deployment failure mode and reports large LIBERO, CALVIN, and real-robot gains without extra robot data or corruption-specific augmentation.
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): The abstract states that IB-Adapter filters noisy visual inputs, adds fewer than 10M parameters, and improves over the baseline without extra data or augmentation.

## Scene-preserving and contact-utility scoring for tabletop dexterity
Teams evaluating dexterous tabletop robots should score whether the table remains usable after each action. DexHoldem gives a direct template: physical rollouts use a four-level rubric that separates scene-preserving success, disruptive completion, task failure, and disruptive failure. The distinction matters because a hand can complete a card or chip action while leaving the next decision state damaged.

This is easy to add to compact tabletop domains. Define legal end states, object displacement limits, chip or part inventory checks, and recovery triggers. Record task completion and scene preservation separately. For systems with tactile sensors or learned dynamics, add a contact-utility check that compares tactile reconstruction with downstream action success.

WorldArena 2.0 shows why this extra score is needed for contact-rich models. Wan2.2 has the best tactile prediction quality on UniVTAC, with 21.26 PSNR and 0.746 SSIM, yet averages 50% task success across Insert HDMI and Lift Bottle. A useful evaluation harness should pair tactile or video quality with physical rollout success, because clean reconstruction can still fail as control evidence.

### Evidence
- [DexHoldem: Playing Texas Hold'em with Dexterous Embodied System](../Inbox/2026-05-18--dexholdem-playing-texas-hold-em-with-dexterous-embodied-system.md): DexHoldem uses a physical rollout rubric that separates scene-preserving success from disruptive completion and reports large gaps between task completion and scene-preserving success.
- [WorldArena 2.0: Extending Embodied World Model Benchmarking on Modality, Functionality and Platform](../Inbox/2026-05-18--worldarena-2-0-extending-embodied-world-model-benchmarking-on-modality-functionality-and-platform.md): WorldArena 2.0 adds visuotactile evaluation and shows that high tactile reconstruction scores do not reliably predict task success.
