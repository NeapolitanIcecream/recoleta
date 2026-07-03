---
source: arxiv
url: https://arxiv.org/abs/2607.01938v1
published_at: '2026-07-02T09:32:39'
authors:
- Peng Yun
- Shouwang Huang
- Hao Li
- Jinxi Li
- Jianan Wang
- Bo Yang
topics:
- robot-world-model
- dynamic-manipulation
- 3d-gaussian-splatting
- vision-language-action
- imitation-learning
- physics-based-prediction
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# PhysMani: Physics-principled 3D World Model for Dynamic Object Manipulation

## Summary
PhysMani is a 3D Gaussian world-model system for robots that manipulate moving targets. It predicts physically constrained scene motion online and feeds that motion into a 3D action policy.

## Problem
- Robots need fast 3D motion forecasts to catch, place, push, or insert objects when targets move at speeds near the robot end-effector limit.
- Existing VLAs and video world models often predict 2D-looking futures without reliable 3D geometry or physical motion, which hurts time-sensitive manipulation.
- The paper also addresses a benchmark gap by introducing PhysMani-Bench with 16 dynamic manipulation tasks based on RLBench.

## Approach
- The world model represents the scene with 30,000 3D Gaussians initialized from RGB-D views from 4 fixed cameras.
- A velocity MLP predicts 6 motion components per Gaussian: 3 linear and 3 angular components. The basis construction makes the velocity field divergence-free.
- The model updates online with RGB-D supervision using L1 and SSIM losses. The reported setting uses 50 velocity-update iterations and 7 refinement iterations per step.
- The policy builds on 3D FlowMatch Actor. It lifts RGB-D observations into 4,096 3D visual tokens, retrieves nearby Gaussians with KNN, and injects local predicted velocities through attention tokens.
- The policy predicts future end-effector keyposes with rectified flow, then converts them to robot joint commands through inverse kinematics.

## Results
- On PhysMani-Bench, PhysMani reports the best mean simulation success rate: 45.9±0.8%, compared with 37.8±0.9% for 3DFA, 37.5±1.0% for 3DFA-OF, 35.1±1.7% for 3DDA, 27.1±2.7% for Act3D, 22.5±0.8% for ManiGaussian, and 8.3±0.2% for pi0.5.
- The largest listed task gain is Drop to Hoop: 71.7±3.1% for PhysMani versus 30.8±3.1% for 3DFA and 27.5±5.4% for 3DFA-OF.
- Pick Cube reaches 84.2±3.1% for PhysMani versus 70.0±6.1% for 3DFA and 63.3±6.6% for 3DDA.
- Push Button reaches 57.5±3.5% for PhysMani versus 55.8±4.2% for 3DFA and 54.2±3.1% for 3DFA-OF.
- PhysMani does not lead every task in the visible table: Beat Buzz is 78.3±4.2% versus 82.5±2.0% for 3DFA, and Insert Peg is 37.5±6.1% versus 68.3±6.6% for 3DDA.
- Online world-model optimization is reported at about 200 ms per update on one RTX 4090 GPU, with moving target speeds up to 2 m/s in the benchmark setup.

## Link
- [https://arxiv.org/abs/2607.01938v1](https://arxiv.org/abs/2607.01938v1)
