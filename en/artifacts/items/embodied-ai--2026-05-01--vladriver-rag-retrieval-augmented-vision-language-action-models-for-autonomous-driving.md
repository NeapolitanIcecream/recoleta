---
source: arxiv
url: https://arxiv.org/abs/2605.08133v2
published_at: '2026-05-01T05:50:00'
authors:
- Rui Zhao
- Haofeng Hu
- Zhenhai Gao
- Jiaqiao Liu
- Gao Fei
topics:
- autonomous-driving
- vision-language-action
- retrieval-augmented-generation
- trajectory-planning
- graph-retrieval
- bench2drive
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving

## Summary
VLADriver-RAG adds retrieval to a VLA driving policy so the planner can use similar past scenarios when choosing path and speed. The paper claims the gain comes from retrieving semantic traffic graphs instead of raw images, which reduces visual ambiguity in long-tail driving cases.

## Problem
- It addresses weak generalization in autonomous-driving VLA models when rare traffic cases are sparse in training data.
- Raw visual retrieval is too slow for closed-loop driving and can match scenes with similar pixels but different traffic logic, such as different signal states.
- The problem matters because a wrong retrieved example can push the planner toward unsafe trajectories in rare or out-of-distribution scenes.

## Approach
- The core mechanism converts camera observations into ego-centered spatiotemporal semantic graphs with vehicles, lanes, signs, signals, and relation edges.
- A Scenario-Aligned Embedding Model encodes graph sequences with an R-GCN and a Transformer encoder.
- Training uses graph reconstruction plus Graph-DTW metric alignment so nearby vectors correspond to similar traffic topology and interaction history.
- At runtime, the current graph retrieves historical driving priors from a vector database.
- The VLA planner fuses visual tokens, navigation and speed tokens, and retrieved context tokens, then uses separate query tokens to predict path waypoints and speed waypoints.

## Results
- On Bench2Drive, VLADriver-RAG reports a Driving Score of 89.12 and a Success Rate of 70.42%.
- It beats the cited VLA baseline ORION, which reports 77.74 DS and 54.62% SR on the same benchmark.
- It also beats the cited VLA baseline Simlingo in Driving Score, reported as 85.0 DS in the excerpt.
- It exceeds several end-to-end baselines listed in the excerpt, including DriverAdapter at 64.22 DS and 33.08% SR, ThinkTwice at 62.44 DS and 31.23% SR, and TCP-traj at 59.90 DS and 30.00% SR.

## Link
- [https://arxiv.org/abs/2605.08133v2](https://arxiv.org/abs/2605.08133v2)
