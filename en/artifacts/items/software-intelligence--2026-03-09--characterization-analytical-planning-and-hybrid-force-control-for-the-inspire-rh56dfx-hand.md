---
source: arxiv
url: http://arxiv.org/abs/2603.08988v1
published_at: '2026-03-09T22:25:38'
authors:
- Xuan Tan
- William Xie
- Nikolaus Correll
topics:
- dexterous-robot-hand
- grasp-planning
- hybrid-force-control
- sim2real-modeling
- contact-rich-manipulation
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Characterization, Analytical Planning, and Hybrid Force Control for the Inspire RH56DFX Hand

## Summary
This paper transforms the commercial Inspire RH56DFX dexterous hand from a “black-box device” into a reproducible research tool: it first performs force and dynamics calibration, then uses analytical planning and hybrid force control to improve grasping and insertion performance. Its significance is that a low-cost commercial hand can achieve more stable and interpretable precise manipulation without retraining models or modifying hardware.

## Problem
- The hand’s native force feedback consists of uncalibrated raw values, making it difficult to use directly for scientific experiments or fine control, so researchers cannot reliably know the true contact force.
- The hand has about **66 ms** of latency, and high-speed contact produces extremely large force overshoot. The paper reports force-limit overshoot as high as **+1618%**, which can damage fragile objects and cause contact tasks to fail.
- The fingers are underactuated and coupled, and closing them causes width-dependent translation and rotation, with maximum tilt change reaching **49°**. Therefore, “closing directly to a target width” does not naturally produce a stable antipodal grasp.

## Approach
- First, perform **hardware characterization**: linearly calibrate raw force readings into newtons, achieving fitted linearity of **R² > 0.98** for three key fingers; also measure a system update rate of **163 Hz**, a control-to-sensing latency of about **66 ms**, and systematically test force overshoot at different speeds.
- Propose **hybrid closed-loop speed-force control**: move quickly while approaching in free space, then switch to low speed near the contact region (with contact speed fixed at **v≤25**). Put simply, it is “fast when far away, slow when nearly touching,” to reduce impact and overshoot caused by latency.
- Build and calibrate a **MuJoCo simulation model**, and through offline scanning of hand kinematics, establish an analytical mapping from “target object width” to “finger closure amount and tilt angle”; use single-variable root solving to quickly obtain the corresponding grasp configuration.
- Use a **QP/differential IK** version for structural validation, showing that the geometric relationships produced by the analytical planner are consistent with numerical optimization, while the analytical method is more accurate in fingertip target error.
- The overall scheme is **modular**: the low-level control and planning can directly interface with external object detectors or vision-language models that provide width, force, and high-level task information.

## Results
- Force calibration results show that the linear fits for three fingers reach **R²=0.987、0.986、0.993**, indicating that the raw force signals can be converted into physical units fairly reliably.
- Dynamic tests show that the system has **66 ms** latency; under a step response to target position 500, the **rise time is 0.18–0.30 s** and the **settling time is 0.27–0.43 s**, with no obvious deceleration near the target, which explains the large overshoot during high-speed collision.
- The paper states that force-limit overshoot under high-speed contact can reach as high as **+1618%**; by contrast, the overshoot of the hybrid controller is close to that of constant low speed **v=25**, indicating that “fast first, then slow” can significantly suppress impact, though the excerpt does not provide a complete itemized numerical table.
- The analytical grasp planner covers a two-finger pinch width range of **0–110 mm**, and **0–100 mm** for three-/four-/five-finger pinch; by construction, the analytical method achieves zero target-point error, while the QP version still has **2.4–3.3 mm** average fingertip error.
- On the **peg-in-hole** insertion task, the method achieves a **65%** success rate, clearly outperforming the wrist-force-only baseline of **10%**.
- Across **300** grasps on **15** physically diverse objects, it achieves an **87%** success rate and outperforms plan-free grasps and learned grasps; the excerpt does not provide the full percentages for those comparison methods.

## Link
- [http://arxiv.org/abs/2603.08988v1](http://arxiv.org/abs/2603.08988v1)
