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
- robot-world-model
- trajectory-prediction
- mixture-of-experts
- morphology-encoding
- zero-shot-generalization
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# WestWorld: A Knowledge-Encoded Scalable Trajectory World Model for Diverse Robotic Systems

## Summary
WestWorld is a scalable trajectory world model for diverse robotic systems. Its core idea is to encode robot structural knowledge into the representation and use a system-aware mixture of experts to handle different dynamics. It aims to simultaneously improve the scalability of cross-robot pretraining and the zero-shot and few-shot generalization ability to unseen robots/environments.

## Problem
- Existing multi-robot trajectory world models usually use one shared set of parameters to fit robot dynamics with large differences, which easily leads to gradient conflicts and negative transfer, and becomes harder to scale as the number of robot types grows.
- Different robots have inconsistent sensor/actuator dimensions and semantics, different sampling frequencies, and large kinematic structure differences, making unified modeling difficult.
- Many methods treat trajectories only as token sequences and ignore the physical prior of robot morphological structure, resulting in weak zero-shot generalization to unseen systems.

## Approach
- First normalize and discretize states and actions by channel, convert each scalar channel into a token embedding, and add embeddings for time, channel order, modality, and more.
- Introduce **knowledge-encoded structural embedding**: represent robot morphology as a kinematic tree, then convert it into a binary tree, encode each part position with pre/in/post-order and object id, and add these structural embeddings to the trajectory representation to explicitly inject morphological priors.
- Use **Sys-MoE**: instead of letting all robots share the same dense parameters, learn a system embedding, extract system-level features through SSM/Mamba-style layers, and then have a router generate expert weights to dynamically combine multiple experts for representing different system dynamics.
- In each layer, first use self-attention to aggregate relationships among state channels, then use cross-attention to inject action conditions, and finally output future state representations through the system-aware mixture of experts to achieve multi-step prediction.
- Pretrain on 89 simulated and real robot environments, with the objective of predicting future multi-step states in a single forward pass given historical states/actions and future actions.

## Results
- **Zero-shot long-horizon prediction (100-step rollout, 50-step history)**: on Walker2D, WestWorld achieves **MAE 16.350 / MSE 5.064 (×10^-2)**, outperforming MLPEnsemble **26.006 / 12.028**, TDM **20.122 / 6.428**, and TrajWorld **22.261 / 8.623**.
- On Hopper, WestWorld achieves **MAE 13.731 / MSE 3.368 (×10^-2)**, outperforming MLPEnsemble **19.987 / 7.216**, TDM **17.634 / 5.076**, and TrajWorld **17.388 / 5.441**.
- On real Franka data, WestWorld achieves **MAE 7.737 / MSE 2.539 (×10^-2)**, outperforming MLPEnsemble **12.164 / 4.271**, TrajWorld **13.102 / 5.127**, and TDM **23.686 / 8.435**.
- **Few-shot adaptation (finetuning with only 10 episodes)**: on Cassie it reaches **5.316±0.108 / 0.808±0.025**, outperforming TrajWorld **7.834±0.167 / 1.697±0.109**; on A1 it reaches **4.227±0.120 / 0.628±0.040**, outperforming TrajWorld **5.138±0.200 / 0.900±0.050**; on UR5 it reaches **4.925±0.317 / 0.831±0.150**, outperforming TrajWorld **8.066±0.799 / 2.117±0.433**.
- The paper also claims that when scaling to more environments, WestWorld’s prediction error remains relatively stable as the number of environments increases, while TrajWorld degrades significantly; however, the provided excerpt does not include the specific values from that figure.
- The authors also claim that the model can significantly improve downstream model-based control and has been deployed on a real **Unitree Go1** to achieve stable locomotion; however, the excerpt does not provide corresponding control metrics or success-rate numbers.

## Link
- [http://arxiv.org/abs/2603.14392v1](http://arxiv.org/abs/2603.14392v1)
