---
source: arxiv
url: http://arxiv.org/abs/2603.04466v1
published_at: '2026-03-03T22:15:55'
authors:
- Vaishak Kumar
topics:
- robot-manipulation
- multimodal-llm
- code-synthesis
- in-context-learning
- vision-language-action
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation

## Summary
AOR proposes a way for robots to learn without training neural policies and without relying on demonstrations or reward engineering: after each failure, a multimodal LLM directly rewrites executable Python controller code. The core contribution is to make the **entire low-level controller implementation**, rather than a skill selector or parameters, the object of in-context learning, enabling the model to diagnose and fix the causes of failure based on visual evidence.

## Problem
- When robot foundation models or VLAs fail in a specific deployment setting, it is usually difficult to identify the cause and adapt quickly **without retraining**.
- Existing LLM-based robotics methods mostly remain at the level of **high-level planning / skill selection / one-shot code generation**, making it hard to fix errors in geometry, perception, contact, and control details in low-level manipulation.
- This matters because real manipulation tasks are often affected by details such as camera coordinate systems, grasp geometry, and control smoothness, and addressing these issues through large-scale data or RL retraining is costly and slow to debug.

## Approach
- AOR uses a **dual-timescale closed loop**: within an episode, a Python controller executes in real time; between episodes, a multimodal LLM inspects keyframe images and structured results, analyzes the failure, and generates a **new controller class**.
- The policy representation is not parameters or a skill library, but **fully executable Python code**, so the LLM can change not only **what to do** but also **how to do it**, including phase structure, geometric computation, state-machine logic, and control details.
- The context provided to the LLM includes the current controller source code, episode reward / step count / phase logs / minimum distance / oscillation flag, as well as keyframe images; it is prompted to first describe the failure mode, root-cause location (vision / logic / parameters), and most important modification, then output code.
- To prevent code generation from going out of control, the system includes mechanisms such as a **compilation sandbox, action clamp, exception-safe stop, and fallback to the previous working controller on failure**.
- In robosuite examples, AOR autonomously discovered and fixed several key issues, such as a **back-projection sign error caused by OpenGL camera-coordinate conventions**, the need to keep the end effector stationary during grasping, and the use of EMA to smooth actions.

## Results
- The paper claims to validate AOR on **3 robosuite manipulation tasks**, reporting **100% success on 2 tasks and 91% success on the remaining task**.
- The abstract explicitly emphasizes that these results were achieved with **no demonstrations, no reward engineering, and no gradient updates**.
- The authors say the remaining failures mainly occur in the **Stack** task: the LLM has identified that **contact between the gripper and the target block** is the cause, but has not yet found a placement strategy that avoids this contact, so performance remains at **91%** rather than 100%.
- The paper provides several quantitative background comparisons to related work, but these are not AOR’s own experiments: for example, Reflexion achieved **+22%** on AlfWorld and **+11%** on HumanEval; ReAct showed a **+34% absolute improvement** over RL/imitation baselines on AlfWorld; OpenVLA achieved **+16.5%** relative to RT-2-X(55B) after LoRA fine-tuning; Diffusion Policy outperformed prior methods by **46.9%** across 12 tasks. These numbers are used to position AOR rather than as direct experimental comparisons.
- The provided excerpt does not include more detailed AOR experimental table information, such as the exact number of samples per task, number of trials, variance, or step-by-step baseline comparisons.

## Link
- [http://arxiv.org/abs/2603.04466v1](http://arxiv.org/abs/2603.04466v1)
