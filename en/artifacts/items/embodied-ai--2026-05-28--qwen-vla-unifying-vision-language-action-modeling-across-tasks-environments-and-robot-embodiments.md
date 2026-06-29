---
source: arxiv
url: https://arxiv.org/abs/2605.30280v1
published_at: '2026-05-28T17:36:31'
authors:
- Qiuyue Wang
- Mingsheng Li
- Jian Guan
- Jinhui Ye
- Sicheng Xie
- Yitao Liu
- Junhao Chen
- Zhixuan Liang
- Jie Zhang
- Xintong Hu
- Xuhong Huang
- Pei Lin
- Junyang Lin
- Dayiheng Liu
- Shuai Bai
- Jingren Zhou
- Jiazhao Zhang
- Haoqi Yuan
- Gengze Zhou
- Hang Yin
- Ye Wang
- Yiyang Huang
- Zixing Lei
- Wujian Peng
- Delin Chen
- Yingming Zheng
- Jingyang Fan
- Xianwei Zhuang
- Xin Zhou
- Haoyang Li
- Anzhe Chen
- Tong Zhang
- Xuejing Liu
- Yuchong Sun
- Ruizhe Chen
- Zhaohai Li
- "Chenxu L\xFC"
- Zhibo Yang
- Tao Yu
- Xionghui Chen
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- cross-embodiment
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments

## Summary
Qwen-VLA is a single vision-language-action policy for manipulation, navigation, and trajectory prediction across robot embodiments. It adds a DiT flow-matching action decoder to Qwen3.5-4B and trains on mixed robot, human, simulation, navigation, and vision-language data.

## Problem
- Embodied AI models are often tied to one task family, robot body, or benchmark, which limits transfer across manipulation, navigation, and new robot platforms.
- Robot control data uses different action types, control rates, horizons, and dimensions, so scaling across datasets is hard without a common training interface.
- The problem matters because robot foundation models need broad data mixtures to improve generalization under changes in objects, scenes, lighting, language, and embodiment.

## Approach
- The core mechanism is simple: the model reads images, a language instruction, and a text description of the current robot, then predicts a future action or trajectory chunk.
- The backbone is Qwen3.5-4B for vision-language understanding. A DiT flow-matching action decoder with about 1.15B parameters generates continuous actions.
- Embodiment-aware prompts specify the robot tag, arm setup, control frequency, and prediction horizon, so one model can handle different platforms without separate output heads.
- Actions and trajectories use a shared tensor shape with padding and masks. Each dataset keeps its native control convention, while the mask prevents padded channels from affecting training.
- Training uses four stages: text-to-action decoder pretraining, multimodal continued pretraining, supervised fine-tuning, and reinforcement learning in SimplerEnv.

## Results
- Qwen-VLA-Instruct reports 97.9% success on LIBERO and 73.7% on Simpler-WidowX.
- It reports 86.1% on RoboTwin-Easy and 87.2% on RoboTwin-Hard.
- For navigation, it reports 69.0% OSR on R2R and 59.6% SR on RxR.
- In real-world ALOHA out-of-distribution experiments, it reports 76.9% average success.
- On DOMINO dynamic manipulation, it reports 26.6% zero-shot success.
- The excerpt gives metric values across benchmarks, but it does not provide detailed baseline-by-baseline comparison numbers.

## Link
- [https://arxiv.org/abs/2605.30280v1](https://arxiv.org/abs/2605.30280v1)
