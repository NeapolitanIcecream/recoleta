---
kind: trend
trend_doc_id: 795
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- robot manipulation
- deployment systems
run_id: materialize-outputs
aliases:
- recoleta-trend-795
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/robot-manipulation
- topic/deployment-systems
language_code: en
pass_output_id: 336
pass_kind: trend_synthesis
---

# Robot VLA progress is measured by control-loop success

## Overview
Robot research this week puts vision-language-action (VLA) policies inside real execution constraints. The strongest evidence comes from models that predict action-relevant change, manage long rollouts, and keep serving latency tied to task progress. Bridge-WA, FurnitureVLA, and ROSA show the clearest pressure points.

## Findings

### Cross-embodiment VLA training
Generalist robot policies are being trained to share high-level manipulation concepts while still producing robot-specific controls. ZR-0 is the clearest example. It uses dense embodied chain-of-thought labels during training for scene description, task progress, future plan, target boxes, and discrete action tokens. At inference, it skips text generation and outputs continuous action chunks through a diffusion action expert.

The measured claim is concrete. ZR-0 reports 97.8% average success on LIBERO, with ProcCorpus-60M covering about 60 million frames, 1,000 hours, and more than 400,000 trajectories. The same daily trend also groups this with reward-free test-time improvement and trajectory memory, showing that policy scale is being tied to executable action timing and state history.

#### Sources
- [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](../Inbox/2026-06-29--training-vision-language-action-models-with-dense-embodied-chain-of-thought-supervision.md): ZR-0 training design, dataset scale, inference path, and LIBERO results.

### 3D and future-change signals for manipulation
Several papers add explicit physical signals before action generation. 3D HAMSTER predicts end-effector waypoints in metric 3D and feeds them to a point-cloud control policy. On DroidSpatial-Bench, it reaches 65.5% Both accuracy at 10 cm, above RoboBrain-2.5-8B at 60.1% and far above general VLM baselines.

Bridge-WA uses a different control signal. It distills a future-change teacher into intended-outcome tokens, change maps, and motion-flow maps, then removes the teacher at deployment. It reports 52.8% average success on VLABench and stronger real-robot Dobot hard-track averages than X-VLA under distractors, lighting changes, and tablecloth changes.

DVG-WM adds video prediction evidence. It separates low-resolution dynamics from high-resolution refinement and reports 88.7 seconds inference on LIBERO video prediction, compared with 236.8 seconds for CogVideoX-5B and 354.2 seconds for LVP-14B. The common pattern is direct: useful robot prediction is judged by contact, changed regions, and planning cost.

#### Sources
- [3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance](../Inbox/2026-06-30--3d-hamster-bridging-planning-and-control-in-hierarchical-vision-language-action-models-through-3d-trajectory-guidance.md): 3D HAMSTER waypoint design and DroidSpatial-Bench results.
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): Bridge-WA future-change priors and benchmark results.
- [DVG-WM: Disentangled Video Generation Enables Efficient Embodied World Model for Robotic Manipulation](../Inbox/2026-06-30--dvg-wm-disentangled-video-generation-enables-efficient-embodied-world-model-for-robotic-manipulation.md): DVG-WM video world model design, quality metrics, and inference-time comparison.

### Long-horizon manipulation needs progress checks
Long tasks are exposing failure modes that short manipulation benchmarks miss. FurnitureVLA targets real-scale bimanual furniture assembly with 4 to 7 subtasks and up to 1,550 control steps. Its policy predicts both 14-dimensional bimanual actions and a continuous progress value, using the progress signal to trigger subtask transitions.

The payoff is measured on full assemblies. Average simulated success rises from 0.48 for a monolithic finetuned VLA to 0.80 across three IKEA-style tasks. The same result also shows the cost of weaker execution design: removing the rear-camera setup drops average success to 0.50, and discrete progress prediction fails all three simulated furniture tasks.

#### Sources
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): FurnitureVLA task horizon, progress prediction method, and success-rate results.

### Factory deployment is treated as a scheduling problem
Robot foundation models are also being evaluated as deployed services. ROSA routes many robots’ model requests to a shared GPU pool and schedules them by service-level objective qualified action throughput. The task file covers model components, prompts, call rates, retry rules, and fallback actions such as stop, resend, replan, or call a human.

The reported gains come from treating robot inference as a fleet workload. On 8 NVIDIA H200 GPUs with up to 64 virtual robots, ROSA improves SLO-qualified factory productivity by up to 12.06x over dedicated serving baselines. Against shared-server baselines without its scheduler, it improves qualified factory action throughput by up to 2.44x. This makes deployment evidence part of the research signal, alongside policy success rates.

#### Sources
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): ROSA architecture, scheduling objective, and throughput results.
