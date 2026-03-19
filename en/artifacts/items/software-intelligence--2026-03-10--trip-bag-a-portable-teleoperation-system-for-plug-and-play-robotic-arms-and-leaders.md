---
source: arxiv
url: http://arxiv.org/abs/2603.09226v1
published_at: '2026-03-10T05:49:47'
authors:
- Noboru Myers
- Sankalp Yamsani
- Obin Kwon
- Joohyung Kim
topics:
- robot-teleoperation
- data-collection
- imitation-learning
- portable-robotics
- bimanual-manipulation
relevance_score: 0.17
run_id: materialize-outputs
language_code: en
---

# TRIP-Bag: A Portable Teleoperation System for Plug-and-Play Robotic Arms and Leaders

## Summary
TRIP-Bag proposes a portable robot teleoperation and data collection system that fits inside a commercial suitcase, aiming to rapidly collect high-fidelity manipulation demonstrations in real, diverse environments. It attempts to combine the data quality of traditional teleoperation with the mobility of handheld solutions.

## Problem
- Robot manipulation learning lacks large-scale, high-quality, cross-environment demonstration data, which directly limits the development of data-driven policies and robotic foundation models.
- Existing in-the-wild collection approaches mostly rely on handheld devices, gloves, or vision estimation, and often suffer from an **embodiment gap**—that is, the human operator’s action space does not match that of the target robot—so the data requires additional retargeting and calibration.
- Traditional high-fidelity teleoperation systems are typically confined to laboratories, with high costs for transport, assembly, wiring, and calibration, making large-scale deployment in real-world settings difficult.

## Approach
- The core idea is a **teleoperation station in a suitcase**: two plug-and-play follower arms, two scaled puppeteer leaders, three RGB-D cameras, and a compute unit are all packed into a standard commercial suitcase.
- It uses **direct joint-to-joint mapping** for bimanual teleoperation: the operator moves the leaders, and the follower robots track the corresponding joints, reducing the embodiment gap and directly recording high-fidelity action data.
- The system is **plug-and-play**: both the robotic arms and leaders can be quickly connected and removed. Experts took about 200 seconds on average from opening the suitcase to first operation, and the paper claims deployment in under 5 minutes.
- The software is built on ROS2/PAPRLE and includes leader/follower interfaces, teleoperation nodes, real-time self-collision detection, and feedback signals to the operator when there is tracking error, obstacle collision, or joint limit violation.
- Data is recorded as synchronized multimodal observations: 3 RGB-D image streams, joint position/velocity/torque states, and joint-command actions; during collection, cameras run at 30Hz, joint states at 125Hz, and synchronized logging at 50Hz.

## Results
- System-level data collection scale: the authors used TRIP-Bag to collect **1238 demonstrations** across **22 different environments**, covering diverse real-world settings such as kitchens and offices.
- Deployment efficiency: evaluated in **8 different environments**, experts required an average setup time of **200 seconds** from opening the suitcase to being ready for the first teleoperation, i.e. about **3.3 minutes**, supporting the claim of deployment within 5 minutes.
- Portability metrics: the full system weighs **29.8 kg**, which fits within standard airline checked-baggage overweight allowance; the suitcase dimensions are **690 × 440 × 275 mm**, and the paper shows examples of overseas air transport and on-site use.
- Non-expert usability: the authors collected **200 demonstrations** from **10 non-expert users**; each watched a **3-minute** instructional video first, then performed **10 attempts per task**. The paper explicitly states that **all 10 participants ultimately succeeded on Task 1**. The success rate for Task 2 also improved over repeated trials, while completion time decreased, though no finer-grained per-round numerical table was provided.
- Learning feasibility validation: the authors trained the baseline policy **ACT (Action Chunking Transformer)** on the full dataset, training each task separately. Inputs were **3 RGB-D streams + current joint states**, and outputs were future joint trajectories; training used **2 NVIDIA A40 GPUs per task**, and inference ran on an **RTX 4070 Laptop GPU**.
- Quantitative performance reporting is limited: the paper does not report policy success rates, numerical comparisons with methods such as ALOHA/UMI, or SOTA metrics on standard benchmarks; the strongest concrete conclusion is that the trained policies **can complete two tasks and exhibit regrasping and task-consistent behaviors**, indicating that the collected data is usable for learning.

## Link
- [http://arxiv.org/abs/2603.09226v1](http://arxiv.org/abs/2603.09226v1)
