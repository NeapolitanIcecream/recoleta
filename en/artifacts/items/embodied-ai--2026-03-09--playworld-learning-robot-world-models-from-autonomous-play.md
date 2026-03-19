---
source: arxiv
url: http://arxiv.org/abs/2603.09030v2
published_at: '2026-03-09T23:58:07'
authors:
- Tenny Yin
- Zhiting Mei
- Zhonghe Zheng
- Miyu Yamane
- David Wang
- Jade Sceats
- Samuel M. Bateman
- Lihan Zha
- Apurva Badithela
- Ola Shorinwa
- Anirudha Majumdar
topics:
- robot-world-model
- autonomous-play
- video-diffusion
- policy-evaluation
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# PlayWorld: Learning Robot World Models from Autonomous Play

## Summary
PlayWorld proposes a framework for learning action-conditioned video world models from robot autonomous “play” data, aiming to more realistically predict contact-rich manipulation dynamics. The core claim is that, compared with success-biased human demonstrations, autonomous self-play data is better suited for training scalable, physically consistent robot world models.

## Problem
- Existing robot video world models mostly rely on human demonstration data, whose distribution is concentrated on **successful trajectories** and lacks critical contact events such as failures, collisions, slipping, and deformation.
- This causes models to produce physical hallucinations during closed-loop prediction, such as object duplication, disappearance, and unrealistic motion, thereby weakening the reliability of policy evaluation, planning, and RL fine-tuning.
- This problem matters because contact-rich manipulation tasks are exactly the difficult part of real-world robot deployment; if a world model cannot reliably simulate these dynamics, it is hard for it to become a truly useful data-driven simulator.

## Approach
- A **VLM task proposer** uses the current scene image to automatically generate diverse natural-language instructions, which are then executed by a pretrained **VLA execution policy**, enabling continuous collection of unsupervised self-play interaction data on a real robot.
- In essence, this mechanism lets the robot “set its own tasks and try to solve them,” naturally producing a richer variety of successful and failed contact patterns through instruction perturbations and different initial object states.
- To support long-duration unattended collection, the system includes lightweight safety filtering and scene reset mechanisms, allowing continuous operation for up to **8 hours**, including overnight collection.
- The world model uses a pretrained **stable video diffusion** action-conditioned video backbone, jointly predicts **3 camera views**, and is fine-tuned on self-play data.
- To better learn long-tail interactions, the authors use a curriculum based on **CLIP-to-success-trajectory distance**: first learning simpler segments close to success, then gradually adding rarer and more difficult exploratory interactions.

## Results
- On the interaction-centric benchmark, **Robot Play (6h)** is significantly better than **Human Demo (6h)** on multiple contact failure modes: for example, LPIPS for **missed grasp** improves **0.080→0.066**, with SSIM **0.875→0.883**; LPIPS for **slide** improves **0.090→0.077**; LPIPS for **slip** improves **0.090→0.078**; and for **collision**, LPIPS improves **0.086→0.074** with SSIM **0.852→0.888**.
- After scaling robot self-play data from **6h to 30h**, performance continues to improve: for example, LPIPS for **success** improves **0.082→0.071**; for **slide**, LPIPS improves **0.077→0.073** and SSIM **0.865→0.876**; this indicates that scaling self-play data continues to provide gains.
- Adding curriculum learning brings further improvements: **Robot Play (Curriculum)** reaches LPIPS **0.070** / SSIM **0.880** on **success**, LPIPS **0.071** / SSIM **0.890** on **slide**, and LPIPS **0.072** / SSIM **0.893** on **collision**, outperforming the 30h self-play model without curriculum.
- The paper claims that models trained with PlayWorld can deliver **up to 40% improvement** in **policy evaluation and failure prediction** compared with models trained on human-collected data.
- The paper also claims that, after performing **reinforcement learning inside the world model**, policy success rates on real-robot deployment can improve by **65%** (relative to the pretrained policy).
- In terms of data scaling, the authors claim that PlayWorld’s downstream visual accuracy continues to improve even at **5× the scale where human demonstration data has already saturated**, highlighting its scalability and advantage in covering long-tail interactions.

## Link
- [http://arxiv.org/abs/2603.09030v2](http://arxiv.org/abs/2603.09030v2)
