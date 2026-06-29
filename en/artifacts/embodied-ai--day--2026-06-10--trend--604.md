---
kind: trend
trend_doc_id: 604
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
topics:
- vision-language-action
- robot manipulation
- contact-rich control
- world models
- multi-robot collaboration
- dexterous manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-604
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/contact-rich-control
- topic/world-models
- topic/multi-robot-collaboration
- topic/dexterous-manipulation
language_code: en
pass_output_id: 272
pass_kind: trend_synthesis
---

# Robot VLA gains are tied to contact, timing, and action priors

## Overview
Vision-language-action (VLA) robot papers in this period focus on making policies work under physical constraints. DAM-VLA, World Pilot, and CHORUS show the main emphasis: faster sensor loops, action-aware guidance, and deployable control across real robot settings.

## Clusters

### Contact-aware control loops
DAM-VLA treats robot inputs as signals with different clocks. Language is encoded once, vision updates sparsely, and force plus proprioception update at the control rate. The action head reads buffered latents at every step, which lets the controller keep producing actions while slower inputs wait for new data. On seven real Franka manipulation tasks, it reports 95.2% average success, compared with 40.95% for the strongest synchronous baseline.

TacCoRL adds tactile tokens to a pretrained VLA policy and trains contact correction in simulation before real deployment. Its contact gate suppresses touch readings when they look like background noise, and reinforcement learning runs in a real-aligned simulator with a supervised anchor on real trajectories. Across four real bimanual contact-rich tasks, the visuo-tactile policy reaches 72.5% average success, compared with 50.0% for a vision-only policy after reinforcement learning.

#### Evidence
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): DAM-VLA summary, asynchronous modality buffers, 100 Hz control, and real-task success rates.
- [TacCoRL: Integrating Tactile Feedback into VLA via Simulation](../Inbox/2026-06-10--taccorl-integrating-tactile-feedback-into-vla-via-simulation.md): TacCoRL summary, tactile gating, sim-real training method, and real-world success rates.

### Action and world priors for generalization
World Pilot adds a frozen world-action model to a VLA policy. One pathway injects a predicted scene-evolution latent into the perception stream. Another feeds an anticipated action trajectory to the action generator. On LIBERO-Plus zero-shot out-of-distribution tests, it reports 84.7% total success, ahead of ABot-M0 at 80.5% and Cosmos Policy at 79.7%. In real-robot tests, the paper reports the highest success rate in every listed setting.

APT attacks a different failure mode: weak instruction generalization caused by imbalanced robot data. It first trains the continuous action expert on vision-action pairs with language masked out, then adds language conditioning. On LIBERO-PRO, APT with vision-language model fine-tuning reports 27% average success, compared with 11% for π0.5 and 14% for LangForce. On LIBERO-PRO Spatial, it reaches 62% on both position and task metrics, compared with 20% and 1% for π0.5.

#### Evidence
- [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](../Inbox/2026-06-10--world-pilot-steering-vision-language-action-models-with-world-action-priors.md): World Pilot method, LIBERO-Plus results, and real-robot evaluation summary.
- [APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies](../Inbox/2026-06-10--apt-action-expert-pretraining-improves-instruction-generalization-of-vision-language-action-policies.md): APT two-stage action-expert pretraining and instruction generalization results.

### Test-time language steering with abstention
One paper keeps the robot policy frozen and learns what language to send it during execution. The language feedback policy proposes subtask instructions at replanning time, then an improvement head decides when steering is likely to help. A conformal prediction gate makes the policy fall back to the original instruction when the learned steering looks risky.

The reported gains are large on the settings described in the summary: 24.7% improvement in simulation and 65.0% on Franka hardware for seen environments. The paper also states a false-positive guarantee for harmful steering under the calibration assumptions. The useful detail is the abstention mechanism, since the same summary says bad steering prompts can reduce task success.

#### Evidence
- [Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering](../Inbox/2026-06-10--learning-what-to-say-to-your-vla-mostly-harmless-vision-language-action-model-steering.md): Language feedback policy, conformal abstention gate, and reported simulation and hardware gains.

### One policy across teams and hands
CHORUS fine-tunes one pretrained VLA policy for heterogeneous robot teams. Each robot runs its own copy with only local observations and an identity prompt. The paper reports a 64 percentage point mean success gain over decentralized diffusion policies trained from scratch, and 17/20 successes in a teammate-perturbation handover test versus 9/20 for separate per-robot VLA policies.

InDex adapts a pretrained VLA policy to a high-degree-of-freedom dexterous hand. It keeps the VLA’s arm-level spatial behavior, predicts a scalar grasp intent, and trains a diffusion head for finger-level actions. In robosuite simulation with 100 demonstrations per task, π0.5+InDex reports 85.8% average task success, compared with 50.3% for π0.5 and 42.8% for Diffusion Policy.

#### Evidence
- [CHORUS: Decentralized Multi-Embodiment Collaboration with One VLA Policy](../Inbox/2026-06-10--chorus-decentralized-multi-embodiment-collaboration-with-one-vla-policy.md): CHORUS decentralized multi-robot setup and real-world success comparisons.
- [Bridging the Morphology Gap: Adapting VLA Models to Dexterous Manipulation via Intent-Conditioned Fine-Tuning](../Inbox/2026-06-10--bridging-the-morphology-gap-adapting-vla-models-to-dexterous-manipulation-via-intent-conditioned-fine-tuning.md): InDex intent-conditioned dexterous adaptation method and simulation results.
