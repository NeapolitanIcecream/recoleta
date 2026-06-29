---
source: arxiv
url: https://arxiv.org/abs/2606.18239v1
published_at: '2026-06-16T17:58:22'
authors:
- Ning Gao
- Jinliang Zheng
- Xing Gao
- Haoxiang Ma
- Hanqing Wang
- Yukai Wang
- Jiantong Chen
- Zanxin Chen
- Shujie Zhang
- Mingda Jia
- Xuekun Jiang
- Zihou Zhu
- Xinyu Li
- Shuai Wang
- Hao Li
- Wenzhe Cai
- Yuqiang Yang
- Xudong Xu
- Zhaoyang Lyu
- Yao Mu
- Tai Wang
- Jiangmiao Pang
- Jia Zeng
- Weinan Zhang
- Chunhua Shen
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- mobile-manipulation
- robot-benchmark
- robot-data-scaling
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# EBench: Elemental Diagnosis of Generalist Mobile Manipulation Policies

## Summary
EBench is a simulation benchmark for diagnosing generalist mobile manipulation policies across mobile, long-horizon, and dexterous tasks. It shows that similar overall success rates can hide large differences in skill, precision, horizon, and out-of-distribution behavior.

## Problem
- Current robot manipulation benchmarks often reduce performance to one success-rate number, which hides where a generalist policy succeeds or fails.
- Many suites cover narrow regimes such as tabletop pick-and-place, mobile rearrangement, or one isolated capability, so they miss combined mobile, long-horizon, and high-precision manipulation.
- This matters because embodied foundation models and vision-language-action policies need diagnostics that explain failure modes before real robot deployment.

## Approach
- EBench defines 26 simulation tasks: 10 mobile pick-and-place tasks, 9 mobile long-horizon tasks, and 7 fixed-base dexterous-and-precise tasks.
- Each task is labeled along 5 capability axes: scene type, atomic skill, temporal horizon, precision, and operating mode.
- The benchmark tests 4 generalization shifts: unseen backgrounds, unseen objects, paraphrased instructions, and their mixture, with train/test asset pools kept separate.
- Data collection uses teleoperation for 7 dexterous tasks and key-frame poses plus cuRobo motion planning for 19 mobile or long-horizon tasks.
- The dataset contains 6,600 demonstration episodes and 91.4 hours of demonstrations, evaluated with binary success rate and staged partial-progress scores.

## Results
- Across π0, π0.5, XVLA, and InternVLA-A1, overall test success rates are close at 24.4% to 29.5%, but capability profiles differ by large margins.
- π0.5 has the best overall test result: 29.5% SR and 45.6% Score, with retention ratios of 0.92 for SR and 0.95 for Score from Val-Train to Test.
- InternVLA-A1 reaches 27.6% test SR and performs well on mobile manipulation, around 34.7% SR, but drops to 5.8% SR on dexterous fixed-base tasks, a 29-point gap.
- π0 leads high-precision sub-centimeter tasks at 13.8% SR, while π0.5 leads low-precision tasks at 44.2% SR.
- Generalization is hardest under combined shifts: Background and Instruction variants give 27% to 35% SR, Object swaps drop to 21% to 29% SR, and Mix drops to 18% to 23% SR.
- Pretraining shows larger gains on EBench than on LIBERO or RoboTwin 2.0 Hard: π0 improves from 11.2% to 24.4% SR, π0.5 from 8.5% to 29.5%, and XVLA from 15.7% to 24.7%.

## Link
- [https://arxiv.org/abs/2606.18239v1](https://arxiv.org/abs/2606.18239v1)
