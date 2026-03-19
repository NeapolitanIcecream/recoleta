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
- multi-agent-rl
- vision-language-models
- whole-body-control
- collaborative-transport
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# Cognition to Control - Multi-Agent Learning for Human-Humanoid Collaborative Transport

## Summary
This paper proposes the C2C (cognition-to-control) hierarchical framework, which connects vision-language reasoning, multi-agent policy learning, and whole-body control for human-humanoid collaborative transport. Its goal is to establish a clear pathway between long-horizon task planning and high-frequency contact-stable control, and to achieve stable collaboration without explicitly assigning leader-follower roles.

## Problem
- Existing human-robot collaborative transport systems often rely on scripts, leader-follower role assignments, or intent prediction, making them fragile, oscillatory, or even prone to failure when human strategies change.
- End-to-end VLA/VLM methods tend to favor more "reactive" behavior and struggle to reliably translate high-level semantic planning into continuous whole-body control with rich contact and strict constraints.
- This problem matters because collaborative transport simultaneously requires **long-horizon cognitive decision-making** and **millisecond-level physical stability**; failure in either directly affects efficiency, safety, and the ability to deploy in real-world settings.

## Approach
- The paper proposes a three-layer hierarchy: the **VLM cognition layer** generates shared anchors/routes from multi-view observations; the **MARL skill layer** performs tactical coordination around those anchors; and the **WBC control layer** executes at high frequency while ensuring kinematic/dynamic feasibility and contact stability.
- Human-robot collaborative transport is modeled as a **task-centric Markov potential game**: all agents share a potential function/team reward aligned with task progress, allowing coordination to converge toward a common goal and reducing multi-agent oscillation.
- The skill layer uses a **residual policy**: instead of directly outputting all actions, the policy outputs small corrections on top of a nominal transport controller, learning how to adapt to partner dynamics and contact details.
- Training uses **CTDE** (centralized training, decentralized execution) and a joint-action critic; at execution time, each agent retains an independent policy, without parameter sharing, explicit leader-follower roles, or a separate intent inference module.

## Results
- Across **9 scenarios** (three categories: OSP/SCT/SLH, each with 3 subtasks), the MARL methods substantially outperform the robot-script baseline overall; the paper's "overall architecture synergy index" (average success rate) improves from **56.5%** to **80.6% / 83.0% / 83.2%** (HAPPO/HATRPO/PCGrad), with a maximum relative gain of **+45.6%**.
- Per-scenario results show that, compared with robot-script, success rates increase from about **49.6%–65.4%** to about **72.7%–88.6%**. For example: **S21 Narrow gate** improves from **59.2 ± 9.0** to **88.6 ± 3.5** (PCGrad); **S31 Facing mode** from **52.8 ± 8.1** to **84.4 ± 1.6** (HATRPO); and **S11 Alignment** from **65.4 ± 7.2** to **87.9 ± 4.5** (HATRPO).
- The structural gains relative to the script baseline reach **+29.3% to +55.9%** across tasks, such as **S31 +55.9%**, **S33 +55.2%**, and **S32 +50.1%**, indicating more pronounced improvements for long-object handling and collaboration in constrained spaces.
- In the ablation study, retaining only part of the hierarchy leads to failure: **No cognition = Fails, No skill = Fails**; the full hierarchy achieves a **78.6%** success rate with an average completion time of **81.2 s**, showing that both the cognition layer and the skill layer are indispensable.
- The training setup includes **2.0×10^9** steps, a policy input dimension of **210**, an action dimension of **11**, and a policy frequency of **2 Hz**; these reflect implementation scale rather than performance metrics.
- The paper also claims that in real-robot experiments (Unitree G1 + human), it achieves higher success rates and better robustness than a single-agent baseline, and exhibits **emergent leader-follower behavior**; however, the provided excerpt does not include the full numerical values from Fig. 4(c).

## Link
- [http://arxiv.org/abs/2603.03768v1](http://arxiv.org/abs/2603.03768v1)
