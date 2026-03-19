---
source: arxiv
url: http://arxiv.org/abs/2603.09121v1
published_at: '2026-03-10T02:55:27'
authors:
- Yifan Han
- Zhongxi Chen
- Yuxuan Zhao
- Congsheng Xu
- Yanming Shao
- Yichuan Peng
- Yao Mu
- Wenzhao Lian
topics:
- vision-language-action
- human-in-the-loop
- dexterous-manipulation
- robot-learning
- teleoperation
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# DexHiL: A Human-in-the-Loop Framework for Vision-Language-Action Model Post-Training in Dexterous Manipulation

## Summary
DexHiL is a human-in-the-loop framework for post-training vision-language-action models in dexterous manipulation, combining offline demonstration, online human takeover for correction, and intervention-aware reweighted training. The paper’s central claim is that for high-DOF dexterous hand tasks, a small amount of high-value human corrective data is more effective than simply adding more offline data.

## Problem
- Existing VLA models have generalization ability in general manipulation, but when transferred to dexterous hand tasks, the action space is high-dimensional, contact is complex, and errors accumulate easily, making it difficult to achieve stable convergence through offline finetuning alone.
- Traditional teleoperation/demonstration systems suffer from kinematic misalignment between the human hand and the robot hand, making it hard to collect high-fidelity, fine-grained dexterous manipulation data, especially for online incremental correction.
- Covariate shift occurs during robot execution; without an immediate recovery mechanism, small errors can push the policy into out-of-distribution states and cause failure, which is especially critical for real-world high-DOF manipulation.

## Approach
- Proposes an **integrated arm-hand HiL system**: the arm uses the 6D pose of an ArUco cube for lightweight teleoperation, while the hand uses a motion-capture glove plus a learned retargeting network to control the dexterous hand, enabling unified online takeover of both arm and fingers.
- Designs a **two-stage finger retargeting** method: first learning a stable motion manifold for the four fingers, then freezing the four fingers and separately learning a residual for the thumb, avoiding collapse into a “pinch grasp” posture when learning all five fingers jointly.
- Uses **asynchronous multithreaded control**: policy inference at 20Hz, manual arm teleoperation at 30Hz, and hand teleoperation at 90Hz; when the system is about to fail, a human can take over in real time and provide a corrective trajectory.
- Uses **intervention-aware reweighting** in training: sparse but high-value intervention samples are upweighted through importance sampling; the target intervention ratio is set to 0.5 to strengthen recovery learning.
- Uses **offline warm-up + online DAgger-style iteration**, and retains only the recovery segments from “the last intervention to task completion,” reducing policy oscillation caused by inconsistent trajectories.

## Results
- On two real-robot tasks, DexHiL improves **average success rate by 25%** over a standard offline finetuning baseline matched for data volume (**main result from the abstract**).
- The paper also reports that after **3 rounds** of online iteration, compared with the “equal-data offline training” baseline, success rates improve by **20%** and **30%** on the two tasks, respectively.
- **Tissue Extraction**: in Round 3, DexHiL reaches a **95%** success rate, outperforming **DAgger\*** at **80%** and the offline baseline at **75%**; evaluation uses **20** independent real-robot trials per task.
- **Plush Toy Grasping**: in Round 3, DexHiL reaches **65%**, while **DAgger\*** achieves **20%** and the offline baseline **35%**.
- Training/data setup: initially uses **60 offline trajectories** for warm-up; afterward, each round adds **10 trajectories** per task, compared against Offline-40/50/60 baselines with the same data budget.
- Implementation details indicate that the base VLA is **Being-H0.5**; initial full training uses **8×NVIDIA H100** and **60k iterations**, while finetuning on online interaction data uses **1×H100**.

## Link
- [http://arxiv.org/abs/2603.09121v1](http://arxiv.org/abs/2603.09121v1)
