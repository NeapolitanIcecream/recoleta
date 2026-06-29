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
LoHo-Manip 是一个分层的长时程操作系统，把负责任务管理的视觉-语言模型和负责短时程执行的 VLA 控制器结合起来。它的核心思路是在每一步都根据当前观测重新规划，并用预测的二维视觉轨迹引导执行器。

## 问题
- 长时程机器人操作很难，因为任务会沿着多个相互依赖的步骤展开，下一步动作取决于当前进度，小的执行误差会随着时间累积。
- 单体 VLA 策略很难同时完成跨长序列的规划和控制，而且也不容易在不同机器人本体或动作空间之间切换。
- 这对补料、烹饪、整理这类真实机器人任务很重要，因为成功取决于进度跟踪、失败步骤后的恢复，以及对新物体或新场景的处理。

## 方法
- 论文把系统拆成两个模块：任务管理器和执行器。管理器预测剩余任务，执行器负责短时程运动控制。
- 每一步，管理器接收当前图像、指令，以及一个简洁的文本记忆，记录已完成的子任务，然后输出一个感知进度的剩余计划和一条二维关键点轨迹，用来表示接下来该移动到哪里、接近什么目标。
- 执行器 VLA 被微调为以渲染后的轨迹作为条件，因此长时程规划变成了反复执行局部控制，通过“跟随轨迹”推进。
- 管理器以滚动时域的闭环方式运行。如果前面的子任务失败了，它仍会出现在下一次的剩余计划里，轨迹也会更新，从而实现隐式重规划和恢复，不需要手写恢复规则。
- 训练使用 Bridge 机器人的演示来监督子任务和轨迹，还使用 RoboVQA 和 EgoPlan-BenchIT 提供规划与推理数据，并加入合成的失败恢复样本来提高鲁棒性。

## 结果
- 在 RoboVQA 上，LoHo-Manip-4B 的平均分达到 63.1，超过 RynnBrain-8B 的 62.1、Fast-ThinkAct-3B 的 60.8、ThinkAct-7B 的 59.8 和 Qwen3-VL-8B 的 60.8。
- 在 EgoPlan2 上，LoHo-Manip-4B 的平均分为 56.7，高于 Gemini-3.0-Flash 的 48.8、ThinkAct-7B 的 48.2、Fast-ThinkAct-3B 的 46.4 和 RoboBrain2.0-3B 的 41.8。
- 在轨迹预测任务上，LoHo-Manip-4B 在 ShareRobot-T 上取得最好结果：DFD 0.2309、HD 0.2058、RMSE 0.1559，优于 Qwen3-VL-4B 的 0.3808、0.3294、0.2204 和 Embodied-R1-3B 的 0.3426、0.3002、0.2388。
- 在 VABench-V 上，LoHo-Manip-4B 也领先，DFD 0.2123、HD 0.1821、RMSE 0.1469；Qwen3-VL-4B 为 0.2792、0.2528、0.2037，Embodied-R1-3B 为 0.3028、0.2588、0.2129。
- 在 EmbodiedBench 的 EB-Alfred 上，LoHo-Manip-4B 的平均分为 0.38，而 Qwen3-VL-4B 为 0.19、GPT-4o mini 为 0.24。在 EB-Habitat 上，它的平均分为 0.38，而 Qwen3-VL-4B 为 0.30、GPT-4o mini 为 0.33。
- 这段摘录声称该方法在仿真和真实 Franka 机器人上都带来了端到端提升，并且鲁棒性和分布外泛化也更好，但提供的文本没有给出 LIBERO 或 VLABench 的完整闭环操作表格。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21924v1](http://arxiv.org/abs/2604.21924v1)
