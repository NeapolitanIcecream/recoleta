---
source: arxiv
url: http://arxiv.org/abs/2603.04531v1
published_at: '2026-03-04T19:17:42'
authors:
- Rosy Chen
- Mustafa Mukadam
- Michael Kaess
- Tingfan Wu
- Francois R Hogan
- Jitendra Malik
- Akash Sharma
topics:
- dexterous-manipulation
- sim-to-real
- tactile-learning
- privileged-distillation
- asymmetric-actor-critic
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# PTLD: Sim-to-real Privileged Tactile Latent Distillation for Dexterous Manipulation

## Summary
PTLD proposes a method for learning dexterous manipulation without modeling tactile sensors in simulation. It first runs a policy with “privileged sensors” in simulation/the real world, and then distills its latent variables into a tactile policy that can be deployed in the real world. It targets the difficult problem of tactile dexterous manipulation with multi-fingered hands, where teaching is hard and performance depends heavily on contact sensing.

## Problem
- Target problem: learning tactile dexterous manipulation policies for multi-fingered hands, especially **in-hand rotation** and the more difficult **in-hand reorientation**.
- Importance: these contact-rich tasks are critical for robotic capabilities in households, tool use, and related settings, but high-quality demonstrations are hard to obtain, especially because teleoperation/teaching for multi-fingered hands is extremely costly.
- Core bottleneck: pure RL can learn in simulation, but **tactile simulation is both slow and unrealistic**, making tactile policies hard to transfer directly via sim-to-real; meanwhile, “blind” policies that rely only on proprioception have limited performance ceilings.

## Approach
- First train a strong policy in simulation that uses **privileged sensors** (such as highly observable information like object pose and shape), rather than simulating touch itself.
- Use **Asymmetric Actor-Critic + online latent distillation** to simplify the traditional two-stage privileged distillation setup: the critic sees privileged state, the actor sees only deployable observations, and latent alignment is used to learn better representations.
- Build a **privileged sensor system** in the real world with 4 cameras and object markers, deploy the privileged policy to collect data, and record both real tactile signals and policy latents.
- Then use supervised learning to distill the “privileged policy latents” into an encoder that takes **tactile + proprioception** as input, yielding a tactile policy that can be deployed in the real world.
- To mitigate distribution shift in offline distillation, the authors use **DAgger-style iterative data aggregation**, collecting more on-policy data with intermediate tactile encoders for continued training.

## Results
- On the **in-hand rotation** benchmark task, PTLD delivers a **182% improvement** over a **proprioception-only policy** (explicitly stated in the abstract, though the excerpt does not provide absolute scores, dataset size, or variance).
- On the more difficult **tactile in-hand reorientation** task, PTLD improves the **number of goals reached** by **57%** relative to using proprioception alone.
- The authors claim PTLD is more robust on the rotation task to **object slip, mass changes, and wrist orientation changes**, but the excerpt does not include full quantitative tables for these robustness experiments.
- The paper also claims its tactile policy outperforms not only proprioceptive policies but also **adaptation-based tactile policies**; however, the current excerpt does not provide specific numerical comparisons.
- At the method level, the authors claim the single-stage **AAC + online latent distillation** performs similarly to traditional two-stage privileged latent distillation in simulation evaluation while making training simpler; the excerpt does not provide detailed numbers.

## Link
- [http://arxiv.org/abs/2603.04531v1](http://arxiv.org/abs/2603.04531v1)
