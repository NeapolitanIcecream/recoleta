---
source: arxiv
url: http://arxiv.org/abs/2603.04029v1
published_at: '2026-03-04T13:07:42'
authors:
- Fabian Domberg
- Georg Schildbach
topics:
- continual-reinforcement-learning
- model-based-rl
- robot-adaptation
- world-models
- out-of-distribution-detection
relevance_score: 0.32
run_id: materialize-outputs
language_code: en
---

# Self-adapting Robotic Agents through Online Continual Reinforcement Learning with World Model Feedback

## Summary
This paper proposes a framework that enables robots to **automatically detect environmental/body changes and continue learning online even after deployment**. The core idea is to use the world model's prediction error to trigger DreamerV3 finetuning. The authors show on continuous control tasks, quadruped robot simulation, and a real small vehicle that the method can recover performance without external supervision.

## Problem
- Traditional learning-based robots are typically **trained offline and deployed with fixed parameters**. Once they encounter unseen dynamics changes, actuator failures, or sim-to-real shifts, performance can degrade significantly.
- There are two key challenges in continual reinforcement learning: **when to detect a change**, and **how to automatically adapt during operation**, without relying on manually labeled task boundaries.
- This matters because real robots inevitably encounter **out-of-distribution events** during long-term operation; without self-adaptation, both system robustness and autonomy are limited.

## Approach
- Built on **DreamerV3**: it jointly learns a **world model** in latent space and a policy, with the policy trained mainly on trajectories “imagined” by the world model, improving sample efficiency.
- During deployment, it continuously performs **n=15**-step future prediction and computes **observation prediction residual (OPR)** and **reward prediction residual (RPR)**. If either metric exceeds the rolling mean by **3 standard deviations**, the system judges that an out-of-distribution change has occurred.
- Once a change is detected, it uses DreamerV3's original training loop to finetune the world model and policy online; the implementation uses the **12M-parameter** medium configuration with **train ratio=16**.
- To **automatically determine whether adaptation is complete**, it monitors not only task-level reward/residuals but also internal training signals: whether **dynamics loss, advantage magnitude, and value loss** tend toward stable convergence.
- During finetuning, **data from before the change is not added to the replay buffer**, avoiding interference from old dynamics when learning the new situation.

## Results
- **DMC Walker-walk**: at **5,000 steps**, the gear ratio of one joint is randomly halved; reward drops immediately and RPR rises. The method quickly detects this and starts adaptation, and after **fewer than 10,000 steps** (about **2 minutes** of simulation time), most metrics return to near their pre-change levels; results are based on the **mean over 10 runs**.
- **ANYmal quadruped robot (Isaac Lab)**: first trained for **25M steps**, then at **9,000 steps** the velocity limits of the 3 actuators in the rear-right leg are reduced to **1/3** of their original values. On average, the method recovers a stable gait after about **5,000 steps** (about **4 minutes**), and the last run stops finetuning at **26,000 steps**; results are based on the **mean over 9 runs**.
- **Real F1Tenth 1:10 vehicle, sim-to-real**: pretrained in simulation for **10M steps**; after switching to the real car at **10,000 steps**, OPR spikes and reward drops. After about **10,000 steps** of online finetuning (about **8 minutes**), behavior becomes stable, and by about **50,000 steps** reward recovers to near the simulation level.
- **Real vehicle friction change**: at about **52,000 steps**, socks are placed over the rear wheels to reduce friction, causing reward to drop by about **20%**. The system enters adaptation again, losses fall back quickly, and it ultimately learns to take turns at a **slightly lower speed** to avoid slipping, though total reward remains slightly below the pre-change level as a result.
- The paper also presents a **failure case**: when multiple metrics remain unstable, the system can identify the situation as **not converged** and terminate adaptation; this supports its claim of “automatically assessing adaptation success or failure.”
- The paper does not provide a **unified numerical comparison table** against other CRL/MBRL methods or standard benchmark SOTA metrics; the strongest evidence is mainly the recovery time, number of steps, and performance recovery behavior demonstrated across the above simulation and real-world systems.

## Link
- [http://arxiv.org/abs/2603.04029v1](http://arxiv.org/abs/2603.04029v1)
