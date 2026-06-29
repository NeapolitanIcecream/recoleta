---
source: arxiv
url: https://arxiv.org/abs/2606.23617v1
published_at: '2026-06-22T17:12:50'
authors:
- Ulas Berk Karli
- Tesca Fitzgerald
topics:
- vision-language-action
- active-learning
- continual-learning
- robot-data-scaling
- imitation-learning
- uncertainty-estimation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models

## Summary
## 摘要
RECALL 研究如何通过在高不确定性状态收集恢复示例，用更少的演示来微调视觉-语言-动作机器人策略。研究发现，不确定性引导的恢复数据能提升适应效果，同时需要回放数据来防止遗忘。

## 问题
- VLA 策略部署到新的任务分布、机器人或环境后，通常需要微调。
- 被动模仿学习会等待失败发生，然后从任务起点收集完整演示，这可能把专家时间花在策略已经能处理的状态上。
- 定向恢复数据可以改进薄弱子步骤，但只用这类狭窄数据训练可能会抹掉已有技能。

## 方法
- 论文从一个在 LIBERO-10 上训练的 π0-FAST 自回归 VLA 开始，然后运行该模型，找出策略可能需要帮助的状态。
- 论文使用 INSIGHT 这一 token 级不确定性和求助预测方法，在运行过程中标记高不确定性状态。
- 论文从一次运行中的第一个不确定状态收集恢复演示，称为在线收集；或从一次运行中的每个不确定状态收集恢复演示，称为离线收集。
- 论文将这些主动恢复数据集与规模匹配的被动起点状态演示进行比较。
- 论文测试了使用仅新数据、完整回放、LIBERO-10 回放、定向回放、较低学习率和弹性权重巩固进行微调的效果。

## 结果
- Strong INSIGHT 在线恢复配合完整回放达到 72.4% 的 LIBERO-10 总体成功率；规模匹配的被动收集为 60.2%，原始基线为 59.8%；主动与被动的增益 p=0.0001。
- 在线恢复达到 72.4% 的总体成功率，离线恢复达到 68.4%；收集任务成功率在线为 49.2%，离线为 48.4%，论文报告的总体差异不显著，p=0.1659。
- 仅新数据微调失败：最好的 Strong INSIGHT 在线仅新数据检查点达到 28.4% 的总体成功率、0.4% 的收集任务成功率和 56.4% 的保留任务成功率。回放版本达到 72.4% 的总体成功率、49.2% 的收集任务成功率和 95.6% 的保留任务成功率。
- 较低学习率的仅新数据训练达到 62.8% 的总体成功率、34.4% 的收集任务成功率和 91.2% 的保留任务成功率。λ=10^12 的 EWC 达到 61.4% 的总体成功率、32.0% 的收集任务成功率和 90.8% 的保留任务成功率。
- LIBERO-10 回放达到 68.6% 的总体成功率，接近完整回放的 72.4%，p=0.1877。定向回放达到 63.2% 的总体成功率，并且与 LIBERO-10 回放相比，将保留任务成功率从 90.0% 降至 83.6%，p=0.0345。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23617v1](https://arxiv.org/abs/2606.23617v1)
