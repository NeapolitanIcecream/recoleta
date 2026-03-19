---
source: arxiv
url: http://arxiv.org/abs/2603.04351v1
published_at: '2026-03-04T18:16:58'
authors:
- Valentin Yuryev
- Josie Hughes
topics:
- sim2real
- tendon-driven-robot
- reinforcement-learning
- force-modeling
- transformer
- dexterous-manipulation
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Tendon Force Modeling for Sim2Real Transfer of Reinforcement Learning Policies for Tendon-Driven Robots

## Summary
This paper proposes a data-driven tendon force modeling method for tendon-driven robots, converting the behavior of servo motors that provide only position/encoder signals into more realistic force simulation, thereby improving the sim2real transfer of reinforcement learning policies. The core contribution is a Transformer-based force estimator with temporal context, combined with a contact-aware data collection test bench, which significantly narrows the simulation gap and improves tracking control performance on a real tendon-driven finger.

## Problem
- Tendon-driven robots often use position-controlled servos rather than actuators that can directly measure force/torque, creating a clear sim2real gap between the force-driven simulation required by RL and the real system.
- This gap comes not only from friction, but also from tendon slack, control delay, gear/actuator nonlinearities, and compliant structures; if simulation assumes an “ideal force source,” the trained policy will fail noticeably when deployed.
- This matters because tendon-driven structures are widely used in dexterous hands, soft robots, and compliant interaction systems; without reliable transfer, RL is difficult to use for real-world complex manipulation.

## Approach
- The authors build a general-purpose data collection test bench with a load sensor, connecting a servo motor in series with tendon-driven systems such as springs or fingers, and collect real tendon tension data under both free-motion and contact scenarios.
- They learn a mapping from historical encoder signals to tendon force: the input is the past 1.5 s of commanded position, measured position, and measured velocity, and the output is the current tendon force estimate; they compare three sequential models: MLP, RNN, and Transformer.
- The Transformer encoder uses causal self-attention to process the full history, with the goal of capturing lag, friction, and context-dependent dynamics of slow servos without relying on force sensors at inference time.
- The learned tendon force model is embedded into a GPU-accelerated tendon-force-driven rigid-body simulation, and fingertip pose tracking policies are then trained using PPO and 30% domain randomization.
- Compared with directly using an idealized force model, this pipeline makes actuator behavior in simulation rollouts closer to real hardware, thereby improving RL policy transferability.

## Results
- In cross-system generalization tests, the Transformer achieves an average force prediction RMSE of **0.61 N**, equivalent to **2.9%** of the motor’s maximum force of **21 N**; the abstract further summarizes this as prediction error within **3%** of maximum motor force.
- The authors report that the Transformer generalizes better than both MLP and RNN: the RNN shows noticeable drift and spikes at step changes, while the MLP is more prone to high-frequency oscillations; the Transformer is overall the most robust across the three configurations of weak spring, strong spring, and finger.
- After integrating the learned tendon force model into simulation, the paper claims a **41% reduction in sim-to-real gap** on test trajectories.
- The RL controller trained with this model achieves a **50% improvement** on fingertip pose tracking tasks on a real tendon-driven finger relative to the baseline (described in the paper as a controller trained using an ideal force source / ideal force assumption).
- In terms of data and system scale: about **36 minutes** of real data were collected at **80 Hz**; the model size is about **0.1–0.2 MB**, and it can run inference on a Raspberry Pi 5.
- The excerpt does not provide every itemized value from all experimental tables (for example, comprehensive quantitative comparisons across all contact scenarios and models), but the strongest quantitative conclusions are **2.9% force prediction error, 41% sim2real gap reduction, and 50% real-world tracking improvement**.

## Link
- [http://arxiv.org/abs/2603.04351v1](http://arxiv.org/abs/2603.04351v1)
