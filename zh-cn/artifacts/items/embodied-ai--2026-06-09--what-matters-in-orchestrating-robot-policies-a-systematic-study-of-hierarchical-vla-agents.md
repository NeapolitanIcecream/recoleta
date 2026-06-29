---
source: arxiv
url: https://arxiv.org/abs/2606.10267v1
published_at: '2026-06-09T00:24:00'
authors:
- Jiaheng Hu
- Mohit Shridhar
- Caden Lu
- Dhruv Shah
- Hao-Tien Lewis Chiang
- Jie Tan
- Annie Xie
topics:
- vision-language-action
- hierarchical-robot-policy
- robot-manipulation
- generalist-robot-policy
- robot-data-scaling
- aloha
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents

## Summary
## 总结
这篇论文研究了在分层视觉-语言-动作机器人智能体中，哪些设计选择最重要。它的最佳 Hi-VLA 方案在 MuJoCo ALOHA 模拟任务和真实 ALOHA 水果分拣任务上，都超过了平面 VLA 控制和简单分层方案。

## 问题
- 平面 VLA 策略常常在长时程操作中失败，因为训练数据通常只包含较短的轨迹片段。
- 用动作数据微调 VLM 可能削弱语言推理能力，这会影响组合任务和间接指令。
- 现有 Hi-VLA 系统在规划器、控制器、记忆、观测和切换规则上的选择不同，因此很难判断到底是哪一部分推动了任务成功。

## 方法
- 论文定义了一个共享的 options 风格控制循环：高层 VLM 选择一个语言子目标，低层 VLA 根据该子目标执行动作。
- 当终止规则触发时，控制权会返回给 VLM，例如固定时长、成功检测器，或 VLM 预测的执行时间。
- 研究测试了高层 Gemini 2.5 VLM 变体、低层 Gemini Robotics On-Device VLA 变体、观测编码、记忆选择和终止规则。
- 评估覆盖 MuJoCo ALOHA 套件中的短时程、长时程和推理任务，以及一个真实 ALOHA 机器人任务。

## 结果
- 最佳分层在短时程任务上达到 78.22 ± 0.91%，而朴素分层为 69.57 ± 1.15%，平面 VLA 为 69.63 ± 1.07%。
- 在长时程任务上，最佳分层达到 67.08 ± 1.38%，朴素分层为 40.56 ± 1.37%，平面 VLA 为 25.30 ± 1.22%。
- 在推理任务上，最佳分层达到 80.89 ± 1.17%，朴素分层为 66.49 ± 1.31%，平面 VLA 为 50.90 ± 1.20%。
- 在真实 ALOHA 水果到匹配盘子的任务上，最佳分层正确放置了 12/15 个水果，朴素分层为 9/15，平面 VLA 为 3/15。
- 消融结果显示，VLM 思考在各类任务上都能提高成功率，而一旦启用思考，VLM 大小的重要性就小一些。
- 论文建议在使用基于计时器的终止时，将固定的 VLA 执行时长设在约 4-8 秒，并报告说，由前 10 个 episode 总结出的跨 episode 记忆，比 episode 内的原始历史更有帮助。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10267v1](https://arxiv.org/abs/2606.10267v1)
