---
source: arxiv
url: http://arxiv.org/abs/2603.06450v1
published_at: '2026-03-06T16:42:46'
authors:
- Jonathan Yang
- Chelsea Finn
- Dorsa Sadigh
topics:
- cross-embodiment-transfer
- robot-data-scaling
- vision-language-action
- trajectory-pairing
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Data Analogies Enable Efficient Cross-Embodiment Transfer

## Summary
This paper studies which data organization methods are most effective for cross-robot morphology transfer. The conclusion is: compared with simply increasing the number of heterogeneous demonstrations, paired demonstrations with cross-robot "data analogies," especially trajectory-level pairing, are more effective at improving few-shot cross-embodiment transfer.

## Problem
- The paper addresses the following question: when the target robot has only a small number of examples, how can data from other robots, viewpoints, and scenes be used to improve the target robot's task success rate?
- This is important because generalist robot policies increasingly rely on large-scale heterogeneous data, but it is still unclear whether what truly helps is "more data" or "more structured data."
- Especially under morphology differences (different grippers / robot arms), simply piling on more data may fail to learn transferable control correspondences.

## Approach
- Without changing the model architecture or training algorithm, the paper studies only **data composition**: under a fixed budget, it compares coverage (targeted vs. diverse) and pairing (unpaired / task-paired / trajectory-paired).
- It proposes **data analogies**: demonstrations that are cross-embodiment but aligned in scene, task instance, or execution trajectory, allowing the model to see "how different robots do the same thing."
- In simulation, it systematically controls three types of distribution shift: **viewpoint, morphology, appearance**; on real robots, it verifies whether the same trends hold.
- Trajectory pairing uses **DTW** to align cross-robot trajectories for the same task instance; during training, these "translation dataset" samples are jointly used in a 50:50 ratio with the target robot's 50-shot data to fine-tune a pretrained VLA (pi\_0.5-style).

## Results
- In simulation, compared with the large-scale but unpaired open dataset **OXE**, the authors' compositional **OXE+Translational** data design improves average **success rate** by **19%**.
- In real-world experiments, changing only the data composition improves average **success rate** by **22.5%** over large-scale unpaired data.
- For **morphology** shifts, pairing matters more than diversity alone: the paper reports that targeted-trajectory-paired and diverse-trajectory-paired achieve about **62% vs. 64%**, respectively, while the average gap between paired and unpaired settings is about **23%**.
- For **viewpoint** and **appearance**, increasing diversity is more effective; as diversity increases, success rate rises by about **17%** on average, and trajectory pairing is still on average **6%** better than weaker pairing schemes.
- For **morphology scaling**, increasing diversity without pairing is almost ineffective, with performance only around **42% -> 44%**; this indicates that simply adding more robot arm / gripper samples is insufficient to bridge differences in control and kinematics.
- In terms of experimental setup, in the real world each transfer direction uses **50** source-robot demonstrations and **50** translational demonstrations per axis / scene / robot; simulation results are based on **100** random seeds, and real-world results are based on **5** random initializations.

## Link
- [http://arxiv.org/abs/2603.06450v1](http://arxiv.org/abs/2603.06450v1)
