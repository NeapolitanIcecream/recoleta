---
kind: trend
trend_doc_id: 326
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
topics:
- robotics
- VLA
- failure recovery
- long-horizon planning
- world models
- sim-to-real
- embodied datasets
run_id: materialize-outputs
aliases:
- recoleta-trend-326
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/failure-recovery
- topic/long-horizon-planning
- topic/world-models
- topic/sim-to-real
- topic/embodied-datasets
language_code: en
pass_output_id: 142
pass_kind: trend_synthesis
---

# Robot papers target failure recovery, domain data, and action-conditioned prediction

## Overview
Robotics work in this period treats reliability as a measured control problem. Vision-Language-Action (VLA) policies get recovery training, uncertainty-triggered search, and store-specific action data. RePO-VLA, CAPS, and SABER give the strongest quantitative signal.

## Findings

### VLA failure recovery and long-horizon control
Two papers attack execution drift directly. RePO-VLA trains on success, failure, and recovery rollouts with separate labels, then deploys with a fixed high value condition and no online failure detector. Its reported adversarial success rises from 20% to 75% on average, with FRBench-Sim covering 23,453 bimanual episodes across 46 tasks.

CAPS keeps the base VLA policy unchanged and spends extra inference only when uncertainty rises. It samples future action chunks with a power distribution and uses Metropolis-Hastings search when entropy crosses a threshold. On RoboTwin 1.0 with π0, average success is 47.4%, compared with 32.2% for π0 and 41.3% for π0 plus TACO. On Simpler-WindowX, it reports 60.5% average success, ahead of π0 and several VLA baselines.

#### Sources
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): RePO-VLA method, FRBench-Sim scale, and adversarial success figures.
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): CAPS inference-time search method and benchmark results on RoboTwin and Simpler-WindowX.

### Domain-specific action data for real environments
SABER shows the data problem in retail robotics with concrete numbers. The dataset uses about 100 hours of grocery-store capture and converts human activity into 44.8K training samples: 25K latent-action sequences, 18.6K hand-pose trajectories, and 1.2K whole-body motion sequences. Post-training GR00T N1.6 on these streams reaches 29.3% mean success across 10 RoboBenchMart tasks, compared with 13.4% for simulation-only fine-tuning.

DRIS addresses a different data gap in dexterous sim-to-real transfer. Each simulated episode contains several object instances with varied dynamics, all advanced under the same robot action. The paper claims zero-shot real transfer for flat-plate reactive catching, but the available excerpt does not provide a real-trial success rate, so the evidence is stronger for the training design than for the deployment result.

#### Sources
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): SABER dataset composition and RoboBenchMart success comparison.
- [Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching](../Inbox/2026-05-10--zero-shot-sim-to-real-robot-learning-a-dexterous-manipulation-study-on-reactive-catching.md): DRIS training setup and limits of the visible quantitative evidence.

### World models built for action rollout
World-model papers focus on prediction that can guide control. Sub-JEPA regularizes latent spaces through low-dimensional Gaussian tests instead of forcing the whole latent vector into an isotropic Gaussian. Against LeWorldModel, it improves planning success on all four reported tasks, including Two-Room at 95.00±2.76% and OGB-Cube at 76.33±5.99%.

DeformMaster tackles ropes, cloths, packages, and soft toys with a physics-neural model learned from real videos. It rolls material particles forward with differentiable MPM, adds bounded neural velocity correction, and renders new action rollouts with Gaussian Splatting. On 20 real PhysTwin sequences, it reports IoU 0.748, Chamfer 0.011, PSNR 25.41, and online interactive rollout above 15 fps.

#### Sources
- [Sub-JEPA: Subspace Gaussian Regularization for Stable End-to-End World Models](../Inbox/2026-05-10--sub-jepa-subspace-gaussian-regularization-for-stable-end-to-end-world-models.md): Sub-JEPA regularization method and planning success results.
- [DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos](../Inbox/2026-05-10--deformmaster-an-interactive-physics-neural-world-model-for-deformable-objects-from-videos.md): DeformMaster action-conditioned deformable-object model and evaluation metrics.
