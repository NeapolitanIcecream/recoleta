---
source: arxiv
url: http://arxiv.org/abs/2603.07949v2
published_at: '2026-03-09T04:30:57'
authors:
- Zihao Zheng
- Sicheng Tian
- Hangyu Cao
- Chenyue Li
- Jiayu Chen
- Maoliang Li
- Xinhao Sun
- Hailong Zou
- Guojie Luo
- Xiang Chen
topics:
- edge-cloud-inference
- vision-language-action
- embodied-ai
- robotics-systems
- dynamic-offloading
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# RAPID: Redundancy-Aware and Compatibility-Optimal Edge-Cloud Partitioned Inference for Diverse VLA Models

## Summary
RAPID is an edge-cloud collaborative inference framework for Vision-Language-Action (VLA) models that uses robot kinematic/dynamic signals, rather than visual confidence, to decide when to offload inference to the cloud. It aims to address both unstable partitioning under visual noise and the neglect of action-stage redundancy in embodied tasks, thereby improving real-time performance and compatibility.

## Problem
- VLA models have large parameter counts and slow inference, making it difficult to meet the real-time requirements of robot control when running directly on edge devices.
- Existing dynamic edge-cloud partitioning methods mostly rely on visual features or action entropy, making them easily disrupted by visual noise, occlusion, and environmental changes, with poor cross-environment compatibility.
- Existing methods ignore step-wise action redundancy in embodied tasks: many "steady approach" actions are not important, and frequent interruption or offloading wastes compute and disrupts action continuity.

## Approach
- Use **instantaneous joint acceleration** to represent "compatibility/abnormal motion changes": when nonlinear changes such as sudden stops, turns, or obstacle avoidance occur during high-speed robot motion, cloud-side replanning is more likely to be needed.
- Use **joint torque changes** to represent "redundancy/critical interaction": during smooth approach phases, torque changes are small and action redundancy is high; during contact/grasp/manipulation phases, torque changes spike and action redundancy is low, making them more worthwhile to offload to the cloud.
- Apply sliding-window normalization to both types of signals to obtain anomaly scores; then dynamically assign weights based on current joint velocity: trust acceleration more at high speed, and trust torque more during low-speed interaction.
- Use a dual-threshold trigger to decide whether to offload, combined with asynchronous multi-rate processing, action preemption, and a cooldown mechanism to avoid frequent network requests and action interruptions.
- The core idea can be summarized as: **changes in the robot body's own motion/force are better suited than whether the image "looks uncertain" for deciding the edge-cloud division of labor.**

## Results
- The paper claims that, compared with Edge-Only VLA and vision-based baselines (ISAR mentioned in the text / SAFE in the table), RAPID can improve **accuracy by up to 15.8%** and achieve **up to 1.73× inference speedup**, with only **5\~7%** additional system overhead.
- On the simulation benchmark, RAPID's total latency is **222.9 ± 11.4 ms**, better than vision-based SAFE's **377.7 ± 26.2 ms**, about **1.69×** faster; it is also better than Edge-Only's **782.5 ± 28.5 ms**, about **3.51×** faster.
- In resource allocation, RAPID reduces edge-side load to **2.4GB**, lower than SAFE's **4.7GB** and Edge-Only's **14.2GB**; the corresponding edge-side latency is **139.4 ms**, significantly lower than SAFE's **315.2 ms**.
- The visual baseline degrades noticeably under noise: total latency rises from **395.4 ms** in the standard environment to **520.6 ms** under visual noise, and further to **685.3 ms** in interference scenarios, supporting the authors' argument that visually driven partitioning is easily affected by noise.
- Action redundancy analysis shows that redundant actions account for more than **80%**: Pick & Place **82.5%**, Drawer Opening **86.4%**, Peg Insertion **81.2%**; the average attention weights of these redundant actions are only **0.005–0.008**, while critical actions are **0.058–0.076**. This provides support for the design of "processing redundant phases at the edge and critical phases in the cloud."

## Link
- [http://arxiv.org/abs/2603.07949v2](http://arxiv.org/abs/2603.07949v2)
