---
kind: trend
trend_doc_id: 171
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
topics:
- robotics
- vision-language-action
- world-models
- cross-embodiment
- tactile-sensing
- medical-robotics
run_id: materialize-outputs
aliases:
- recoleta-trend-171
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/cross-embodiment
- topic/tactile-sensing
- topic/medical-robotics
language_code: en
pass_output_id: 102
pass_kind: trend_synthesis
---

# Robot foundation models are getting grounded in transfer, planning, and contact

## Overview
This day is strongest on one idea: robotics papers are tying broad pretraining, explicit planning, and contact feedback to concrete execution metrics. JoyAI-RA, Cortex 2.0, and Open-H-Embodiment anchor the brief. They report gains on cross-body transfer, long-horizon planning, and medical robotics with results that reach real robots, industrial deployment, or both.

## Clusters

### Cross-embodiment training gets real benchmark wins
Vision-language-action work is getting broader in data and more explicit about how actions transfer across bodies. JoyAI-RA trains one policy on web data, egocentric human video, simulation, and robot trajectories, then maps actions into a shared representation. The reported gains are large on both simulation and a real humanoid benchmark: 90.48% and 89.28% on RoboTwin Easy and Hard, 63.2% on RoboCasa GR1 Tabletop, and 0.74 average success on the AgiBot real-world benchmark versus 0.62 for π0.5. Open-H-Embodiment makes the same scale argument in medical robotics with 770 hours, 20 platforms, and a GR00T-H policy that reaches 25% end-to-end suturing success where ACT, GR00T-N1.6, and LingBot-VA each report 0 out of 20 trials. The day’s strongest evidence says cross-embodiment learning is becoming a concrete training target, not just a claim about generality.

#### Evidence
- [JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy](../Inbox/2026-04-22--joyai-ra-0-1-a-foundation-model-for-robotic-autonomy.md): JoyAI-RA data mix, unified action space, and benchmark gains across simulation and real robot settings
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): Open-H dataset scale and cross-platform medical VLA results with GR00T-H

### Planning over futures moves into deployed robot systems
World models keep showing up where mistakes compound over long horizons. Cortex 2.0 adds latent rollout planning to an industrial VLA stack and scores candidate futures for progress, risk, and completion before acting. The summary claims the best success rates across four deployed warehouse tasks and zero human interventions during evaluation, though the excerpt does not include exact task-by-task numbers. In a tighter safety setting, a TD-MPC2 world-model agent for thrombectomy reaches 58% mean success on held-out simulation anatomies versus 36% for SAC, improves path ratio from 22% to 49%, and keeps max tip force at 0.55 N, well below the paper’s 1.5 N rupture threshold. Medical robotics also joins this line of work through Open-H’s action-conditioned surgical simulator trained across nine platforms.

#### Evidence
- [Cortex 2.0: Grounding World Models in Real-World Industrial Deployment](../Inbox/2026-04-22--cortex-2-0-grounding-world-models-in-real-world-industrial-deployment.md): Industrial world-model planning with deployment-scale data and claimed real-world gains
- [Toward Safe Autonomous Robotic Endovascular Interventions using World Models](../Inbox/2026-04-22--toward-safe-autonomous-robotic-endovascular-interventions-using-world-models.md): World-model RL improves held-out navigation and reports force-based safety numbers
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): Multi-embodiment surgical world model trained across nine platforms

### Compact VLA systems add task structure and confidence signals
Smaller models are getting extra structure before action learning. PokeVLA builds a compact VLA around embodied pretraining, target segmentation from base and wrist views, and geometry alignment during training. The reported gains matter because they hold under transfer and perturbation: +9.7% over OpenVLA-OFT and +20.2% over VLA-Adapter on LIBERO-Plus variations, plus a 20.0% gain under real-world perturbations. A separate paper tackles a different weak point: confidence. Temporal Difference Calibration defines success prediction over whole episodes, trains it with temporal-difference targets, and reports better calibration and early failure detection across OpenVLA, π0, π0-FAST, and UniVLA. It also gives a 15% success-rate lift for OpenVLA on LIBERO when the learned value predictor is used to rank sampled actions. The common thread is that lightweight or black-box VLA systems now get task-specific supervision around perception and reliability, not only bigger backbones.

#### Evidence
- [PokeVLA: Empowering Pocket-Sized Vision-Language-Action Model with Comprehensive World Knowledge Guidance](../Inbox/2026-04-22--pokevla-empowering-pocket-sized-vision-language-action-model-with-comprehensive-world-knowledge-guidance.md): Compact VLA with embodied pretraining, segmentation token, and perturbation robustness gains
- [Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models](../Inbox/2026-04-22--temporal-difference-calibration-in-sequential-tasks-application-to-vision-language-action-models.md): Sequential calibration for VLA policies and reported early-failure detection improvements

### Tactile work gets cheaper to build and faster to train
Contact-rich robotics is pushing sensing quality in two directions at once: better hardware and faster simulation. FingerEye keeps one visual stream active before touch, at contact onset, and after contact with a small fingertip module that costs about $60 in materials. The paper reports six-axis wrench sensitivity and uses the signal for delicate grasping, including contact-aware stopping on fragile objects. ETac attacks the same problem from the training side. It approximates FEM-quality tactile deformation with a fast propagation model plus a small learned residual, reaches 4,096 parallel environments and 869 FPS on one RTX 4090, and trains blind grasping policies that average 84.45% success across four object types. The day’s tactile papers make a practical point: richer contact feedback is becoming easier to build and easier to train on at scale.

#### Evidence
- [FingerEye: Continuous and Unified Vision-Tactile Sensing for Dexterous Manipulation](../Inbox/2026-04-22--fingereye-continuous-and-unified-vision-tactile-sensing-for-dexterous-manipulation.md): Continuous vision-tactile sensing hardware with low cost and contact-onset use in dexterous tasks
- [ETac: A Lightweight and Efficient Tactile Simulation Framework for Learning Dexterous Manipulation](../Inbox/2026-04-22--etac-a-lightweight-and-efficient-tactile-simulation-framework-for-learning-dexterous-manipulation.md): Efficient tactile simulation and large-scale RL throughput for blind grasping
