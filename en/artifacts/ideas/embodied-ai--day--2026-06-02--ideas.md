---
kind: ideas
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
run_id: 5c00ed90-c13e-4aa3-8381-43abd0849e26
status: succeeded
topics:
- VLA
- robot manipulation
- geometry grounding
- world models
- test-time adaptation
- continual learning
- robot safety
tags:
- recoleta/ideas
- topic/vla
- topic/robot-manipulation
- topic/geometry-grounding
- topic/world-models
- topic/test-time-adaptation
- topic/continual-learning
- topic/robot-safety
language_code: en
pass_output_id: 251
pass_kind: trend_ideas
upstream_pass_output_id: 250
upstream_pass_kind: trend_synthesis
---

# Contact-Aware Robot Policy Control

## Summary
VLA teams can make three concrete changes to current robot policy work: add geometry-conditioned action decoding for fine manipulation, run a local latent-prompt adaptation pass before rollout, and store replay memory by manipulation phase during sequential skill training. Each change targets a failure mode that appears when a policy has to execute actions under contact, layout, or task-sequence pressure.

## Geometry-conditioned action decoding for transparent objects and insertion tasks
Robot policy teams working on fine manipulation should add a geometry path to the action decoder and test it on tasks where semantic object recognition is already good but control fails: transparent bottles, ring-shaped objects, tight insertions, stable release, and contact-heavy alignment.

GeoAlign gives a concrete implementation pattern. It post-trains a Depth Anything V2-Small branch on robot RGB-D data, discards the depth head at rollout, and uses RGB-derived geometry features. The robot state creates query slots that select local geometry from the feature grid, then compact geometry tokens condition the flow-matching action decoder. This keeps rollout inputs to RGB, language, and proprioception while still giving the action head local shape cues.

The cheap validation is a task slice with geometry-sensitive objects. GeoAlign reports 78.8% average success on eight real ALOHA tasks, compared with 65.0% for a matched RGB-only baseline, with transparent-bottle success rising from 35.0% to 75.0% and tape-roll insertion from 40.0% to 65.0%. GeoSem-WAM points in the same direction for world action models: future geometry and semantic supervision are used during training, dense heads are removed at deployment, and real Franka success rises from 88.9% for Fast-WAM to 95.4%.

### Sources
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): GeoAlign describes RGB-derived geometry features, state-guided spatial querying, and real ALOHA gains on transparent and insertion tasks.
- [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](../Inbox/2026-06-02--geosem-wam-geometry-and-semantic-aware-world-action-models.md): GeoSem-WAM reports training-time geometry and semantic supervision with deployment-time action prediction and real Franka gains.

## Latent prompt adaptation pass for a frozen VLA policy in a new workspace
A deployment workflow can add a short adaptation step before a frozen VLA policy is used in a new workspace. The robot collects interaction data in the target setting, keeps the policy backbone fixed, and updates only learned latent prompt tokens using a self-supervised state-grounding loss that predicts end-effector position and gripper state.

TTT-VLA is the concrete case to copy first. It adds a latent prompt to the policy conditioning input during training, then adapts that prompt at test time with data from the current environment. On SimplerEnv WidowX single-embodiment tasks, π0.5 improves from 51.1% mean success to 63.5% with state-grounded latent prompts and to 67.4% after test-time prompt optimization. The method also improves Google Robot visual matching from 67.5% to 72.4% after test-time training.

This is most useful for teams that already trust a base policy but see failures after camera, lighting, object layout, or embodiment changes. The reported compute is high, 15–30 minutes on 8 NVIDIA H100 GPUs for the listed experiments, so the practical first check is an offline replay or simulator trial that measures whether prompt-only updates correct a small number of repeated decision errors without changing the policy weights.

### Sources
- [TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models](../Inbox/2026-06-02--ttt-vla-test-time-latent-prompt-optimization-for-vision-language-action-models.md): TTT-VLA describes frozen-backbone latent prompt optimization with a self-supervised state-grounding loss and reports SimplerEnv gains.
- [TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models](../Inbox/2026-06-02--ttt-vla-test-time-latent-prompt-optimization-for-vision-language-action-models.md): The paper states that test-time optimization updates only the latent prompt using data from the current environment.

## Phase-aware replay buffers for sequential manipulation skill training
Teams fine-tuning VLA policies on a sequence of manipulation skills should store replay data by sub-skill phase, not only by trajectory or task. The operational pain is clear: brief contact phases such as grasping can be under-sampled when replay frames are drawn uniformly, even though those frames decide whether the full task succeeds.

PHASER splits trajectories into phases such as approach, grasp, and transport, gives each phase an equal frame budget, and routes replay toward old phases likely to conflict with the current phase. The routing uses language similarity, visual similarity, and action divergence, with scores computed once at each task transition. Auto-PC can propose phase boundaries using action-signal change-point detection plus VLM semantic verification, reducing the need for manual labels.

The first implementation can be a buffer change around an existing fine-tuning pipeline: segment demonstrations into phases, reserve equal memory per phase, and compare against uniform experience replay on a sequential LIBERO-style suite. PHASER reports 85.8% average success on LIBERO-Long with OpenVLA-OFT-7B, compared with 54.6% for standard experience replay. The same paper reports large gains across QwenGR00T-3B and QwenOFT-3B, which makes the buffer design worth testing before changing the policy architecture.

### Sources
- [PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models](../Inbox/2026-06-02--phaser-phase-aware-and-semantic-experience-replay-for-vision-language-action-models.md): PHASER describes phase-aware storage, replay routing, Auto-PC phase discovery, and gains over standard experience replay.
- [PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models](../Inbox/2026-06-02--phaser-phase-aware-and-semantic-experience-replay-for-vision-language-action-models.md): The paper explains why uniform replay under-samples short but critical manipulation phases.
