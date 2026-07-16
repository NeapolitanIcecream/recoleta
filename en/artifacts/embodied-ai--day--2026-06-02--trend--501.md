---
kind: trend
trend_doc_id: 501
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
topics:
- VLA
- robot manipulation
- geometry grounding
- world models
- test-time adaptation
- continual learning
- robot safety
run_id: materialize-outputs
aliases:
- recoleta-trend-501
tags:
- recoleta/trend
- topic/vla
- topic/robot-manipulation
- topic/geometry-grounding
- topic/world-models
- topic/test-time-adaptation
- topic/continual-learning
- topic/robot-safety
language_code: en
pass_output_id: 250
pass_kind: trend_synthesis
---

# Robot policy work is being judged by executable grounding

## Overview
The day’s robotics papers focus on making Vision-Language-Action (VLA) policies execute reliably under real deployment conditions. ERVLA, GeoAlign, and TTT-VLA show the clearest pattern: performance depends on action-grounded signals that match the robot’s state, geometry, and task phase.

## Findings

### Geometry-aware action prediction
GeoAlign and GeoSem-WAM both treat geometry as a control signal, not just a perception side channel. GeoAlign derives geometry features from RGB, lets the robot state query local spatial features, and feeds compact geometry tokens into the action decoder. It reports 99.0% average success on LIBERO and 78.8% on eight real ALOHA tasks, with large gains on transparent bottles and tape-roll insertion.

GeoSem-WAM applies the same pressure to World Action Models (WAMs), which learn predictive latent states for action. It trains on future RGB, geometry, and semantic maps, then removes the dense prediction heads at deployment. The reported real Franka success rises to 95.4% compared with 88.9% for Fast-WAM, and LIBERO ablations show gains when geometry and semantic supervision are combined.

#### Sources
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): GeoAlign summary and results for RGB-derived geometry tokens, LIBERO, SimplerEnv, and real ALOHA performance.
- [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](../Inbox/2026-06-02--geosem-wam-geometry-and-semantic-aware-world-action-models.md): GeoSem-WAM summary and results for geometry/semantic predictive supervision and real Franka gains.

### Action-grounded reasoning supervision
ERVLA gives embodied chain-of-thought (CoT) a narrow role: it supervises training and can be absent as visible text during inference. The paper’s ablations make the point concrete. High-level fields such as goal, planning, subtask, and reasoning alone hurt or barely help without pretraining. Movement descriptions and point trajectories add more value, and the full embodied CoT setup gives an 8.2-point gain in that setting.

The scaling result is also practical. Under an autoregressive CoT-prefix setup, adding larger robot datasets reduces VLABench performance across several tracks. ERVLA avoids requiring generated reasoning before action tokens and reports 86.9% average success on LIBERO-Plus and 53.2% on VLABench.

#### Sources
- [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](../Inbox/2026-06-02--revisiting-embodied-chain-of-thought-for-generalizable-robot-manipulation.md): ERVLA summary and ablations for embodied CoT fields, scaling behavior, and benchmark results.

### Deployment-time adaptation and phase-aware memory
Two papers target failures that appear after a policy leaves its original training setup. TTT-VLA freezes the VLA backbone and updates only latent prompt tokens using a self-supervised state-grounding loss. On SimplerEnv WidowX tasks, mean success rises to 67.4% after test-time prompt optimization, compared with 51.1% for the π0.5 base policy.

PHASER addresses continual learning. It stores and replays manipulation phases such as approach, grasp, and transport, so short contact-heavy phases get protected memory. On LIBERO-Long with OpenVLA-OFT-7B, PHASER reports 85.8% average success rate, compared with 54.6% for standard experience replay.

#### Sources
- [TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models](../Inbox/2026-06-02--ttt-vla-test-time-latent-prompt-optimization-for-vision-language-action-models.md): TTT-VLA summary and results for frozen-backbone latent prompt optimization at deployment.
- [PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models](../Inbox/2026-06-02--phaser-phase-aware-and-semantic-experience-replay-for-vision-language-action-models.md): PHASER summary and results for phase-aware replay in continual VLA learning.

### Real-world access and safety constraints
Several papers widen the evaluation lens beyond benchmark policy scores. OpenEAI-Platform lowers the hardware barrier with a $790 open 6+1 DoF arm and a Qwen3-VL-4B-based VLA policy trained on public robot and multimodal data. EaDex uses one RGB-D camera to collect low-cost human hand demonstrations and retargets them across three dexterous robot hands, raising average success on its custom tasks to 36.5% with demonstration annealing.

Safety evidence is already appearing alongside access work. A partially observable adversarial patch attack learns one fixed patch from a short observed rollout prefix and applies it to the unseen future of the task. On LIBERO with OpenVLA victims, attack success at K=30 reaches 90.7% on Object and 86.6% on Long, above the listed baselines in those settings.

#### Sources
- [OpenEAI-Platform: An Open-source Embodied Artificial Intelligence Hardware-Software Unified Platform](../Inbox/2026-06-02--openeai-platform-an-open-source-embodied-artificial-intelligence-hardware-software-unified-platform.md): OpenEAI-Platform summary and results for low-cost open robot hardware and VLA training setup.
- [EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations](../Inbox/2026-06-02--eadex-a-cross-embodiment-dexterous-manipulation-framework-from-low-cost-demonstrations.md): EaDex summary and results for low-cost RGB-D demonstrations and cross-embodiment dexterous manipulation.
- [Partially Observable Adversarial Patch Attacks on Vision-Language-Action Models in Robotics](../Inbox/2026-06-02--partially-observable-adversarial-patch-attacks-on-vision-language-action-models-in-robotics.md): Adversarial patch attack summary and LIBERO attack success results under partial observability.
