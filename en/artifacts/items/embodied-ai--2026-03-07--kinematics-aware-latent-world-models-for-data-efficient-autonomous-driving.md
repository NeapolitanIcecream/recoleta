---
source: arxiv
url: http://arxiv.org/abs/2603.07264v1
published_at: '2026-03-07T15:47:54'
authors:
- Jiazhuo Li
- Linjiang Cao
- Qi Liu
- Xi Xiong
topics:
- autonomous-driving
- world-model
- rssm
- model-based-rl
- kinematics-aware
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Kinematics-Aware Latent World Models for Data-Efficient Autonomous Driving

## Summary
This paper proposes a kinematics-aware latent world model for autonomous driving, explicitly injecting vehicle physical states and geometric supervision into a Dreamer/RSSM-style world model to improve data efficiency and long-horizon imagination quality. The core idea is to make the latent state not only reconstruct pixels, but also encode lane and neighboring-vehicle structure that is critical for driving decisions.

## Problem
- Reinforcement learning for autonomous driving is data-expensive, and real-world interaction carries safety risks, while purely model-free methods typically require a large number of environment steps to converge.
- Although existing pixel-driven world models can perform imagination in latent space, they often lack explicit constraints on spatial geometry and vehicle kinematics, leading to unstable long-horizon prediction and insufficient physical consistency.
- This matters because closed-loop driving decisions depend on accurate representations of lane boundaries, relative heading, neighboring vehicle positions, and speeds, while these key signals occupy only a small portion of the image.

## Approach
- Build the world model based on RSSM/DreamerV3: input a front-view camera image and 5-dimensional vehicle physical variables (speed, steering angle, action history, yaw rate), encode them separately with a CNN and MLP, then concatenate them into an observation embedding.
- Use RSSM to learn latent dynamics, simultaneously predicting reconstruction, reward, and continuation signals in latent space, and train an actor-critic policy through imagined trajectories without interacting with the real environment at every step.
- Add a lane supervision head to predict left/right lane-boundary distances and relative lane heading angle; add a neighboring-vehicle supervision head to predict the relative positions and relative velocities of up to 3 surrounding vehicles.
- These auxiliary heads are used only during training, and their gradients regularize the latent state through backpropagation, making the latent representation better match geometric structure and interaction semantics rather than optimizing only for pixel reconstruction.

## Results
- In MetaDrive simulation, the authors' method reaches a stable high return close to **200 return** within **80,000 real interaction steps**; by comparison, PPO requires **300,000 steps**, and its convergence level is still **below 150**.
- In the ablation study, **ImgOnly** achieves **176.5 / 0.17** average return/success rate; after adding lane and neighboring-vehicle supervision (**Img+Head**), this improves to **193.6 / 0.33**, i.e., about a **9.7%** gain in average return and a **16 percentage point** increase in success rate.
- The full model **Img+Head+Phys** reaches **217.2 / 0.49**; this is about a **12.2%** further gain in average return over **Img+Head**, and about a **23.1%** total gain over **ImgOnly**.
- When the reward/continuation heads are removed but physical inputs and geometric heads are retained, performance drops to **172.6 / 0.18**, showing that reward and termination modeling are also critical for policy learning.
- Qualitative results show that **ImgOnly** produces blurry neighboring-vehicle positions and incorrect lane-line types; the full model generates more stable, physically plausible imagined trajectories and better preserves neighboring-vehicle and lane semantics.

## Link
- [http://arxiv.org/abs/2603.07264v1](http://arxiv.org/abs/2603.07264v1)
