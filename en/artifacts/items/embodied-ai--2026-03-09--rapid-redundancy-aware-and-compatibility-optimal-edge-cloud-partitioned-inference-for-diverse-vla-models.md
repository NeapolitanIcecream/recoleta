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
- vision-language-action
- edge-cloud-inference
- kinematic-triggering
- robot-systems
- latency-optimization
relevance_score: 0.8
run_id: materialize-outputs
language_code: en
---

# RAPID: Redundancy-Aware and Compatibility-Optimal Edge-Cloud Partitioned Inference for Diverse VLA Models

## Summary
RAPID proposes an edge-cloud collaborative inference framework for VLA models that uses robot proprioceptive kinematics, rather than visual confidence, to decide when to offload inference to the cloud. Its goal is to maintain compatibility and action continuity under diverse environmental noise while reducing latency and minimizing ineffective cloud calls.

## Problem
- VLA models have large parameter sizes and slow edge-side inference, making it difficult to satisfy the real-time requirements of robot control, hence the need for edge-cloud collaborative inference.
- Existing dynamic partitioning methods mostly rely on environmental features such as visual entropy, making them prone to false triggers from visual noise, occlusion, and interference, with poor cross-environment compatibility.
- Existing methods ignore the step-wise action redundancy in embodied tasks, leading to frequent interruptions during stages that could otherwise be executed smoothly on the edge, increasing communication and inference overhead.

## Approach
- Use **joint acceleration** and **joint torque change**, two kinds of proprioceptive signals independent of environmental vision, to replace visual entropy as the trigger basis for edge-cloud partitioning.
- Design two scoring mechanisms: one uses sliding-window statistical normalization of acceleration anomaly scores to detect nonlinear motion changes such as task switching, sudden stops, and obstacle avoidance; the other uses the sliding mean of torque changes and normalized anomaly scores to estimate low-redundancy actions corresponding to critical interaction stages.
- Dynamically allocate the weights of the two signal types according to real-time joint velocity: acceleration is emphasized during high-speed motion, while torque is emphasized during low-speed contact/manipulation, thereby forming an action-importance score and triggering dual-threshold offloading.
- At the system implementation level, introduce asynchronous multi-rate processing, action preemption, and a cooldown mechanism: sensors monitor at high frequency while control executes at low frequency; once a critical stage is detected, the old action chunk is terminated and a new action chunk is requested from the cloud, while preventing continuous request flooding.
- The core idea can be summarized as simply as: **stable, repetitive, low-risk actions stay on the edge; sudden changes or critical contact events trigger stronger cloud-based VLA replanning.**

## Results
- The paper claims that, compared with Edge-Only and vision-based baselines (such as SAFE/ISAR), RAPID can achieve **up to a 15.8% accuracy improvement** and **up to 1.73× inference speedup**, with only **5~7%** additional system overhead.
- On simulation benchmarks, total latency drops from **Edge-Only 782.5±28.5 ms** to **RAPID 222.9±11.4 ms**, about **3.51× faster**; compared with vision-based SAFE at **377.7±26.2 ms**, RAPID is about **1.69× faster**.
- In the latency breakdown, RAPID’s cloud-side/edge-side latency is **83.5 ms / 139.4 ms**, respectively, while SAFE’s is **62.5 ms / 315.2 ms**; this indicates that RAPID significantly reduces the edge burden through a more reasonable division of labor.
- In the noise robustness analysis for the vision baseline, total latency increases as the environment deteriorates from **395.4 ms** (standard) to **520.6 ms** (visual noise) and **685.3 ms** (interference); based on this, the authors argue that kinematics-based triggering is more robust than vision-based triggering.
- The action redundancy analysis shows that the proportion of redundant actions exceeds **80%**: Pick & Place **82.5%**, Drawer Opening **86.4%**, Peg Insertion **81.2%**; the corresponding average attention weights of redundant actions are only **0.008/0.005/0.007**, while critical actions are **0.076/0.062/0.058**.
- The paper provides multiple quantitative tables, but the excerpt does not fully show all details such as real-robot success rates; the strongest conclusion is that RAPID achieves lower latency, higher compatibility, and fewer ineffective offloads under multi-noise environments.

## Link
- [http://arxiv.org/abs/2603.07949v2](http://arxiv.org/abs/2603.07949v2)
