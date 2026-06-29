---
source: arxiv
url: http://arxiv.org/abs/2604.08780v1
published_at: '2026-04-09T21:31:24'
authors:
- Mohamad H. Danesh
- Chenhao Li
- Amin Abyaneh
- Anas Houssaini
- Kirsty Ellis
- Glen Berseth
- Marco Hutter
- Hsiu-Chin Lin
topics:
- world-model
- quadruped-locomotion
- morphology-conditioning
- zero-shot-transfer
- sim-to-real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning

## Summary
This paper proposes a quadrupedal world model that conditions dynamics on a robot's morphology taken from its USD description. The goal is zero-shot transfer across different quadruped bodies without online adaptation, warm-up, or retraining.

## Problem
- Standard robot world models are tied to one hardware setup, so a model trained on one quadruped can fail on another with different limb lengths, mass distribution, or actuator limits.
- Many transfer methods treat morphology as a hidden variable inferred from motion history. That creates an adaptation delay at the start of deployment and can hurt safety and control quality.
- Training a separate model for each robot is expensive and blocks scaling to heterogeneous robot fleets.

## Approach
- The method builds on DreamerV3 and adds explicit morphology conditioning to the world model, calling the system a Quadrupedal World Model (QWM).
- A Physical Morphology Encoder extracts a normalized feature vector from the robot's USD file. The features include leg segment lengths, knee configuration, stance geometry, total mass, trunk-mass ratio, and actuator torque density.
- The model uses a dual-tower encoder: one tower processes proprioceptive observations and one processes the static morphology vector, then fuses them before latent state inference.
- The recurrent dynamics are also conditioned on morphology at every step, so the latent state does not need to infer static body properties from interaction history.
- An Adaptive Reward Normalization module rescales rewards per robot using EMA-tracked 5th and 95th return percentiles to keep robots with larger reward magnitudes from dominating training.

## Results
- The paper claims this is the first world model for locomotion that enables zero-shot generalization to unseen quadruped morphologies within the quadrupedal family.
- It claims deployment on entirely unseen quadrupeds without fine-tuning, adaptation, or warm-up, in both simulation and real robot settings.
- The excerpt does not provide benchmark tables or final task metrics, so no direct success rate, return, or baseline comparison numbers are available here.
- The text gives concrete reward-scale examples that motivate normalization: Spot converges around 350 mean reward, ANYmal variants around 25, Unitree A1/Go1/Go2 around 40, and Unitree B2 around 15.
- The method is described as distribution-bounded: it interpolates within the trained quadrupedal morphology family rather than acting as a universal physics engine.

## Link
- [http://arxiv.org/abs/2604.08780v1](http://arxiv.org/abs/2604.08780v1)
