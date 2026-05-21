---
source: arxiv
url: https://arxiv.org/abs/2604.25126v1
published_at: '2026-04-28T02:04:50'
authors:
- Ethan Foong
- Yunshuang Li
- Hao Jiang
- Gaurav S. Sukhatme
- Daniel Seita
topics:
- dexterous-manipulation
- sequential-manipulation
- resource-aware-grasping
- sim2real
- robot-benchmark
- reinforcement-learning
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness

## Summary
HANDFUL trains a LEAP Hand to grasp one object while leaving fingers available for a later action. It targets sequential dexterous manipulation, where a stable first grasp can block the second task.

## Problem
- The paper addresses two-step dexterous tasks: grasp an object, then push, press, twist, pull, or pick another object while still holding the first.
- This matters because grasps optimized only for stability can use the fingers or palm space needed for the next action.
- Prior dexterous manipulation work often studies one object or one skill, so it misses finger allocation across a sequence.

## Approach
- HANDFUL treats fingers as limited resources. Some fingers are active for the first grasp, while other fingers are kept inactive for the second task.
- The grasp reward adds an active-finger contact reward and an inactive-finger contact-force penalty, so selected fingers hold the object and unused fingers avoid contact.
- It trains 9 grasp policies from one- and two-finger combinations on a 4-finger LEAP Hand, with two initial hand poses.
- For each second task, it trains second-stage policies from terminal grasp states, then uses a 3-stage curriculum to keep the best candidates: 9 policies in C0, 6 survivors in C1, and 3 survivors in C2.
- For real deployment, it retrieves a successful simulated trajectory whose initial object pose best matches the observed real pose, using SAM2 segmentation and fused point clouds.

## Results
- In simulation over 5 seeds, HANDFUL reached success rates of 69.90±5.54% on Push Object, 77.75±2.15% on Press Button, 61.52±5.47% on Twist Knob, 78.94±1.77% on Pull Drawer, and 76.54±3.63% on Pick Second.
- The first-stage grasping policies reached 94.67±2.60% average grasp success when trained only for grasping.
- Removing finger constraints reduced success to 66.69±5.66% on Push Object, 44.26±40.58% on Press Button, 49.44±5.73% on Twist Knob, 58.99±17.36% on Pull Drawer, and 0.00±0.00% on Pick Second.
- The phase-based single-environment baseline reached 32.38±6.36% on Push Object, 10.08±19.23% on Press Button, and 0.00±0.00% on Twist Knob, Pull Drawer, and Pick Second.
- Curriculum training kept similar final success to non-curriculum training while cutting second-stage training from 90 million steps to 54 million steps, a 40% reduction.
- The paper reports real LEAP Hand validation, but the excerpt gives no real-world success rates.

## Link
- [https://arxiv.org/abs/2604.25126v1](https://arxiv.org/abs/2604.25126v1)
