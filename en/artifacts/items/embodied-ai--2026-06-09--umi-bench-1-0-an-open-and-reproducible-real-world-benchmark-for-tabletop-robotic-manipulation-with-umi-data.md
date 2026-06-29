---
source: arxiv
url: https://arxiv.org/abs/2606.10382v1
published_at: '2026-06-09T03:47:54'
authors:
- Shi Jin
- Yuntian Wang
- Yuhui Duan
- Di Wu
- Gaoqi Dong
- Xiaohang Liu
- Xiaotong Li
- Hongfei Jia
- Zehao Zhang
- Tianyu Wang
- Zhongjie Jia
- Yuanqi Yao
- Chenjia Bai
- Zhaxizhuoma
- Siao Liu
- Nieqing Cao
- Jin Wang
- Chao Yu
- Yan Ding
topics:
- real-world-benchmark
- umi-data
- robot-manipulation
- vision-language-action
- bimanual-manipulation
- generalist-robot-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data

## Summary
UMI-Bench 1.0 is a real-robot benchmark for testing UMI-style wrist-view manipulation policies under a shared data, reset, execution, and scoring protocol. It matters because UMI policy results can change with camera setup, action interface, object reset, and physical execution details.

## Problem
- Learned manipulation policies need real-robot evaluation because simulation and offline metrics miss contact dynamics, camera artifacts, timing variation, and hardware noise.
- Existing real-world benchmarks do not specify the full UMI data-to-deployment chain, so comparisons can mix model quality with differences in hardware, wrist cameras, action spaces, and reset procedures.
- UMI-style policies need diagnostics for object shifts, appearance shifts, layout shifts, pose shifts, and dynamics shifts, rather than a single aggregate success number.

## Approach
- The benchmark fixes a tabletop robot workstation, wrist-view RGB observation interface, action setup, scene reset procedure, rollout logging, and human scoring workflow.
- Each episode has a reset image and scene JSON with task ID, object metadata, position, pose, target region, split, and task-specific factors.
- The release covers 10 tabletop tasks: 4 single-arm tasks and 6 bimanual tasks, with 50 real-robot evaluation rollouts per task.
- The training repository contains about 20k UMI demonstrations, with 1,600 to 3,000 demos per task.
- Evaluation reports Full Success Rate and a 0 to 100 Progress Score, split across Seen/Seen, Seen/Unseen, Unseen/Seen, and Unseen/Unseen condition cells.

## Results
- Across 10 tasks, π0.5 has the best mean Overall Score: 55.84, compared with 48.90 for π0 and 40.59 for DreamZero.
- π0.5 ranks first on 6 of 10 tasks; π0 leads on T1 Sequential Object Stacking and T2 Articulated Container Manipulation, while DreamZero leads on T3 Tool-Mediated Stamping and T6 Bimanual Packing and Transport.
- Average Progress Score drops from 59.62 in Seen/Seen episodes to 53.45 under Factor-A shifts, 45.33 under Factor-B shifts, and 40.19 under combined shifts.
- Factor-B shifts, covering position, layout, pose, or dynamics, hurt performance more than Factor-A shifts, covering object, appearance, category, or combination changes.
- The hardest tasks are T3 and T9 Long-Horizon Rearrangement: all three evaluated models get 0% Full Success Rate on both tasks.

## Link
- [https://arxiv.org/abs/2606.10382v1](https://arxiv.org/abs/2606.10382v1)
