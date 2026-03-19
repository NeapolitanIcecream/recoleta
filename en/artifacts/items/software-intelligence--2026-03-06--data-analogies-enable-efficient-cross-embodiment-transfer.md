---
source: arxiv
url: http://arxiv.org/abs/2603.06450v1
published_at: '2026-03-06T16:42:46'
authors:
- Jonathan Yang
- Chelsea Finn
- Dorsa Sadigh
topics:
- robot-learning
- cross-embodiment-transfer
- data-centric-learning
- trajectory-pairing
- vision-language-action
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# Data Analogies Enable Efficient Cross-Embodiment Transfer

## Summary
This paper studies what kind of data organization is most effective for cross-morphology transfer in robotics. The core conclusion is: compared with simply scaling up heterogeneous demonstration data, "data analogies" with cross-robot correspondences—especially trajectory-level pairing—better improve transfer performance on target robots with limited samples.

## Problem
- The paper aims to solve the following problem: when the target robot has only a small amount of demonstration data, how can data from other robots, viewpoints, and scenes be used to achieve efficient cross-embodiment transfer?
- This is important because current generalist robot policies often rely on large-scale heterogeneous data, but it remains unclear whether what really matters is "data quantity/diversity" or "cross-robot alignable structure."
- In particular, morphological differences (such as grippers and kinematics) are harder to transfer than visual differences; if one only performs unstructured data aggregation, the policy may fail to learn reusable action correspondences.

## Approach
- The authors change only the **data composition**, not the model architecture or training algorithm: starting from a pretrained VLA/π0.5-style policy, they fine-tune jointly with 50-shot few-shot data from the target robot.
- They divide cross-embodiment differences into three axes: **viewpoint, morphology, appearance**, and under a fixed budget systematically compare two factors: **coverage** (targeted vs. diverse) and **pairing** (unpaired / task-paired / trajectory-paired).
- So-called **data analogies** are paired demonstrations across different robots in the same scene, task, or even similar trajectories; among them, trajectory-paired uses DTW alignment on trajectories from the same task instance to make different robots execute as much as possible the "same action strategy."
- The paper proposes a compositional data recipe: for perceptual shifts (viewpoint, appearance), emphasize broader coverage; for morphology, emphasize stronger pairing; then mix these subsets under a fixed budget into a compositional dataset.
- When combined with open-source data, the authors also apply coverage reweighting to OXE and inject 40% trajectory-paired data, forming **OXE+Translational**.

## Results
- In real-world experiments, by changing only the data composition, the **cross-embodiment transfer success rate is on average 22.5% higher than with large-scale unpaired data**.
- In simulation, the authors report that their compositional / translational data strategy improves **success rate by an average of 19%** relative to large-scale open-source unpaired data (such as OXE), and consistently outperforms on two target robots and four RoboCasa tasks.
- On the morphology axis, the **average gap between paired vs. unpaired is about 23%**; meanwhile, targeted vs. diverse differs only slightly under the trajectory-paired condition (example in the paper: **62% vs. 64%**), showing that the key to morphology transfer is not blind augmentation but cross-robot correspondence.
- For viewpoint and appearance, as diversity increases, performance **improves by about 17% on average**; at the same time, trajectory pairing still maintains an **average advantage of about 6%** over weaker pairing methods.
- Simply increasing morphology diversity is almost ineffective: the example curve given in the paper rises only from **42% to 44%**, indicating that without explicit pairing, adding more robot arms/grippers does not automatically yield action transfer.
- The paper also provides specific training settings: the target few-shot data and translational data are usually **50 demonstrations** each; real-robot experiments involve **Franka, WidowX, PiperX**; simulation statistics are based on **100 random seeds**, and real-world experiments are based on **5 random initializations**.

## Link
- [http://arxiv.org/abs/2603.06450v1](http://arxiv.org/abs/2603.06450v1)
