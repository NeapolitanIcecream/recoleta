---
source: arxiv
url: https://arxiv.org/abs/2605.13119v1
published_at: '2026-05-13T07:40:34'
authors:
- Zixing Lei
- Changxing Liu
- Yichen Xiong
- Minhao Xiong
- Yuanzhuo Ding
- Zhipeng Zhang
- Weixin Li
- Siheng Chen
topics:
- vision-language-action
- robot-foundation-models
- generalist-robot-policy
- long-horizon-manipulation
- robot-tool-use
- instruction-alignment
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Towards Long-horizon Embodied Agents with Tool-Aligned Vision-Language-Action Models

## Summary
## 摘要
论文提出 VLAs-as-Tools：由 VLM 规划器调用专用 VLA 策略，把它们作为有边界的机器人工具来完成长时程操作任务。Tool-Aligned Post-Training 训练这些工具，使其遵循明确的子任务调用并报告进度。

## 问题
- 当前 VLA 策略可以执行由语言条件控制的机器人动作，但长时程任务需要任务分解、状态跟踪、恢复和技能组合。
- 基于规划器的机器人智能体可以分解任务，但很多系统使用手工构建或范围较窄的技能，这些技能弱于现代 VLA 控制器。
- 标准 VLA 可能忽略确切的工具调用，转而遵循视觉先验或演示偏差；放在高层规划器后面时，这会降低可靠性。

## 方法
- 高层 VLM 负责场景分析、全局规划、工具选择和恢复。
- 每个工具调用包含一个离散的工具族标签，例如 grasp、open 或 place，并包含一条基于场景的局部指令。
- 被选中的 VLA 工具只执行一个有边界的子任务窗口，然后返回进度反馈，使规划器无需轮询每个低层步骤即可重新规划。
- Tool-Aligned Post-Training 将演示切分为带调用标签的窗口，并使用测试时相同的单元进行训练：工具族、局部指令、动作和进度。
- 工具族残差适配器在共享 VLA 主干之上，为每个工具族提供自己的低秩执行路径。

## 结果
- 在 LIBERO-Long 的模仿学习结果中，带工具族接口的 TAPT 将 OpenVLA 的成功率从 77.2% 提高到 82.4%，将 OpenVLA-OFT 从 92.0% 提高到 95.6%，将 π0.5 从 92.4% 提高到 97.2%。
- 在 RoboTwin 上，相同设置将 OpenVLA 的成功率从 1.9% 提高到 5.7%，将 OpenVLA-OFT 从 16.9% 提高到 52.4%，将 π0.5 从 39.4% 提高到 62.5%。
- 对于 π0.5，论文称相对于对应的单模型 SFT 基线，LIBERO-Long 提升 +4.8 个百分点，RoboTwin 提升 +23.1 个百分点。
- 在 LIBERO-Long 的强化学习结果中，TAPT 加 VLA 工具族接口使 OpenVLA-OFT 达到 82.6%，标准 RL 为 78.8%；使 π0.5 达到 91.2%，标准 RL 为 80.0%。
- 在 LIBERO-CF-Long 调用保真度上，完整 TAPT 将 OpenVLA-OFT 的 Non-biased Rate 从 31.2% 提高到 47.4%，将 π0.5 的 Non-biased Rate 从 39.6% 提高到 54.6%。
- 完整 TAPT 还将 LIBERO-CF-Long 上的 Faithful Rate 从 19.4% 提高到 54.0%（OpenVLA-OFT），从 24.8% 提高到 54.8%（π0.5）。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13119v1](https://arxiv.org/abs/2605.13119v1)
