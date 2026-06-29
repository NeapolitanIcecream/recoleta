---
source: arxiv
url: http://arxiv.org/abs/2604.12908v1
published_at: '2026-04-14T15:57:16'
authors:
- Zijian Song
- Qichang Li
- Jiawei Zhou
- Zhenlong Yuan
- Tianshui Chen
- Liang Lin
- Guangrun Wang
topics:
- vision-language-action
- robot-manipulation
- 3d-world-model
- geometry-aware-policy
- zero-shot-generalization
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models

## Summary
VGA argues that robot manipulation should use native 3D geometry features instead of language-model or video-model features. It builds a policy on top of a pretrained 3D world model and reports state-of-the-art LIBERO performance plus stronger zero-shot cross-view transfer on real robots.

## Problem
- The paper targets a mismatch in current robot foundation models: manipulation depends on 3D position, rotation, and spatial relations, but many Vision-Language-Action and video-action models are pretrained on 2D image-text or pixel prediction data.
- This mismatch matters because policies can learn visual patterns or semantics without learning the geometry needed for precise grasping, reaching, and object placement, which hurts robustness and viewpoint generalization.
- Prior attempts to add 3D cues still keep a 2D-centric backbone or require extra depth sensors, which the authors say creates a 3D-to-2D bottleneck or extra hardware complexity.

## Approach
- The core method is VGA, a **Vision-Geometry-Action** model that replaces the usual VLM or video backbone with **VGGT**, a pretrained 3D world model that maps multi-view RGB directly into native 3D scene representations.
- Inputs are multi-view RGB, language instructions, and robot proprioception. These tokens go through the VGGT transformer with alternating local and global attention to produce shared 3D-aware tokens for control.
- Action prediction uses an action decoder with chunk size **C=8**. A new **Progressive Volumetric Modulation (PVM)** module injects geometry into the action decoder layer by layer through staged cross-attention.
- Training is multi-task: the shared backbone predicts **actions + camera parameters + depth maps** with a joint loss. At test time, the camera and depth heads are dropped, so inference only decodes actions.
- The model is trained with **LoRA rank 64** on a system with about **500M trainable parameters** according to the excerpt.

## Results
- On **LIBERO**, VGA reports **99.0%** on Spatial, **99.6%** on Object, **98.6%** on Goal, **95.0%** on Long, and **98.1% average**.
- Against major VLA baselines on LIBERO, VGA beats **pi_0.5** (**96.9% avg**) by **+1.2 points**, **OpenVLA-oft** (**97.1% avg**) by **+1.0**, and **VLA-Thinker** (**97.5% avg**) by **+0.6**.
- Against 3D-VLA baselines, VGA beats **SpatialVLA** (**78.1% avg**) by **+20.0 points**, **GeoAwareVLA** (**96.8% avg**) by **+1.3**, and **GeoVLA** (**97.7% avg**) by **+0.4**.
- Against world-action/video-style baselines, VGA beats **Motus** (**97.7% avg**) by **+0.4 points** and is above **mimic-video** (**93.9% avg**) by **+4.2**.
- For real-world robots, the excerpt claims better **zero-shot generalization to unseen camera viewpoints** and higher success rate than **pi_0.5**, but it does not provide the real-world numbers in the provided text.
- The excerpt also claims quantitative confirmation that VGA predicts 3D properties with high fidelity, but the specific camera/depth metrics are not included in the provided text.

## Link
- [http://arxiv.org/abs/2604.12908v1](http://arxiv.org/abs/2604.12908v1)
