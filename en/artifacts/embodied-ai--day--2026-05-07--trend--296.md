---
kind: trend
trend_doc_id: 296
granularity: day
period_start: '2026-05-07T00:00:00'
period_end: '2026-05-08T00:00:00'
topics:
- robot manipulation
- vision-language-action
- world models
- human video data
- simulation evaluation
- dexterous manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-296
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action
- topic/world-models
- topic/human-video-data
- topic/simulation-evaluation
- topic/dexterous-manipulation
language_code: en
pass_output_id: 136
pass_kind: trend_synthesis
---

# Robot policies are judged by object identity, contact, and simulator fidelity

## Overview
Robot research in this period concentrates on control that survives scene changes. Vision-language-action (VLA) papers make object identity, hand contact, action-conditioned world models, and simulator fidelity measurable. OA-WAM, HumanNet, and VISER give the clearest evidence because they pair mechanisms with benchmark or validation results.

## Findings

### Object-grounded VLA control
VLA policies are adding explicit object and relation structure inside the action path. OA-WAM separates a fixed object address from changing object content, which makes target binding testable through slot interventions. It reports 97.8% average success on LIBERO and a swap-binding cosine of 0.87, while holistic baselines stay at 0.09 or lower.

TriRelVLA takes a related route through object, hand, and task nodes. Its graph uses four relation types: task-object, task-hand, object-hand, and object-object. The available excerpt gives mechanism detail and claimed gains for cross-scene, cross-object, and cross-task manipulation, but no quantitative benchmark table.

#### Sources
- [OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation](../Inbox/2026-05-07--oa-wam-object-addressable-world-action-model-for-robust-robot-manipulation.md): OA-WAM object-slot design and LIBERO, SimplerEnv, LIBERO-Plus, and slot-intervention results.
- [TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation](../Inbox/2026-05-07--trirelvla-triadic-relational-structure-for-generalizable-embodied-manipulation.md): TriRelVLA relation graph, task tokens, relation types, and stated generalization settings.

### World models built for control signals
World-model work is being evaluated by whether its latent state preserves action-relevant information. One study trains action-conditioned diffusion world models on BridgeV2 while varying only the latent encoder. Semantic encoders such as V-JEPA 2.1 and SigLIP 2 beat reconstruction-focused VAEs on policy rollouts, action recovery, and success classification. V-JEPA 2.1_96 reaches 0.362 consensus success in DiT-S rollouts, compared with 0.169 for VAE.

EA-WM attacks the action-conditioning side. It converts robot kinematics into camera-aligned visual fields, including arm skeletons, gripper geometry, end-effector heatmaps, and pose axes. On WorldArena, it reports 76.60 P3CScore versus 71.08 for CogVideoX, with ablations showing losses when kinematic-to-visual fields or event-aware fusion are removed.

#### Sources
- [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](../Inbox/2026-05-07--reconstruction-or-semantics-what-makes-a-latent-space-useful-for-robotic-world-models.md): Comparison of semantic and reconstruction latents for robot diffusion world models, with rollout and action-recovery metrics.
- [EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields](../Inbox/2026-05-07--ea-wm-event-aware-generative-world-model-with-structured-kinematic-to-visual-action-fields.md): EA-WM action-field design, WorldArena scores, and ablation results.

### Human interaction data for robot execution
Human data appears in two forms: large video pretraining and small motion sets refined into executable dexterity. HumanNet reports 1,000,000 hours of human-centric video with first-person and third-person views, captions, motion descriptions, and hand/body signals. In a controlled VLA validation, 1,000 hours of egocentric HumanNet pretraining reportedly matches or slightly beats 100 hours of real-robot CoBot pretraining under the same LingBot-VLA setup.

DexSynRefine shows the smaller-data path. It starts with seven human-object interaction demonstrations per task, expands them to about 300 trajectories per task, and adds residual reinforcement learning plus contact and dynamics adaptation. Across five dexterous tasks, task-space residual actions reach 68.1% mean simulated success, while raw kinematic retargeting stays near failure.

#### Sources
- [HumanNet: Scaling Human-centric Video Learning to One Million Hours](../Inbox/2026-05-07--humannet-scaling-human-centric-video-learning-to-one-million-hours.md): HumanNet scale, annotations, and controlled VLA validation against robot-data pretraining.
- [DexSynRefine: Synthesizing and Refining Human-Object Interaction Motion for Physically Feasible Dexterous Robot Actions](../Inbox/2026-05-07--dexsynrefine-synthesizing-and-refining-human-object-interaction-motion-for-physically-feasible-dexterous-robot-actions.md): DexSynRefine data expansion, residual policy design, contact/dynamics adaptation, and task success results.

### Adaptation and evaluation under visual perturbations
Two papers focus on whether robot policy claims hold under distribution changes. VLA-GSE uses parameter-efficient fine-tuning: it trains 114.04M of 4,551.85M parameters, or 2.51%, with shared and routed low-rank experts. It reports 81.2% average zero-shot success on LIBERO-Plus, ahead of full fine-tuning and several PEFT baselines in its same-backbone comparison.

VISER tests the evaluation side. It builds 1,049 physically based rendering assets across 319 categories and adds specular materials, soft shadows, and reconstructed real-world tasks. The benchmark reports an average Pearson correlation of 0.92 between simulation and real-world policy performance, with visual cues changing task outcomes sharply: eggplant-in-pot success rises from 10% without specular highlights to 90% with them.

#### Sources
- [VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts](../Inbox/2026-05-07--vla-gse-boosting-parameter-efficient-fine-tuning-in-vla-with-generalized-and-specialized-experts.md): VLA-GSE trainable-parameter count, LIBERO-Plus zero-shot results, and distribution-shift scores.
- [Toward Visually Realistic Simulation: A Benchmark for Evaluating Robot Manipulation in Simulation](../Inbox/2026-05-07--toward-visually-realistic-simulation-a-benchmark-for-evaluating-robot-manipulation-in-simulation.md): VISER asset scale, visual realism design, sim-to-real correlation, and lighting/material ablations.
