---
source: arxiv
url: http://arxiv.org/abs/2603.08122v1
published_at: '2026-03-09T09:02:30'
authors:
- Tutian Tang
- Xingyu Ji
- Wanli Xing
- Ce Hao
- Wenqiang Xu
- Lin Shao
- Cewu Lu
- Qiaojun Yu
- Jiangmiao Pang
- Kaifeng Zhang
topics:
- vision-language-action
- dexterous-manipulation
- bimanual-robotics
- tactile-force-fusion
- hierarchical-policy
- shared-autonomy
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Towards Human-Like Manipulation through RL-Augmented Teleoperation and Mixture-of-Dexterous-Experts VLA

## Summary
This paper proposes an integrated framework for human-like bimanual dexterous manipulation: RL-trained IMCopilot assists teleoperation and serves as a low-level skill module during execution, while MoDE-VLA robustly incorporates force/tactile sensing into a pretrained VLA. Targeting high-DoF, contact-rich in-hand manipulation, it claims about a 2x success-rate improvement over the baseline across 4 tasks.

## Problem
- Existing VLAs mostly remain limited to low-DoF grippers and simple pick-and-place, and are difficult to extend to **63-DoF** human-like in-hand manipulation and bimanual coordination with two arms and two hands.
- High-quality demonstration data are hard to collect: pure teleoperation struggles to stably complete multi-finger coordination and in-hand rotation, especially for contact-rich tasks such as apple peeling.
- A single policy has difficulty covering coarse motion, force-control phases such as insertion/cutting, and tactile-driven in-hand adjustment at the same time; meanwhile, directly concatenating force/tactile inputs into a pretrained VLA may also damage its original capabilities.

## Approach
- Proposes **IMCopilot**: a set of RL-trained atomic in-hand skills (e.g., stable grasping, rotation around a specified axis). During data collection, they are triggered by the human operator via a foot pedal to help complete the hardest in-hand stages; during autonomous execution, they are likewise called by trigger signals output by the VLA, forming hierarchical control.
- Proposes **MoDE-VLA**: beyond a pretrained OpenPI-0 / PaliGemma-style VLA backbone, it builds separate force and tactile channels instead of simply concatenating inputs.
- Uses **arm joint torques** as the force modality and **10 fingertip 6-DoF tactile/force-torque readings** as the tactile modality; after projection into tokens, they interact through self-attention together with backbone context and autoregressive/flow-matching action states.
- Uses a **sparse Mixture-of-Experts** to select experts by token/time step, learning different correction patterns for different contact phases (approach, initial contact, stable grasping, dynamic rotation).
- Through **residual injection**, force mainly corrects arm actions and tactile mainly corrects hand actions; when IMCopilot is triggered, hand actions can be directly taken over by the RL skills.

## Results
- In the comparison of in-hand manipulation capability, **IMCopilot significantly outperforms pure teleoperation**: ping-pong ball **3/30→25/30 (10%→83%)**, tennis ball **20/30→28/30 (67%→93%)**, apple **8/30→27/30 (27%→90%)**, overall **31/90→80/90 (34%→89%)**.
- The paper evaluates **4 contact-rich tasks**: gear assembling, charger plugging, test tube rearranging, and apple peeling; each method is tested for **20 trials per task**, with **Success Rate** as the main metric, and apple peeling additionally reports **Peel Completion Ratio**.
- The abstract claims that on dexterous contact-rich tasks, compared with the baseline, it achieves **"doubled success rate improvement"**, i.e., success rate improves to roughly **2x** the previous level; the explicit baseline is the pretrained **\(\pi_0\)**.
- The paper also claims, to the best of its knowledge, the **first autonomous apple peeling with dual dexterous hands**, a composite task requiring the joint contribution of vision, force, touch, bimanual coordination, and in-hand rotation.
- Limited by the provided excerpt, the complete per-task numeric tables and ablation results are not fully available; the strongest quantitative evidence currently comes mainly from **Table I** and the abstract’s claim of **about 2x success-rate improvement**.

## Link
- [http://arxiv.org/abs/2603.08122v1](http://arxiv.org/abs/2603.08122v1)
