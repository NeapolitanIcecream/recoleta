---
source: arxiv
url: http://arxiv.org/abs/2604.20100v2
published_at: '2026-04-22T01:51:48'
authors:
- Tianle Zhang
- Zhihao Yuan
- Dafeng Chi
- Peidong Liu
- Dongwei Li
- Kejun Hu
- Likui Zhang
- Junnan Nie
- Ziming Wei
- Zengjue Chen
- Yili Tang
- Jiayi Li
- Zhiyuan Xiang
- Mingyang Li
- Tianci Luo
- Hanwen Wan
- Ao Li
- Linbo Zhai
- Zhihao Zhan
- Xiaodong Bai
- Jiakun Cai
- Peng Cao
- Kangliang Chen
- Siang Chen
- Yixiang Dai
- Shuai Di
- Yicheng Gong
- Chenguang Gui
- Yucheng Guo
- Peng Hao
- Qingrong He
- Haoyang Huang
- Kunrui Huang
- Zhixuan Huang
- Shibo Jin
- Yixiang Jin
- Anson Li
- Dongjiang Li
- Jiawei Li
- Ruodai Li
- Yihang Li
- Yuzhen Li
- Jiaming Liang
- Fangsheng Liu
- Jing Long
- Mingxi Luo
- Xing Pan
- Hui Shen
- Xiaomeng Tian
- Daming Wang
- Song Wang
- Junwu Xiong
- Hang Xu
- Wanting Xu
- Zhengcheng Yu
- He Zhang
- Jiyao Zhang
- Lin Zhao
- Chen Zhou
- Nan Duan
- Yuzheng Zhuang
- Liang Lin
topics:
- vision-language-action
- robot-foundation-model
- cross-embodiment-transfer
- generalist-robot-policy
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy

## Summary
JoyAI-RA 0.1 is a vision-language-action foundation model for robot manipulation that mixes web data, egocentric human videos, simulation trajectories, and real-robot demonstrations. The paper claims that this data mix plus a unified action space improves cross-embodiment transfer and raises success rates in simulation and on a real humanoid robot.

## Problem
- Robot manipulation models struggle with open-world generalization because robot datasets are costly, narrow in task coverage, and weak on long-tail interactions.
- Data from humans, simulators, and different robots use different bodies and action formats, which makes behavior transfer across embodiments hard.
- This matters because general-purpose robot autonomy needs policies that can handle new tasks, scenes, and hardware without collecting large amounts of fresh robot data each time.

## Approach
- JoyAI-RA trains one VLA model on four sources: multimodal web data, an in-house egocentric human manipulation dataset called EgoLive, simulation datasets, and real-robot datasets including JDAgibot and open-source corpora.
- The main mechanism is an explicit unified action space: actions and proprioception are mapped into a fixed shared representation, mostly in camera-frame end-effector coordinates, with masking for missing degrees of freedom on different robots.
- The model has a vision-language backbone for semantic and spatial understanding and a Perceiver-based action expert that predicts continuous action chunks with a flow-matching objective.
- Training runs in three stages: VLM co-pretraining on multimodal tasks, VLA co-pretraining with action learning on aligned heterogeneous data, and post-training on the target robot embodiment.
- Human hand trajectories from EgoLive are estimated and retargeted to robot embodiments such as ALOHA, Fourier, and Agibot G1 to support cross-embodiment learning.

## Results
- On RoboTwin 2.0, JoyAI-RA reports **90.48%** success on Easy and **89.28%** on Hard, beating π0 (**65.92/58.40**), π0.5 (**82.74/76.76**), Motus (**88.66/87.02**), and LingBot-VLA (**88.56/86.68**).
- On RoboCasa GR1 Tabletop, JoyAI-RA reports **63.2%** average success, ahead of ABot-M0 (**58.3%**), DualCoT-VLA (**55.1%**), TwinBrainVLA (**54.6%**), Being-H0.7 (**49.2%**), GR00T-N1.6 (**47.6%**), and Qwen3PI (**43.9%**).
- On the real-world AgiBot benchmark, the cross-task average success rate improves from **0.62** with π0.5 to **0.74** with JoyAI-RA across six tasks and 20 trials per task.
- The paper highlights large task gains on RoboCasa long-horizon tasks: **CanToDrawerClose +16.0**, **MilkToMicrowaveClose +24.0**, and **TrayToPot +18.0** over the previous best.
- EgoLive ablation on RoboTwin 2.0 shows **87.42%** success for **JDAgibot + full EgoLive**, compared with **81.64%** for no pretraining, **77.62%** for JDAgibot only, and **81.40%** for **JDAgibot + 10% EgoLive**.
- The excerpt gives dataset scale details rather than total pretraining token counts or model size. It states EgoLive covers **1,969** object categories, **1,796** action categories, and more than **10k** tasks across household, retail, and logistics settings.

## Link
- [http://arxiv.org/abs/2604.20100v2](http://arxiv.org/abs/2604.20100v2)
