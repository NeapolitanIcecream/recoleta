---
source: arxiv
url: http://arxiv.org/abs/2604.17245v1
published_at: '2026-04-19T04:12:04'
authors:
- Zhuoheng Li
- Qingquan Lin
- Checheng Yu
- Qiangyu Chen
- Zhiqian Lan
- Lutong Zhang
- Hongyang Li
- Ping Luo
topics:
- dexterous-manipulation
- robot-hand
- remote-actuation
- tactile-sensing
- stereo-vision
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# MM-Hand: A 21-DOF Multi-modal Modular Dexterous Robotic Hand with Remote Actuation

## Summary
MM-Hand is an open-source 21-DOF dexterous robot hand that moves its fingers through long tendon-sheath cables from a remote motor hub. The design trades some delay and friction for lower hand mass, more internal space, easier maintenance, and more sensing in the hand.

## Problem
- High-DOF robot hands need many actuators and sensors, but putting motors inside the hand adds mass, uses up space, and creates heat near the end effector.
- Remote tendon actuation can move motors away from the hand, but long tendon-sheath paths add friction, hysteresis, and arm-motion-dependent length changes that hurt control accuracy.
- A practical research hand also needs to be easy to build, repair, and extend with sensing hardware.

## Approach
- The paper builds a **21-DOF, 5-finger hand** with remote tendon-driven actuation, mostly using **single-tendon spring-return joints** and an **antagonistic dual-tendon** design for thumb base rotation.
- It analyzes two main transmission effects: **tendon length change** from total sheath bending angle and **friction loss** that grows exponentially with bending angle under a capstan-style model.
- The mechanical design is **modular and 3D-printed**, with split phalanges, internal routing space, and **quick tendon connectors** in the palm so fingers or sheaths can be replaced without rerouting the full system.
- The sensing stack includes **joint encoders, tactile sensors, motor-side feedback, and in-palm stereo cameras**. Control uses **joint-mounted absolute encoders with PID closed-loop control** instead of relying on an accurate feedforward tendon model.
- The system uses **software pretensioning** for spring-return joints, reeling tendons back when encoder readings indicate slack.

## Results
- The hand reaches **25 N fingertip force** with a **1 m remote sheath** and about **33 N** with a **0.1 m sheath**, so the longer routing costs about **8 N** of peak force in this test.
- In step-response joint control, the reported **steady-state error is below 0.1°**, with about **0.2 s delay** between motor actuation onset and joint motion onset because of tendon-sheath friction.
- Dynamic tracking was tested with a **0.5 Hz sinusoidal command** on one joint for **over 20 s**, both with the arm fixed and while the arm moved through the workspace. Tracking got worse during arm motion, but the paper states that friction-caused delay had a larger effect than arm-motion disturbance.
- Friction experiments tested **4 sheath types**, **0° to 180° wrap angles**, and **10 to 100 mm disk diameters**. The measured kinetic friction followed the paper's predicted **exponential trend** with bending angle, and the authors selected a **metal spring tube** for later tests based on balanced friction and simplicity.
- The hand also demonstrated **in-palm stereo depth sensing** using **RAFT-Stereo**, but the excerpt gives **no quantitative depth accuracy numbers**.

## Link
- [http://arxiv.org/abs/2604.17245v1](http://arxiv.org/abs/2604.17245v1)
