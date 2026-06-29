---
source: arxiv
url: https://arxiv.org/abs/2605.22183v1
published_at: '2026-05-21T08:52:47'
authors:
- Weilong Guo
- Yuchen Wang
- Renping Zhou
- Yunfeng Zhang
- Rui Fang
- Yue Meng
- Wenda Xu
- Yuan He
- Gao Huang
topics:
- vision-language-action
- robot-manipulation
- visual-primitives
- generalist-robot-policy
- spatial-grounding
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Action with Visual Primitives

## Summary
AVP is a VLA architecture that makes the VLM output visual target tokens before action prediction. It reports large real-robot gains over π₀.₅ on pick-and-place tasks that need precise spatial grounding.

## Problem
- Current VLA policies often map images and language straight to robot actions, so the action head must learn instruction parsing, spatial grounding, and motor control at the same time.
- This matters because robot policies can fail when object layouts, target positions, or object appearances change, especially in dense scenes such as Chinese chess boards.
- Prior visual-prompt methods use external detectors or VLM APIs, which add latency and can pass localization errors into the robot policy.

## Approach
- AVP splits the work: the VLM decides what target matters and where it is, then the action expert predicts how to move the robot.
- The VLM autoregressively predicts visual primitives such as points, boxes, masks, or memory primitives for the next execution stage.
- These primitives are projected into visual token space and fused with the observation tokens, then a flow-matching action expert predicts future robot actions.
- The primitive labels come from end-effector kinematics through camera calibration, so the method avoids per-sample human prompt labels.
- At inference, AVP uses only the observation, instruction, and robot state; it does not call an external detector, segmenter, or online VLM API.

## Results
- On Chinese chess manipulation, AVP reaches 90.28% average success versus 62.67% for π₀.₅, a +27.61 point gain. Metric breakdown: instruction following 98.61% vs 74.00%, pick 90.28% vs 72.00%, place 81.94% vs 42.00%.
- On the same Chinese chess task, AVP runs at 0.27 s per instruction. Point-VLA with Kimi reports 48.15% average success and 37.32 s latency on a 20-instruction subset.
- On domino placement, AVP reaches 88.19% average success versus 81.94% for π₀.₅. Pick improves from 87.50% to 100.00%, orientation from 93.75% to 100.00%, and place stays at 64.58%.
- On general object pick-and-place, AVP reaches 86.18% average success versus 64.96% for π₀.₅. Pick improves from 71.79% to 90.24%, and place improves from 23.08% to 68.29%.
- On unseen direct Chinese-chess transitions, AVP reports 83% average success with 100% instruction following, 90% pick, and 60% place, while π₀.₅ reports 0% on all four metrics.
- In the visual-primitive ablation, average success rises from 78% with no primitive to 83% with boxes, 85% with box plus mask, and 91% with box plus mask plus memory.

## Link
- [https://arxiv.org/abs/2605.22183v1](https://arxiv.org/abs/2605.22183v1)
