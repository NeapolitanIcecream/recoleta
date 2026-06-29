---
kind: trend
trend_doc_id: 390
granularity: day
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-19T00:00:00'
topics:
- embodied AI
- robot manipulation
- VLA models
- dexterous robotics
- world models
- robot benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-390
tags:
- recoleta/trend
- topic/embodied-ai
- topic/robot-manipulation
- topic/vla-models
- topic/dexterous-robotics
- topic/world-models
- topic/robot-benchmarks
language_code: en
pass_output_id: 184
pass_kind: trend_synthesis
---

# Embodied AI papers make real robot execution the main test

## Overview
The period is dominated by embodied AI work that treats policies as deployable robot systems. Vision-language-action (VLA) models are tested on dexterous hands, corrupted cameras, dual-arm tasks, and contact-rich world-model benchmarks. Dexora, StableVLA, and WorldArena 2.0 set the tone: success rates, physical rollouts, tactile signals, and transfer tests matter more than clean simulation scores alone.

## Clusters

### Dexterous manipulation moves onto real hands and tables
Dexora is the strongest execution result in the set. It combines two 6-DoF arms with two 12-DoF dexterous hands, a matched MuJoCo twin, 100K simulated trajectories, and 10K real teleoperated episodes. Its reported 89.6% average success on 12 basic real-world tasks and 66.7% on six dexterous tasks put high-DoF bimanual control at the center of the period.

DexHoldem tests a different failure mode: whether a dexterous system can keep a changing tabletop scene usable while handling cards and chips. The benchmark includes 1,470 teleoperated demonstrations across 14 primitives and scores both task completion and scene preservation. The best policy reaches 61.2% task completion, while scene-preserving success tops out at 47.5%, showing that fine manipulation and state-safe execution remain difficult even in a compact tabletop domain.

#### Evidence
- [Dexora: Open-source VLA for High-DoF Bimanual Dexterity](../Inbox/2026-05-18--dexora-open-source-vla-for-high-dof-bimanual-dexterity.md): Dexora hardware, data scale, and real-world success rates.
- [DexHoldem: Playing Texas Hold'em with Dexterous Embodied System](../Inbox/2026-05-18--dexholdem-playing-texas-hold-em-with-dexterous-embodied-system.md): DexHoldem benchmark design and real primitive execution results.

### VLA reliability is being attacked through memory and visual tolerance
Key-Gram and StableVLA target two practical weaknesses in VLA policies. Key-Gram stores reusable instruction knowledge outside the main backbone, retrieves short “key-grams” such as object relations and subgoals, and injects them into selected Transformer layers. The reported gains are broad: pi0-KG improves RoboTwin2.0 hard-task success from 58.4% to 75.6%, and real long-horizon dual-arm success from 69.3% to 80.0%.

StableVLA focuses on bad camera inputs. It replaces the visual projector with an Information Bottleneck Adapter, which suppresses noisy feature channels while preserving spatial detail through a parallel path. The paper reports no extra robot data or corruption-specific augmentation, yet shows severity-5 LIBERO gains such as 70.2% versus 29.3% on Object tasks and 45.3% versus 26.2% on Long tasks.

#### Evidence
- [Key-Gram: Extensible World Knowledge for Embodied Manipulation](../Inbox/2026-05-18--key-gram-extensible-world-knowledge-for-embodied-manipulation.md): Key-Gram memory mechanism and success-rate gains across RoboTwin2.0, LIBERO-Plus, and real dual-arm tasks.
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): StableVLA adapter design and corruption-tolerance results.

### World models are judged by contact, control use, and physical structure
WorldArena 2.0 expands world-model evaluation beyond video prediction. It adds visuotactile sensing, reinforcement learning inside learned dynamics, and real-robot platform tests. The UniVTAC results are mixed: Wan2.2 gets the best tactile quality at 21.26 PSNR and 0.746 SSIM, yet averages 50% task success across Insert HDMI and Lift Bottle. Good tactile reconstruction does not guarantee useful control.

WorldString and PH-Dreamer address physical structure at different levels. WorldString predicts occupied 3D shape from sparse state keypoints and reports an 86.61 IoU average on four articulated objects. PH-Dreamer regularizes latent rollouts with Port-Hamiltonian energy dynamics and reports a 789.2 average return across six DeepMind Control visual tasks, above DreamerV3 and R2Dreamer, with lower phase-space volume and smoother action statistics.

#### Evidence
- [WorldArena 2.0: Extending Embodied World Model Benchmarking on Modality, Functionality and Platform](../Inbox/2026-05-18--worldarena-2-0-extending-embodied-world-model-benchmarking-on-modality-functionality-and-platform.md): WorldArena 2.0 modalities, RL-in-world-model evaluation, and tactile/task results.
- [WorldString: Actionable World Representation](../Inbox/2026-05-18--worldstring-actionable-world-representation.md): WorldString controllable 3D object representation and reconstruction metrics.
- [PH-Dreamer: A Physics-Driven World Model via Port-Hamiltonian Generative Dynamics](../Inbox/2026-05-18--ph-dreamer-a-physics-driven-world-model-via-port-hamiltonian-generative-dynamics.md): PH-Dreamer physical regularization and DeepMind Control results.

### Embodied memory is becoming an action mechanism, not only a log
Two papers use memory as a control input rather than a passive record. Key-Gram retrieves reusable language priors for manipulation, while Robo-Cortex turns navigation episodes into natural-language heuristics that guide later planning. Robo-Cortex++ updates its heuristic library during inference, then reports IGNav success of 45.07 compared with 38.57 for World-In-World, and raises IGNav SPL to 35.06.

The useful detail is how the memory is consumed. Robo-Cortex predicts short future visual outcomes, evaluates candidate actions with a vision-language model, and feeds back recent failure summaries plus retrieved long-term principles. The reported heuristic-transfer table is strong for navigation: IGNav SPL rises from 24.03 for the basic pipeline to 39.33 with transferred heuristics.

#### Evidence
- [Robo-Cortex: A Self-Evolving Embodied Agent via Dual-Grain Cognitive Memory and Autonomous Knowledge Induction](../Inbox/2026-05-18--robo-cortex-a-self-evolving-embodied-agent-via-dual-grain-cognitive-memory-and-autonomous-knowledge-induction.md): Robo-Cortex memory design, online heuristic induction, and navigation gains.
- [Key-Gram: Extensible World Knowledge for Embodied Manipulation](../Inbox/2026-05-18--key-gram-extensible-world-knowledge-for-embodied-manipulation.md): Key-Gram external language memory used inside VLA manipulation policies.
