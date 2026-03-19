---
source: arxiv
url: http://arxiv.org/abs/2603.04351v1
published_at: '2026-03-04T18:16:58'
authors:
- Valentin Yuryev
- Josie Hughes
topics:
- sim2real-transfer
- reinforcement-learning
- tendon-driven-robots
- force-modeling
- transformer
- robot-control
relevance_score: 0.13
run_id: materialize-outputs
language_code: en
---

# Tendon Force Modeling for Sim2Real Transfer of Reinforcement Learning Policies for Tendon-Driven Robots

## Summary
This paper addresses the difficulty of transferring reinforcement learning policies from simulation to real tendon-driven robotic systems by proposing a tendon force learning model based on temporal context. The core contribution is embedding a force estimator that relies only on motor encoder signals into simulation, enabling more realistic training of RL controllers and improving performance on a real robotic finger.

## Problem
- Tendon-driven robots often use position-controlled servo motors, but RL training depends on sufficiently accurate force/torque-driven simulation; in real systems, motor friction, tendon slack, control delay, and compliance create a significant sim-to-real gap.
- Using only ideal force sources or simple friction models cannot capture the complex nonlinear dynamics present in contact-rich manipulation, leading to poor real-world performance of policies learned in simulation.
- This matters because tendon-driven structures are widely used in dexterous hands, soft robots, and compliant interaction systems, while efficient and transferable control remains a bottleneck.

## Approach
- The authors build a general-purpose data collection platform with a load cell, collecting commanded motor position, measured position, velocity, and true tendon force data on both spring systems and a real tendon-driven finger, including contact scenarios.
- Tendon force estimation is formulated as supervised sequence learning: the input is a 1.5-second history window (30 steps, 20Hz) of \(\theta^d, \theta, \dot{\theta}\), and the output is the current tendon force estimate \(\hat F\).
- They compare three model classes: MLP, RNN, and a Transformer encoder; the authors argue that the Transformer better leverages long-term temporal context through self-attention, and therefore better captures lag, friction, and direction-dependent effects in slow servo motors.
- The learned tendon force model is embedded into a GPU-accelerated tendon force-driven rigid-body simulation, and fingertip pose tracking policies are then trained using PPO and domain randomization over a 30% range.
- At inference time, no force sensor is needed; the method relies only on motor encoder signals, making it robot-agnostic and easier to deploy.

## Results
- In the overall comparison across three systems—weak spring, strong spring, and finger—the Transformer achieves an average RMSE of **0.61 N**, about **2.9%** of the motor's maximum force of **21 N**; the paper states it outperforms the RNN and shows better cross-system generalization than the MLP.
- The abstract claims that this Transformer-based force model keeps tendon force prediction error within **3% of the maximum motor force** and is applicable across different robotic systems.
- After integrating the learned force model into simulation, the authors report a **41% reduction in sim-to-real gap** on test trajectories; the excerpt does not provide a more detailed definition of the trajectory metric or full tables.
- The RL controller trained with this model achieves a **50% improvement** on fingertip pose tracking tasks on a real tendon-driven robotic finger compared with a baseline controller trained using an ideal force source estimate.
- The paper also qualitatively notes that the RNN exhibits noticeable drift and force spikes at step changes during testing; the MLP is more prone to high-frequency oscillations under input perturbations; the Transformer is the most robust across different systems and contact conditions.
- Because the provided content is truncated, more fine-grained quantitative results for contact-rich scenarios are not fully shown.

## Link
- [http://arxiv.org/abs/2603.04351v1](http://arxiv.org/abs/2603.04351v1)
