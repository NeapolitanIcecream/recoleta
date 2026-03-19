---
source: arxiv
url: http://arxiv.org/abs/2603.14327v1
published_at: '2026-03-15T11:13:04'
authors:
- Yixuan Li
- Le Ma
- Yutang Lin
- Yushi Du
- Mengya Liu
- Kaizhe Hu
- Jieming Cui
- Yixin Zhu
- Wei Liang
- Baoxiong Jia
- Siyuan Huang
topics:
- humanoid-teleoperation
- robot-learning
- benchmarking
- transformer-policy
- motion-retargeting
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System

## Summary
OmniClone is an engineered system for whole-body humanoid robot teleoperation, aimed at achieving robustness, versatility, and low cost simultaneously in real-world deployment. The paper also introduces the fine-grained diagnostic benchmark OmniBench, which is used to reveal imbalances in existing methods across different motion types and to optimize training data and system design accordingly.

## Problem
- Existing whole-body humanoid teleoperation systems usually report only aggregate metrics, mixing different motion modes such as manipulation, squatting, running, and jumping, which obscures critical failure modes.
- Existing systems are often tightly coupled to specific hardware/software configurations, requiring cumbersome calibration across operators and MoCap setups, making stable deployment difficult.
- This matters because whole-body teleoperation is not only a real-time remote control tool, but also a data engine for collecting high-quality demonstrations and training autonomous robot/VLA policies.

## Approach
- Proposes **OmniBench**: a diagnostic benchmark for unseen motions, covering 6 functional motion categories (loco-manipulation、manipulation、squatting、walking、running、jumping), further divided into 18 evaluation categories by difficulty/dynamic intensity.
- Proposes **OmniClone**: a unified Transformer-based whole-body tracking policy that replaces the weaker MLP to better model temporal dependencies; a deployable student policy is trained through teacher-student distillation.
- Uses OmniBench to guide the training data recipe in reverse: the final setup uses about 60% manipulation data, with the remaining 40% balanced between dynamic actions and stable motions to achieve more balanced skill coverage.
- Adds **subject-agnostic refined retargeting** at the system level, dynamically scaling human MoCap data based on the initial calibration frame to reduce morphological mismatch caused by different heights and devices, without requiring per-person manual calibration.
- Adds robust FIFO-queue-based communication and zero-order hold, using UDP to reduce transmission overhead, maintaining smooth control under signal fluctuation/latency, and achieving about 80 ms end-to-end latency; the same policy is also compatible with real-time teleoperation, generated motion playback, and VLA control sources.

## Results
- The paper claims that after system-level improvements, **MPJPE is reduced by more than 66%**, while requiring only **30 hours of motion data** and a **single consumer GPU**; total training cost is about **80 GPU hours** (RTX 4090, broken down above as about 60 hours for the teacher and about 22 hours for student distillation), which is described as “orders of magnitude lower” than comparable methods.
- Across the 18 stratified categories of OmniBench, OmniClone is significantly more balanced than GMT / Twist2: for example, on **Loco-Manip Low**, OmniClone achieves **SR 100%, MPJPE 51.3 mm**, compared with **95%, 180.5 mm** for GMT and **65%, 210.5 mm** for Twist2.
- It also clearly leads on manipulation-related tasks: for example, on **Manip Medium**, OmniClone achieves **SR 100%, MPJPE 20.4 mm**, versus **100%, 54.7 mm** for GMT and **100%, 156.3 mm** for Twist2.
- It maintains strong performance on agile motions: for example, on **Run Medium**, OmniClone achieves **SR 100%, MPJPE 42.0 mm**, compared with **100%, 120.8 mm** for GMT and **100%, 176.9 mm** for Twist2; on **Jump Medium**, OmniClone achieves **SR 100%, MPJPE 34.5 mm**, versus **90%, 105.3 mm** for GMT and **85%, 177.2 mm** for Twist2.
- Ablations show that the Transformer clearly outperforms the MLP: for example, on **Walk Fast**, OmniClone MLP reaches only **SR 20%, MPJPE 111.7 mm**, while OmniClone achieves **SR 100%, MPJPE 63.5 mm**.
- The system can generalize across operators with different body types: a composite loco-manipulation task was completed by **6** participants ranging from **1.47 m–1.94 m**; the paper states that all novice operators were able to complete the task within **5–7 practice attempts**. Another downstream result is that a VLA policy trained on OmniClone data achieves success rates of **85.71%** and **80.00%** on **Pick-and-Place** and **Squat to Pick-and-Place**, respectively.

## Link
- [http://arxiv.org/abs/2603.14327v1](http://arxiv.org/abs/2603.14327v1)
