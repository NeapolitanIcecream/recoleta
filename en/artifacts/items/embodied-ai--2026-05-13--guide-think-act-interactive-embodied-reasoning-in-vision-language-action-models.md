---
source: arxiv
url: https://arxiv.org/abs/2605.13632v1
published_at: '2026-05-13T14:58:29'
authors:
- Yiran Ling
- Qing Lian
- Jinghang Li
- Qing Jiang
- Tianming Zhang
- Xiaoke Jiang
- Chuanxiu Liu
- Jie Liu
- Lei Zhang
topics:
- vision-language-action
- interactive-robot-policy
- embodied-reasoning
- robot-data-scaling
- ood-generalization
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Guide, Think, Act: Interactive Embodied Reasoning in Vision-Language-Action Models

## Summary
GTA-VLA lets a user steer a robot VLA policy with visual cues such as points, boxes, or drawn traces, then uses those cues in its reasoning before action. The paper targets failure recovery under visual ambiguity and out-of-distribution shifts while keeping autonomous execution available.

## Problem
- Existing VLA policies often map image and language inputs straight to actions, which can fail when lighting, camera pose, object identity, or clutter differs from training data.
- Embodied Chain-of-Thought methods expose intermediate reasoning, but the excerpt says they lack a direct way for a human to correct wrong spatial grounding during execution.
- This matters because many manipulation failures come from choosing the wrong object, grasp point, contact region, or motion path, and a user can often fix that with a simple spatial cue.

## Approach
- GTA-VLA adds an optional spatial prior to the policy input: a 2D affordance point, bounding box, or trace on the primary camera image.
- A Qwen3-VL-2B backbone generates a spatial-visual reasoning sequence with task reasoning, visual grounding, and robot motion reasoning.
- The model passes the hidden states from those reasoning tokens to a Flow-Matching action head, which predicts continuous action chunks.
- Reasoning runs at a lower rate, while the action head runs at a higher control rate using cached reasoning states, reducing the cost of autoregressive reasoning during control.
- The authors build Interact-306K from about 306K real-world manipulation trajectories, adding synthetic spatial guidance and reasoning supervision from existing robot data.

## Results
- On the in-domain SimplerEnv WidowX benchmark, GTA-VLA reports an 81.2% success rate and claims state-of-the-art performance.
- The excerpted table lists OpenVLA at 14.6% average success on SIMPLER-Env Bridge tasks, with per-task scores of 4.2% for Spoon, 0.0% for Carrot, 8.3% for Cube, and 45.8% for Eggplant.
- On LIBERO, the excerpted table lists OpenVLA at 76.5% average success across Spatial, Object, Goal, and Long tasks; OpenVLA-OFT is shown at 95.3% average.
- The paper introduces SimplerEnv-Plus with OOD changes including camera variation, lighting changes, unseen objects, and language perturbations.
- Under OOD visual shifts and spatial ambiguity, the paper claims that one visual interaction improves task success over existing methods, but the excerpt does not provide the exact OOD improvement numbers.

## Link
- [https://arxiv.org/abs/2605.13632v1](https://arxiv.org/abs/2605.13632v1)
