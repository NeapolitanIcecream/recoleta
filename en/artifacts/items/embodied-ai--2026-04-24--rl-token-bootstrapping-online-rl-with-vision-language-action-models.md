---
source: arxiv
url: http://arxiv.org/abs/2604.23073v1
published_at: '2026-04-24T23:57:45'
authors:
- Charles Xu
- Jost Tobias Springenberg
- Michael Equi
- Ali Amin
- Adnan Esmail
- Sergey Levine
- Liyiming Ke
topics:
- vision-language-action
- online-reinforcement-learning
- real-robot-manipulation
- sample-efficient-rl
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# RL Token: Bootstrapping Online RL with Vision-Language-Action Models

## Summary
RLT fine-tunes a pretrained vision-language-action model on real robots with online reinforcement learning by exposing a compact "RL token" and training a small actor-critic on top of it. The method aims to keep the VLA's general skills while improving task-specific precision and speed within minutes to a few hours of robot practice.

## Problem
- Pretrained VLA models can do many manipulation tasks, but they often fail in the last millimeter of precise execution, where small errors, pauses, and retries cause slowdowns or failures.
- Full RL fine-tuning of large VLA models is too expensive and sample-inefficient for real-world robot training, where only a few hours of interaction may be available.
- Small real-world RL policies can adapt quickly, but they usually give up the VLA's strong visual and behavioral prior.

## Approach
- The paper adds an **RL token** to a frozen pretrained VLA. This token is a compact vector learned to reconstruct the VLA's internal embeddings, so it keeps task-relevant information in a small state representation for RL.
- After a small amount of task-specific demonstration adaptation, the VLA and RL-token module are frozen. Online learning updates only a lightweight actor and critic.
- The actor does not plan actions from scratch. It takes the RL token, robot proprioception, and a **reference action chunk** sampled from the VLA, then learns to adjust that chunk.
- The critic is trained off-policy on chunked actions with sparse binary success labels, which shortens the decision horizon compared with single-step control.
- A regularization term keeps the actor close to the VLA action, and **reference action dropout** prevents the actor from copying the VLA without learning.

## Results
- On **four real-robot precision tasks**—**screw installation, zip tie fastening, charger insertion, and Ethernet insertion**—the method improves both success rate and execution speed after **minutes to a few hours** of online practice.
- On the hardest task phase, RLT improves execution speed by **up to 3×**.
- For a challenging **screw insertion** setting, success rate improves from **20% to 65%**.
- The paper claims that on one of the most dexterous task segments, the learned policy can **surpass expert human teleoperation speed** while keeping reliability.
- The excerpt does not provide a full table of per-task metrics, dataset sizes, or detailed baseline-by-baseline numbers beyond the examples above.

## Link
- [http://arxiv.org/abs/2604.23073v1](http://arxiv.org/abs/2604.23073v1)
