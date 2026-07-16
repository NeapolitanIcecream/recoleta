---
kind: trend
trend_doc_id: 839
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
topics:
- robot manipulation
- vision-language-action models
- policy adaptation
- temporal memory
- dexterous benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-839
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/policy-adaptation
- topic/temporal-memory
- topic/dexterous-benchmarks
language_code: en
pass_output_id: 344
pass_kind: trend_synthesis
---

# Robot policy gains now depend on memory, targeted adaptation, and harder dexterity tests

## Overview
Robot learning work in this period concentrates on making existing policies more dependable under perturbations and sparse feedback. Harness VLA adds planning and retries around a frozen controller. Prompt-Driven Exploration searches over language-conditioned behaviors. DexVerse shows why these controls matter: leading methods average only 34% success on its tested dexterous tasks.

## Findings

### Memory and task-state control
Several papers give vision-language-action (VLA) policies explicit control over task progress. Harness VLA treats a frozen VLA as a short, retryable contact skill, while a planner handles grounding, transport, staging, and failure recovery. It reaches 82.4% on LIBERO-Pro, compared with 50.0% for the direct frozen baseline. TFP stores an episode-local belief and updates it using elapsed time and interaction events; real-robot object-swap success rises from 3/20 to 15/20. LEEVLA adds task-relevant region weighting and latent future-feature prediction during training, reaching 98.2% on LIBERO without extra inference cost.

#### Sources
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): Planner-controlled staging, retries, frozen-VLA design, and LIBERO-Pro results.
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): Continuous-time task memory and real-robot object-swap results.
- [LEEVLA: Seeing What Matters in Latent Environment Evolution for Vision-Language-Action](../Inbox/2026-07-09--leevla-seeing-what-matters-in-latent-environment-evolution-for-vision-language-action.md): Task-aware visual weighting, latent feature prediction, and LIBERO performance.

### Targeted adaptation and exploration
Adaptation methods are modifying compact interfaces around pretrained policies. FlowDAgger converts sparse human corrections into latent noise targets for a frozen generative controller. On 12 MetaWorld tasks, mean success reaches 0.78 after 50 rollouts, versus 0.53 for the base policy. Prompt-Driven Exploration rewrites task prompts after inspecting rollout videos; in its microwave case study, canonical-prompt success reaches about 98% while action-noise PPO remains near zero. CLAP places a natural-language action description before numeric controls. Its 2B model reaches 90.8% on LIBERO after one epoch, 14.9 points above the matched baseline.

#### Sources
- [FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](../Inbox/2026-07-09--flowdagger-human-in-the-loop-adaptation-of-generative-robot-policies-in-latent-space.md): Latent action inversion, sparse intervention setup, and MetaWorld results.
- [Prompt-Driven Exploration](../Inbox/2026-07-09--prompt-driven-exploration.md): Prompt-based exploration mechanism and zero-reward-start results.
- [CLAP: Direct VLM-to-VLA Adaptation via Language-Action Grounding](../Inbox/2026-07-09--clap-direct-vlm-to-vla-adaptation-via-language-action-grounding.md): Language-action token sequence and one-epoch LIBERO gains.

### Compact models meet a dexterity ceiling
FabriVLA shows that a 0.89B-parameter model can reach 92.0% episode success on Meta-World MT50 using intermediate visual-language features and gated attention across action tokens. DexVerse exposes a much harder boundary. Across 19 dexterous tasks, the best mean success is 0.34, shared by 3D Diffusion Policy and pi0.5. Every tested method scores zero on PushT, and insertion, knife sliding, and laptop opening remain near zero. Strong results on standard suites therefore provide limited evidence for force control, fine alignment, and multi-stage hand use.

#### Sources
- [FabriVLA: A Lightweight Vision-Language-Action Model for Precise Multi-Task Manipulation](../Inbox/2026-07-09--fabrivla-a-lightweight-vision-language-action-model-for-precise-multi-task-manipulation.md): Model size, architectural components, and MT50 performance.
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): DexVerse scope, comparative success rates, and near-zero precision-task results.
