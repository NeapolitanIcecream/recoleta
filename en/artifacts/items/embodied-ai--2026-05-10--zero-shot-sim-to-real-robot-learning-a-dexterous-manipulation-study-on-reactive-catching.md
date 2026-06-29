---
source: arxiv
url: https://arxiv.org/abs/2605.09789v1
published_at: '2026-05-10T22:20:20'
authors:
- Kejia Ren
- Gaotian Wang
- Andrew S. Morgan
- Kaiyu Hang
topics:
- sim2real
- dexterous-manipulation
- domain-randomization
- reactive-catching
- reinforcement-learning
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching

## Summary
DRIS trains one policy on a set of randomized simulated object instances that move in parallel under the same action, then deploys the policy on a real robot without fine-tuning. The paper applies this to flat-plate reactive catching, a contact-rich dexterous task with little passive stabilization.

## Problem
- Dynamic dexterous manipulation fails under small errors in contact timing, friction, restitution, object size, and sensing, so simulation-trained policies often do not transfer to real robots.
- Standard domain randomization samples one randomized instance per rollout, which gives the policy limited exposure to how uncertain dynamics evolve during a single action sequence.
- The task matters because flat-plate catching gives the robot no cup, net, or hand shape to hold the ball, so the policy must react fast and control contacts accurately.

## Approach
- The core method is Domain-Randomized Instance Set (DRIS): each simulated episode contains several versions of the object with different physical parameters, and all versions are advanced at the same time with the same robot action.
- The policy receives a fixed-size latent vector from a set encoder, rather than a variable-size list of object states. In the catching case, the encoder is a point-cloud autoencoder extended to 6D ball position and velocity states.
- The reward averages over the instances in the set, so PPO updates favor actions that work across many possible object dynamics instead of one sampled object.
- For catching, the randomized parameters are ball radius, static friction, dynamic friction, and restitution. The action commands plate displacement and plate tilt.
- A FiLM-conditioned policy uses the current plate tilt to modulate the encoded DRIS state before an MLP outputs the next action.

## Results
- The excerpt gives no quantitative success rate, real-robot trial count, or ablation table. It claims reliable zero-shot sim-to-real transfer against conventional domain randomization, but the shown text does not provide the success metric or percentage.
- The abstract claims DRIS can reduce the need for real-world fine-tuning with a modest instance count, giving 10 instances as an example.
- The simulation setup used 128 parallel environments, episodes of up to 20 steps, and 1 second of simulated time per episode.
- The DRIS encoder dataset used 200 balls per DRIS, 50 random-action episodes, and 128,000 recorded DRIS state samples across the 128 environments.
- Encoder training ran for 100 epochs, about 10 minutes; PPO policy training ran for 1000 epochs, about 2 hours.
- The real task uses a flat, low-friction plate rather than a cup, net, or articulated hand, so the claimed transfer result targets a harder catching setup than mechanically stabilized catchers.

## Link
- [https://arxiv.org/abs/2605.09789v1](https://arxiv.org/abs/2605.09789v1)
