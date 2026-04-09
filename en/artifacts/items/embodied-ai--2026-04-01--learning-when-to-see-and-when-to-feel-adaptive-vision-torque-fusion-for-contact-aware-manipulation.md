---
source: arxiv
url: http://arxiv.org/abs/2604.01414v1
published_at: '2026-04-01T21:23:41'
authors:
- Jiuzhou Lei
- Chang Liu
- Yu She
- Xiao Liang
- Minghui Zheng
topics:
- robot-manipulation
- multimodal-fusion
- force-torque-sensing
- diffusion-policy
- contact-aware-control
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation

## Summary
This paper studies how to combine vision and joint torque signals for contact-rich robot manipulation with diffusion policies. Its main claim is that torque should be ignored during free motion and added only during contact through an adaptive fusion rule.

## Problem
- Vision-only manipulation policies miss contact state, alignment quality, friction, and insertion progress in tasks where visual change is small or the scene is occluded.
- Naive vision-plus-torque fusion can hurt performance because joint torque signals during free-space motion contain noise and inertia effects.
- Prior work proposes auxiliary losses, routing, and gating, but this paper argues there was no clear head-to-head comparison inside the same diffusion-policy setup.

## Approach
- The policy uses a diffusion-policy backbone with two RGB views, joint positions, and a 10-step history of 7 joint external torques from a Franka Research 3 robot.
- A contact gate checks whether any joint external torque passes a threshold. If there is no contact, the torque feature is replaced by a learned default vector; if there is contact, the real torque feature is used.
- The model trains two separate U-Nets: one for vision plus proprioception, and one for gated torque plus proprioception.
- At each diffusion denoising step, the final noise prediction is a learned blend of the two experts. A small MLP predicts the torque weight from image and gated torque features, and the weight is forced to zero when there is no contact.
- The paper benchmarks this method against vision-only, feature concatenation, torque gating alone, auxiliary future-torque prediction, and mixture-of-experts fusion.

## Results
- Across three real-world tasks, the proposed method reaches **82.0% average success**: bottle placement **16/20**, connector pull-out **7/10**, egg-boiler lid opening **18/20**.
- The strongest baseline in Table I is **torque gating** at **68.0% average success**: **14/20**, **5/10**, **15/20**. The reported gain is **14 percentage points** over this baseline.
- Vision-only gets **30.0% average success** (**8/20**, **0/10**, **7/20**). Feature concatenation also gets **30.0%** (**3/20**, **0/10**, **12/20**). Auxiliary goals get **28.0%** (**6/20**, **1/10**, **7/20**). MoE gets **24.0%** (**5/20**, **1/10**, **7/20**).
- On the weight-based bottle task, the proposed method gets **9/10** for empty bottles and **7/10** for full bottles, for **16/20** total. Vision-only gets **8/10** on empty and **0/10** on full, which shows it fails to infer weight.
- On egg-boiler lid opening single-attempt performance, torque gating gets **20.0%** first-try success with **110.7** average task-horizon steps, while the proposed method gets **60.0%** with **87.1** steps.
- The paper’s strongest qualitative claim is that most of the gain comes from filtering torque during free motion, while the adaptive guidance weight improves precision once contact starts.

## Link
- [http://arxiv.org/abs/2604.01414v1](http://arxiv.org/abs/2604.01414v1)
