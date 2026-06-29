---
kind: ideas
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
run_id: 006dd63e-d43e-4c5c-97bc-f01a25413d82
status: succeeded
topics:
- robotics
- vision-language-action
- world-models
- benchmarks
- simulation
- quantization
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/benchmarks
- topic/simulation
- topic/quantization
language_code: en
pass_output_id: 69
pass_kind: trend_ideas
upstream_pass_output_id: 68
upstream_pass_kind: trend_synthesis
---

# Language-guided manipulation control

## Summary
The clearest near-term changes are tighter VLA baselines, direct tests for semantic control, and an affordance layer for manipulation data generation. The supporting evidence is strongest for a simple VLM-plus-MLP baseline, language-scored planning on held-out instruction variants, and affordance-conditioned grasp generation on tasks where object part selection determines success.

## Controlled VLA baseline with a pretrained VLM and MLP action head
A practical baseline for many VLA teams is now a pretrained VLM with a small continuous MLP action head, evaluated under one fixed recipe across tasks. StarVLA-α reports 98.8 average on LIBERO, 88.2 on RoboTwin 2.0 clean*, and 53.8 on RoboCasa-GR1 with a minimal pipeline and no benchmark-specific tuning. In the same setup, the MLP head matches or beats heavier action heads: 53.8 on RoboCasa-GR1 versus 52.8 for a GR00T-style head and 48.9 for a diffusion-style head, and 76.0 on SimplerEnv Google VM versus 60.1 for FAST.

The workflow change is straightforward. Before adding robot pretraining, action tokenizers, diffusion heads, or extra interface features, teams can maintain a fixed baseline built from a strong pretrained VLM, raw RGB, language instruction, training-split action normalization, and a continuous MLP head. New components should enter only after they clear that baseline on the same backbone and data. The ablations support that discipline: extra robot pretraining helps one benchmark and hurts another, and common data-engineering additions shrink to small gains once task data is large.

A cheap check is to rerun one current internal model comparison with the backbone and dataset held constant, then compare only the action head and one added training trick. If the simple head stays within a few points or wins outright, the team can cut model complexity and keep evaluation cleaner.

### Evidence
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md): StarVLA-α reports the benchmark results and action-head ablations that support a simple VLM plus MLP baseline.

## Language-scored trajectory reranking for semantic generalization tests
Robotics teams working on instruction following can add a language-scored planning harness to test semantic generalization before training another end-to-end policy. Grounded World Model shows a concrete way to do this: predict future latent states for candidate action chunks, score each future against the text instruction in a shared vision-language embedding space, and execute the best-scoring chunk. On WISER, this reaches 0.87 test success with 0.92 train success, while the VLA baselines average 0.90 on train and 0.22 on test.

This matters for workflows where the robot has seen the motions before but fails when the wording or visual cue changes. WISER is built around that exact pressure. Named VLA baselines drop to 0.47 for InstructVLA, 0.40 for Wall-OSS, 0.26 for InternVLA-A1 and π0.5, and lower for others on the held-out test tasks. GWM-MPC also reaches 0.83 test success after transfer to xArm6, which suggests the scoring layer is useful across embodiments.

A buildable first step is a reranker over retrieved trajectories or policy proposals. Keep the current proposal generator, predict short-horizon outcomes, and rank them by cosine similarity to the instruction in a frozen multimodal embedding model. The first validation pass does not need full robot retraining. It needs a held-out instruction split with paraphrases, new referring expressions, and visual substitutions that preserve the required motion.

### Evidence
- [Grounded World Model for Semantically Generalizable Planning](../Inbox/2026-04-13--grounded-world-model-for-semantically-generalizable-planning.md): Grounded World Model provides the language-conditioned MPC setup and the train/test semantic generalization results on WISER.

## Affordance-conditioned grasp generation for pouring and hanging tasks
Affordance-heavy manipulation still needs a support layer between task text and trajectory generation. AffordSim shows the gap clearly. On 17 representative tasks, Pi 0.5 averages 61% success, but pouring and mug hanging remain much lower than easy grasping. Example tasks reach 93% on `pick_banana`, 43% on `pour_cup_into_bowl`, and 47% on `hang_mug_on_rack`. The generator-side ablation points to the missing piece: AnyGrasp averages 20% on trajectory generation, while VoxAfford reaches 61%, with large gains on affordance-sensitive tasks such as `pour_into_cup` at 63% versus 0%.

The concrete build is an affordance-conditioned grasp proposer for data generation and policy evaluation. Given a task phrase such as "graspable handle" or "pourable rim," predict 3D affordance regions on the object point cloud, sample grasps around those regions, and score them for both affordance contact and reachability. That is useful for teams training imitation policies in simulation, because physically valid grasps still produce task-wrong demonstrations on objects with handles, rims, hooks, and openings.

A cheap check is to pick five existing tasks that depend on object parts, regenerate demonstrations with affordance-conditioned grasps, and compare success against a generic grasp planner. The early readout should focus on pouring, hanging, and tool-use tasks, where part selection decides most of the outcome.

### Evidence
- [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](../Inbox/2026-04-13--affordsim-a-scalable-data-generator-and-benchmark-for-affordance-aware-robotic-manipulation.md): AffordSim reports the task breakdown and the affordance-aware trajectory generation ablation that motivate an affordance-conditioned grasp layer.
