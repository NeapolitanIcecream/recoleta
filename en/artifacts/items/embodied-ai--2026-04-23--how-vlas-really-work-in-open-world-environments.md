---
source: arxiv
url: http://arxiv.org/abs/2604.21192v1
published_at: '2026-04-23T01:32:51'
authors:
- Amir Rasouli
- Yangzheng Wu
- Zhiyuan Li
- Rui Heng Yang
- Xuan Zhao
- Charles Eret
- Sajjad Pakdamansavoji
topics:
- vision-language-action
- robot-evaluation
- open-world-robotics
- safety-metrics
- behavior1k
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# How VLAs (Really) Work In Open-World Environments

## Summary
This paper argues that current BEHAVIOR1K evaluation can overstate how well vision-language-action models work in open-world household tasks because it scores only final task state and ignores unsafe execution. The authors audit top B1K systems, show large instability and frequent safety violations, and propose safety-aware metrics that penalize harmful behavior during the task.

## Problem
- BEHAVIOR1K mainly uses success rate and Q-score, which check final sub-goal satisfaction but ignore how the robot reached that state.
- That misses safety-critical failures such as dropping objects, colliding with furniture, damaging support objects, or finishing sub-goals in unsafe ways.
- For long-horizon household tasks, final-state scoring also gives weak diagnostic signal because failures can come from many stages: task understanding, navigation, grasping, manipulation, or action ordering.

## Approach
- The paper analyzes the top two B1K 2025 Challenge policies, RLC and Comet, on the 50 challenge tasks with 10 randomized trials each.
- It studies robustness in two ways: reproducibility of official results using released checkpoints, and consistency across trials for the same task.
- It uses expert video review on 500 task recordings by 8 robotics experts to label failure causes in 10 categories, including grasp failure, collision, task confusion, navigation failure, and execution order confusion.
- It proposes two safety-aware metrics on top of B1K Q-score: **sQ**, which penalizes unsafe handling or bad placement of target objects, and **seQ**, which also adds sub-goals for support non-target objects and penalizes hazards such as dropping them or moving them more than 10 cm.
- The safety rules are concrete: for example, target objects can be penalized if placed with roll or pitch more than 30 degrees from upright, and support objects are marked violated if they fall or are displaced too far.

## Results
- Reproducing the official RLC checkpoint showed large gaps from posted results on many tasks, with differences above **27%** on tasks **24, 26, and 27**; for task **37**, the reproduced score was **0.1** while the posted score was **0.0**.
- The qualitative audit covered **500 recordings** (**50 tasks × 10 trials**) reviewed by **8 experts**. The paper reports that **grasp failure** was the most common error category, with collisions also frequent, plus cases of task confusion such as putting chicken on a shoe rack or a shoe in a fridge.
- On the 20-task table shown, average RLC performance drops from **Q = 0.256** to **sQ = 0.239**, and average Comet drops from **Q = 0.192** to **sQ = 0.173**, showing that safety penalties reduce apparent performance even before accounting for support-object damage.
- With the broader safety-enhanced metric, average scores are **seQ = 0.356** for RLC and **0.304** for Comet, compared with **seQ-Oracle = 0.395** and **0.338**. The gap reflects violations on support objects and target handling that plain Q-score does not capture.
- The same table reports average violation counts of **nTV = 0.35** and **TV = 0.53** for RLC, versus **nTV = 0.31** and **TV = 0.59** for Comet, indicating both non-target and target safety issues are common.
- Several task-level examples show large safety impact: for RLC on **Bring water**, **Q = 0.233** drops to **sQ = 0.133** with **TV = 1.2**; on **Rearrange kitchen**, **Q = 0.275** drops to **sQ = 0.175**; for Comet on **Bring water**, **Q = 0.400** drops to **sQ = 0.267**; on **Set up coffee**, **Q = 0.200** drops to **sQ = 0.150** with **TV = 1.1**.

## Link
- [http://arxiv.org/abs/2604.21192v1](http://arxiv.org/abs/2604.21192v1)
