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
- ood-monitoring
- manipulation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation

## Summary
This paper proposes RC-NF, a real-time anomaly detection module for robotic manipulation, used to monitor whether the robot state and the target object's motion trajectory remain consistent with the task. It targets the OOD failure problem of VLA/imitation learning policies in dynamic environments, emphasizing unsupervised training using only normal demonstrations and online alerts with sub-100 ms latency.

## Problem
- VLA models often encounter Out-of-Distribution (OOD) situations in real dynamic environments, causing execution to deviate from task goals, yet sufficiently fast and accurate runtime monitoring is lacking.
- Existing failure detection methods often rely on enumerating anomaly categories or hand-crafted rules, making it difficult to cover the combinatorial explosion of anomaly cases in robotic manipulation.
- Monitoring based on large models/VLMs has semantic capabilities, but often requires multi-step reasoning with latency on the order of seconds, making it hard to trigger rollback or replanning in time.

## Approach
- Use a **conditional normalizing flow** to model the joint distribution of “normal task execution”: the input is the target object's point-set trajectory, and the condition is the robot state and task embedding; during inference, negative log-likelihood is used as the anomaly score, with higher scores indicating more anomalous behavior.
- Propose **RCPQNet** as the affine coupling layer of the flow model: robot state is treated as a task-aware query, object point-set features as memory, and transformation parameters are generated through cross-attention.
- On the vision side, **SAM2** is first used to segment the target object, and then grid sampling is applied to the mask to obtain a point set; compared with directly using raw image features, this is more focused and more noise-robust.
- Point feature encoding uses a dual-branch design: one branch models normalized dynamic shape, while the other preserves positional residual information, and then GRU/Transformer is used to capture temporal relationships.
- Training uses only successful demonstrations (LIBERO-10, 50 trajectories per task), and anomaly triggering is achieved through task-level threshold calibration; after deployment it can serve as a plug-and-play module to drive state-level rollback or task-level replanning.

## Results
- On the newly proposed **LIBERO-Anomaly-10** benchmark, RC-NF achieves the best performance on all three anomaly types, with average **AUC 0.9309 / AP 0.9494**.
- Compared with the strongest baseline, the average improvement is about **8% AUC** and **10.0% AP**; based on the table values, compared with GPT-5's average **0.8500/0.8507**, the gains are **+0.0809 AUC** and **+0.0987 AP**, respectively.
- For **Gripper Open**: RC-NF reaches **AUC 0.9312 / AP 0.9781**, outperforming GPT-5's **0.9137 / 0.9642**, and also significantly exceeding FailDetect's **0.7883 / 0.9032**.
- For **Gripper Slippage**: RC-NF reaches **AUC 0.9195 / AP 0.9180**, outperforming GPT-5's **0.8941 / 0.8720**, and significantly exceeding FailDetect's **0.6665 / 0.6932**.
- For **Spatial Misalignment**: RC-NF reaches **AUC 0.9676 / AP 0.9585**, while GPT-5/Gemini/Claude are around **AUC 0.49–0.53, AP 0.40–0.43**, and FailDetect is **0.6557 / 0.5820**, showing especially clear advantages in detecting spatial-semantic misalignment.
- In real-robot experiments, RC-NF reports **response latency under 100 ms**, and can serve as a plug-and-play monitor for VLA policies such as [0mπ₀, triggering state-level rollback or task-level replanning; the paper does not provide more detailed real-world success rate numbers.

## Link
- [http://arxiv.org/abs/2603.11106v1](http://arxiv.org/abs/2603.11106v1)
