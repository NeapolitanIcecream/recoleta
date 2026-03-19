---
source: arxiv
url: http://arxiv.org/abs/2603.04466v1
published_at: '2026-03-03T22:15:55'
authors:
- Vaishak Kumar
topics:
- robot-manipulation
- multimodal-llm
- code-generation
- in-context-learning
- policy-rewriting
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation

## Summary
This paper proposes AOR, which enables a multimodal large model to directly rewrite executable Python controller code after each robot manipulation failure by observing key frames and structured returns, thereby improving the manipulation policy **without gradient updates, demonstrations, or reward engineering**. The core contribution is treating the **entire controller implementation**, rather than skill selection or parameters, as the object of in-context learning.

## Problem
- When robot manipulation models fail in specific deployment scenarios, it is usually difficult to **diagnose the cause of failure and adapt quickly** without relying on retraining.
- Existing methods often depend on **pretrained skill libraries, demonstration data, reward design, or large-scale RL training**, which are costly and weak in interpretability.
- The key question is whether an LLM can learn to correct low-level motion policies in continuous control using only **multi-round failure experience + visual evidence**, which is important for low-cost, auditable robot development.

## Approach
- AOR uses a **two-timescale loop**: within each episode, a Python controller executes in real time; between episodes, a multimodal LLM examines key-frame images, reward/stage logs, and more, analyzes failures, and generates a new controller class.
- Unlike representing policy as parameters, a skill selector, or a reward function, AOR represents policy as **complete executable controller code**, so the LLM can change not only **what to do**, but also **how to do it**.
- The system contains 4 components: a vision pipeline (extracting features from RGB-D), a controller (`reset/get_action`), cross-episode memory (rewards, step count, minimum distance, oscillation flags, key frames), and a multimodal LLM reflection agent.
- To control risk, AOR adds safety mechanisms such as **a compilation sandbox, action clipping, runtime safety shutdown, failure rollback to the previous usable controller, and restrictive local rewrites**.
- Examples in the paper show that the LLM can identify specific implementation issues through failure analysis, such as **camera coordinate system / back-projection sign errors causing 5–8 cm error**, unstable downward pressure during grasping, and the need for EMA smoothing, then encode these diagnoses into a new controller.

## Results
- The paper validates AOR on **3 robosuite manipulation tasks** and states that it achieves high success rates without **demonstrations, reward engineering, or gradient updates**.
- The main numbers given in the contributions section: AOR reaches **100% success rate on two tasks** and **91% success rate on the third task**.
- The authors specifically note that the remaining failures occur in the **Stack** task: the agent has identified the root cause as **contact between the gripper and the target block**, but has not yet found a placement strategy that avoids this problem.
- The paper also reports a concrete intermediate finding: AOR independently discovered that inconsistency between OpenGL and OpenCV camera conventions can produce **5–8 cm** of localization error, presented as evidence that it can perform **causal-level code diagnosis**.
- The paper emphasizes that its main breakthrough is **a new capability at the architectural level**, not merely a particular absolute SOTA number: the LLM can directly localize failure causes to code logic and rewrite the controller implementation.

## Link
- [http://arxiv.org/abs/2603.04466v1](http://arxiv.org/abs/2603.04466v1)
