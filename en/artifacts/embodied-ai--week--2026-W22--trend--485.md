---
kind: trend
trend_doc_id: 485
granularity: week
period_start: '2026-05-25T00:00:00'
period_end: '2026-06-01T00:00:00'
topics:
- robot learning
- vision-language-action models
- real-robot evaluation
- dexterous manipulation
- tactile control
- continual learning
run_id: materialize-outputs
aliases:
- recoleta-trend-485
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/real-robot-evaluation
- topic/dexterous-manipulation
- topic/tactile-control
- topic/continual-learning
language_code: en
pass_output_id: 244
pass_kind: trend_synthesis
---

# Robot VLA claims now need real control evidence

## Overview
This week’s robotics research judges vision-language-action (VLA) policies by real execution: online fine-tuning speed, task retention, contact quality, and cross-embodiment coverage. EXPO-FT, OASIS, and Qwen-VLA anchor the strongest claims, with most evidence tied to real robots or manipulation benchmarks.

## Clusters

### Real-robot post-training
Several papers treat VLA deployment as a post-training problem with measurable robot time and failure recovery. EXPO-FT reports 30/30 success on eight real manipulation tasks after an average of 19.1 minutes of online robot data. BORA adds an offline critic and a small human-guided residual actor for dexterous hand control, reaching 86.0% average success across five Franka arm plus 12-DoF hand tasks. A continual-learning study gives the counterweight: plain sequential fine-tuning can erase earlier skills, while experience replay with fixed action normalization raises the final average score to 93.5.

#### Evidence
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): EXPO-FT reports 30/30 real-task success after 19.1 minutes of online data on average.
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): BORA reports offline-to-online RL gains on real dexterous manipulation tasks.
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): Continual VLA study quantifies forgetting and replay-based retention on real manipulation tasks.

### Action geometry and cross-task transfer
The strongest control papers add structure around action prediction. OASIS predicts future end-effector poses in SE(3) before decoding action chunks, and reports 97.6% average success on LIBERO plus 89.2% average success in real-world tests. Qwen-VLA uses embodiment-aware prompts and a shared action-and-trajectory format to cover manipulation, navigation, and trajectory prediction with one policy. VLA-Pro stores task-specific LoRA adapters as procedural memories and retrieves them at inference, raising real-world success on held-out UR7e tasks from 5.8% to 65.0%.

#### Evidence
- [OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation](../Inbox/2026-05-25--oasis-observation-action-space-alignment-via-se-3-trajectory-prediction-for-robotic-manipulation.md): OASIS summary gives the SE(3) trajectory mechanism and simulation plus real-world success results.
- [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](../Inbox/2026-05-28--qwen-vla-unifying-vision-language-action-modeling-across-tasks-environments-and-robot-embodiments.md): Qwen-VLA summary describes the shared action format, embodiment prompts, and benchmark results.
- [VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models](../Inbox/2026-05-28--vla-pro-cross-task-procedural-memory-transfer-for-vision-language-action-models.md): VLA-Pro summary reports procedural-memory retrieval and real-world held-out task gains.

### Touch and force control
Contact quality becomes part of the evaluation target. Tabero adds tactile tokens and closed-loop force commands, then measures success together with grip and applied force. It reports over 70% lower average grip force under gentle instructions. CoP compresses tactile taxel readings into contact force and contact location for sim-to-real dexterous manipulation, reaching 0.78 real peg-in-hole success across six shapes. Mag-VLA extends the same execution focus to microscope-scale bimanual magnetic manipulation, with 90% approach success and lower transport success as path curvature rises.

#### Evidence
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero summary details tactile-force data, closed-loop control, and force-reduction claims.
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP summary reports contact representation and real peg-in-hole results.
- [Mag-VLA: Vision-Language-Action Model for Bimanual Magnetically Actuated Microrobot Manipulation](../Inbox/2026-05-27--mag-vla-vision-language-action-model-for-bimanual-magnetically-actuated-microrobot-manipulation.md): Mag-VLA summary reports phase-aware bimanual microrobot control and real-robot success rates.

### Cheaper validation and smaller policies
Cost is a visible constraint in the week’s evidence. ProgVLA uses a 0.1B-parameter policy with compressed multimodal tokens and progress heads, reaching 91.1% average success on LIBERO and 88.6% on LIBERO Long. Its real PiPER-arm tests are more modest at 68% success over 100 trials, which gives a useful check against benchmark-only claims. The day-level trend also groups HyperSim and SDPG with efforts to reduce real-data or GPU cost, placing efficiency alongside execution quality.

#### Evidence
- [ProgVLA: Progress-Aware Robot Manipulation Skill Learning](../Inbox/2026-05-27--progvla-progress-aware-robot-manipulation-skill-learning.md): ProgVLA summary provides parameter count, benchmark scores, ablations, and real-robot test results.
