---
source: arxiv
url: http://arxiv.org/abs/2603.08988v1
published_at: '2026-03-09T22:25:38'
authors:
- Xuan Tan
- William Xie
- Nikolaus Correll
topics:
- dexterous-manipulation
- robot-hand-control
- grasp-planning
- force-control
- mujoco
- sim2real
relevance_score: 0.52
run_id: materialize-outputs
language_code: en
---

# Characterization, Analytical Planning, and Hybrid Force Control for the Inspire RH56DFX Hand

## Summary
This paper transforms the commercial Inspire RH56DFX dexterous hand from a "black-box hardware" device into a researchable, interpretable, and deployable manipulation platform, centered on calibration, analytical grasp planning, and hybrid force control. Its focus is that even without learning-based methods or hardware modifications, the hand's reliability in precision grasping and contact tasks can be significantly improved.

## Problem
- The dexterous hand natively provides only uncalibrated force/proprioceptive signals, making measurable, repeatable scientific experiments and precision manipulation difficult.
- The fingers have about **66 ms** of latency, and high-speed contact produces severe force overshoot; the paper reports force-limit overshoot of up to **+1618%**, leading to unstable collisions.
- Its underactuated, coupled linkage structure means that "closing directly based on object width" does not work; different widths require substantial pose compensation, and without modeling this, grasps become misaligned.

## Approach
- First, perform **hardware characterization**: linearly calibrate the raw force readings `0-1000` into newtons, obtaining highly linear fits for the index/middle/thumb flexion actuators with **R²>0.98**, thereby producing usable force feedback.
- Measure dynamic properties: the actuators show about **66 ms** delay between command issuance and the first sensor reading, and there is almost no active deceleration near the target, so high-speed impacts with objects produce severe overshoot because the system "cannot brake in time."
- Build and calibrate a **MuJoCo** model, sweep the hand kinematics offline, and establish an analytical mapping of "**object width -> finger closure amount and tilt angle**"; use fast single-variable root solving to find configurations matching the target width, while compensating for width-dependent tilt up to **49°** and fingertip displacements of about **7 mm** upward and **12 mm** sideways.
- Design a **hybrid closed-loop speed-force controller**: approach quickly in free space, then switch to low speed before contact (contact speed fixed at `v<=25`); the switching point is set to `q_sw=q_g+25`, where the 25-unit buffer comes from statistics over **800 trials**, providing about **3.3σ** margin for the highest-speed contact-onset variation of **σ≈7.5** command units.
- Additionally, use a QP / differential IK planner for structural validation, showing that it produces nearly the same width-dependent poses as the analytical method, but the analytical method can hit target fingertip positions with "zero construction error," making it better suited for precision pinching.

## Results
- For force calibration, the linear fits for the three actuator channels reach **R²=0.987 / 0.986 / 0.993** (index/middle/thumb flexion), indicating that the raw force signals can be stably mapped to physical units.
- For dynamic response, the system transmission and sensing delay is about **66 ms**; step-response rise time is about **0.18-0.30 s**, and settling time is about **0.27-0.43 s**. Based on this, the authors explain the root cause of severe overshoot during high-speed contact and point out that the original hand can show force-limit overshoot up to **+1618%** at high speed.
- In task performance, on the **peg-in-hole** task, hybrid force control achieves **65%** success, significantly higher than the wrist-force-only baseline of **10%**.
- In grasping, across **300** grasps on **15** physically diverse objects, analytical planning + hybrid control achieves **87%** success and outperforms the **plan-free grasping** and **learning-based grasping** baselines; the abstract does not provide specific percentages for those baselines.
- In planning capability, the achievable width range for two-finger pinching is **0-110 mm**, while the range for 3/4/5-finger planar pinching is about **7-100 mm** (elsewhere the paper states 0-100 mm, while the main text gives 7-100 mm, indicating a slight inconsistency); compared with QP, the analytical method avoids average residual fingertip errors of **2.4-3.3 mm**.
- The authors also claim that the method has **sim2real validation**, is modular and can connect to external object detectors / vision-language models, and has been **open-sourced**, but the excerpt does not provide more detailed quantitative ablations.

## Link
- [http://arxiv.org/abs/2603.08988v1](http://arxiv.org/abs/2603.08988v1)
