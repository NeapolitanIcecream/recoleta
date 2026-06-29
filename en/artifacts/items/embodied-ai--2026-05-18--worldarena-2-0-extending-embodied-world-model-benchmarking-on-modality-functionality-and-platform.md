---
source: arxiv
url: https://arxiv.org/abs/2605.17912v1
published_at: '2026-05-18T06:18:21'
authors:
- Yu Shang
- Yinzhou Tang
- Yiding Ma
- Zhuohang Li
- Lei Jin
- Weikang Su
- Xin Jin
- Zhaolu Wang
- Ziyou Wang
- Xin Zhang
- Haisheng Su
- Weizhen He
- Wei Wu
- Haoyi Duan
- Gordon Wetzstein
- Xihui Liu
- Dhruv Shah
- Zhaoxiang Zhang
- Zhibo Chen
- Jun Zhu
- Yonghong Tian
- Tat-Seng Chua
- Wenwu Zhu
- Chen Gao
- Yong Li
topics:
- embodied-world-models
- visuotactile-robotics
- robot-benchmarking
- rl-world-models
- sim2real
- dexterous-manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# WorldArena 2.0: Extending Embodied World Model Benchmarking on Modality, Functionality and Platform

## Summary
WorldArena 2.0 is a benchmark for embodied world models that adds visuotactile sensing, RL training inside learned dynamics, and real-robot evaluation. It tests whether models can predict contact-rich interaction and help train policies that transfer across robot platforms.

## Problem
- Existing embodied world model benchmarks focus on vision-only video prediction, so they miss tactile signals needed for contact, slip, friction, and force-sensitive manipulation.
- Many evaluations stop at fixed-policy scoring or open-loop planning, so they do not test whether a world model can support policy improvement through repeated imagined rollouts.
- Simulator-only scores do not show whether learned dynamics help real robots, especially under changes in embodiment, sensors, and physical contact.

## Approach
- WorldArena 2.0 extends WorldArena along three axes: modality, functionality, and platform.
- For modality, it upgrades video world models with a tactile VAE, a two-stream visuotactile denoising model, and an action diffusion head; UniVTAC evaluates tactile PSNR, tactile SSIM, and task success rate.
- For functionality, it treats a learned transition model as an RL environment: the policy acts on predicted observations, a reward model scores transitions, and an optimizer updates the policy from imagined rollouts.
- For platform coverage, it evaluates RoboTwin 2.0, LIBERO, and a real AgileX Split-Type ALOHA robot, using data-engine and action-planner protocols across six tasks.

## Results
- The paper reports experiments on 12 embodied world models across simulated and real robot settings, with detailed numbers shown in the excerpt for UniVTAC and RoboTwin 2.0.
- On UniVTAC Insert HDMI and Lift Bottle, Wan2.2 gets the best tactile prediction quality: 21.26 PSNR and 0.746 SSIM. Its task success is 100% on Insert HDMI, 0% on Lift Bottle, and 50% average.
- On the same UniVTAC tasks, ACT reaches 20% on Insert HDMI, 80% on Lift Bottle, and 50% average, while Vidar reaches 13.97 PSNR, 0.278 SSIM, 70% on Insert HDMI, 0% on Lift Bottle, and 35% average.
- Genie Envisioner reaches 13.36 PSNR and 0.456 SSIM on tactile prediction, but scores 0% success on both UniVTAC tasks.
- In the RoboTwin 2.0 RL-environment evaluation, simulator-based RL is still highest: 87.30-87.45% on Click Bell and 78.90% on Adjust Bottle. Among world models, WoVR reaches 75.00% on Click Bell with proxy rewards and 69.38% with VLM rewards; Ctrl-World reaches 70.70% on Adjust Bottle with proxy rewards and 66.02% with similarity rewards.
- The excerpt names real-world AgileX ALOHA tasks, including pour water and wipe the table, and claims a sim-to-real usability gap, but it does not provide the real-robot success-rate table.

## Link
- [https://arxiv.org/abs/2605.17912v1](https://arxiv.org/abs/2605.17912v1)
