---
kind: trend
trend_doc_id: 120
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
topics:
- robotics
- vision-language-action
- world-models
- benchmarks
- simulation
- quantization
run_id: materialize-outputs
aliases:
- recoleta-trend-120
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/benchmarks
- topic/simulation
- topic/quantization
language_code: en
pass_output_id: 68
pass_kind: trend_synthesis
---

# Robotics papers reward cleaner baselines and sharper tests of semantic control

## Overview
April 13’s robotics set is strongest when it strips evaluation down to concrete control questions. The best-supported papers ask whether a simple VLA recipe already saturates many benchmarks, whether visual features actually carry action information, and whether world models can score futures in a semantically meaningful way. StarVLA-α, LARYBench, and GWM-MPC give the clearest evidence.

## Clusters

### Simple VLA baselines hold up under controlled evaluation
StarVLA-α makes the clearest period-level claim: a plain vision-language model (VLM) plus a small MLP action head can match or beat heavier vision-language-action systems when the recipe is controlled. Its specialist model reports 98.8 average on LIBERO, 88.2 on RoboTwin 2.0 clean*, and 53.8 on RoboCasa-GR1, with the simple MLP head matching or beating more complex heads in the same setup. The ablations are as important as the headline numbers. Extra robot pretraining helps some benchmarks and hurts others, and common pipeline additions give only small gains once task data is large. This day’s strongest concrete result is not a new stack. It is a cleaner accounting of what actually changes outcomes.

#### Evidence
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md): Summary and benchmark results for the simple VLM-to-action baseline and its ablations.

### Evaluation focuses on action semantics and affordances
Benchmarks are getting sharper about what a representation must do before it is called useful for control. LARYBench tests both semantic action decoding and low-level trajectory regression, and the result is blunt: general visual encoders are already stronger than many specialized latent action models. V-JEPA 2 reaches 76.62% average action classification, while DINOv3 posts the best control regression at 0.19 average MSE. AffordSim pushes on a different failure mode. It shows that imitation policies still break on tasks that depend on acting on the right object part. Across 17 representative tasks, Pi 0.5 averages 61%, but pouring and mug hanging remain far below easy grasping, and affordance-aware trajectory generation beats generic grasping by large margins on those tasks.

#### Evidence
- [LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment](../Inbox/2026-04-13--lary-a-latent-action-representation-yielding-benchmark-for-generalizable-vision-to-action-alignment.md): Benchmark evidence that general visual encoders outperform latent action models on semantics and control regression.
- [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](../Inbox/2026-04-13--affordsim-a-scalable-data-generator-and-benchmark-for-affordance-aware-robotic-manipulation.md): Benchmark evidence that affordance-heavy manipulation remains difficult and benefits from affordance-aware data generation.

### World models are judged by semantic scoring and deployment cost
World models in this period try to make planning and action decoding more semantically grounded. AIM inserts a spatial value map between future prediction and action generation, then reports 94.0% average success on RoboTwin 2.0 Easy and 92.1% on Hard. Grounded World Model uses a shared language-image latent space for model-predictive control, so candidate futures are scored against text instructions instead of a goal image. On WISER, that gives 0.87 test success versus a 0.22 average for VLA baselines, while keeping train success at 0.92. DexWorldModel points to the same concern at deployment time: predict semantic features, keep memory fixed with horizon, and hide some inference behind robot execution. The latency claim is concrete, about 50%, but the task-performance evidence in the available excerpt is still thin.

#### Evidence
- [AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps](../Inbox/2026-04-13--aim-intent-aware-unified-world-action-modeling-with-spatial-value-maps.md): AIM results on spatial intent modeling and RoboTwin success rates.
- [Grounded World Model for Semantically Generalizable Planning](../Inbox/2026-04-13--grounded-world-model-for-semantically-generalizable-planning.md): Grounded World Model results on language-conditioned planning and WISER generalization.
- [DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks](../Inbox/2026-04-13--dexworldmodel-causal-latent-world-modeling-towards-automated-learning-of-embodied-tasks.md): DexWorldModel claims on semantic latents, O(1) memory, and latency reduction, with limited quantitative task evidence in the excerpt.

### On-device efficiency is framed as drift control
Efficiency work is getting closer to robot-specific failure analysis. DA-PTQ treats quantization error as a control problem, with the key risk defined as trajectory drift over time rather than static layer reconstruction error. The method adds interface compensation and drift-aware mixed precision, aiming to keep low-bit VLA behavior close to full precision without extra runtime cost after calibration. The idea fits the day’s broader emphasis on execution fidelity, but the available excerpt does not include benchmark tables, so this remains a plausible systems contribution with limited visible verification in the local corpus.

#### Evidence
- [DA-PTQ: Drift-Aware Post-Training Quantization for Efficient Vision-Language-Action Models](../Inbox/2026-04-13--da-ptq-drift-aware-post-training-quantization-for-efficient-vision-language-action-models.md): Summary of drift-aware quantization and the lack of quantitative benchmark tables in the excerpt.
