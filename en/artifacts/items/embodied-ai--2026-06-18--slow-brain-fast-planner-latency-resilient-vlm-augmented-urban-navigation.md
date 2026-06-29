---
source: arxiv
url: https://arxiv.org/abs/2606.20458v1
published_at: '2026-06-18T16:40:07'
authors:
- Zhenghao "Mark'' Peng
- Honglin He
- Quanyi Li
- Yukai Ma
- Bolei Zhou
topics:
- vlm-navigation
- trajectory-scoring
- latency-resilient-control
- mobile-robots
- planner-fusion
- urban-navigation
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Slow Brain, Fast Planner: Latency-Resilient VLM-Augmented Urban Navigation

## Summary
The paper improves sidewalk robot navigation by using a slow VLM to choose among fast planner trajectories, then converting delayed VLM choices into live planner scores.

## Problem
- Learned local planners can generate safe candidate paths at 5–20 Hz, but their scorer often chooses the wrong candidate in hard sidewalk scenes, such as junctions, grass boundaries, pedestrians, and ambiguous forks.
- On about 2,000 hard real-world scenarios, the planner top choice has 1.64 m ADE while the oracle-best candidate in the same set has 0.39 m ADE, leaving 1.25 m of recoverable error inside the planner output.
- VLMs can read scene context, but their 1–3 s query latency is too slow for direct control of a mobile robot.

## Approach
- The planner generates kinematically feasible candidate trajectories; the VLM only selects an index from that candidate set.
- The system overlays numbered candidate trajectories on the camera image and prompts off-the-shelf VLMs such as Gemini, GPT-5, and Qwen without fine-tuning.
- A delayed VLM-selected trajectory is motion-compensated into the current robot frame, then compared with fresh planner candidates using geometric similarity.
- Score Fusion adds a decayed VLM similarity bonus to the planner score; Probability Fusion mixes planner and VLM distributions with a bounded, time-decayed weight.
- VLM Streaming sends queries at a fixed cadence and uses the newest returned response, so the robot keeps moving without waiting for the VLM.

## Results
- On the hard split, Gemini 3 Flash reaches 1.16 m ADE versus 1.64 m for planner argmax, a 30% ADE reduction; the oracle lower bound is 0.39 m.
- The hard-split scoring gap is large: planner argmax has 1.64 m ADE, while the best available candidate among the same planner outputs has 0.39 m ADE.
- Gemini 3 Flash reports 0.39 m ADE@1s and 0.66 m ADE@2s, compared with planner argmax at 0.64 m ADE@1s and 1.06 m ADE@2s.
- Gemini 2.5 Flash Lite gives a practical latency-quality point: 1.21 m ADE with 1.7 s median latency.
- In simulation, Score Fusion stays above 80% success with VLM delays up to 5 s; Probability Fusion is about 78% success at 5 s.
- Direct stale-execution baselines fail under delay: VLM Hold collapses after 2 s and is near zero by 4 s, while VLM Stream falls below 20% success at 5 s.

## Link
- [https://arxiv.org/abs/2606.20458v1](https://arxiv.org/abs/2606.20458v1)
