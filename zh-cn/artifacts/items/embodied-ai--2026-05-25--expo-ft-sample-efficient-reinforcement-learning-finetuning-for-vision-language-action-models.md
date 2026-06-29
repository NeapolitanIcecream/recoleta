---
source: arxiv
url: https://arxiv.org/abs/2605.25477v1
published_at: '2026-05-25T06:31:03'
authors:
- Perry Dong
- Kuo-Han Hung
- Tian Gao
- Dorsa Sadigh
- Chelsea Finn
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- rl-finetuning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models

## Summary
## 摘要
EXPO-FT 通过离策略 RL 对预训练的 VLA 机器人策略进行微调，让它们用很少的在线机器人数据就能在真实任务中达到很高的成功率。论文报告，在 8 个操作任务上，平均只用 19.1 分钟的在线数据就达到 30/30 成功。

## 问题
- 预训练的 VLA 策略能处理许多操作任务，但在零样本条件下的成功率常常太低，不适合真实机器人使用，因为失败代价很高。
- 从头开始做 RL 不能利用大规模预训练 VLA 已学到的行为，而以往的 VLA 微调方法往往需要太多机器人交互，或者在可靠成功率之前就停下。
- 许多现代 VLA 会输出动作块，所以 RL 微调需要优化多步动作序列，而不是单个动作。

## 方法
- EXPO-FT 基于 EXPO，这是一种面向流匹配和扩散式策略的离策略 RL 方法。
- 该方法保留预训练 VLA 作为基础策略，并训练一个轻量级编辑策略来提出小的动作修正；Q 函数在基础动作和编辑后的动作之间选择价值最高的一个。
- 它把 EXPO 扩展到时间上延展的动作，对执行的动作块进行编辑和打分，并在块边界上做 TD 回传。
- 人类操作员可以在在线 rollout 过程中纠正动作块中的单个时间步；纠正后的动作会存入回放缓冲区。
- 论文报告的系统使用 π0.5 作为 VLA 主干、两个 RGB 相机、本体感觉、稀疏二元奖励、ResNet-50 critic 编码器，以及独立的 actor-learner 设置。

## 结果
- 论文在 8 个真实世界操作任务上评估 EXPO-FT：Egg Flip、String Light Routing Route I、String Light Routing Route II、String Light Insert、Candy Scoop、Cube Pick、Flower Insert 和 Pool Shot。
- 论文声称最终评测表现达到满分：每个评测任务都是 30/30 成功。
- 论文报告达到这一表现平均需要 19.1 分钟的在线机器人数据；引言部分也将其描述为大约 20 分钟。
- 实验每个任务使用 8k 到 20k 个环境步，10 Hz 的笛卡尔末端执行器和夹爪速度控制，以及每个任务 30 次评测试验。
- 报告称基于规则的任务成功检测器准确率超过 95%，而最终评测成功由人工观察者判断。
- 摘要说明 EXPO-FT 优于从头训练的 RL 方法和先前的 VLA 微调方法，但没有给出完整的基线表或各基线的具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.25477v1](https://arxiv.org/abs/2605.25477v1)
