---
source: arxiv
url: http://arxiv.org/abs/2603.28542v1
published_at: '2026-03-30T15:04:13'
authors:
- Feiyu Jia
- Xiaojie Niu
- Sizhe Yang
- Qingwei Ben
- Tao Huang
- Feng zhao
- Jingbo Wang
- Jiangmiao Pang
topics:
- dexterous-manipulation
- teleoperation
- tactile-feedback
- robot-data-collection
- haptic-glove
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Feel Robot Feels: Tactile Feedback Array Glove for Dexterous Manipulation

## Summary
TAG is a low-cost teleoperation glove for dexterous manipulation that combines precise 21-DoF hand tracking with high-resolution fingertip tactile feedback. It targets contact-rich robot teleoperation and demonstration collection, where motion errors and missing touch feedback reduce task success and data quality.

## Problem
- Dexterous teleoperation still struggles with two practical limits: hand tracking errors during human-to-robot motion mapping, and weak or missing tactile feedback during contact.
- Vision- and VR-based systems depend heavily on camera view, alignment, and pose estimation, while many glove sensors drift, wear out, or lose accuracy near electromagnetic noise.
- For robot learning, poor teleoperation fidelity matters because bad demonstrations reduce physical consistency and make collected data less useful for imitation learning.

## Approach
- TAG uses 21 non-contact magnetic encoders to track full-hand joint motion. Each joint angle is recovered from 3-axis magnetic field measurements, which gives drift-free tracking and cancels some common-mode errors through ratio-based angle computation.
- Each fingertip has a compact **32-actuator** electro-osmotic tactile array in a **2 cm²** module. The module supports spatial tactile patterns so the operator can feel where contact occurs, not only that contact happened.
- The glove provides two feedback modes: **shape mapping**, which transfers the robot fingertip contact pattern onto the human fingertip, and **pressure mapping**, which converts stronger contact into a larger active tactile area.
- The system is built for real robot use and cross-platform compatibility. The paper tests it with multiple robot tactile sensing modalities and two teleoperation setups, including G1 + Inspire Hand and UR5e + XHand.
- TAG is designed to be cheap and reproducible: the full system cost is reported as **below $500**, versus commercial haptic gloves above **$5,000**.

## Results
- Joint tracking accuracy is strong: the paper reports **sub-degree error**, with design-level accuracy below **0.8°**, a measured maximum tracking error within **±0.35°**, and long-run error distribution with **σ = 0.215°**.
- Long-term stability is good in a **1000 s** test: the average discrepancy between the first and last **30 s** windows is about **0.02°**, indicating very low drift.
- EMI robustness is much better than a commercial baseline in the reported setup: near an active PC chassis, **Manus glove** deviation reaches **5.69°**, while **TAG** stays within **0.24°**.
- Hardware density is high for a glove device: **21 DoF** hand capture and **32 tactile actuators per fingertip** in a module measuring **29 × 18.4 × 5.5 mm**.
- In a user study with **5 participants** on contact shape discrimination, **single-point contacts reached 100% accuracy**. The excerpt also states that **two-point** and **plane** contacts had **23/25** correct identifications each.
- The excerpt claims improved success in contact-rich teleoperation tasks and more reliable demonstrations for imitation learning, but the provided text does not include the final task success numbers or learning metrics.

## Link
- [http://arxiv.org/abs/2603.28542v1](http://arxiv.org/abs/2603.28542v1)
