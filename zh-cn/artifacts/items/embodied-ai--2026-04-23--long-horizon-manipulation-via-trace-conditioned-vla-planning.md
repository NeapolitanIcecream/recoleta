---
source: arxiv
url: http://arxiv.org/abs/2604.21924v1
published_at: '2026-04-23T17:59:04'
authors:
- Isabella Liu
- An-Chieh Cheng
- Rui Yan
- Geng Chen
- Ri-Zhao Qiu
- Xueyan Zou
- Sha Yi
- Hongxu Yin
- Xiaolong Wang
- Sifei Liu
topics:
- vision-language-action
- long-horizon-planning
- robot-manipulation
- hierarchical-policy
- trace-conditioning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Long-Horizon Manipulation via Trace-Conditioned VLA Planning

## Summary
## 摘要
LoHo-Manip 是一个分层的长时程操作系统，把任务管理视觉语言模型与短时程 VLA 执行器结合起来。它的核心思路是在每一步都根据当前观测重新规划，并用预测的 2D 视觉轨迹引导执行器。

## 问题
- 长时程机器人操作很难，因为任务要经过许多相互依赖的步骤，下一步动作取决于当前任务进度，而且小的执行误差会随时间累积。
- 一体化的 VLA 策略很难在长序列上同时完成规划和控制，也不容易在不同机器人形态或动作空间之间替换。
- 这对真实机器人任务很重要，例如补充物品、做饭或整理，因为成功依赖于进度跟踪、失败步骤后的恢复，以及对新物体或新场景的处理。

## 方法
- 论文把系统拆成两个模块：任务管理器和执行器。管理器预测还剩下哪些事要做，执行器负责短时程电机控制。
- 在每一步，管理器接收当前图像、指令以及已完成子任务的紧凑文本记忆，然后输出一个考虑任务进度的剩余计划，以及一个 2D 关键点轨迹，用来指示下一步移动到哪里或接近什么。
- 执行器 VLA 经过微调后可以以渲染出的轨迹为条件，因此长时程规划被转化为通过跟随轨迹反复执行局部控制。
- 管理器以滚动时域的闭环方式运行。如果前面的某个子任务失败了，它仍会出现在下一次的剩余计划中，轨迹也会更新，这样就能在没有手写恢复规则的情况下实现隐式重规划和恢复。
- 训练使用 Bridge 机器人演示数据来监督子任务和轨迹，并使用 RoboVQA 与 EgoPlan-BenchIT 的规划和推理数据，同时加入合成的失败恢复样例来提高鲁棒性。

## 结果
- 在 RoboVQA 上，LoHo-Manip-4B 的平均分达到 63.1，超过 RynnBrain-8B 的 62.1、Fast-ThinkAct-3B 的 60.8、ThinkAct-7B 的 59.8，以及 Qwen3-VL-8B 的 60.8。
- 在 EgoPlan2 上，LoHo-Manip-4B 的平均分为 56.7，高于 Gemini-3.0-Flash 的 48.8、ThinkAct-7B 的 48.2、Fast-ThinkAct-3B 的 46.4，以及 RoboBrain2.0-3B 的 41.8。
- 在轨迹预测上，LoHo-Manip-4B 在 ShareRobot-T 上给出最好的结果：DFD 0.2309、HD 0.2058、RMSE 0.1559，优于 Qwen3-VL-4B 的 0.3808、0.3294、0.2204，以及 Embodied-R1-3B 的 0.3426、0.3002、0.2388。
- 在 VABench-V 上，LoHo-Manip-4B 也领先，DFD 为 0.2123、HD 为 0.1821、RMSE 为 0.1469；相比之下，Qwen3-VL-4B 为 0.2792、0.2528、0.2037，Embodied-R1-3B 为 0.3028、0.2588、0.2129。
- 在 EmbodiedBench EB-Alfred 上，LoHo-Manip-4B 的平均值达到 0.38，而 Qwen3-VL-4B 为 0.19，GPT-4o mini 为 0.24。在 EB-Habitat 上，它达到 0.38，而 Qwen3-VL-4B 为 0.30，GPT-4o mini 为 0.33。
- 摘要称该方法在仿真环境和真实 Franka 机器人上的端到端表现都有明显提升，鲁棒性和分布外泛化也更好，但当前提供的文本没有包含 LIBERO 或 VLABench 的完整闭环操作结果表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21924v1](http://arxiv.org/abs/2604.21924v1)
