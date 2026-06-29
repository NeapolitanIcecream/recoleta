---
kind: trend
trend_doc_id: 158
granularity: week
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-20T00:00:00'
topics:
- robotics
- embodied-ai
- vla
- evaluation
- long-horizon-control
- memory
- safety
- geometry
run_id: materialize-outputs
aliases:
- recoleta-trend-158
tags:
- recoleta/trend
- topic/robotics
- topic/embodied-ai
- topic/vla
- topic/evaluation
- topic/long-horizon-control
- topic/memory
- topic/safety
- topic/geometry
language_code: en
pass_output_id: 82
pass_kind: trend_synthesis
---

# Robotics papers tighten evaluation and make control state explicit

## Overview
This week’s robotics corpus is strongest on one point: embodied AI papers are tightening the action loop with harder evaluation and more explicit internal structure. LongBench, HazardArena, and HiVLA capture the emphasis well. The papers reward systems that expose planning state, memory, risk, and task-relevant signals during execution, then test those choices on concrete action failures and long-horizon behavior.

## Clusters

### Stricter evaluation of action quality
Evaluation is the clearest weekly theme. The corpus keeps asking whether robot policies make the right action under concrete constraints. HazardArena scores semantic safety at the action level. LongBench measures execution drift, timing failures, and context use on real long-horizon manipulation. Earlier in the week, StarVLA-α and related evaluation work also tested how far simpler VLA recipes already go before extra system complexity pays off. The common standard is tighter: benchmark design now targets feasible action choice, failure modes, and multi-step execution quality.

#### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md)
- [LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment](../Inbox/2026-04-13--lary-a-latent-action-representation-yielding-benchmark-for-generalizable-vision-to-action-alignment.md)
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md)
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md)
- [ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control](../Inbox/2026-04-17--reconvla-an-uncertainty-guided-and-failure-aware-vision-language-action-framework-for-robotic-control.md)
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md)

### Planning and memory enter the control loop
Long-horizon control papers keep adding explicit planning state. HiVLA and Goal2Skill separate planning, grounding, memory, and recovery from low-level action generation. Dual-Anchoring applies the same idea to navigation by supervising progress and landmark memory inside a Video-LLM. ChemBot and related work add memory and progress tracking for longer open-world tasks. Across these papers, better results come from exposing intermediate state the policy can track and update during execution.

#### Evidence
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md)
- [Long-Term Memory for VLA-based Agents in Open-World Task Execution](../Inbox/2026-04-17--long-term-memory-for-vla-based-agents-in-open-world-task-execution.md)
- [3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS](../Inbox/2026-04-13--3d-anchored-lookahead-planning-for-persistent-robotic-scene-memory-via-world-model-based-mcts.md)
- [Dual-Anchoring: Addressing State Drift in Vision-Language Navigation](../Inbox/2026-04-19--dual-anchoring-addressing-state-drift-in-vision-language-navigation.md)
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md)
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md)

### Reliability work becomes more operational
Several papers make reliability a direct part of the stack. ReconVLA treats uncertainty and failure handling as part of control. AEGIS targets knowledge preservation during VLA fine-tuning, which matters when robot systems are updated on new tasks. The same weekly pattern appears in semantic safety tests and deployment-minded papers that list unresolved operating constraints instead of hiding them. This gives the week a practical tone: systems are judged by whether they stay stable, keep useful knowledge, and flag risky actions early.

#### Evidence
- [ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control](../Inbox/2026-04-17--reconvla-an-uncertainty-guided-and-failure-aware-vision-language-action-framework-for-robotic-control.md)
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md)
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md)
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md)
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md)
- [AEGIS: Anchor-Enforced Gradient Isolation for Knowledge-Preserving Vision-Language-Action Fine-Tuning](../Inbox/2026-04-17--aegis-anchor-enforced-gradient-isolation-for-knowledge-preserving-vision-language-action-fine-tuning.md)

### Geometry, touch, and data design stay central
Model design and data work both favor task structure. The April 16 set adds richer prompts, latent planning, and geometry-aware data generation. The April 14 set reports strong manipulation results from a 3D geometry backbone and from tactile prediction on real humanoid tasks. The weekly implication is concrete: policies improve when inputs match the control problem more closely, whether that signal is scene geometry, contact state, or a narrower synthetic data pipeline built around the task.

#### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md)
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md)
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md)
- [$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](../Inbox/2026-04-16--p-0-7-a-steerable-generalist-robotic-foundation-model-with-emergent-capabilities.md)
- [DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks](../Inbox/2026-04-13--dexworldmodel-causal-latent-world-modeling-towards-automated-learning-of-embodied-tasks.md)
- [3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS](../Inbox/2026-04-13--3d-anchored-lookahead-planning-for-persistent-robotic-scene-memory-via-world-model-based-mcts.md)
