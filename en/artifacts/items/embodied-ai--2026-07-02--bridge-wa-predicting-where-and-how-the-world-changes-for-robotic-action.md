---
source: arxiv
url: https://arxiv.org/abs/2607.02195v1
published_at: '2026-07-02T14:03:44'
authors:
- Yongjie Bai
- Hanting Wang
- Mingtong Dai
- Qijun Zhong
- Yang Liu
- Liang Lin
topics:
- vision-language-action
- robot-world-models
- world-prior-distillation
- manipulation
- real-robot-evaluation
- ood-generalization
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Bridge-WA: Predicting Where and How the World Changes for Robotic Action

## Summary
Bridge-WA adds compact future-change priors to a vision-language-action robot policy. It predicts intended outcome, likely changing pixels, and local motion, then uses those signals to guide action generation without running the 5B teacher at deployment.

## Problem
- Many VLA robot policies map the current image, language, and robot state directly to actions, so they can miss how the scene should change after contact.
- Dense image or video world models add training and inference cost, and they spend capacity on background, lighting, and other pixels that do not guide control.
- This matters for manipulation because success often depends on the action-relevant change region and movement direction, especially under visual shifts and distractors.

## Approach
- The authors pre-train a robot-state-conditioned future-change teacher based on the Wan2.2-5B generative backbone on BridgeData V2 manipulation trajectories.
- The frozen teacher produces three cached targets for policy training: future tokens for the intended outcome, change maps for where the scene should change, and motion-flow maps for how changed regions should move.
- A lightweight predictor learns these three priors from current RGB views, proprioception, and language.
- WorldBridge injects the predicted priors into the action transformer through attention memories and change or flow attention biases.
- At inference, the teacher and cache are removed; the deployed policy runs only the predictor and the conditioned action transformer.

## Results
- On VLABench, Bridge-WA reports 52.8% average success rate, compared with the strongest listed SR baseline at 43.1% for pi0-Fast with delta chunks, a gain of 9.7 points.
- On VLABench intention and progress metrics, Bridge-WA reports 71.2% average IS and 64.0% average PS; X-VLA reports 70.2% IS and 51.2% PS.
- On RoboTwin 2.0, Bridge-WA reports 79.7% Easy success and 37.7% Hard success on the 15-task subset; its Easy/Hard mean is 58.7% versus 52.3% for X-VLA.
- On LIBERO-Plus zero-shot evaluation, Bridge-WA reports 72.1% average success, above OpenVLA-OFT at 69.6% and RIPT-VLA at 68.4%; it is weaker on the Camera perturbation at 25.0%.
- On the Dobot real-robot suite with 5 tasks and 50 demonstrations per task, Bridge-WA reports 73.6% Easy average success and 69.1% Hard average success, compared with X-VLA at 69.6% Easy and 58.0% Hard.
- In Dobot hard-track averages, Bridge-WA reports 62.8% with distractors, 74.0% under lighting shifts, and 70.4% under tablecloth shifts; X-VLA reports 53.2%, 65.2%, and 55.6%.

## Link
- [https://arxiv.org/abs/2607.02195v1](https://arxiv.org/abs/2607.02195v1)
