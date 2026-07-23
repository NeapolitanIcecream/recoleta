---
source: arxiv
url: https://arxiv.org/abs/2607.20061v1
published_at: '2026-07-22T12:05:13'
authors:
- Hanjing Ye
- Tianle Zeng
- Jiazhao Zhang
- Shaoan Wang
- Zibo Zhang
- Weisi Situ
- Yuchen Zhou
- Yonggen Ling
- Hong Zhang
topics:
- embodied-visual-tracking
- vision-language-action
- robot-foundation-model
- target-identification
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# ReferTrack: Referring Then Tracking for Embodied Visual Tracking

## Summary
ReferTrack improves embodied visual tracking by separating target selection from waypoint prediction while keeping both decisions in one vision-language-action policy. On the single-forward-camera EVT-Bench setting, it reports state-of-the-art results across three splits using a 4B-parameter model and supervised fine-tuning only.

## Problem
- A mobile robot must continuously follow a person specified by natural language using only onboard vision, while maintaining a 1–3 meter distance and keeping the person visible.
- In crowded or ambiguous scenes, VLA policies may reason through abstract spatial tokens that are difficult to supervise and weakly tied to image detections; reliable target identification matters because an identification error directly undermines tracking and navigation.

## Approach
- ReferTrack first runs YOLO11 and ByteTrack, places detected pedestrians into an indexed bounding-box catalog, and predicts one Refer-CoT token selecting the instructed person or a `<NO_EXIST>` option.
- It then conditions waypoint prediction on that selected index, turning target identification into a supervised discrete choice over image-space candidates before generating navigation actions.
- A sliding-window queue stores selected historical bounding boxes and injects their geometry into visual history through temporal-viewpoint-bbox indicator (TVBI) tokens, providing target-specific motion cues.
- The model jointly trains on 1.3M simulated tracking trajectories and 1.3M custom Refer-QA samples derived from SYNTH-PEDES, using trajectory, referring, and text losses with full fine-tuning of the Qwen3-4B backbone and auxiliary modules.

## Results
- On single-view EVT-Bench, ReferTrack reports 89.4% SR, 92.5% TR, and 1.6% CR on Single-Target Tracking; 73.3% SR, 81.8% TR, and 7.6% CR on Distracted Tracking; and 74.1% SR, 85.7% TR, and 7.7% CR on Ambiguity Tracking.
- Against the single-view TrackVLA++ baseline, it improves Distracted Tracking by 6.8 percentage points in SR and 13.0 points in TR, and improves Ambiguity Tracking by 22.9 points in SR and 22.3 points in TR.
- On Distracted Tracking, removing both Refer-CoT and TVBI lowers performance to 55.7% SR and 71.4% TR, while removing only TVBI lowers it to 70.4% SR and 80.8% TR.
- An oracle variant using ground-truth target boxes reaches 81.5% SR and 84.7% TR on Distracted Tracking, compared with 73.3% and 81.8% for the full model; the paper therefore identifies target recognition as a major remaining bottleneck.
- The paper also reports real-world deployments on legged and humanoid robots as evidence of sim-to-real transfer, but the supplied excerpt gives no deployment metrics or controlled real-world baseline comparison.

## Link
- [https://arxiv.org/abs/2607.20061v1](https://arxiv.org/abs/2607.20061v1)
