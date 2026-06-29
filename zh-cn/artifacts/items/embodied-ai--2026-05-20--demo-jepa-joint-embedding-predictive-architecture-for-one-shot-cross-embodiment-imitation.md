---
source: arxiv
url: https://arxiv.org/abs/2605.20811v1
published_at: '2026-05-20T07:05:49'
authors:
- Jingyang He
- Guangrun Li
- Jieyu Zhang
- Chengkai Hou
- Zhengping Che
- Shanghang Zhang
topics:
- cross-embodiment-imitation
- world-models
- latent-planning
- robot-manipulation
- jepa
- one-shot-imitation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Demo-JEPA: Joint-Embedding Predictive Architecture for One-shot Cross-Embodiment Imitation

## Summary
## 总结
Demo-JEPA 把另一种 embodiment 的视觉示范转成潜在子目标，让目标机器人用自己的动力学模型去规划实现。它在跨 embodiment 和 zero-shot 结果上比 VPP 和 XSkill 更强，但在域内行为落地上的表现不一致。

## 问题
- 它解决的是一次性跨 embodiment 模仿：目标机器人要根据视觉示范跟随人类或另一台机器人，而且没有共享动作空间。
- 这个问题很关键，因为不同机器人在形态、运动学和动作空间上都不一样，直接复制动作和手工重定向都可能失败，或者需要代价很高的成对数据。
- 目标使用场景是机器人先从源视频和自身交互数据中学习，再用自己的控制器完成任务。

## 方法
- V-JEPA 风格的编码器把观测映射到可预测的潜在状态，减少对像素或源动作的依赖。
- Dreamer Predictor 接收目标端的当前观测和一对源示范帧，然后预测一个目标可用的未来潜在目标。
- 交叉注意力模块估计源-目标对应关系和源运动；3D 卷积融合这些特征；Transformer 预测潜在目标。
- 目标机器人使用自己的动作条件世界模型和交叉熵方法规划，寻找那些预测潜在轨迹能到达推断目标的动作。
- 训练分两阶段：Stage I 用成对视觉轨迹做潜在目标预测，Stage II 做动作共训练，把目标动力学模型和 Dreamer Predictor 的目标对齐。

## 结果
- 模拟训练使用了 86 个 Stage I 任务、13,444 条轨迹，以及 39 个 Stage II 任务、8,324 条轨迹；真实世界训练使用了 22 个 Stage I 任务、4,508 条轨迹，以及 19 个 Stage II 任务、3,903 条轨迹。
- 在 RLBench 模拟中的行为落地任务上，Demo-JEPA 平均成功率为 0.31，低于 VPP 的 0.47 和 XSkill 的 0.39。
- 在模拟跨 embodiment 桥接任务上，Demo-JEPA 平均成功率为 0.45，高于 VPP 的 0.28 和 XSkill 的 0.17。
- 在模拟 zero-shot 泛化任务上，Demo-JEPA 平均成功率为 0.36，高于 VPP 的 0.04 和 XSkill 的 0.03。
- 在真实世界行为落地任务上，Demo-JEPA 平均成功率为 0.43，低于 VPP 的 0.65，和 XSkill 的 0.45 接近。
- 在真实世界迁移设置中，Demo-JEPA 的跨 embodiment 桥接平均为 0.55，高于 VPP 的 0.53 和 XSkill 的 0.40；zero-shot 泛化平均为 0.25，高于 VPP 的 0.00 和 XSkill 的 0.05。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20811v1](https://arxiv.org/abs/2605.20811v1)
