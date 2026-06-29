---
kind: trend
trend_doc_id: 131
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
topics:
- robotics
- long-horizon manipulation
- hierarchical control
- reinforcement learning
- uav navigation
run_id: materialize-outputs
aliases:
- recoleta-trend-131
tags:
- recoleta/trend
- topic/robotics
- topic/long-horizon-manipulation
- topic/hierarchical-control
- topic/reinforcement-learning
- topic/uav-navigation
language_code: en
pass_output_id: 72
pass_kind: trend_synthesis
---

# Long-horizon robot control is getting more explicit about planning, memory, and guidance

## Overview
This day’s robotics set favors explicit structure over monolithic control. HiVLA and Goal2Skill both report gains from separating planning, grounding, memory, and recovery from low-level action generation. VLAJS applies the same idea during training by using a VLA model as sparse early guidance for reinforcement learning. The most concrete gains are in long-horizon manipulation; the drone navigation paper adds a clear list of unresolved deployment constraints.

## Clusters

### Hierarchical planning is carrying long-horizon manipulation
Long-horizon manipulation papers are getting more explicit about the control loop above the actuator policy. HiVLA keeps a vision-language model (VLM) on planning and grounding, then hands execution to a diffusion policy with both global scene tokens and a high-resolution local crop. That setup posts 83.3% average success on RoboTwin 2.0, ahead of H-RDT at 70.6%. Goal2Skill adds structured memory, post-condition checks, and recovery logic for multi-stage tasks. On five RMBench tasks it reports 32.4% average success versus 9.8% for the strongest baseline. The common message is clear: better long-horizon results now come from explicit subtask structure, scene grounding, and step verification, not only from a larger end-to-end policy.

#### Evidence
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): HiVLA architecture and RoboTwin 2.0 results
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Goal2Skill memory, verification, and RMBench results

### VLA priors are being used as temporary training signals
Another strong theme is how to use pretrained vision-language-action priors without locking the robot to the teacher. VLAJS adds sparse guidance from a model such as OpenVLA to PPO, queries the teacher on at most 20% of rollout steps, and aligns action direction while leaving action magnitude to reinforcement learning. The guidance weight decays with reward progress and is removed once learning is stable. In the reported ManiSkill results, this cuts required environment interactions by more than 50% on several tasks, while keeping the final controller as a high-frequency RL policy. This is a practical recipe for borrowing semantic priors early and preserving closed-loop control later.

#### Evidence
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): VLAJS method details and sample-efficiency claim

### UAV language navigation is still defined by deployment limits
Aerial language-conditioned robotics appears here as a map of open deployment problems rather than a new model result. The UAV-VLN survey frames drone navigation as a partially observable control problem with natural-language input, then organizes methods across modular systems, spatiotemporal models, and foundation-model agents. Its useful contribution for this period is the constraint list: sim-to-real transfer, outdoor perception drift, ambiguous instructions, and onboard compute remain the main blockers. That makes the paper more valuable as a research agenda than as evidence of benchmark progress.

#### Evidence
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md): Survey taxonomy and deployment bottlenecks for UAV-VLN
