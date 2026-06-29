---
source: arxiv
url: https://arxiv.org/abs/2604.26839v1
published_at: '2026-04-29T16:02:13'
authors:
- Lingfeng Zhang
- Xiaoshuai Hao
- Xizhou Bu
- Yingbo Tang
- Hongsheng Li
- Jinghui Lu
- Xiu-shen Wei
- Jiayi Ma
- Yu Liu
- Jing Zhang
- Hangjun Ye
- Xiaojun Liang
- Long Chen
- Wenbo Ding
topics:
- social-navigation
- outdoor-navigation
- vision-language-action
- human-robot-assistance
- map-free-navigation
- safety-reasoning
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance

## Summary
Walk with Me is a robot navigation system for outdoor assistance from high-level language instructions. It grounds user intent with public map POIs, plans coarse waypoints, and uses VLM/VLA modules for local motion and safety decisions.

## Problem
- It solves long-horizon outdoor social navigation where a user gives an abstract request such as “I want to go for a walk” instead of a coordinate goal.
- This matters for last-mile delivery and blind guidance, where the robot must choose a real destination, follow a long route, and behave safely near crossings, traffic, and crowds.
- HD-map navigation is costly to build and maintain, while many learned navigation policies focus on indoor or short routes with low-level goals.

## Approach
- A High-Level VLM receives the user instruction, GPS context, and candidate POIs from a public map API, then selects a concrete destination.
- The system queries a walking-route API and resamples the route into geo-referenced waypoints for long-horizon guidance.
- At each step, the robot forms an observation from the RGB image, local pose, recent trajectory, and next waypoint.
- A VLM router decides whether the scene is routine or complex and whether the robot should proceed or stop and wait.
- If proceeding is safe, a Low-Level VLA predicts a short local trajectory; if safety confidence is low, the robot waits and rechecks the scene.

## Results
- The real-world evaluation uses 20 outdoor trials: 2 application categories, 2 scenarios per category, and 5 independent trials per scenario.
- The two application categories are last-mile delivery and blind guidance; example instructions include “Take the milk tea to Building B” and “I want to go shopping.”
- The paper claims kilometer-scale outdoor navigation from abstract instructions on an Athena 2.0 Pro AGV robot.
- The excerpt gives no success rate, path length distribution, completion time, collision rate, or social-compliance metric.
- The main experiment reports no full-system baseline comparison; the authors state that existing methods do not match the same input-output setting.

## Link
- [https://arxiv.org/abs/2604.26839v1](https://arxiv.org/abs/2604.26839v1)
