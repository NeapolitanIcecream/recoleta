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
- open-world-navigation
- vision-language-models
- frontier-based-exploration
- zero-shot-navigation
- object-goal-navigation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# OpenFrontier: General Navigation with Visual-Language Grounded Frontiers

## Summary
OpenFrontier proposes a **training-free** open-world navigation framework that uses **frontiers** as the bridge between visual-language semantics and executable navigation. It does not rely on dense 3D semantic maps, policy training, or fine-tuning, yet achieves strong zero-shot performance on multiple ObjNav benchmarks and demonstrates real-robot deployment capability.

## Problem
- When navigating in open environments, robots must simultaneously understand the **semantics of language-specified goals** and **geometrically reachable locations**; traditional methods often depend on dense 3D mapping and hand-crafted goal metrics, leading to poor generalization and heavyweight systems.
- Although end-to-end VLN/VLA methods can use natural language for control, they usually require **substantial interactive training, data collection, or task-specific fine-tuning**, and they struggle to stably ground high-level semantics into navigation decisions in metric space.
- The paper aims to solve: **how to achieve open-vocabulary, zero-shot, practically deployable language-conditioned navigation without training a navigation policy or building dense semantic maps**; this matters because it lowers deployment cost and improves cross-environment generalization.

## Approach
- Reformulate navigation as a **sparse subgoal identification and reaching** problem: first detect visual frontiers from the current RGB image, instead of performing full 3D reconstruction first.
- Use a VLM to score each frontier in the image with **set-of-marks**: mark frontier locations on the image, combine them with the language goal, and let the model output the probability \(p_i\) that the frontier “leads to the goal.”
- Combine semantic probability with exploration benefit to obtain frontier utility: \(g_i = p_i \cdot \hat{g}_i\), where \(\hat{g}_i\) is the frontier’s own information gain; then combine this with distance to get global utility \(u_i = g_i / \|p_r - p_i\|\), prioritizing frontiers that are “both relevant and nearby.”
- Frontiers are evaluated in image space, then back-projected and managed in 3D space: the system maintains a global frontier set, continuously updates, merges, and prunes it, and passes it to a low-level PointNav/planner for execution.
- When open-vocabulary segmentation detects a suspected target, the system inserts a high-priority “viewpoint frontier,” moves to a better observation pose, and then uses the same VLM for target confirmation and termination decisions.

## Results
- On **HM3D ObjNav Val**, OpenFrontier reaches **77.3% SR / 35.6% SPL**; compared with zero-shot baselines: BeliefMapNav has **61.4 / 30.6**, InstructNav **58.0 / 20.9**, VLFM **52.5 / 30.4**, and OpenFMNav **52.5 / 24.1**. Its SR is **15.9** points higher than BeliefMapNav and **19.3** points higher than InstructNav.
- On **MP3D ObjNav Val**, OpenFrontier achieves **40.7% SR / 17.8% SPL**; compared with UniGoal’s **41.0 / 16.4**, it is **0.3** points lower in SR but **1.4** points higher in SPL; it also outperforms BeliefMapNav’s **37.3 / 17.6** and VLFM’s **36.4 / 17.5**.
- On the open-vocabulary benchmark **OVON Val Unseen**, OpenFrontier achieves **39.0% SR / 20.1% SPL**; this exceeds VLFM’s **35.2 / 19.6** and DAgRL+OD’s **37.1 / 19.9**, and is close to the non-zero-shot Uni-NaVid’s **39.5 / 19.8**: **0.5** points lower in SR but **0.3** points higher in SPL.
- The paper emphasizes that these results are achieved under **zero-shot, no dense semantic maps, and no policy training/fine-tuning** conditions, while some comparison methods require dense semantic maps or are not zero-shot.
- In the experimental setup, the system uses **Gemini-2.5-flash** for VLM inference, runs frontier detection every **6 steps**, and the full experimental pipeline can run on a **single RTX 4090 24GB**, supporting its claim of a “lightweight system design.”
- In the real world, the paper shows a successful case of a mobile robot finding a **fire extinguisher** in a large-scale indoor environment, but the excerpt **does not provide quantitative real-robot metrics**; the strongest concrete conclusion is that it demonstrates effective and robust open-world navigation capability on a real robot.

## Link
- [http://arxiv.org/abs/2603.05377v1](http://arxiv.org/abs/2603.05377v1)
