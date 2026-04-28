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
language_code: zh-CN
---

# 机器人论文收紧评测，并让控制状态更显式

## Overview
本周机器人论文最突出的点很明确：具身智能论文正在用更严格的评测和更显式的内部结构收紧动作闭环。LongBench、HazardArena 和 HiVLA 很好地体现了这一重点。这些论文更认可这样一类系统：它们在执行过程中显式暴露规划状态、记忆、风险和与任务相关的信号，然后再用具体动作失败和长时程行为来检验这些设计。

## Clusters

### 对动作质量的评测更严格
评测是本周最清晰的主题。这个语料库反复追问的一点是：机器人策略在具体约束下是否会做出正确动作。HazardArena 在动作层面评估语义安全。LongBench 在真实长时程操作任务中衡量执行漂移、时序失败和上下文使用。周初的 StarVLA-α 及相关评测工作也在检验：在额外系统复杂性开始带来收益之前，更简单的 VLA 配方已经能走多远。共同标准变得更严格了：基准设计现在更关注动作选择是否可行、失败模式，以及多步执行质量。

#### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md)
- [LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment](../Inbox/2026-04-13--lary-a-latent-action-representation-yielding-benchmark-for-generalizable-vision-to-action-alignment.md)
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md)
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md)
- [ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control](../Inbox/2026-04-17--reconvla-an-uncertainty-guided-and-failure-aware-vision-language-action-framework-for-robotic-control.md)
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md)

### 规划和记忆进入控制回路
长时程控制论文持续加入显式规划状态。HiVLA 和 Goal2Skill 把规划、 grounding、记忆和恢复与底层动作生成分开。Dual-Anchoring 把同样的思路用于导航，在 Video-LLM 内部监督进度和地标记忆。ChemBot 及相关工作则为更长的开放世界任务加入记忆和进度跟踪。纵观这些论文，更好的结果来自把中间状态显式暴露出来，让策略能在执行过程中跟踪并更新。

#### Evidence
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md)
- [Long-Term Memory for VLA-based Agents in Open-World Task Execution](../Inbox/2026-04-17--long-term-memory-for-vla-based-agents-in-open-world-task-execution.md)
- [3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS](../Inbox/2026-04-13--3d-anchored-lookahead-planning-for-persistent-robotic-scene-memory-via-world-model-based-mcts.md)
- [Dual-Anchoring: Addressing State Drift in Vision-Language Navigation](../Inbox/2026-04-19--dual-anchoring-addressing-state-drift-in-vision-language-navigation.md)
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md)
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md)

### 可靠性工作更偏向实际运行
有几篇论文把可靠性直接纳入系统栈。ReconVLA 把不确定性和失败处理当作控制的一部分。AEGIS 关注 VLA 微调过程中的知识保持，这在机器人系统适配新任务时很重要。本周同样的模式也出现在语义安全测试和面向部署的论文中：它们会列出尚未解决的运行约束，而不是把这些问题藏起来。这让本周研究带有很强的工程导向：系统的判断标准是它们能否保持稳定、保留有用知识，并及早标记高风险动作。

#### Evidence
- [ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control](../Inbox/2026-04-17--reconvla-an-uncertainty-guided-and-failure-aware-vision-language-action-framework-for-robotic-control.md)
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md)
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md)
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md)
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md)
- [AEGIS: Anchor-Enforced Gradient Isolation for Knowledge-Preserving Vision-Language-Action Fine-Tuning](../Inbox/2026-04-17--aegis-anchor-enforced-gradient-isolation-for-knowledge-preserving-vision-language-action-fine-tuning.md)

### 几何、触觉和数据设计仍是核心
模型设计和数据工作都更偏向任务结构。4 月 16 日这一组论文加入了更丰富的提示、潜在规划和几何感知的数据生成。4 月 14 日这一组论文则报告了基于 3D 几何骨干网络的强操作结果，以及在真实人形任务上通过触觉预测得到的结果。本周给出的含义很直接：当输入更贴近控制问题时，策略会表现得更好；这种信号可以是场景几何、接触状态，或是围绕任务构建的、更窄的合成数据管线。

#### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md)
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md)
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md)
- [$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](../Inbox/2026-04-16--p-0-7-a-steerable-generalist-robotic-foundation-model-with-emergent-capabilities.md)
- [DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks](../Inbox/2026-04-13--dexworldmodel-causal-latent-world-modeling-towards-automated-learning-of-embodied-tasks.md)
- [3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS](../Inbox/2026-04-13--3d-anchored-lookahead-planning-for-persistent-robotic-scene-memory-via-world-model-based-mcts.md)
