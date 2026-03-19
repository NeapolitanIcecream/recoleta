---
source: arxiv
url: http://arxiv.org/abs/2603.11106v1
published_at: '2026-03-11T10:14:37'
authors:
- Shijie Zhou
- Bin Zhu
- Jiarui Yang
- Xiangyu Zhao
- Jingjing Chen
- Yu-Gang Jiang
topics:
- robot-anomaly-detection
- normalizing-flow
- vision-language-action
- real-time-monitoring
- ood-detection
- robot-manipulation
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation

## Summary
This paper proposes RC-NF, a real-time anomaly detection module for robotic manipulation, used to monitor whether VLA robot execution deviates from the task distribution. By using only normal demonstrations for unsupervised training, it achieves high-accuracy, low-latency OOD detection and intervention triggering on both simulation benchmarks and real robots.

## Problem
- The paper aims to solve the issue that VLA robots are prone to execution drift or failure in dynamic environments and under Out-of-Distribution (OOD) conditions, while existing monitoring methods either rely on exhaustively enumerating anomaly categories or have inference latency on the order of seconds, making timely intervention impossible.
- This matters because robotic manipulation is a closed-loop control problem: if failures such as grasping errors, object slippage, or spatial target misalignment cannot be detected early, errors can accumulate quickly and lead to task failure or even safety risks.
- Existing classification-based methods generalize poorly, while monitoring based on large models is too slow, so a runtime monitor is needed that is real-time, task-relevant, and does not require anomaly annotations.

## Approach
- The core method is **Robot-Conditioned Normalizing Flow (RC-NF)**: it learns what “normal task execution” should look like in terms of robot state + object motion trajectory; at runtime, if the current observation has very low probability under this distribution, it is classified as anomalous.
- It is trained only on successful examples, making it an unsupervised anomaly detector; during inference, it uses negative log-likelihood as the anomaly score, where a higher score indicates greater deviation from normal execution.
- The input consists of three parts: robot proprioceptive state, task text embedding, and the target object point-set trajectory obtained from video after SAM2 segmentation, rather than using raw images directly.
- The paper proposes a new coupling layer, **RCPQNet**: it uses the robot state and task embedding as the query, and the object point-set features as the memory, generating the flow’s scaling/translation parameters through cross-attention, thereby preserving interaction relationships while “decoupling” the processing of robot and object information.
- The system is attached in parallel to the VLA control loop as a plug-and-play monitoring module; once the anomaly score exceeds a threshold, it triggers state-level fallback (homing/rollback) or task-level replanning.

## Results
- On the newly proposed **LIBERO-Anomaly-10** benchmark, RC-NF achieves the best results across all three anomaly categories: average **AUC 0.9309 / AP 0.9494**, outperforming FailDetect’s **AUC 0.7181 / AP 0.7700**, an improvement of about **+0.2128 AUC** and **+0.1794 AP**.
- Compared with the strongest baseline, the paper claims average gains of about **8% AUC** and **10% AP**; from the table, RC-NF improves over the best non-proposed method (by average), GPT-5’s **AUC 0.8500 / AP 0.8507**, by about **+0.0809 AUC** and **+0.0987 AP**.
- Category-wise results: on **Gripper Open**, RC-NF reaches **AUC 0.9312 / AP 0.9781**; on **Gripper Slippage**, **0.9195 / 0.9180**; on **Spatial Misalignment**, **0.9676 / 0.9585**. On spatial misalignment tasks, VLM baselines are near random, for example GPT-5 achieves only **AUC 0.4904 / AP 0.4015**.
- In real-robot experiments, RC-NF serves as a plugin module for VLA models (e.g., **π0**), with anomaly response latency **under 100 ms**, and can trigger state-level rollback and task-level replanning.
- The training data uses the original **LIBERO-10**, with **50** demonstrations per task; RC-NF uses **12** flow steps and is trained for **100** epochs. The paper also releases **LIBERO-Anomaly-10**, which contains **3** types of manipulation anomalies.

## Link
- [http://arxiv.org/abs/2603.11106v1](http://arxiv.org/abs/2603.11106v1)
