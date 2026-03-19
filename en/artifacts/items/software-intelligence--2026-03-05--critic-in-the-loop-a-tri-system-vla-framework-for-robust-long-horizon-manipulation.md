---
source: arxiv
url: http://arxiv.org/abs/2603.05185v1
published_at: '2026-03-05T13:55:33'
authors:
- Pengfei Yi
- Yingjie Ma
- Wenjiang Xu
- Yanan Hao
- Shuai Gan
- Wanting Li
- Shanlin Zhong
topics:
- robot-manipulation
- vision-language-action
- hierarchical-control
- anomaly-detection
- long-horizon-planning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation

## Summary
This paper proposes a tri-system VLA framework for long-horizon robotic manipulation: a VLM handles slow planning, a VLA handles fast execution, and a lightweight Critic monitors the process and decides when to switch. Its core value is improving robustness, anomaly recovery, and OOD generalization in complex manipulation tasks without frequently invoking the expensive VLM.

## Problem
- Existing robotic manipulation systems struggle to balance **high-level semantic reasoning** and **low-level real-time control** at the same time: VLMs can reason but are too slow, while VLAs execute quickly but lack sufficiently deep semantic understanding.
- Traditional dual-system approaches usually rely on fixed-frequency or rigid switching rules, which wastes compute during smooth execution and reacts too slowly when errors occur, especially hurting long-horizon tasks.
- Real-world environments also involve stagnation, drops, disturbances, and out-of-distribution scenarios; without online anomaly detection and recovery mechanisms, robots can easily fall into infinite retries or task failure, which is critical for real deployment.

## Approach
- The paper proposes a **Tri-System** architecture: System 2 “Brain” uses a VLM to generate semantic subtasks, System 1 “Cerebellum” uses a flow-matching action model for continuous control execution, and System 3 “Critic” continuously observes the current scene and evaluates progress.
- The Critic is modeled as a lightweight visual question answerer: given an image and the current subtask, it outputs either a **progress value** (discretized into 101 bins, corresponding to completion in [-1,0]) or an anomaly tag `<aci>`.
- The scheduling mechanism is **event-driven asynchronous switching**: under normal conditions, only the VLA performs high-speed closed-loop execution; the VLM is awakened for replanning only when a subtask is completed, an anomaly is detected, or there is no progress for a long time (stagnation).
- To avoid getting stuck indefinitely, the system adds **human-like heuristic rules**: if the number of stagnation frames reaches the threshold `N_stag=180`, it resets the robot state and replans with the memory “stagnation timeout.”
- The paper also proposes an **automatic subtask annotation pipeline**: it first uses end-effector trajectories and gripper states for keyframe proposals, then uses a VLM to retrieve semantic labels, reducing the cost of manually annotating long-horizon demonstration data.

## Results
- On the real-robot **Arrange the Tableware** task, Tri-System outperformed the baselines in all 4 scenarios: Ordered **10/10** (Single **8/10**, Dual **7/10**); Scattered **9/10** (vs **0/10**, **6/10**); Left cup OOD **7/10** (vs **0/10**, **1/10**); Fallen **7/10** (vs **2/10**, **5/10**).
- On the **Tidy up the Desk** long-horizon task, Tri-System also achieved the highest stepwise success counts: Open **9/10** (Single **7/10**, Dual **6/10**); Bottle1 **8/10** (vs **5/10**, **5/10**); Bottle2 **5/10** (vs **2/10**, **1/10**); Overall **4/10** (vs **0/10**, **0/10**).
- The paper claims the method achieves **state-of-the-art** real-world long-horizon manipulation performance, and in the **left-arm cup grasping** out-of-distribution scenario, it still attains a **7/10** success rate even though no left-arm data for that task was included during training.
- In system operation, the Critic supports about **20 Hz** asynchronous monitoring; the Critic uses Florence-2-base with about **0.2B** parameters to enable online progress tracking and anomaly interruption at relatively low cost.
- For data, **200** teleoperated trajectories were collected for each task; for the tableware task, an additional **100** trajectories of “recovery after the cup is knocked over” were added to train recovery ability. The paper does not provide a more detailed quantitative comparison of computational cost beyond “number of VLM calls/latency,” but explicitly claims that dynamic scheduling reduces expensive VLM queries.

## Link
- [http://arxiv.org/abs/2603.05185v1](http://arxiv.org/abs/2603.05185v1)
