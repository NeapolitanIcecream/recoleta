---
source: arxiv
url: http://arxiv.org/abs/2603.14392v1
published_at: '2026-03-15T14:12:43'
authors:
- Yuchen Wang
- Jiangtao Kong
- Sizhe Wei
- Xiaochang Li
- Haohong Lin
- Hongjue Zhao
- Tianyi Zhou
- Lu Gan
- Huajie Shao
topics:
- world-model
- trajectory-prediction
- mixture-of-experts
- robot-morphology
- scalable-pretraining
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# WestWorld: A Knowledge-Encoded Scalable Trajectory World Model for Diverse Robotic Systems

## Summary
WestWorld proposes a scalable trajectory world model for jointly learning dynamics across a wide variety of robotic systems, while explicitly encoding knowledge of robot morphological structure. Its core contribution is combining the ideas that “different robots should use different dynamics submodules” and “robot structural priors matter,” in order to improve zero-shot, few-shot, and downstream control performance.

## Problem
- Existing multi-robot trajectory world models typically force all systems into a single shared dense model. As the number of robot types grows, this easily leads to gradient conflicts and negative transfer, resulting in poor scalability.
- Different robots differ in sensor/actuator dimensions and sampling frequencies, as well as in morphological and kinematic structure, making shared representations difficult to learn well.
- Many methods treat trajectories only as token sequences and ignore the physical prior of robot morphological structure, leading to weak zero-shot generalization to unseen robots.

## Approach
- The authors propose **WestWorld**, a unified trajectory world model pretrained on 89 simulated and real-world environments to predict future states from past state-action history.
- To handle dynamics differences across robots, the model uses a **system-aware Mixture-of-Experts (Sys-MoE)**: it first learns a system embedding, then uses it to assign weights to multiple experts, allowing different robots to dynamically combine different experts instead of forcing all systems to share the same parameter set.
- To inject physical structural priors, the model constructs a **structural embedding**: it represents the robot as a kinematic tree, converts it via LCRS, extracts pre-/in-/post-order traversal indices and object IDs, and embeds these structural indices into the state/action channel representations.
- On the input side, each scalar state/action channel is first normalized, discretized, and embedded; in the backbone, self-attention models relationships among state channels, cross-attention injects action conditioning, and then Mamba-style SSM and MoE experts perform dynamics modeling.
- The training objective is cross-entropy prediction over discretized next-state tokens; at inference time, multi-step prediction can be completed in a single forward pass.

## Results
- **Zero-shot long-horizon prediction** (50-step history input, 100-step prediction) outperforms baselines on all 3 unseen environments:
  - **Walker2d**: MAE **16.350** vs TDM 20.122 / TrajWorld 22.261 / MLPEnsemble 26.006; MSE **5.064** vs 6.428 / 8.623 / 12.028.
  - **Hopper**: MAE **13.731** vs 17.634 / 17.388 / 19.987; MSE **3.368** vs 5.076 / 5.441 / 7.216.
  - **Franka**: MAE **7.737** vs 23.686 / 13.102 / 12.164; MSE **2.539** vs 8.435 / 5.127 / 4.271.
- **Few-shot adaptation** (fine-tuning with only 10 episodes per dataset) also performs best on 3 real robot systems:
  - **Cassie**: MAE **5.316±0.108** vs TrajWorld 7.834±0.167; MSE **0.808±0.025** vs 1.697±0.109.
  - **A1**: MAE **4.227±0.120** vs TrajWorld 5.138±0.200; MSE **0.628±0.040** vs 0.900±0.050.
  - **UR5**: MAE **4.925±0.317** vs TrajWorld 8.066±0.799; MSE **0.831±0.150** vs 2.117±0.433.
- **Scalability**: as the number of pretraining environments increases from **N=1,2,5,10,20,30**, the paper states that WestWorld’s error remains relatively low and changes little, whereas TrajWorld degrades significantly as more environments are added; this section does not provide specific values in the excerpt, but it is emphasized as a main scalability conclusion.
- **Downstream and real-world deployment**: the authors claim WestWorld significantly improves downstream model-based control performance across different robots, and has been deployed on a real **Unitree Go1** demonstrating stable locomotion; the excerpt does not provide specific control scores or success-rate numbers.

## Link
- [http://arxiv.org/abs/2603.14392v1](http://arxiv.org/abs/2603.14392v1)
