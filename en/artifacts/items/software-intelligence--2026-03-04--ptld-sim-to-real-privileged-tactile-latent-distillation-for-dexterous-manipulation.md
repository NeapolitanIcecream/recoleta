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
- robot-learning
- dexterous-manipulation
- tactile-sensing
- sim-to-real
- privileged-distillation
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# PTLD: Sim-to-real Privileged Tactile Latent Distillation for Dexterous Manipulation

## Summary
PTLD proposes a dexterous manipulation learning method that does not require explicitly simulating tactile sensors in simulation. It first trains a strong policy in simulation using “privileged sensors,” then distills that policy’s latent representation onto a tactile encoder in the real world, enabling stronger tactile manipulation.

## Problem
- The paper addresses the challenge that **tactile control for multi-fingered dexterous hands is difficult to train**: demonstration data is expensive, while tactile simulation is both slow and unrealistic, which limits traditional imitation learning and end-to-end tactile RL.
- This matters because contact-rich tasks in household and service robotics, such as in-hand rotation, reorientation, and tool use, require stronger state awareness than proprioception alone can provide.
- Existing zero-shot sim-to-real methods usually fall back to proprioception-only “blind manipulation” policies, whose performance ceiling is limited, especially for slip, mass variation, and complex reorientation tasks.

## Approach
- The core mechanism is simple: **instead of simulating touch, train a strong teacher in simulation that can see more information, run it on the real robot, and then let a tactile student imitate the teacher’s internal latent representation.**
- In simulation, the authors train the policy with **Asymmetric Actor-Critic + PPO**: the critic sees privileged state, the actor sees only deployable observations, and an online latent distillation loss is added so the actor encoder learns to approximate the privileged representation.
- In the real world, the authors build a “privileged sensor” setup with **4 RGB-D cameras + Aruco markers**, obtaining highly observable information such as object pose, which allows the privileged policy to be deployed in practice and **tactile observation–privileged latent** paired data to be collected.
- They then train a tactile encoder with supervised learning: the input includes **18 Xela uSkin tactile pads on the Allegro hand, totaling 368 taxels with 3-axis raw signals**, along with relevant positional information, and the output is matched to the teacher latent; to reduce distribution shift in offline distillation, they also use **DAgger** for iterative data aggregation.
- For the tasks, the rotation task uses **0.5 seconds, 100Hz** of tactile history plus a 1D temporal convolution encoder; the reorientation task uses a **causal Transformer** encoder combining touch, joint proprioception, target pose, and latent history.

## Results
- On the **in-hand rotation** benchmark, PTLD achieves a **182% improvement** over a **proprioception-only policy**; the abstract does not provide absolute scores, but clearly claims that adding touch significantly improves rotation performance.
- On the more challenging **tactile in-hand reorientation** task, PTLD improves the **number of goals reached** by **57%** compared with using proprioception alone.
- The figure captions and abstract also claim that, in in-hand rotation, PTLD is more robust to **object slip, mass variation, and wrist orientation changes**; however, the excerpt does not provide the full quantitative tables for these robustness experiments.
- The paper also claims that the reorientation task **cannot be learned in simulation using proprioceptive history alone**, while PTLD can learn it, indicating that tactile distillation breaks through the capability ceiling of purely proprioceptive policies.
- Regarding the training method, the authors claim that their **single-stage AAC + online latent distillation** achieves **comparable performance** in simulation evaluation to traditional two-stage privileged latent distillation, but the excerpt does not provide specific numbers.

## Link
- [http://arxiv.org/abs/2603.04531v1](http://arxiv.org/abs/2603.04531v1)
