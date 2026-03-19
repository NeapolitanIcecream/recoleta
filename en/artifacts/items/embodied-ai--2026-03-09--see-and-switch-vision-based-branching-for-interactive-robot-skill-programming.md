---
source: arxiv
url: http://arxiv.org/abs/2603.08057v1
published_at: '2026-03-09T07:47:47'
authors:
- Petr Vanc
- Jan Kristof Behrens
- "V\xE1clav Hlav\xE1\u010D"
- Karla Stepanova
topics:
- programming-by-demonstration
- vision-based-branching
- dexterous-manipulation
- task-graphs
- anomaly-detection
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# See and Switch: Vision-Based Branching for Interactive Robot-Skill Programming

## Summary
This paper proposes See & Switch, a vision-based interactive robot teaching framework that handles environmental variation using branching skill segments in a task graph. It uses eye-in-hand camera images to automatically select the next skill during execution, or to trigger additional user demonstrations when encountering new situations.

## Problem
- Traditional PbD/LfD often can only reproduce a single demonstrated trajectory, and easily fails when faced with real-world changes such as a closed door, changed object positions, or occlusion.
- Although conditional task graphs can express "take different branches if the environment differs," the key challenge is: how can the robot select the correct branch online based on high-dimensional visual input, and recognize novel situations it has never seen before?
- This matters because without reliable branch selection and anomaly detection, non-expert users cannot easily expand robot skills incrementally through demonstration, and the system cannot adapt well to variation in open environments.

## Approach
- Represent the task as an **extendable task graph**: nodes are skill segments, and execution can switch to different successor branches when reaching a decision state (DS).
- Propose a visual **Switcher**: near each DS, it uses eye-in-hand camera images for both **branch classification** (which successor skill to choose) and **OOD/anomaly detection** (whether a new demonstration is needed).
- Use frozen **DINO** visual features as the representation, then train a local classifier/estimator for each DS, making decisions only within the candidate branch set allowed at that DS, which reduces the difficulty of global scene understanding.
- When an anomaly is detected, the user can provide an online **recovery demonstration**, and the system automatically inserts a new DS/branch and retrains the corresponding local Switcher, thereby incrementally expanding the task graph.
- An input abstraction layer unifies **kinesthetic teaching, joystick control, and gesture teleoperation** as three teaching modes, making error correction and recovery demonstrations independent of the specific input modality.

## Results
- Validated on **3 dexterous manipulation tasks**: **Peg pick, Probe measure, Cable wrap**.
- Conducted a user study with **8 participants**, totaling **192** demonstrations (from **8 users × 3 tasks × 3 modalities × 2–3 variants**).
- Evaluated **576 real-robot rollouts** in total; the paper claims the method can reliably perform branch selection and anomaly detection even for **novice users**.
- Key quantitative results: across 576 real-robot runs, **branch selection accuracy was 90.7%**, and **anomaly detection accuracy was 87.9%**.
- About **4%** of demonstrations in the data were filtered out for safety reasons, and a second attempt was allowed in about **3%** of cases.
- The abstract does not provide a complete numerical comparison table against a clearly defined baseline method; the strongest empirical claim is that the visual Switcher can achieve reliable branch decisions in real tasks and support modality-independent online recovery demonstrations.

## Link
- [http://arxiv.org/abs/2603.08057v1](http://arxiv.org/abs/2603.08057v1)
