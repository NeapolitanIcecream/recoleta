---
source: arxiv
url: http://arxiv.org/abs/2604.03781v1
published_at: '2026-04-04T16:07:33'
authors:
- Siddhartha Kapuria
- Mohammad Rafiee Javazm
- Naruhiko Ikoma
- Joga Ivatury
- Mohammad Ali Nasseri
- Nassir Navab
- Farshid Alambeigi
topics:
- robot-data-collection
- medical-robotics
- vision-language-action
- surgical-autonomy
- multimodal-dataset
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research

## Summary
OpenRC is an open-source robotic colonoscopy platform that retrofits standard scopes and records synchronized video, operator actions, robot state, and distal tip pose. The paper’s main contribution is the combination of low-cost hardware validation and a multimodal dataset for closed-loop autonomy research in colonoscopy.

## Problem
- Colonoscopy research often splits perception and control: many datasets have video only, while robotic systems often lack shared, synchronized logs for actions, actuation, and tip motion.
- This blocks reproducible work on closed-loop robotic colonoscopy, control-aware perception, and vision-language-action training, where observations, actions, and state must be aligned.
- The problem matters because colonoscopy is central to colorectal cancer screening, yet adenoma miss rates can reach **34%**, and operator variability and device limits still affect outcomes.

## Approach
- The authors build a modular robotic retrofit for conventional colonoscopes with **3 clinically relevant DoFs**: insertion/retraction and two distal bending axes.
- The system logs four main modalities on a shared ROS 2 stack: colonoscope video, operator command vectors, motor/actuation state, and **6-DoF EM-tracked** distal tip pose.
- They validate timing and motion consistency with controlled sinusoidal excitation, then estimate modality offsets and resample all streams to **30 Hz** using video as the reference.
- They collect teleoperated data in two colon phantoms and store the dataset in **LeRobot 2.1** format, including task instructions and episodes for navigation, failures, and recovery.

## Results
- The full framework, excluding the EM tracker, can be assembled for **under $5,000 USD**.
- The dataset contains **1,894 episodes** and about **19 hours** of teleoperated colonoscopy data across **10 task variations**.
- The dataset includes **142 failure episodes** and **141 recovery episodes**, covering cases such as lumen loss, wall contact, and fold engagement.
- In timing characterization, estimated offsets relative to control actions are about **102 ms** for motor encoder state, **435 ms** for EM tracking, and **412 ms** for optical-flow-derived motion.
- After alignment, the median residual lag between **operator action and actuation state** is **55.6 ms** (about **1.6 frames** at 30 Hz).
- After alignment, the residual lag between **actuation state and distal tip pose** is centered at **0.0 ms**. The paper does not report task-performance gains against an autonomy baseline; its strongest concrete claim is that it provides an open, synchronized platform and dataset that prior colonoscopy resources did not combine.

## Link
- [http://arxiv.org/abs/2604.03781v1](http://arxiv.org/abs/2604.03781v1)
