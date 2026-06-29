---
source: arxiv
url: https://arxiv.org/abs/2606.27375v1
published_at: '2026-06-25T17:59:57'
authors:
- Arthur Allshire
- Himanshu Gaurav Singh
- Ritvik Singh
- Adam Rashid
- Hongsuk Choi
- David McAllister
- Justin Yu
- Yiyuan Chen
- Huang Huang
- Pieter Abbeel
- Xi Chen
- Rocky Duan
- Phillip Isola
- Jitendra Malik
- Fred Shentu
- Guanya Shi
- Philipp Wu
- Angjoo Kanazawa
topics:
- behavior-cloning
- vision-language-action
- robot-data-scaling
- sim2real
- dexterous-manipulation
- bimanual-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Scalable Behavior Cloning with Open Data, Training, and Evaluation

## Summary
ABC releases an open behavior-cloning stack for bimanual manipulation, centered on ABC-130K, a 3,553-hour real-world teleoperation dataset with 134,806 episodes over 195 tasks. The paper also reports model ablations, simulation data, sim-to-real correlation, and real-world policy rollouts for DiT and VLA policies.

## Problem
- Robot manipulation behavior cloning is hard to reproduce because large datasets, hardware setups, training code, and evaluation rollouts are often private or incomplete.
- Design choices for DiT and VLA robot policies are costly to test on real robots, so researchers need cheaper signals that track real-world performance.
- Complex bimanual and dexterous tasks need more diverse data than standard pick-and-place datasets.

## Approach
- ABC-130K contains 3,553 hours, 134,806 episodes, 195 tasks, and 1,552 hours with subgoal annotations; tasks include pick-and-place, folding, insertion, tool use, handover, and assembly.
- The release includes hardware setup, data loading, training and deployment code, model weights, ABC-Eval real rollout scores, and ABC-Sim.
- ABC-DiT uses a 2B-parameter diffusion transformer with DINOv3 visual features and cross-attention to action tokens.
- ABC-VLA uses a 4B Gemma 3 VLM with a diffusion action head; the paper compares cross-attention, FAST co-training, and AdaLN connectors.
- ABC-Sim adds MuJoCo tasks, VR teleoperation, more than 400 hours of simulation data, and Blender re-rendering for higher-quality images.

## Results
- ABC-130K is reported as the largest open-source teleoperation dataset: 3,553 real-world hours, 134,806 episodes, and 195 tasks; ABC-Eval includes more than 100 hours of real policy rollouts.
- Architecture ablation on an internal 7,000-hour corpus after 200k steps: best DiT, DINOv3 cross-attention, reached 32.9% mean strict success and 67.5% mean progress; CLIP-AdaLN DiT reached 13.4% and 47.3%.
- VLA connector ablation: AdaLN reached 32.8% mean strict success and 61.4% mean progress; FAST plus cross-attention reached 3.6% and 32.6%; vanilla cross-attention reached 0.0% and 11.7%.
- Specific task results from Table 1 include bottles progress of 93.1% for DINOv3-DiT versus 53.6% for CLIP-AdaLN and 74.1% for CLIP-cross-attention; dishrack strict success was best for CLIP-cross-attention DiT at 34.7%.
- Offline diagnostics tracked real performance across 16 checkpoints: training loss versus strict success had Pearson r=-0.89 and Spearman rho=-0.93; validation action error versus strict success had r=-0.84 and rho=-0.83; validation loss had no significant relation to strict success, with r=-0.04.
- Simulation tracked real performance across 12 checkpoints on three tasks: strict success Pearson r=0.85 with p=4.2e-4; task progress Pearson r=0.91 with p=5.0e-5.

## Link
- [https://arxiv.org/abs/2606.27375v1](https://arxiv.org/abs/2606.27375v1)
