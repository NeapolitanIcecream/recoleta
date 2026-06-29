---
source: arxiv
url: http://arxiv.org/abs/2604.15013v1
published_at: '2026-04-16T13:41:07'
authors:
- Joonho Koh
- Haechan Jung
- Nayoung Kim
- Wook Ko
- Changjoo Nam
topics:
- dexterous-manipulation
- teleoperation
- force-feedback
- robot-data-collection
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands

## Summary
DEX-Mouse is a low-cost hand-held interface for collecting dexterous robot-hand demonstrations on real hardware. It aims to make data collection portable, calibration-free across operators, and more physically aligned with the target robot by adding force feedback and an attached forearm-mounted setup.

## Problem
- Dexterous robot learning needs large amounts of real demonstration data that match the robot's actual kinematics and contact dynamics.
- Simulation and video pipelines lose fidelity through sim-to-real error, occlusion, and human-to-robot retargeting mismatch.
- Existing teleoperation devices such as MoCap gloves and other hand-held systems often need per-user calibration, custom hardware, fixed lab setups, or do not support multiple robot hands well.

## Approach
- The paper builds a portable teleoperation device from off-the-shelf parts for under **USD 150**, with no per-operator calibration and no structural modification for different users.
- The interface uses tendon-driven fingers, a direct-driven thumb, and current-based kinesthetic force feedback so the user feels resistance when the robot hand is blocked by contact.
- It supports an **attached configuration** where the robot hand is mounted on the operator's forearm, plus a standard spatially separated teleoperation mode. The attached mode is meant to collect robot-aligned data with less coordinate mismatch.
- Hand motion is mapped to the robot with simple proportional retargeting instead of complex morphology-dependent retargeting. The firmware runs at **100 Hz**; a VIVE tracker provides global pose, and an onboard camera records aligned RGB at **30 Hz**.

## Results
- In a user study with **8 participants** across **3 interfaces** and **2 collection configurations**, DEX-Mouse in the attached setup reached **86.67%** overall success with **10.05 s** average completion time.
- Under the same attached setup, DEX-Mouse beat DOGlove and Manus glove on overall average success: **86.67%** vs **77.5%** and **62.5%**. It also had the fastest attached completion time: **10.05 s** vs **11.67 s** and **11.93 s**.
- Task breakdown for DEX-Mouse attached: **95.0%** success / **5.57 s** on pick-and-place, **72.5%** / **14.29 s** on peg-in-hole, and **92.5%** / **10.29 s** on hammering.
- DEX-Mouse teleoperation was worse than its attached mode: **52.5%** overall success and **18.77 s** average time, compared with **86.67%** and **10.05 s** when attached.
- Across all interfaces, attached collection outperformed remote teleoperation on overall average success and speed: **75.56%** and **11.22 s** vs **46.39%** and **19.42 s**.
- The paper also claims the attached configuration lowered perceived operator workload across compared interfaces, but the excerpt does not include the full workload table or exact questionnaire values.

## Link
- [http://arxiv.org/abs/2604.15013v1](http://arxiv.org/abs/2604.15013v1)
