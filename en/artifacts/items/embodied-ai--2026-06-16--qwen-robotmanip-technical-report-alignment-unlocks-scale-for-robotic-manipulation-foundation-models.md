---
source: arxiv
url: https://arxiv.org/abs/2606.17846v1
published_at: '2026-06-16T12:14:39'
authors:
- Haoqi Yuan
- Zhixuan Liang
- Anzhe Chen
- Ye Wang
- Haoyang Li
- Pei Lin
- Yiyang Huang
- Zixing Lei
- Tong Zhang
- Jiazhao Zhang
- Jie Zhang
- Jingyang Fan
- Gengze Zhou
- Qihang Peng
- Chenxu Lv
- Xiaoyue Chen
- An Yang
- Fei Huang
- Junyang Lin
- Dayiheng Liu
- Jingren Zhou
- Chenfei Wu
- Xiong-Hui Chen
topics:
- vision-language-action
- robot-foundation-model
- cross-embodiment
- robot-data-scaling
- human-to-robot-synthesis
- ood-evaluation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models

## Summary
Qwen-RobotManip is a Qwen-VL-based vision-language-action model for manipulation that targets out-of-distribution robot generalization. The report claims that cross-embodiment alignment lets the model train on a 38,100-hour multi-source manipulation corpus and beat prior VLA systems on OOD tests.

## Problem
- Robot manipulation data differs across robot bodies, cameras, coordinate frames, action spaces, and task setups, so adding more data can hurt training when the signals conflict.
- Existing VLA benchmarks often test narrow in-domain behavior, so strong scores can hide weak transfer to new robots, instructions, layouts, and perturbations.
- This matters because a generalist robot policy needs to follow language, recover from errors, and transfer skills across embodiments without collecting a new large dataset for each robot.

## Approach
- The model uses Qwen-VL as the vision-language base and trains an action policy on robot observations, instructions, states, and actions.
- It maps different robots into one canonical state-action template and uses per-dimension binary masks so robots with different joints and grippers can share training data.
- It predicts camera-frame delta end-effector poses so visually similar motions have similar action values across coordinate systems.
- It uses recent execution history inside an episode as an implicit clue about the current robot body, which helps the policy adapt its actions to the embodiment.
- It expands data with a human-to-robot synthesis pipeline: egocentric hand trajectories are converted to robot end-effector motions, rendered onto cleaned video backgrounds, and generated for 15 dual-arm robot platforms.

## Results
- The pretraining corpus contains about 38,100 hours of manipulation data: 3,808 hours single-arm robot data, 6,744 hours dual-arm robot data, 868 hours mobile and humanoid data, 1,933 hours human egocentric data, and 24,808 hours synthesized human-to-robot data.
- The human-to-robot pipeline renders each human demonstration into 15 bimanual robot configurations, including Panda, UR5e, ARX-L5, xArm7, Sawyer, Kinova Gen3, IIWA, Jaco, FR3, UR10e, ViperX, WidowX, Piper, YAM, and AgileX ALOHA.
- The training also uses about 28M vision-language data points to preserve visual understanding, spatial reasoning, OCR, instruction following, and embodied reasoning during VLA training.
- On RoboChallenge Table30-v1 generalist track, Qwen-RobotManip ranks 1st with a 20% relative improvement over the prior result reported in the excerpt.
- The report claims better performance than prior VLA models, including π0.5 and GR00T-N1.7, across OOD settings such as RoboCasa365, LIBERO-Plus, EBench, RoboTwin-Clean2Rand, RoboTwin-IF, and RoboTwin-XE, but the excerpt does not provide exact success rates for those benchmarks.
- Real-robot validation is reported on 4 platform families: AgileX ALOHA, Franka, UR, and ARX, covering in-domain use, OOD use, few-shot adaptation, and zero-shot cross-embodiment transfer.

## Link
- [https://arxiv.org/abs/2606.17846v1](https://arxiv.org/abs/2606.17846v1)
