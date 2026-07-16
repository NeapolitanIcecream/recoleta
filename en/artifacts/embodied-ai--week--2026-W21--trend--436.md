---
kind: trend
trend_doc_id: 436
granularity: week
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-25T00:00:00'
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D grounding
- spatial memory
- real-world evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-436
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-grounding
- topic/spatial-memory
- topic/real-world-evaluation
language_code: en
pass_output_id: 198
pass_kind: trend_synthesis
---

# Robot VLA claims now need real execution evidence

## Overview
Embodied AI research this week treats robot policies as systems that must survive real control conditions. Vision-language-action (VLA) models are tested through visual corruptions, 3D contact cues, memory, latency, and reproducible hardware runs. StableVLA, GaussianDream, and AVP give the clearest signal.

## Findings

### Execution reliability under imperfect sensing
VLA work is being judged by what happens during execution: blur, lighting changes, delays, perturbations, and fine task stages. StableVLA targets this directly with an Information Bottleneck Adapter that filters noisy visual channels without extra robot data. The reported gains are concrete: 82.0% versus 58.5% on LIBERO Spatial under severity-5 corruptions, and 50% versus 20% on a real Pack Doll task against the VLA-Adapter baseline. The daily trend evidence also points to latency and illumination tests as common reliability checks across the week.

#### Sources
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): StableVLA summary gives the visual-corruption setup, adapter design, and reported simulation and real-robot gains.

### 3D contact cues inside action prediction
Several papers add explicit geometry to the policy path, not just to perception. GaussianDream trains a VLA policy with 3D Gaussian reconstruction and short-horizon future prediction, then keeps only learned prefix tokens at inference. It reports 98.4% average success on LIBERO, 52.6% on RoboCasa Human-50, and 50.0% in real-robot evaluation. PointACT feeds hierarchical point-cloud features into the action decoder, reaching 96.0% average success on LIBERO and beating SpatialVLA by 17.9 points in the reported table. These results make 3D structure part of the action interface.

#### Sources
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream summary covers 3D Gaussian training supervision, inference design, and reported benchmark and real-robot numbers.
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT summary covers point-cloud action decoding and its LIBERO and SpatialVLA comparisons.

### Spatial grounding and memory for closed-loop manipulation
The strongest grounding papers add intermediate state that the robot can act on. AVP makes the vision-language model output visual primitive tokens before action prediction, then uses a flow-matching action expert. On Chinese chess manipulation, it reports 90.28% average success versus 62.67% for π₀.₅, while running at 0.27 seconds per instruction. SOMA adds persistent spatial memory for objects outside the current camera view. On five real-world out-of-vision tasks, full SOMA reaches 28.3% average success and cuts time-to-grasp across tasks compared with GR00T-N1.5. The shared point is practical: policies need target state, scene memory, and fast action checks during execution.

#### Sources
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP summary gives the visual-primitive action interface, real-robot success rates, and latency.
- [Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action](../Inbox/2026-05-21--spatial-memory-for-out-of-vision-manipulation-in-vision-language-action.md): SOMA summary gives persistent spatial memory, out-of-vision task results, search time, and grasp-time reductions.

### Reproducible real-world benchmarks become infrastructure
Evaluation work is trying to make physical robot testing easier to repeat. VLA-REPLICA uses off-the-shelf hardware, fixed lighting, camera alignment tools, reference placements, and 500 expert demonstrations across 10 manipulation tasks. The full setup is reported at about $1050 and was assembled by a new user in under an hour. Its 90 test scenes cover in-distribution and out-of-distribution evaluation, and π₀.₅ reaches the best reported in-distribution average success rate at 0.54. This type of benchmark lowers the cost of checking whether a policy works outside a simulator.

#### Sources
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA summary provides hardware cost, setup details, task suite, demonstration count, test scenes, and baseline results.
