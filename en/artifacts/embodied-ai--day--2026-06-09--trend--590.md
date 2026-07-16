---
kind: trend
trend_doc_id: 590
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
topics:
- robot manipulation
- VLA policies
- real-robot evaluation
- occlusion
- dexterous manipulation
- sim-real correlation
run_id: materialize-outputs
aliases:
- recoleta-trend-590
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vla-policies
- topic/real-robot-evaluation
- topic/occlusion
- topic/dexterous-manipulation
- topic/sim-real-correlation
language_code: en
pass_output_id: 270
pass_kind: trend_synthesis
---

# Robot manipulation papers are testing policies against real failure modes

## Overview
Robot research in this window is centered on making manipulation claims survive real execution. LIBERO-Occ, UMI-Bench 1.0, and Dexterous Point Policy show the emphasis: hidden objects, physical rollout protocols, and robot data scarcity.

## Findings

### Occlusion and physical benchmarks expose brittle manipulation results
Several papers tighten evaluation for vision-language-action (VLA) robot policies, where VLA means mapping language and visual input to robot actions. LIBERO-Occ adds 2,000 occluded LIBERO tasks and reports large drops when task objects or receptacles are hidden. VIM recovers part of the loss by generating a complementary wrist or gripper view, reaching 65.05% average success without a real extra view.

UMI-Bench 1.0 gives Universal Manipulation Interface policies a real-robot tabletop protocol with fixed resets, wrist-view inputs, rollout logging, and human scoring. Its results show that physical factors such as layout, pose, and dynamics hurt more than appearance or object-category changes. A separate sim-real study finds REALM tracks real robot policy rankings better than VLA-Arena and SIMPLER, with Spearman correlation 0.700 before simulator post-training and 0.875 after it.

#### Sources
- [LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination](../Inbox/2026-06-09--libero-occ-evaluating-and-improving-vision-language-action-models-under-scene-induced-occlusion-via-viewpoint-imagination.md): LIBERO-Occ task design, VIM method, and occlusion success rates.
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): UMI-Bench protocol, task coverage, model scores, and shift diagnostics.
- [A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation](../Inbox/2026-06-09--a-practical-recipe-towards-improving-sim-and-real-correlation-for-vla-evaluation.md): Sim-real evaluation setup and REALM correlation results.

### Test-time checks add geometry, contact, and dense progress signals
Execution-time safety and correction are a major theme. VeriSpace samples multiple candidate actions from a frozen VLA policy, scores them with color-depth (RGB-D) spatial reasoning, and executes the best candidate. On SimplerEnv-WidowX with OpenVLA, average success rises from 37.0% to 55.0% across four tasks.

Contact-rich work adds another layer of feedback. TacForeSight predicts short-horizon tactile latents from wrist force and current tactile input, then uses those predictions for action generation. It reports a 79.0% average completion score across five real-robot contact tasks, compared with 43.0% for the strongest listed baseline. SARM2 tackles long-horizon progress estimation through a stage-aware dense reward model; paired with SPIRAL, it reaches 18/20 successes on Cleaning Whiteboard and 12/12 on Folding Shorts Flat.

#### Sources
- [VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models](../Inbox/2026-06-09--verispace-spatially-grounded-action-verification-for-vision-language-action-models.md): VeriSpace test-time verifier design and success gains.
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](../Inbox/2026-06-09--tacforesight-force-guided-tactile-world-model-for-contact-rich-manipulation.md): TacForeSight force-conditioned tactile world model and real-robot scores.
- [SARM2: Multi-Task Stage Aware Reward Modeling for Self Improving Robotic Manipulation](../Inbox/2026-06-09--sarm2-multi-task-stage-aware-reward-modeling-for-self-improving-robotic-manipulation.md): SARM2 reward accuracy and SPIRAL real-robot improvement results.

### Long-horizon control benefits from explicit orchestration and planning
Long tasks are being treated as control-loop design problems. The hierarchical VLA study separates high-level language subgoals from low-level action execution, then tests planner choice, controller choice, memory, observation encoding, and termination rules. Its best hierarchy reaches 67.08% on long-horizon MuJoCo ALOHA tasks, compared with 25.30% for a flat VLA. On a real ALOHA fruit-sorting task, it places 12 of 15 fruits correctly, compared with 3 of 15 for the flat setup.

MODIP applies a similar concern to diffusion policies. It uses a latent world model and model predictive control to create improved trajectories, then trains the diffusion policy with supervised denoising. The method reports 0.94 success on D4RL Kitchen Complete and 0.98 on Kitchen Partial, beating behavior cloning by wide margins in those settings.

#### Sources
- [What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents](../Inbox/2026-06-09--what-matters-in-orchestrating-robot-policies-a-systematic-study-of-hierarchical-vla-agents.md): Hierarchical VLA design study and long-horizon simulation plus real ALOHA results.
- [MODIP: Efficient Model-Based Optimization for Diffusion Policies](../Inbox/2026-06-09--modip-efficient-model-based-optimization-for-diffusion-policies.md): MODIP world-model planning approach and offline-to-online success metrics.

### Human video becomes practical when policies use transferable hand geometry
Dexterous Point Policy is the strongest data-scaling result in the window. It trains dexterous robot hand behavior from human videos only, with no robot demonstrations. The key abstraction is six shared 3D points: the wrist and five fingertips. Object points, language, camera pose, and contact labels then guide an autoregressive transformer, while inverse kinematics maps predicted points to robot joints.

The reported real-robot gap is large. Across eight dexterous tasks, DPP reaches 75.0% average success, while Point Policy reaches 3.7% and VITRA reaches 1.0%. Contact prediction is central in the paper’s ablation, accounting for a 71.3 percentage point gain over the point-only baseline.

#### Sources
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](../Inbox/2026-06-09--dexterous-point-policy-learning-point-based-dexterous-hand-policies-from-human-demonstrations.md): DPP human-video training setup, 3D keypoint abstraction, and real-robot success rates.
