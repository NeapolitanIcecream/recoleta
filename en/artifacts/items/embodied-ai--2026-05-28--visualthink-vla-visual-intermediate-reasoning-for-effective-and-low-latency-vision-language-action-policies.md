---
source: arxiv
url: https://arxiv.org/abs/2605.30011v1
published_at: '2026-05-28T14:36:53'
authors:
- Mingjian Gao
- Wenqiao Zhang
- Yuqian Yuan
- Yang Dai
- Binhe Yu
- Zheqi Lv
- Haoyu Zheng
- Jiaqi Zhu
- Zhiqi Ge
- Zixuan Wan
- Siliang Tang
- Yueting Zhuang
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- visual-reasoning
- robot-data-scaling
- low-latency-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies

## Summary
VisualThink-VLA adds sparse visual evidence tokens to VLA policies so they can use intermediate visual reasoning with sub-second action latency. It targets the delay and weak visual grounding of text chain-of-thought methods for robot control.

## Problem
- VLA policies can fail when manipulation needs object grounding, spatial relations, motion tracking, or long-horizon progress tracking.
- Text chain-of-thought adds multi-second autoregressive latency, which is too slow for closed-loop robot control.
- Dense visual side inputs can add irrelevant or redundant cues that interfere with action prediction.

## Approach
- The method builds six candidate visual evidence channels: bounding box, edge, motion, relation, depth, and segmentation.
- Channel screening keeps four operational channels: bounding box, edge, motion, and relation; depth and segmentation are dropped in the default setting.
- A task-adaptive router chooses which evidence channels to use at each decision step.
- A Visual State Composer maps the selected channel vectors into learned visual states and inserts them before action decoding while keeping the VLA backbone frozen.
- Training uses soft-hard route masks, distillation from a dense FullSoft teacher, and VisualEvidence-Set route labels from 754.7k visual-thinking VLA instructions.

## Results
- On BridgeData V2, VisualThink-VLA reports 89.49% success at 0.367 s per step, compared with ECoT at 85.09% and 8.377 s; the paper reports a 22.8x latency reduction.
- Against BaseVLA, it improves success on 7 of 8 main benchmarks, including BridgeData V2 from 75.37% to 89.49% and UT Austin MUTEX from 41.09% to 77.26%.
- On LIBERO, it reports 97.74% on Object, 97.05% on Goal, 96.69% on Spatial, and 95.87% on Long, with latencies between 0.345 s and 0.421 s.
- Compared with the dense FullSoft variant, it keeps similar success while lowering latency on every listed benchmark; for UT Austin MUTEX, success is 77.26% vs. 77.10% and latency is 0.451 s vs. 0.551 s.
- In the backbone portability test, adding VisualThink-VLA raises success by +16.37 points on OpenVLA, +10.87 on Octo, and +11.95 on SmolVLA, with latency increases of 0.050 s, 0.077 s, and 0.104 s.

## Link
- [https://arxiv.org/abs/2605.30011v1](https://arxiv.org/abs/2605.30011v1)
