---
source: arxiv
url: https://arxiv.org/abs/2605.02881v2
published_at: '2026-05-04T17:51:21'
authors:
- Haoquan Fang
- Jiafei Duan
- Donovan Clay
- Sam Wang
- Shuo Liu
- Weikai Huang
- Xiang Fan
- Wei-Chuan Tsai
- Shirui Chen
- Yi Ru Wang
- Shanli Xing
- Jaemin Cho
- Jae Sung Park
- Ainaz Eftekhar
- Peter Sushko
- Karen Farley
- Angad Wadhwa
- Cole Harrison
- Winson Han
- Ying-Chun Lee
- Eli VanderBilt
- Rose Hendrix
- Suveen Ellawela
- Lucas Ngoo
- Joyce Chai
- Zhongzheng Ren
- Ali Farhadi
- Dieter Fox
- Ranjay Krishna
topics:
- vision-language-action
- robot-foundation-model
- embodied-reasoning
- robot-data-scaling
- action-tokenization
- bimanual-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# MolmoAct2: Action Reasoning Models for Real-world Deployment

## Summary
MolmoAct2 is an open vision-language-action model for real robot deployment, with released weights, code, and training data. It combines an embodied-reasoning VLM, new robot datasets, an action tokenizer, a continuous action expert, and faster scene-change reasoning.

## Problem
- Current VLA robot policies are hard to deploy because strong models are often closed, open models can depend on costly hardware, and reasoning-heavy policies can be too slow for real-time robot control.
- Fine-tuned robot policies still miss dependable success rates on realistic tasks, especially across different embodiments and real-world scenes.
- This matters because researchers and robot builders need reproducible models that can run on accessible platforms and adapt to local data.

## Approach
- MolmoAct2 starts from Molmo2-ER, a 4B VLM trained for spatial and embodied reasoning on a 3.3M-sample embodied corpus, then rehearsed with general multimodal data.
- The authors release three main robot data sources: 720 hours of bimanual YAM data, filtered SO-100/101 community data, and a filtered DROID Franka subset.
- MolmoAct2-FAST Tokenizer converts continuous robot trajectories into discrete action tokens, so the VLM can learn actions with next-token training.
- Post-training adds a flow-matching continuous action expert. Each expert layer conditions on the matching VLM layer's keys and values, which connects VLM grounding to smooth robot actions.
- MolmoAct2-Think speeds reasoning by re-predicting depth tokens only for scene regions that change between timesteps.

## Results
- Molmo2-ER reaches a reported 63.8% average across 13 embodied-reasoning benchmarks, a 17-point gain over Molmo2.
- Molmo2-ER reportedly beats GPT-5 and Gemini Robotics ER-1.5 on 9 of 13 embodied-reasoning benchmarks.
- The BimanualYAM dataset contains 34.5k demonstrations, over 720 hours of robot data, and more than 28 real-world tasks, collected on a setup costing under $6,000.
- The SO-100/101 dataset is curated from 1,222 public LeRobot datasets by 377 users and contains 38,059 episodes, 19.8M frames, and about 184 hours of interaction data.
- The DROID subset contains 74,604 valid successful episodes and 17,758,044 frames after filtering idle segments and requiring valid language instructions.
- The excerpt says MolmoAct2 outperforms strong baselines including π0.5 across 7 simulation and real-world benchmarks, but it does not provide task success-rate numbers in the provided text.

## Link
- [https://arxiv.org/abs/2605.02881v2](https://arxiv.org/abs/2605.02881v2)
