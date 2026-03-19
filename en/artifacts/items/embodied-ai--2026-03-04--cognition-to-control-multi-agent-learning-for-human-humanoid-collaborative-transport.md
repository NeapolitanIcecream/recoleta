---
source: arxiv
url: http://arxiv.org/abs/2603.03768v1
published_at: '2026-03-04T06:24:55'
authors:
- Hao Zhang
- Ding Zhao
- H. Eric Tseng
topics:
- human-robot-collaboration
- multi-agent-reinforcement-learning
- humanoid-control
- vision-language-models
- whole-body-control
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Cognition to Control - Multi-Agent Learning for Human-Humanoid Collaborative Transport

## Summary
This paper proposes the C2C (cognition-to-control) hierarchical framework for human-humanoid collaborative transport, explicitly separating high-level semantic reasoning, tactical coordination decisions, and high-frequency whole-body control. The core goal is to achieve both interpretable cognitive planning and stable, reliable physical execution in contact-rich, long-horizon human-robot collaboration tasks.

## Problem
- The problem it addresses is: how to stably translate high-level task intent (such as “move the object to the target while avoiding obstacles”) into whole-body contact control synchronized with a human partner, especially in long-horizon human-robot collaborative transport with contact constraints and safety constraints.
- This is important because traditional scripted leader-follower methods, intent inference, or single-agent RL often become brittle when human behavior changes, making oscillation, instability, object dropping, or failure to generalize to complex environments more likely.
- Existing VLA/VLM systems are usually low-frequency and reactive, making them difficult to use directly for millisecond-level continuous control; meanwhile, purely control-based methods struggle to exploit open-vocabulary semantics and long-term planning information.

## Approach
- The paper proposes a three-layer structure: the **VLM grounding layer** first generates shared 2D anchors/paths from multi-view perception; the **MARL skill layer** performs distributed tactical coordination based on these anchors; the **WBC layer** then converts tactical commands into high-frequency joint control that satisfies dynamics, contact stability, and feasibility.
- The core mechanism can be understood simply as: VLM is only responsible for answering “where to go,” MARL is responsible for answering “how the human and robot should currently coordinate to walk/carry/turn,” and WBC is responsible for answering “how to stably move the body and arms in detail.”
- Collaboration is modeled as a **Markov potential game**, using a shared team reward to align multi-agent goals, avoiding explicit leader-follower role assignment or separate human intent prediction, and allowing leader-follower behavior to emerge naturally from training.
- MARL actions use **residual control**: instead of outputting the entire action from scratch, the policy outputs small tactical corrections on top of a nominal transport controller (such as base velocity, center-of-mass height, torso posture, and wrist offset), making learning easier and improving adaptation to partner dynamics.
- For training, it uses **CTDE** (centralized training, decentralized execution) and a joint-action critic to reduce non-stationarity caused by changing partner policies; the experimental platform includes Isaac Lab simulation and real-world deployment with Unitree G1 + humans.

## Results
- Across 9 collaborative scenarios, the overall MARL + C2C architecture outperforms the scripted baseline. Table III shows that the average success rate (architecture synergy index) of the robot scripted baseline is **56.5%**, while **HAPPO 80.6%**, **HATRPO 83.0%**, and **PCGrad 83.2%**; the overall gain relative to the scripted baseline is **+45.6%**.
- By scenario, the highest success rate reaches **88.6% ± 3.5** (S21 Narrow gate, PCGrad), while the corresponding scripted baseline is **59.2% ± 9.0**; for example, in S31 Facing mode, the scripted method is **52.8% ± 8.1**, HATRPO reaches **84.4% ± 1.6**, and the architectural gain is **+55.9%**.
- Other representative improvements include: S11 Alignment improving from **65.4% ± 7.2** to **87.9% ± 4.5** (HATRPO); S22 S-shaped path improving from **57.5% ± 8.8** to **82.1% ± 5.0** (HATRPO); and S33 Pivoting improving from **49.6% ± 8.3** to **78.6% ± 4.5** (PCGrad).
- Ablation results show that the complete three-layer structure is necessary: **No cognition** and **No skill** both fail directly, while **Full hierarchy** reaches a **78.6%** success rate and an average completion time of **81.2 s** in the provided ablation table.
- The paper also claims that in real-world Unitree G1 + human collaboration experiments, it achieves higher success rate, better completion time, and lower object tilt rate than single-agent baselines, but the current excerpt does not provide the specific values from Fig. 4(c).

## Link
- [http://arxiv.org/abs/2603.03768v1](http://arxiv.org/abs/2603.03768v1)
