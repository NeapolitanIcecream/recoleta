---
kind: trend
trend_doc_id: 388
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- robot manipulation
- embodied AI
- safety evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-388
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/robot-manipulation
- topic/embodied-ai
- topic/safety-evaluation
language_code: en
pass_output_id: 162
pass_kind: trend_synthesis
---

# Robot VLA progress is being judged by execution under real control pressure

## Overview
This week’s strongest signal is execution quality for robot Vision-Language-Action (VLA) models. Work on HarmoWAM, RAW-Dream, and Pelican-Unified ties policy gains to imagined rollouts, phase-aware action control, and shared reasoning-action state.

## Findings

### World-model training and adaptation
World models are now used as training spaces and control priors, with clear pressure to reduce task-specific robot data. HarmoWAM combines a video world model with predictive and reactive action experts, then routes between transit and interaction phases. Its reported out-of-domain gains are 33 percentage points over prior VLA models and 29 points over prior World Action Models (WAMs) across six real-world tasks.

RAW-Dream gives the week’s clearest data-efficiency claim. It trains OpenVLA-OFT with reinforcement learning inside a task-agnostic video world model and uses Qwen3-VL for reward judgments. On LIBERO, it raises a 1-shot supervised fine-tuning baseline from 43.4% to 52.3% with 10 target demonstrations and no target rollouts for world-model training; with in-domain world-model tuning, it reaches 66.0%.

#### Sources
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): HarmoWAM summary gives the two-expert design, phase gate, real-world evaluation setup, and OOD gains.
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream summary provides the task-agnostic world-model training setup and LIBERO data-efficiency results.

### Action timing and spatial grounding
Several papers target the exact moments and scene features that decide whether a VLA policy succeeds. GuidedVLA assigns action-decoder attention heads to object grounding, skill phase recognition, and depth-based geometry. On LIBERO-Plus, the full model reaches 75.4% average success, above its π0 base at 68.2%, and its real-world trials improve over the base policy across in-domain, scene-change, and lighting-change settings.

FrameSkip treats dense demonstrations as uneven supervision. It keeps 20% of unique frames, protects gripper transitions and high-action-change frames, and raises the macro average across RoboCasa-GR1, SimplerEnv, and LIBERO from 66.50% to 76.15%. Evo-Depth and AffordVLA add complementary spatial signals: RGB-derived depth for placement and grasping, and training-time affordance alignment for contact regions without an added inference module.

#### Sources
- [GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization](../Inbox/2026-05-12--guidedvla-specifying-task-relevant-factors-via-plug-and-play-action-attention-specialization.md): GuidedVLA summary gives action-head specialization and results on LIBERO-Plus, perturbations, RoboTwin 2.0, and real-world trials.
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): FrameSkip summary reports the 20% frame-retention setup and benchmark gains.
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Evo-Depth summary gives the RGB-derived depth design, model size, benchmark results, memory use, and inference rate.
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA summary explains affordance-feature alignment, contact-region focus, and the no-extra-inference-cost claim.

### Long-horizon and multi-task control
Long execution is treated as a control problem with shared state and protected task knowledge. Pelican-Unified trains one embodied model to reason in language, predict future video, and output action chunks through a common latent state. It reports 93.5% average success on the 50-task RoboTwin dual-arm benchmark and an EWM Score of 66.03 on WorldArena.

DyGRO-VLA focuses on reinforcement learning after imitation training. It freezes a base VLA and learns routed residual experts that correct action chunks, reducing damage to shared representations during multi-task tuning. On LIBERO it reports 97.1% average success, and on LIBERO-Long it adds 9.8 percentage points over its offline base.

#### Sources
- [Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action](../Inbox/2026-05-14--pelican-unified-1-0-a-unified-embodied-intelligence-model-for-understanding-reasoning-imagination-and-action.md): Pelican-Unified summary provides the shared latent-state design and RoboTwin, WorldArena, and VLM benchmark results.
- [DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization](../Inbox/2026-05-17--dygro-vla-cross-task-scaling-of-vision-language-action-models-via-dynamic-grouped-residual-optimization.md): DyGRO-VLA summary provides the frozen-base residual RL design and LIBERO, LIBERO-Long, and RoboTwin2 results.

### Safety and behavior-level validation
Evaluation is adding checks for what happens during a rollout, not only the final task state. SafeManip defines temporal safety properties with finite-trace Linear Temporal Logic monitors over predicates such as collision, stable grasp, containment, sanitation, and fixture access. In 50 RoboCasa365 tasks, π0.5 improves task success over π0 from 8.1% to 9.3%, while its safety violation rate rises from 69.7% to 82.8%.

The same concern appears in the week’s contact-aware VLA work. AffordVLA trains policies to attend to functional contact regions, and the May 17 trend note highlights behavior-level checks as part of VLA interpretability and safety. The evidence points to a stricter deployment bar: success rates need to be paired with contact, order, recovery, and unsafe-state exposure measurements.

#### Sources
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip summary gives the temporal safety-monitor design, task set, policy set, and safety-versus-success results.
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA summary grounds the contact-region training method and inference-path detail.
