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
- world-models
- autonomous-driving
- reinforcement-learning
- rssm
- kinematics-aware
- sample-efficiency
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# Kinematics-Aware Latent World Models for Data-Efficient Autonomous Driving

## Summary
This paper proposes a kinematics-aware latent world model for autonomous driving, explicitly injecting vehicle physical states and geometric supervision into the Dreamer/RSSM framework to improve data efficiency and long-horizon imagination quality. Its core value is making latent dynamics better align with the spatial structure and physical motion in driving, rather than merely reconstructing pixels.

## Problem
- Reinforcement learning for autonomous driving is costly in terms of data, and real-world interaction carries safety risks, while purely model-free methods usually require a large number of environment steps to converge.
- Although existing pixel-driven world models can perform imagination in latent space, they often lack explicit constraints on key driving structure such as lane geometry and the relative motion of surrounding vehicles.
- This can lead to unstable long-horizon prediction and latent representations that lack physical interpretability, which in turn affects closed-loop control and policy optimization.

## Approach
- At the observation encoding stage of the RSSM world model, front-view camera images are fused with 5-dimensional vehicle physical quantities, including speed, steering angle, previous action, and yaw rate, so that the latent state is directly anchored to real kinematic information.
- In addition to the basic reconstruction, reward, and termination prediction objectives, two auxiliary supervision heads used only during training are added: a lane-geometry head that predicts left/right lane-boundary distances and heading differences, and a neighboring-vehicle head that predicts the relative position and velocity states of up to 3 surrounding vehicles (12 dimensions).
- These geometry- and interaction-related auxiliary losses are used to regularize the RSSM latent state, enabling it to learn spatial semantics more critical for driving decisions rather than focusing only on pixel reconstruction.
- The method then follows DreamerV3-style imagined-trajectory actor-critic learning, performing H=15-step rollout in latent space and training the policy and value function with \(\lambda\)-return, thereby reducing the need for real-environment interaction.

## Results
- In MetaDrive simulation, the authors claim their method can reach a stable high return close to **200 return** within **80,000 real interaction steps**; in contrast, **PPO** requires **300,000 steps**, and its final convergence level is **below 150**.
- Ablation results show that moving from **ImgOnly** to **Img+Head** with lane/surrounding-vehicle supervision increases mean return (MR) from **176.5** to **193.6**, and success rate (SR) from **0.17** to **0.33**; the paper summarizes this as an MR improvement of about **9.7%** and an SR improvement of **16 percentage points**.
- The full model **Img+Head+Phys** achieves the best result: **MR = 217.2, SR = 0.49**; this is a further improvement of about **12.2%** over **Img+Head**, and a total improvement of about **23.1%** over **ImgOnly**.
- Removing the reward/termination heads (while still retaining image input, physical input, and lane/neigh supervision) reduces performance to **MR = 172.6, SR = 0.18**, indicating that these basic prediction heads are also critical for stable learning.
- For qualitative results, the authors claim the full model produces more stable and more physically consistent imagined trajectories than the image-only model, and better preserves semantics such as the position of the leading vehicle and lane-line color/type; however, this part is mainly illustrated through figures and does not provide additional quantitative metrics.

## Link
- [http://arxiv.org/abs/2603.07264v1](http://arxiv.org/abs/2603.07264v1)
