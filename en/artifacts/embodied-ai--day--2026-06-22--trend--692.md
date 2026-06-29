---
kind: trend
trend_doc_id: 692
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
topics:
- robotics
- vision-language-action models
- reinforcement learning
- robot safety
- world models
- human demonstrations
- shared autonomy
run_id: materialize-outputs
aliases:
- recoleta-trend-692
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/robot-safety
- topic/world-models
- topic/human-demonstrations
- topic/shared-autonomy
language_code: en
pass_output_id: 306
pass_kind: trend_synthesis
---

# Robot VLA research is targeting closed-loop reliability under contact, safety limits, and scarce demonstrations

## Overview
Robot vision-language-action (VLA) work in this period centers on reliability after deployment. dVLA-RL, LIBERO-Safety, and LaST-HD show the main pressure points: task reward optimization, safety-constrained evaluation, and cheaper human-sourced data for contact-rich manipulation.

## Clusters

### Closed-loop VLA training
Several papers treat supervised imitation as an incomplete training signal for robot policies. dVLA-RL applies proximal policy optimization (PPO) to the sampled denoising path of a discrete diffusion VLA, which gives the policy a usable likelihood during multi-step action generation. It reports 99.7% average success on LIBERO and raises an MM-ACT backbone on RoboTwin 2.0 from 61.4% to 92.0% average success.

Flatness Preserves Instruction Following attacks a different failure mode: small robot datasets can make a VLA ignore changed language instructions. Adding sharpness-aware minimization (SAM) during finetuning improves counterfactual instruction following without new data, including 47.8% success on LIBERO-CF compared with 13.2% for the default π0.5 finetune. RECALL adds a deployment loop: collect recovery demonstrations at high-uncertainty states, then train with replay to avoid forgetting. Its strongest setting reaches 72.4% overall LIBERO-10 success, compared with 60.2% for matched passive collection.

#### Evidence
- [dVLA-RL: Reinforcement Learning over Denoising Trajectories for Discrete Diffusion Vision-Language-Action Models](../Inbox/2026-06-22--dvla-rl-reinforcement-learning-over-denoising-trajectories-for-discrete-diffusion-vision-language-action-models.md): dVLA-RL method and reported LIBERO/RoboTwin gains
- [Flatness Preserves Instruction Following in Vision-Language-Action Models](../Inbox/2026-06-22--flatness-preserves-instruction-following-in-vision-language-action-models.md): SAM finetuning results for instruction following
- [RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models](../Inbox/2026-06-22--recall-recovery-experience-collection-for-active-lifelong-learning-in-vision-language-action-models.md): Uncertainty-guided recovery data and replay results

### Human data for contact-rich manipulation
Data collection is a major bottleneck in these robotics papers, so several systems put humans back into the loop in more selective ways. LaST-HD uses human-hand demonstrations, a motion-capture glove, and latent dynamics alignment to train robot policies across grippers and dexterous hands. It reports 0.73 average success across six real-world tasks and says the glove collects data 4–5× faster than robot teleoperation.

Assistron keeps a VLA frozen and asks for joystick help near contact-heavy moments such as grasping and release. In a novice-user assistive manipulation benchmark, it reaches 91.3% partial success while running autonomously for 43.5% of the task time. CoorDex shows a simulation-side version of the same contact problem for humanoids: separate body and hand priors make moving grasp tasks trainable, while direct joint-space PPO fails in the reported WalkGrab ablations.

#### Evidence
- [LaST-HD: Learning Latent Physical Reasoning from Scalable Human Data for Robot Manipulation](../Inbox/2026-06-22--last-hd-learning-latent-physical-reasoning-from-scalable-human-data-for-robot-manipulation.md): LaST-HD human-hand data, glove pipeline, and real-world success results
- [Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models](../Inbox/2026-06-22--assistron-bayesian-shared-autonomy-with-off-the-shelf-vision-language-action-models.md): Assistron shared-autonomy design and novice-user benchmark results
- [CoorDex: Coordinating Body and Hand Priors for Continuous Dexterous Humanoid Loco-Manipulation](../Inbox/2026-06-22--coordex-coordinating-body-and-hand-priors-for-continuous-dexterous-humanoid-loco-manipulation.md): CoorDex body/hand priors and loco-manipulation ablations

### Safety and world-model checks
The safety work is becoming more concrete. LIBERO-Safety adds 75 tasks across physical and semantic safety suites, with 19,664 human-screened collision-free demonstrations. The benchmark shows strong task policies still break under hard safety settings: OpenVLA-OFT falls to 1.3% success on AAG-L2, and π0.5 reaches only 35.3% on the same hard affordance-aware grasping level.

IOI addresses simulated rollouts by injecting exact robot kinematics into an action-conditioned video model. On RoboTwin, it reports the best overall SSIM, LPIPS, and FVD among the listed baselines, with FVD 41.23 compared with 126.20 for IRASim and 64.90 for Ctrl-World. A separate watermarking paper adds an ownership angle for deployed VLA and world-action model services: with 16 audit rollouts, it reports true positive rate 1.00 at 1% false positive rate across four policy-robot combinations.

#### Evidence
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety benchmark scale and safety evaluation results
- [IOI: Decoupling Kinematics and Physics for Interactive World Models](../Inbox/2026-06-22--ioi-decoupling-kinematics-and-physics-for-interactive-world-models.md): IOI kinematics-guided world model and RoboTwin metrics
- [A Watermark for Vision-Language-Action and World Action Models](../Inbox/2026-06-22--a-watermark-for-vision-language-action-and-world-action-models.md): Latent-noise watermarking method and audit results

### Medical and aerial control use VLA-style training selectively
The period also includes domain-specific autonomy papers that borrow pieces of the VLA recipe. BiliVLA trains an endoscopic navigation policy to output target category, bounding box, and motor command for ERCP phantom tasks. Its two-stage training uses supervised tuning followed by group relative policy optimization (GRPO), raising success to 84.85% compared with 58.86% for EndoVLA in the reported total results.

SkyJEPA focuses on quadrotors rather than language-conditioned manipulation. It trains a latent world model for long-horizon prediction, then maps predicted latents back to metric state variables for sampling-based control. The available excerpt gives method details and claims outdoor closed-loop tests, but it does not provide metric values, so the grounded takeaway is narrower: latent prediction is being paired with physics-shaped readouts for real-time control.

#### Evidence
- [BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation](../Inbox/2026-06-22--bilivla-scene-aware-vision-language-action-model-with-reinforcement-learning-for-autonomous-biliary-endoscopic-navigation.md): BiliVLA training setup and ERCP phantom results
- [SkyJEPA: Learning Long-Horizon World Models for Zero-Shot Sim-to-Real Control of Quadrotors](../Inbox/2026-06-22--skyjepa-learning-long-horizon-world-models-for-zero-shot-sim-to-real-control-of-quadrotors.md): SkyJEPA latent world model design and limits of available reported metrics
