---
source: arxiv
url: https://arxiv.org/abs/2606.31836v1
published_at: '2026-06-30T15:39:29'
authors:
- Xinyi Wang
- Donghan Li
- Zi'Ang Chen
- Chong Yu
- Chen Xin
- Peng Ye
- Yingkai Sun
- Tao Chen
topics:
- humanoid-manipulation
- dexterous-manipulation
- visual-tactile-data
- robot-data-scaling
- imitation-learning
- vision-language-action
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# RoboTacDex: A Dexterous Visual-Tactile-Action Dataset for Humanoid Manipulation

## Summary
RoboTacDex is a humanoid manipulation dataset with 6k visual-tactile-action trajectories for dual-arm, dexterous-hand tasks. Its main value is data: synchronized multi-view RGB-D, tactile signals, joint states, actions, and task annotations on a Unitree G1.

## Problem
- Humanoid manipulation datasets are scarce, especially for dual-arm dexterous hands with tactile sensing and multi-view depth.
- Fixed-arm datasets do not cover the high-DOF action space, bimanual coordination, and contact-rich tasks expected from humanoid upper-body manipulation.
- This matters because imitation learning and VLA policies need real demonstrations with aligned observations, actions, and contact feedback to learn tasks such as page turning, book insertion, and bottle unscrewing.

## Approach
- The authors teleoperate a Unitree G1 humanoid with a Meta Horizon VR headset and record upper-body manipulation by 14-DOF dual arms and 12-DOF Brainco dexterous hands.
- Each trajectory records 4 RGB-D camera views at 640x480, arm and hand joint states, arm and finger actions, and tactile signals from both hands.
- The system uses hardware and software synchronization across cameras, with recording at 30 Hz; tactile and hand joint messages are published at 100 Hz and logged with the other modalities at 30 Hz.
- The dataset covers tasks designed for dual arms and dexterous hands, including basic, articulated, dual-arm collaborative, fine, and humanoid-interactive manipulation.
- The paper evaluates ACT, Diffusion Policy, and GROOT N1.5 on selected tasks to test whether the dataset can train imitation policies.

## Results
- RoboTacDex contains 6k trajectories, about 25 hours of data, 19 tasks, 23 skills, and 22 objects.
- The dataset includes 4 camera perspectives: head view, 2 wrist views, and a third-person view; most tasks are collected across 4 scene settings from 2 table distances, 5 cm and 15 cm, and 2 table backgrounds.
- In 10-trial evaluations per task, GROOT N1.5 averaged 6/10 success, compared with 3/10 for ACT and 3/10 for Diffusion Policy.
- On PickAndPlacePear, GROOT N1.5 reached 9/10 success, while Diffusion Policy reached 3/10 and ACT reached 0/10.
- On harder tasks, GROOT N1.5 scored 6/10 on TurnPage, 4/10 on InsertBook, and 6/10 on UnscrewBottle; ACT scored 6/10, 4/10, and 3/10, while Diffusion Policy scored 5/10, 3/10, and 2/10.
- Multi-view inputs did not clearly improve success for the tested models, and tactile input did not raise UnscrewBottle success for Diffusion Policy, though it changed failures from idle spinning toward grip-adjustment failures, which suggests the tactile signal affected contact behavior.

## Link
- [https://arxiv.org/abs/2606.31836v1](https://arxiv.org/abs/2606.31836v1)
