---
source: arxiv
url: https://arxiv.org/abs/2605.00471v1
published_at: '2026-05-01T07:18:11'
authors:
- Xianbo Cai
- Hideyuki Ichiwara
- Hyogo Hiruma
- Masaki Yoshikawa
- Hiroshi Ito
- Tetsuya Ogata
topics:
- mobile-manipulation
- stereo-vision
- spatial-attention
- imitation-learning
- recurrent-policy
- visual-disturbance
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Stereo Multistage Spatial Attention for Real-Time Mobile Manipulation Under Visual Scale Variation and Disturbances

## Summary
Stereo Multistage Spatial Attention improves real-world mobile manipulation under camera viewpoint changes by tracking task-relevant points in stereo images and feeding them to a recurrent action predictor. In four robot tasks, it reports higher success than ACT, Diffusion Policy, π0, and SmolVLA under the same 10 Hz control setting.

## Problem
- Mobile manipulators use onboard cameras, so object size, position, and visibility change as the robot moves. These scale changes can make vision-based action prediction unstable.
- Rule-based visual servoing and feature tracking need reliable object models, features, or pose estimates, which can fail with occlusion, lighting shifts, and poor texture.
- Large imitation and VLA models can require more data and compute than a small onboard real-time controller can afford.

## Approach
- The method takes left and right RGB images plus robot motor state, then predicts the next robot motor command and the next attention-point positions.
- A stereo multistage spatial attention module extracts 6 task-relevant attention points from each image. It uses 3 CNN stages, compares each stage with an input-image key feature, averages the attention maps, and applies a soft-argmax with temperature 0.001.
- Weight sharing across the left and right image streams encourages the two views to attend to matching objects or robot parts.
- A hierarchical LSTM processes left attention points, right attention points, and robot state in separate low-level LSTMs, then combines their cell states in a high-level LSTM for closed-loop motion prediction.
- Training uses joint-state prediction loss, a motion smoothing term with weight 0.1, and a bidirectional attention-point prediction loss whose coefficient rises from 0.0001 to 0.1.

## Results
- Across 4 real-world tasks with 50 randomized trials per task, the full stereo MSA model reached 85.0% average success with 99% CI 77.4 to 90.4. Baselines were ACT 46.0%, Diffusion Policy 28.5%, π0 3.5B 29.0%, and SmolVLA 0.45B 12.5%.
- Final-task success for the proposed method was 72.0% on Place Coffee, 98.0% on Open Microwave, 92.0% on Take Kettle, and 78.0% on Retrieve Clothing.
- Ablations show the stereo MSA design mattered: stereo MSA reached 85.0% average success, compared with 37.5% for stereo single-stage spatial attention and 33.0% for monocular MSA.
- Under visual disturbance tests across 560 trials, the proposed method reached 76.8% overall success, compared with ACT at 24.8% and ACT plus extracted attention points at 39.6%.
- In disturbance conditions, the method reached 100.0% on Open Microwave with a visual distractor, 86.7% in low light, and 93.3% with an unseen background. ACT scored 6.7%, 26.7%, and 3.3% on the same Open Microwave conditions.
- The dataset used 54 successful demonstrations per task, 15 s sequences at 10 Hz, stereo RGB images of size 3×128×256×2, a 9-DoF right arm, and a 4-DoF mobile base.

## Link
- [https://arxiv.org/abs/2605.00471v1](https://arxiv.org/abs/2605.00471v1)
