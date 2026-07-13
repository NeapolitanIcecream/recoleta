---
kind: trend
trend_doc_id: 778
granularity: day
period_start: '2026-07-01T00:00:00'
period_end: '2026-07-02T00:00:00'
topics:
- robotics
- vision-language-action models
- world models
- robot evaluation
- long-horizon manipulation
- robot safety
- tactile pretraining
- sim2real
- robot serving
run_id: materialize-outputs
aliases:
- recoleta-trend-778
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/robot-evaluation
- topic/long-horizon-manipulation
- topic/robot-safety
- topic/tactile-pretraining
- topic/sim2real
- topic/robot-serving
language_code: en
pass_output_id: 326
pass_kind: trend_synthesis
---

# Robot learning papers put VLA policies under execution pressure

## Overview
Robotics dominates this period. The strongest papers test vision-language-action (VLA) policies against rollout cost, long-horizon drift, collision risk, tactile data gaps, and factory serving. RoboWorld, FurnitureVLA, and ROSA give the clearest measured claims.

## Clusters

### World models for evaluation and control
RoboWorld gives the cleanest world-model result. It evaluates eight open robot policies through 4,186 generated rollouts, then matches the RoboArena real-world ranking with Pearson r=0.989 and Spearman rho=0.970. The key design is closed-loop rollout generation plus a 0–5 task-progress vision-language model judge, which is more informative than binary success scoring in the reported ablation.

Other papers make the control link explicit. ABot-M0.5 defines a world action model (WAM) for mobile manipulation that predicts future video, latent motion, and executable robot actions in sequence. The tutorial paper also tries to tighten terminology by defining robot world models as action-conditioned predictors and grouping WAM designs by how predicted futures connect to actions. The measured evidence is strongest for RoboWorld; ABot-M0.5 and the tutorial mainly clarify model design choices in the available excerpts.

#### Evidence
- [RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation](../Inbox/2026-07-01--roboworld-fast-and-reliable-neural-simulators-for-generalist-robot-policy-evaluation.md): RoboWorld summary reports closed-loop neural evaluation, Step Forcing, 4,186 generated rollouts, and ranking agreement with RoboArena.
- [ABot-M0.5: Unified Mobility-and-Manipulation World Action Model](../Inbox/2026-07-01--abot-m0-5-unified-mobility-and-manipulation-world-action-model.md): ABot-M0.5 summary describes future-video, latent-action, and executable-action prediction for mobile manipulation.
- [From World Models to World Action Models: A Concise Tutorial for Robotics](../Inbox/2026-07-01--from-world-models-to-world-action-models-a-concise-tutorial-for-robotics.md): Tutorial summary defines world models and world action models, including the taxonomy used for synthesis.

### Long-horizon manipulation is being scored by task completion, contact, and safety
FurnitureVLA is the main long-horizon manipulation result. It decomposes IKEA-style bimanual assembly into language-conditioned subtasks and predicts continuous subtask progress alongside a 14-dimensional dual-arm action. In simulation, average full-assembly success rises from 0.48 for monolithic finetuning to 0.80 across LACK, KALLAX, and IVAR.

Safety work adds another execution test. The constrained flow-matching paper edits predicted 10-step end-effector trajectories during denoising, using control barrier function constraints before the action chunk is finalized. On SafeLIBERO, it reports 82.81% collision avoidance and 81.62% task success, compared with 18.69% and 50.88% for unguided π0.5. The gain comes with slower execution, so the result is a safety-throughput tradeoff rather than a free improvement.

#### Evidence
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): FurnitureVLA summary gives the subtask-progress method and simulated success gains.
- [Neuro-Symbolic Safety Guidance for Vision-Language-Action Models via Constrained Flow Matching](../Inbox/2026-07-01--neuro-symbolic-safety-guidance-for-vision-language-action-models-via-constrained-flow-matching.md): Safety guidance summary reports trajectory-level constrained flow matching and SafeLIBERO results.

### Sensing, touch, and retrieval become policy inputs
Tactile pretraining receives a concrete data contribution. H-Tac contains 160 hours, more than 300 tasks, and over 135,000 episodes with tactile, action, vision, and language signals. Transferable Tactile Pre-Training adds a tactile expert that predicts future touch readings alongside action chunks. The excerpt gives dataset scale, while downstream success rates are not available in the supplied text.

Data access also gets practical attention. The Daft post shows per-frame search over Apple EgoDex using SigLIP-2 text-video embeddings plus hand-pose geometry. Its examples retrieve events such as stapler grips, block lifts, and t-shirt folding clips. That matters for robotics teams because fine manipulation failures often sit inside long unlabeled episodes.

Certified sensing clocks add a third sensor-facing thread. A frozen 3D VN-JEPA world model exposes a drift-aware deadline for when an agent should re-sense, with held-out interval certificate violation upper bounds below the stated 0.15 target in three tests.

#### Evidence
- [Human-Centric Transferable Tactile Pre-Training for Dexterous Robotic Manipulation](../Inbox/2026-07-01--human-centric-transferable-tactile-pre-training-for-dexterous-robotic-manipulation.md): TTP summary provides H-Tac scale, tactile-action pretraining design, and limits of reported downstream metrics.
- [Finding a Needle in the Haystack: Querying Physical AI Data with Daft](../Inbox/2026-07-01--querying-physical-ai-data-with-daft.md): Daft summary describes per-frame EgoDex retrieval with text embeddings and hand-pose geometry.
- [Certified World Models as Sensing Clocks: Drift-Aware Deadlines for Active Perception](../Inbox/2026-07-01--certified-world-models-as-sensing-clocks-drift-aware-deadlines-for-active-perception.md): Certified world-model summary reports drift-aware sensing deadlines and held-out interval violation results.

### Deployment work targets domain changes and shared GPU use
Adaptation and serving papers focus on what happens after a policy leaves its training setup. DART adapts a VLA to a new camera, lighting, sensor, or embodiment condition using one target-domain demonstration for one task plus a matching source demonstration. It extracts a domain vector from weight updates and adds it to the base policy, but the supplied excerpt does not include success-rate tables.

BIFROST addresses sim-to-real transfer through a shared latent history encoder trained on paired cross-domain segments. In sim-to-sim navigation, it reports 0.68 ± 0.08 success for top-down views and 0.50 ± 0.08 for egocentric views, with weaker direct-transfer baselines at 0.19 ± 0.04 and 0.03 ± 0.02. The excerpt claims sim-to-real tests, but the quantitative tables are absent.

ROSA treats robot foundation model inference as a fleet scheduling problem. On eight H200 GPUs and up to 64 virtual robots, it reports up to 12.06× higher SLO-qualified factory productivity than dedicated serving baselines, and up to 2.44× over shared-server baselines without its scheduler.

#### Evidence
- [Domain Arithmetic: One-Shot VLA Adaptation under Environmental Shifts](../Inbox/2026-07-01--domain-arithmetic-one-shot-vla-adaptation-under-environmental-shifts.md): DART summary describes one-shot domain-vector adaptation and notes missing numerical margins in the excerpt.
- [BIFROST: Bridging Invariant Feature Representation for Observation-space Sim2Real Transfer](../Inbox/2026-07-01--bifrost-bridging-invariant-feature-representation-for-observation-space-sim2real-transfer.md): BIFROST summary gives the paired latent encoder method and sim2sim success rates.
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): ROSA summary reports shared GPU-pool scheduling and factory productivity gains.
