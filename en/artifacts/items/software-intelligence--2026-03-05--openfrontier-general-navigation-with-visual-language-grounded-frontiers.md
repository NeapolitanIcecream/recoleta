---
source: arxiv
url: http://arxiv.org/abs/2603.05377v1
published_at: '2026-03-05T17:02:22'
authors:
- Esteban Padilla
- Boyang Sun
- Marc Pollefeys
- Hermann Blum
topics:
- robot-navigation
- vision-language-models
- frontier-based-exploration
- zero-shot-learning
- open-world-navigation
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# OpenFrontier: General Navigation with Visual-Language Grounded Frontiers

## Summary
OpenFrontier proposes a **training-free** open-world robot navigation framework that uses **frontiers** as the bridge between vision-language semantics and actual navigation. It does not rely on dense 3D mapping, policy training, or fine-tuning, yet achieves strong zero-shot performance on multiple navigation benchmarks and is deployed on a real robot.

## Problem
- Existing open-world navigation methods often rely on **dense 3D reconstruction, semantic maps, or hand-crafted goal metrics**. These systems are heavy, generalize poorly, and are unreliable in cluttered scenes and under open-vocabulary targets.
- Although end-to-end VLN/VLA methods can control navigation with natural language, they usually require **interactive training, large-scale data collection, or task-specific fine-tuning**, making them costly and hard to directly ground into executable navigation decisions in metric space.
- The core challenge is how to reliably **ground high-level vision-language semantics into physically reachable navigation targets**. This is important for open-vocabulary robot navigation because robots must both understand semantics and explore efficiently in unknown environments.

## Approach
- Reformulate navigation as a problem of **finding sparse subgoals and reaching them sequentially**: detect visual frontiers from the current RGB image and use them as candidate navigation targets, instead of first building a complete 3D semantic map.
- Use a **set-of-marks** prompt: mark each frontier in the image, then feed the image and the natural-language goal into a VLM so the model assigns each frontier a task-relevance probability score \(p_i\) in one pass.
- Multiply the VLM semantic score by the frontier’s exploration information gain \(\hat g_i\) to obtain the final utility \(g_i = p_i \cdot \hat g_i\), providing a simple balance between “where is worth exploring” and “which direction is more likely to contain the target.”
- Maintain a sparse global frontier set and choose frontiers by \(u_i = g_i / \|p_r - p_i\|\), balancing **semantic relevance and travel cost**, then hand them to a low-level PointNav/planner for execution.
- When open-vocabulary segmentation detects a suspected target, the system generates a high-priority “viewpoint frontier” near the target, then uses the same VLM for target confirmation, terminating navigation only after confirmation.

## Results
- On **HM3D ObjNav Val**, OpenFrontier reaches **77.3% SR / 35.6% SPL**, outperforming zero-shot baselines: BeliefMapNav **61.4 / 30.6**, InstructNav **58.0 / 20.9**, OpenFMNav **52.5 / 24.1**, VLFM **52.5 / 30.4**, and UniGoal **54.5 / 25.1**. Its SR is also higher than the non-zero-shot Uni-NaVid’s **73.7%**, though its SPL is slightly lower than **37.1%**.
- On **MP3D ObjNav Val**, OpenFrontier achieves **40.7% SR / 17.8% SPL**. Compared with zero-shot methods, it outperforms BeliefMapNav **37.3 / 17.6**, VLFM **36.4 / 17.5**, and OpenFMNav **37.2 / 15.7**, and is close to UniGoal **41.0 / 16.4** (SR lower by 0.3 points, SPL higher by 1.4 points).
- On **OVON Val Unseen** open-vocabulary navigation, OpenFrontier reaches **39.0% SR / 20.1% SPL**, outperforming zero-shot VLFM **35.2 / 19.6** and non-zero-shot DAgRL+OD **37.1 / 19.9**, and approaching non-zero-shot Uni-NaVid **39.5 / 19.8** (SR lower by 0.5 points, but SPL higher by 0.3 points).
- The paper also claims the system performs consistently across three benchmarks under **the same unified configuration**, requiring only **sparse keyframe inference** (frontier detection and inference once every 6 steps), thereby avoiding step-by-step high-frequency action inference or continuous dense semantic mapping.
- For the real world, the authors show a deployment example on a mobile robot searching for a **fire extinguisher** and claim the system is interchangeable across different VLMs, but the excerpt does not provide quantitative real-robot success rate or path-efficiency numbers.

## Link
- [http://arxiv.org/abs/2603.05377v1](http://arxiv.org/abs/2603.05377v1)
