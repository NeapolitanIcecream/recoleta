---
kind: trend
trend_doc_id: 61
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- robotics
- vision-language-action
- video-planning
- event-cameras
- evaluation
- reinforcement-learning
run_id: materialize-outputs
aliases:
- recoleta-trend-61
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/video-planning
- topic/event-cameras
- topic/evaluation
- topic/reinforcement-learning
language_code: zh-CN
---

# 机器人动作系统正在围绕可复用的控制基础设施构建

## Overview
4 月 6 日最强的内容是具身控制方法，它们让机器人动作系统更容易构建、更容易调控，也更不容易失效。最清楚的证据来自 Veo-Act、StarVLA 和 E-VLA：视频预测被用于高层规划，VLA 代码库正在标准化，事件感知正在改善低光和模糊条件下的操控。当天也有评测工具和更快的机器人强化学习工作，但最扎实的主题是围绕动作的实用控制基础设施。

## Clusters

### 视频模型正在成为机器人规划器
视频生成正在作为操控的规划模块出现，而不只是数据来源。Veo-Act 使用 Veo-3 预测未来的运动序列，然后在接触密集的交互中把控制权交给低层视觉-语言-动作策略。报告中的提升很大，主要出现在模糊场景和灵巧执行上：在测试的仿真和真实设置里，平均成功率从 45% 提高到 80%，真实场景中的 pass-by 交互从 2/13 提高到 11/13。论文也把边界讲得很清楚。视频预测可以勾画任务，但精确控制仍需要反应式动作策略。

#### Evidence
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md): Summary and headline results for hierarchical video planner plus VLA executor.

### VLA 工作正在收紧策略栈和传感器栈
几篇论文都在处理 VLA 模型周围的动作栈。StarVLA 把多个动作头、骨干网络、训练配方和基准接口放进同一个代码库，支持七个集成基准，也支持视觉-语言和世界模型骨干。E-VLA 解决的是另一个瓶颈：感知差。它加入事件相机输入，让 VLA 策略在低光和模糊条件下还能继续行动。在 Pick-Place 任务上，仅图像基线在 25 和 20 lux 时掉到 0%，而事件适配器在这两个照度下都达到 90%。这些工作一起把注意力放在可复用的策略支撑代码和能抵抗真实采集失败的感知上。

#### Evidence
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md): Summary of the modular VLA framework and benchmark integration claims.
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md): Summary and quantitative low-light results for event-augmented VLA.

### 评测和编排正在成为机器人系统工作的核心
基础设施也在更接近部署。RoboPlayground 把自然语言任务请求变成可执行的评测任务，并带有校验和修复功能；在一项 26 人研究中，它的可用性优于 Cursor 和 GenSim。ROSClaw 面向异构多机器人执行，结合了工具调用、基于仿真的安全检查和共享执行记忆。它的证据更像系统演示，而不是基于基准的结果，但意思很明确：任务编写、可行性检查和硬件协同正在被当作一等研究问题，而不是准备工作。

#### Evidence
- [ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration](../Inbox/2026-04-06--rosclaw-a-hierarchical-semantic-physical-framework-for-heterogeneous-multi-agent-collaboration.md): Summary of semantic-to-physical multi-robot coordination, safety checks, and evidence limits.

### 效率主张集中在训练吞吐量和结构化规划
只要论点具体到速度和规模，经典强化学习在机器人控制里仍然活跃。FlashSAC 认为，如果吞吐量足够高，而且 critic 更新受到严格约束，off-policy RL 还能在高维控制中保持稳定。论文覆盖了 10 个模拟器中的 60 多个任务，在灵巧操控和类人机器人行走上报告了最强提升，还给出一个仿真到真实的类人机器人结果，训练时间从数小时降到数分钟。另一篇神经符号 VLA 报告提出了不同的效率主张，Tower of Hanoi 成功率达到 95%，训练能耗降低 100 倍，但证据来自一个范围很窄的规划基准，而不是大规模测试套件。

#### Evidence
- [FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control](../Inbox/2026-04-06--flashsac-fast-and-stable-off-policy-reinforcement-learning-for-high-dimensional-robot-control.md): Summary of method scope, scale, and efficiency claims across many robot control tasks.
- [Neuro-symbolic AI breakthrough cuts energy use by 100x while boosting accuracy](../Inbox/2026-04-06--neuro-symbolic-ai-breakthrough-cuts-energy-use-by-100x-while-boosting-accuracy.md): Summary of proof-of-concept neuro-symbolic VLA efficiency and planning results.
