---
source: arxiv
url: https://arxiv.org/abs/2605.30282v1
published_at: '2026-05-28T17:37:16'
authors:
- Kuangji Zuo
- Gen Li
- Bofan Lyu
- Yanshuo Lu
- Boyu Ma
- Shijia Han
- Xinyu Zhou
- Xichen Yuan
- Chuhao Zhou
- Jiaqi Bai
- Geng Li
- Jianfei Yang
topics:
- vision-language-action
- gaze-conditioned-control
- robot-manipulation
- human-robot-interaction
- generalist-robot-policy
- robot-foundation-model
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Gaze2Act: Gaze-Conditioned Vision-Language-Action Policies for Interactive Robot Manipulation

## Summary
Gaze2Act adds human gaze to a Vision-Language-Action robot policy so a user can select the target object, target part, or revised target during execution. The paper claims large gains on real Unitree G1 manipulation tasks compared with language-only and language-grounded spatial baselines.

## Problem
- Language instructions often fail when several similar objects are present, when the robot must act on a specific object part, or when the user changes the target during execution.
- This matters for interactive manipulation because the robot needs a precise spatial intent signal, not only a task sentence such as "pick up the cup."
- Existing mask-based VLA methods still derive spatial targets from language, so they can miss the user’s intended referent under ambiguity or visual difficulty.

## Approach
- The user wears Meta Aria glasses, and gaze provides a 2D point in the first-person view.
- Gaze2Act maps that first-person gaze into the robot camera view using marker-free cross-view semantic matching: SAM3 proposes masks, DINOv3 features match the gazed object across views, and dense feature matching finds the corresponding part point on the selected object.
- The matched object mask and gaze point are drawn onto the robot observation as visual cues: contours for object selection and Gaussian heatmaps for part-level action.
- The same mask and point are also encoded as a gaze token and injected into the GROOT N1.5 diffusion action head through an added cross-attention branch.
- The added gaze branch starts as a no-op through zero initialization and adds 4.95% parameters, so fine-tuning can preserve the pretrained action prior at the start.

## Results
- On a Unitree G1 humanoid across 7 categories and 15 main real-robot tasks with 50 trials per task, Gaze2Act reports 88.8% overall intent accuracy and 83.5% overall task success. Vanilla GROOT gets 33.6% intent and 23.2% success, RoboGround gets 60.6% and 39.6%, and ControlVLA gets 68.0% and 41.5%.
- On the 10 object-level tasks, Gaze2Act reaches 93.0% intent accuracy and 89.0% task success. The strongest baseline, ControlVLA, reaches 68.0% intent and 46.4% success.
- On the 5 part-level tasks, Gaze2Act reaches 80.4% part-level intent accuracy and 72.4% task success. Baseline task success is 21.2% for Vanilla GROOT, 29.6% for RoboGround, and 31.6% for ControlVLA.
- On compositional tasks, Gaze2Act gets 96% intent and 94% success for "pick bread place bowl," and 88% intent and 84% success for "pick paper ball place bin."
- On dynamic intent steering with target switches during execution, Gaze2Act succeeds in 14/30 trials. RoboGround succeeds in 4/30 trials, and ControlVLA succeeds in 5/30 trials.

## Link
- [https://arxiv.org/abs/2605.30282v1](https://arxiv.org/abs/2605.30282v1)
