---
source: arxiv
url: https://arxiv.org/abs/2605.28634v1
published_at: '2026-05-27T15:41:18'
authors:
- Yutai Li
- Shaohui Peng
- Jiaming Guo
- Di Huang
- Zihao Zhang
- Yuxuan Guo
- Yunkai Gao
- Siming Lan
- Ling Li
- Xing Hu
- Yunji Chen
topics:
- vision-language-action
- robot-foundation-model
- motion-primitives
- generalist-robot-policy
- robot-data-scaling
- robot-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation

## Summary
## 摘要
PrimitiveVLA 把整段任务示范拆成可复用的动作原语，再用这些原语对 VLA 机器人策略进行微调。论文声称，这种做法通过训练时分段和测试时原语串接，提高了 LIBERO 上的数据效率和零样本迁移能力。

## 问题
- 标准的 VLA 微调会把完整的语言指令直接映射到低层机器人动作，这会促使模型记忆任务特定的轨迹和视觉线索。
- 这会影响机器人数据扩展，因为每增加一个新的对象-技能组合或长时序任务，往往都需要更多示范。
- 公共机器人数据集通常只提供任务级指令，缺少原语标签和片段边界。

## 方法
- 该方法定义了 11 个原语：Grasp、Place、Lift、Move、Push、Pull、Insert、Press、Twist、Tilt 和 Rotate。
- 在微调阶段，VLM 会根据任务指令、RGB 轨迹和原语库推断原语序列。
- LLM 会基于机器人状态写出 Python 规则，用来检测原语边界，例如夹爪闭合后接上向运动可判定为 Grasp。
- VLA 使用规范化的原语指令和由 SAM 与 Cutie 跟踪的以物体为中心的掩码进行训练，因此不同任务共享同一种原语输入格式。
- 在推理阶段，系统会检索最相似的 3 个任务-序列示例，用 VLM 规划原语，并用 LLM 生成的切换代码在滑动状态历史上做判断，同时由 VLA 输出连续动作。

## 结果
- 在 LIBERO-90 上，OpenVLA + PrimitiveVLA 的成功率达到 79.80%，而 OpenVLA 为 70.60%，提升 9.20 个百分点。
- 在 LIBERO-90-Novel 上，OpenVLA 从 7.38% 提升到 45.50%，在未见任务上的提升约为 6.2 倍。
- OpenVLA-OFT + PrimitiveVLA 在 LIBERO-90-Novel 上达到 71.00%，而基线为 13.50%；在 LIBERO-Long 上达到 66.50%，而基线为 3.75%。
- pi0.5 + PrimitiveVLA 在 LIBERO-90-Novel 上达到 75.50%，而基线为 56.00%；在 LIBERO-Long 上达到 80.25%，而基线为 30.50%。
- 小规模 LIBERO 的平均成功率上，OpenVLA 从 82.40% 提高到 88.00%，OpenVLA-OFT 从 97.60% 提高到 98.53%；pi0.5 从 97.53% 变为 97.33%。
- 摘录说明，仿真使用 50 次试验，真实世界和 RLBench 使用 20 次试验，但没有给出真实世界或 RLBench 的结果表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28634v1](https://arxiv.org/abs/2605.28634v1)
