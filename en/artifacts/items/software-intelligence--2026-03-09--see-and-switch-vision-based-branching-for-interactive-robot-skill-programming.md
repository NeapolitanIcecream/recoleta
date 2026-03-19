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
- robot-programming-by-demonstration
- vision-based-branching
- interactive-robot-learning
- anomaly-detection
- task-graph-execution
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# See and Switch: Vision-Based Branching for Interactive Robot-Skill Programming

## Summary
This paper proposes **See & Switch**, an interactive framework for robot programming by demonstration: when the robot reaches a "decision state" during execution, it automatically selects the next skill branch using eye-in-hand camera images, or detects a new situation and requests additional human demonstration. It unifies conditional task graphs, visual branch selection, and multiple teaching modalities to improve robustness under real-world variability.

## Problem
- Traditional Programming by Demonstration / Learning from Demonstration often simply replays a single demonstration trajectory, and can easily fail when facing environmental changes such as whether a door is closed, changes in object position, or the appearance of obstacles.
- Conditional task graphs can express "if the scene is different, follow a different skill branch," but the key challenge is that the robot must **reliably choose the correct branch** based on perception during execution, and **detect anomalies and request new demonstrations** when it encounters unseen situations.
- This matters because without online perception and switching, demonstration-based robot systems struggle to move from the lab into real, variable, non-expert-use scenarios.

## Approach
- Represent the task as an **incrementally extendable graph of skill parts**: nodes are skill parts, and edges are connected via decision states; during execution, the system can switch to different successor skills at these decision points.
- Propose a vision-based **Switcher**: at each decision state, it reads an eye-in-hand camera image and uses DINO visual features to determine which successor skill branch should be selected.
- The same visual representation space is also used for **anomaly/OOD detection**: if the current image does not resemble the context of any known branch, it triggers an anomaly, and the user decides whether to add a new branch (recovery demonstration) or merely refine an existing skill with this data.
- Adopt a **decision-state-local** local classification approach: classification is performed only among the allowed successor set at the current decision point, rather than doing global scene understanding, thereby reducing ambiguity and simplifying the learning problem.
- Design a **teaching-modality-independent** input abstraction layer that uniformly supports kinesthetic teaching, joystick/keyboard, and hand gestures, allowing users to provide in-situ recovery demonstrations during execution.

## Results
- The system is validated on **3 dexterous manipulation tasks** (Peg pick, Probe measure, Cable wrap), along with a user study involving **8 participants**.
- The dataset scale is **192 demonstrations** (8 users × 3 tasks × 3 modalities × 2–3 variants) and **576 real-robot rollouts** (about 3 execution replays per demonstration).
- The paper claims that for novice users, the system can **reliably complete branch selection and anomaly detection**: across **576** real robot executions, **branch selection accuracy = 90.7%** and **anomaly detection accuracy = 87.9%**.
- About **4%** of demonstrations were filtered out due to safety issues, and in about **3%** of cases users were allowed a second attempt; the authors use this to argue that the system is usable in real interactive settings.
- The excerpt does not provide finer-grained per-task, per-modality, or per-baseline numerical comparisons, but it clearly states that compared with methods relying on manual branching or low-dimensional proprioceptive signals, their method provides **vision-driven, online graph-extensible, and teaching-modality-independent** conditional skill programming capability.

## Link
- [http://arxiv.org/abs/2603.08057v1](http://arxiv.org/abs/2603.08057v1)
