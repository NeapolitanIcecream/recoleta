---
source: arxiv
url: http://arxiv.org/abs/2603.04029v1
published_at: '2026-03-04T13:07:42'
authors:
- Fabian Domberg
- Georg Schildbach
topics:
- continual-rl
- world-model
- dreamerv3
- ood-detection
- online-adaptation
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Self-adapting Robotic Agents through Online Continual Reinforcement Learning with World Model Feedback

## Summary
This paper proposes an online continual reinforcement learning framework for robots during deployment: it uses prediction residuals from a world model to automatically detect environmental/dynamics changes, and triggers DreamerV3 finetuning when anomalies are detected. Its goal is to move robots from “fixed parameters after offline training” toward “discovering problems and continually adapting during operation.”

## Problem
- Existing learning-based robot controllers are typically **trained offline and frozen online**, making them prone to failure when faced with unseen dynamics changes, actuator damage, or sim-to-real mismatch.
- The two core challenges in continual reinforcement learning are: **when to detect out-of-distribution changes**, and **how to automatically adapt without human supervision and determine when convergence has occurred**.
- This matters because real robot operating environments keep changing; improving robustness only through larger datasets or randomization will still eventually encounter situations outside the training distribution.

## Approach
- Based on **DreamerV3**: it jointly learns a latent-space world model and a policy, and the policy can be trained on “imagined trajectories,” thereby maintaining relatively high sample efficiency.
- The world model predicts future **n=15** steps of observations and rewards; the discrepancy between predictions and actual outcomes is defined as the **Observation Prediction Residual (OPR)** and **Reward Prediction Residual (RPR)**.
- Threshold detection is performed using rolling means and standard deviations: if OPR or RPR exceeds the mean by **3 standard deviations**, it is treated as an out-of-distribution change and automatically triggers finetuning.
- During finetuning, new data continues to be collected online, and the original DreamerV3 training loop is used to update both the world model and policy; the **12M-parameter** medium configuration is used, with **train ratio=16**, and **data from before the change is not added to the replay buffer for this finetuning**, to avoid interference from the old dynamics.
- Multiple internal/external signals are jointly used to determine whether adaptation is complete: besides OPR/RPR and task reward, the method also monitors declines and stabilization in **dynamics loss, advantage magnitude, value loss** to judge convergence or failure without external supervision.

## Results
- **DMC Walker-walk**: at **5,000 steps**, one joint gear ratio is randomly halved, causing the robot’s reward to drop immediately and RPR to rise; the method quickly detects the change and triggers adaptation, with most metrics returning close to pre-modification levels in **fewer than 10,000 steps** (about **2 minutes** of simulated time); results are reported as the **mean over 10 runs**.
- **ANYmal quadruped robot simulation**: first trained to convergence (**25M steps**), then at **9,000 steps** the speed limits of the three actuators on the rear-right leg are reduced to **1/3** of their original values. After a significant reward drop, the method automatically finetunes and recovers a stable gait in about **5,000 steps** or **4 minutes** on average; the final run ends finetuning at **26,000 steps**; results are reported as the **mean over 9 runs**.
- The ANYmal experiments also show a **failure case**: when metrics remain unstable over the long term and cannot converge, the system eventually aborts adaptation, which the authors claim shows that their multi-metric monitoring can not only trigger learning but also identify non-convergent processes.
- **Real F1Tenth 1:10 model car, sim2real**: first trained in simulation for **10M steps**, then switched to the real vehicle at **10,000 steps** (**20 Hz**). After the switch, OPR spikes and reward drops, and the vehicle becomes more prone to oscillation and wall collisions; behavior then stabilizes over about **10,000 steps** (about **8 minutes** of wall-clock time), and reward recovers to near-simulation level by around **50,000 steps**.
- **Second real-car change**: at about **52,000 steps**, socks are placed over the rear wheels to reduce friction, causing reward to drop by about **20%**. Overall OPR does not change much, but angular velocity prediction shows a significant spike; losses then quickly fall back, and the policy learns to reduce cornering speed, recovering to a slightly lower but stable reward level than before.
- The paper does not provide a systematic numerical comparison table against other CRL/adaptation baselines; the strongest quantitative claim is that the method can **automatically detect changes, trigger online finetuning, and recover performance within thousands to tens of thousands of steps** across multiple continuous-control scenarios, and the authors claim it is the first **fully automatic, continuous-control, open-set CRL** method.

## Link
- [http://arxiv.org/abs/2603.04029v1](http://arxiv.org/abs/2603.04029v1)
