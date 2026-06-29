---
source: arxiv
url: https://arxiv.org/abs/2606.13053v1
published_at: '2026-06-11T08:35:37'
authors:
- Kailin Wang
- Haoxiang Jie
- Yaoyuan Yan
- Jiacheng Zhou
- Zhiyou Heng
topics:
- world-model
- robot-manipulation
- event-prediction
- task-grounding
- model-based-planning
- libero
relevance_score: 0.77
run_id: materialize-outputs
language_code: zh-CN
---

# EA-WM: Event-Aware World Models with Task-Specification Grounding for Long-Horizon Manipulation

## Summary
## 摘要
EA-WM 解决了长时程机器人操作中的一个规划缺口：视觉世界模型可以预测未来特征，但仍未必能判断这个未来是否满足任务规则或接触约束。论文在预训练特征滚动预测之上加入了任务约束的事件预测与验证，让规划可以按任务进展、可行性和置信度对候选动作排序。

## 问题
- 长时程操作需要状态变化，例如开/关、移动到位、在目标上方、接触状态，而不只是一个看起来合理的未来图像或潜变量。
- 只看视觉的世界模型可能会漏掉任务前置条件、谓词顺序，以及预测的未来是否安全或可执行。
- 在 LIBERO 中，任务规范通过 BDDL 规则和模拟器谓词给出，但标准的特征空间规划不会使用这些结构。

## 方法
- 使用冻结的视觉编码器和带动作条件的特征世界模型来展开候选未来。
- 将每个想象中的未来解码为任务事件，例如物体移动、空间关系、接触进展和成功谓词。
- 用一个验证器对候选方案打分，分数由任务进展、语义一致性、物理可行性和不确定性组成。
- 事件预测器用模拟器生成的标签训练，因此不需要人工逐帧标注。
- 在 PointMaze、Deformable、Wall-Single 和 LIBERO-goal 上使用验证器引导的 CEM，并在接触敏感的 LIBERO wine-rack 任务上加入一个 PPO 候选策略。

## 结果
- 在 PointMaze 随机状态规划中，EA-WM 将成功率从 0.90 提升到 0.94，并在校准后将平均状态距离从 0.93568 降到 0.90573。
- 在 PointMaze 数据集目标上，DINO-WM 和 EA-WM 都达到 1.00 成功率；EA-WM 在改变评分规则的同时保持了基线表现。
- 在 Deformable 上，检索初始化的 EA-CEM 在 e10 blocks 设置中达到 94% 成功率。
- 在 Wall-Single 上，档案验证的 EA-CEM 达到 95% 成功率。
- 在 LIBERO-goal 上，和 check-success 对齐的验证器达到 AUC 0.993947。
- 在 LIBERO wine-rack 任务上，PPO 候选策略研究将在线混合成功率提高到 H=20 时的 97/100。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13053v1](https://arxiv.org/abs/2606.13053v1)
