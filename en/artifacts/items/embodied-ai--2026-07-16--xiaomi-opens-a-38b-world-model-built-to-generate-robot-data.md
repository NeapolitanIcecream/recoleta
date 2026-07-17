---
source: hn
url: https://topicqueue.substack.com/p/xiaomi-opens-a-38b-world-model-built
published_at: '2026-07-16T23:41:36'
authors:
- DISCURSIVE
topics:
- world-model
- robot-data
- robot-foundation-model
- sim2real
- generalist-robot-policy
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Xiaomi Opens a 38B World Model Built to Generate Robot Data

## Summary
Xiaomi-Robotics-U0 is a 38-billion-parameter open robot world model used to generate robot training data rather than control robots directly. Xiaomi reports that data generated with U0 increased π0.5's success on unfamiliar real-world manipulation from 36.9% to 63.2%, although the result is vendor-reported and measured on Xiaomi's evaluations.

## Problem
- Robot policies need large, diverse training data, but collecting real-world manipulation demonstrations is expensive and limits performance on unfamiliar scenes and objects.
- The paper addresses whether a world model can serve as a data-generation engine for robot policies instead of acting as the controller itself.

## Approach
- Xiaomi-Robotics-U0 is a single 38B-parameter model that generates robot scenes and videos using a method described as similar to image and video generation.
- The generated scenes and videos are used as additional training data for π0.5, a robot policy.
- Xiaomi evaluates U0 on embodied video quality through the World Arena leaderboard and compares human preferences for its generated scenes against GPT-Image-2.0.
- The model weights and code are open, allowing external users to reproduce the data-generation pipeline and test its effect on other policies or setups.

## Results
- On unfamiliar real-world manipulation, π0.5's reported success increased from 36.9% to 63.2% after training with U0-generated data, a 26.3-percentage-point gain.
- Xiaomi reports that U0 topped the World Arena embodied-video leaderboard.
- Human raters reportedly preferred U0-generated scenes over scenes from GPT-Image-2.0.
- The reported comparisons are Xiaomi's own evaluations; the excerpt provides no independent replication or separate dataset details.

## Link
- [https://topicqueue.substack.com/p/xiaomi-opens-a-38b-world-model-built](https://topicqueue.substack.com/p/xiaomi-opens-a-38b-world-model-built)
