---
source: arxiv
url: http://arxiv.org/abs/2604.14125v1
published_at: '2026-04-15T17:50:07'
authors:
- Tianshuo Yang
- Guanyu Chen
- Yutian Chen
- Zhixuan Liang
- Yitian Liu
- Zanxin Chen
- Chunpu Xu
- Haotian Liang
- Jiangmiao Pang
- Yao Mu
- Ping Luo
topics:
- vision-language-action
- hierarchical-policy
- robot-manipulation
- visual-grounding
- diffusion-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System

## Summary
HiVLA is a hierarchical robot manipulation system that keeps a vision-language model focused on planning and grounding, while a separate diffusion policy handles motor control. The paper claims this split avoids reasoning loss from end-to-end fine-tuning and improves long-horizon, cluttered manipulation.

## Problem
- End-to-end vision-language-action models often lose reasoning ability when fine-tuned on small, domain-specific robot control datasets.
- Manipulation tasks need both semantic planning and precise object-level perception, especially in cluttered scenes and multi-step tasks.
- Existing grounding interfaces lose either global spatial context or fine local detail, which hurts fine-grained control.

## Approach
- HiVLA splits the system into two parts: a high-level VLM planner and a low-level Diffusion Transformer action expert.
- The VLM planner takes the task, scene, action history, and robot state, then outputs a structured plan with a subtask instruction, skill label, target object, and a normalized bounding box.
- The bounding box is used to crop a high-resolution local image patch from the original 1920x1080 camera frame, so the controller gets detailed target-object appearance.
- The action expert uses conditional flow matching in a DiT policy and applies cascaded cross-attention in each block to inject three signals in sequence: global scene features, position-aware local crop features, and subtask language embeddings.
- Local crop tokens get absolute positional embeddings tied to their coordinates in the original image, so the policy keeps both object detail and scene location.

## Results
- On the RoboTwin 2.0 benchmark, HiVLA reaches **83.3%** total average success, compared with **70.6%** for **H-RDT**, **46.4%** for **StarVLA**, **45.6%** for **pi_0**, and **44.8%** for **pi_0.5**.
- The paper states this is an absolute gain of **17.7 points** over **H-RDT** and **42.7 points** over **pi_0** on RoboTwin 2.0.
- On hard tasks, HiVLA scores **73.2%** average success versus **54.6%** for **H-RDT** and **36.4%–38.6%** for **pi_0/pi_0.5/StarVLA**.
- On easy tasks, HiVLA scores **96.0%** average, close to **96.5%** for the ablation without skill input, and above **90.5%** for **H-RDT**.
- Example task results for HiVLA: **60%** on *Move Stapler* vs **34%** for H-RDT, **76%** on *Stamp Seal* vs **43%**, **37%** on *Stack 3 Blocks* vs **20%**, and **98%** on *Click 3 Bells* vs **88%**.
- The excerpt says experiments also include real-world evaluation, but it does not provide real-world quantitative numbers in the provided text.

## Link
- [http://arxiv.org/abs/2604.14125v1](http://arxiv.org/abs/2604.14125v1)
