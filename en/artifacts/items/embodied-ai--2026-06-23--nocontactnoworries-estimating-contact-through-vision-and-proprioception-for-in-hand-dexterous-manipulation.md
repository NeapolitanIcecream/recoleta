---
source: arxiv
url: https://arxiv.org/abs/2606.24450v1
published_at: '2026-06-23T11:36:46'
authors:
- Soham Patil
- Avirup Das
- Sourabh Bhosale
- Spandan Roy
topics:
- dexterous-manipulation
- pseudo-tactile-sensing
- rgb-d-proprioception
- contact-estimation
- sim2real
- robot-policy
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# NoContactNoWorries: Estimating Contact through Vision and Proprioception for In-Hand Dexterous Manipulation

## Summary
NoContactNoWorries predicts fingertip contact for a LEAP Hand using wrist RGB-D video plus joint state, giving the robot binary pseudo-tactile feedback without tactile sensors. The paper claims this signal can replace simulator or tactile contact for in-hand object reorientation, including real-robot transfer.

## Problem
- Dexterous in-hand manipulation depends on contact feedback, but fingertip tactile sensors add cost, fragility, wiring, calibration, and limited coverage.
- Wrist RGB-D cameras are easier to deploy, yet finger-object contact is often hidden by the hand or object during manipulation.
- The task matters because a contact signal can help policies react to grasp changes, slip, and contact loss without adding custom hardware.

## Approach
- The model predicts a 4-bit binary contact vector, one bit for each fingertip site on the LEAP Hand.
- A frozen RGB-D segmentation encoder extracts spatial visual features from 240×320 RGB and depth frames.
- Current joint angles and commanded joint angles are embedded separately, then used as queries over visual tokens with cross-attention.
- A causal transformer reads an 8-frame window and outputs current fingertip contact probabilities through a sigmoid contact head.
- Training uses simulator contact labels from PhysX; real force-sensitive resistors are used only for evaluation, with a 0.1 N threshold for contact.

## Results
- The contact predictor was trained on 50 simulated rollouts, each 15 s, across 5 training objects; labels cover 4 fingertip sites at 30 Hz.
- In simulation on seen objects, the full model reached F1 scores of 0.93 cuboid, 0.90 pentagonal prism, 0.91 dodecahedron, 0.88 star, and 0.88 stairs.
- In simulation on held-out objects, it reached 0.89 F1 on a hexagonal prism and 0.87 F1 on a letter R.
- On the real LEAP Hand, it reached 0.84 cuboid, 0.83 pentagonal prism, 0.82 dodecahedron, 0.71 star, 0.79 stairs, 0.80 hexagonal prism, and 0.74 letter R.
- Under simulated occlusion analysis on the hexagonal prism, contact regions were occluded in about 61% of frames; the full model scored 0.93 F1 when visible and 0.85 when occluded, while vision-only dropped from 0.79 to 0.51.
- Ablations show the full model beat vision-only, pose-only, no-temporal, and kinematic-depth baselines; for example, on real cuboid data the scores were 0.84 full, 0.72 best pose-only, 0.48 vision-only, 0.69 no temporal modeling, and 0.55 kinematic depth.

## Link
- [https://arxiv.org/abs/2606.24450v1](https://arxiv.org/abs/2606.24450v1)
