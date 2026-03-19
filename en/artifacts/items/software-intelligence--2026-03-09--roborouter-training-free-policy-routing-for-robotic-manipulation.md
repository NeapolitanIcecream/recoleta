---
source: arxiv
url: http://arxiv.org/abs/2603.07892v3
published_at: '2026-03-09T02:14:32'
authors:
- Yiteng Chen
- Zhe Cao
- Hongjia Ren
- Chenjie Yang
- Wenbo Li
- Shiyi Wang
- Yemin Wang
- Li Zhang
- Yanming Shao
- Zhenjun Zhao
- Huiping Zhuang
- Qingyao Wu
topics:
- robotic-manipulation
- policy-routing
- training-free
- multi-agent-system
- retrieval-augmented
relevance_score: 0.32
run_id: materialize-outputs
language_code: en
---

# RoboRouter: Training-Free Policy Routing for Robotic Manipulation

## Summary
RoboRouter proposes a **training-free** policy routing framework for robotic manipulation: instead of pursuing a single universal policy, it automatically selects the most suitable policy for each task from an existing heterogeneous policy pool. By retrieving similar historical execution records and continuously updating with structured feedback, it consistently outperforms any single policy in both simulation and real-robot settings.

## Problem
- The robotic manipulation field already includes multiple policy types such as VLA, VA, and code-based composition, but each performs well only on part of the task distribution, with limited cross-task and out-of-distribution generalization.
- In practice, new policies continually emerge. If a centralized router must be retrained each time, the cost is high, adaptation is slow, and continual expansion becomes difficult.
- The key question is therefore: **how to choose the policy most likely to succeed for the current task without additional training and without executing all candidate policies through trial and error**.

## Approach
- Build a training-free framework composed of four agents: **Retriever, Router, Evaluator, Recorder**.
- First encode the current task into a multimodal representation by combining language instructions, visual observations, and task metadata extracted by vision foundation models (such as object information).
- The Retriever searches the historical execution database for similar task records and reranks candidates; the Router then directly predicts which policy to choose for the current task based on these similar cases and each policy's historical performance.
- The Evaluator watches execution videos and combines rule-based metrics (success flags, time, distance, contact/alignment, etc.) to generate structured summaries; the Recorder writes this feedback back into the database and routing context, forming an online improvement loop.
- When integrating a new policy, only lightweight evaluation on a small number of representative tasks is needed, and the results are written into memory; retraining the whole system is unnecessary.

## Results
- **Simulation (RoboTwin 2.0)**: across 20 representative tasks with 100 trials per task, RoboRouter achieves an average success rate of **79.85%**, outperforming all single baselines: ACT **55.90%**, DP **51.05%**, DP3 **76.45%**, RDT **60.35%**, π0 **69.90%**, Code as Policies **54.45%**.
- According to the paper's abstract and main text, RoboRouter improves average simulation success rate by **more than 3 percentage points** over the best single policy; from Table 1, compared with the best average baseline DP3 (**76.45%**), the gain is about **3.40 percentage points**.
- **Real world**: across 5 representative tasks with 20 repeated trials per task, RoboRouter reaches an average success rate of **47%**, higher than ACT **26%**, DP **18%**, RDT **33%**, and π0 **34%**; compared with the best single baseline π0, this is an improvement of **13 percentage points**.
- In real-task breakdowns, RoboRouter reaches **10/20** on **Click Alarmclock**, higher than the best baseline at **8/20**; on **Open Laptop** it reaches **9/20**, higher than the best baseline at **8/20**; on **Place Container Plate** it ties the best baseline at **12/20**.
- The paper also claims that the additional latency introduced by routing is small and negligible relative to total execution time, but the timing table in the provided excerpt is truncated, so **no complete, verifiable latency figures are provided**.

## Link
- [http://arxiv.org/abs/2603.07892v3](http://arxiv.org/abs/2603.07892v3)
