---
source: arxiv
url: https://arxiv.org/abs/2607.19338v1
published_at: '2026-07-21T17:56:49'
authors:
- Qijia He
- Jiayi Cheng
- Chenqian Le
- Rui Wang
- Xunmei Liu
- Yixian Chen
- Jie Mei
- Zhihao Wang
- Xupeng Chen
- Yuhuan Chen
- Tao Wang
topics:
- coding-agents
- cost-aware-routing
- test-time-recovery
- conformal-calibration
- software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents

## Summary
## 摘要
CodeRescue 将失败的编码代理尝试路由到反思、重新规划或升级路径，在解题率与恢复成本之间进行权衡。监督式路由器结合保形校准后，无需重新训练即可支持多个部署预算。

## 问题
- 廉价编码模型失败后，系统通常会立即升级，但执行反馈有时能够支持成本更低的修复或重新尝试。
- 这一问题之所以重要，是因为编码代理的恢复动作具有不同成本和非单调的成功模式，因此，在预算变化时，固定动作或二元级联无法稳定地优化质量。

## 方法
- 廉价模型首先尝试解决每个编程任务。失败后，路由器观察问题、执行判定和 stderr 轨迹，然后选择 **reflect**（利用反馈进行修复）、**replan**（生成新的廉价方案）或 **escalate**（使用更强的模型）。
- 路由器是经过微调的 Qwen3.5-4B 模型，使用执行 rollout 进行训练；每个样本都根据其能够成功恢复的最低成本动作进行标注。
- 路由器使用归一化的标签概率为动作评分，并选择使路由器得分减去成本惩罚最大化的动作：`s(a|x) - λc(a,x)`。
- 保形风险控制（Conformal Risk Control，CRC）层根据校准集，为用户指定的平均成本预算选择 `λ`，因此可以通过查表改变预算，而无需重新训练路由器。其保证是在可交换性条件下控制边际期望成本，而不是控制解题率。

## 结果
- 在 APPS、TACO、BigCodeBench、LiveCodeBench 和 CodeContests 上，研究共尝试了约 **27,300** 个问题；训练集包含 **4,656** 个样本，校准集和测试集各包含 **360** 个问题。
- 微调后的路由器在平均恢复成本为 **5.51 m$** 时取得 **0.817 的解题率**；相比之下，always-escalate 为 **0.686 / 7.22 m$**，always-replan 为 **0.453 / 1.59 m$**，always-reflect 为 **0.275 / 1.24 m$**。
- 摘要指出，在主要的 GPT-5.4-nano/GPT-5.4 设置中，某个经过 CRC 校准的前沿点在使用 always-escalate 平均恢复成本 **35%** 的情况下，解题率超过了 always-escalate。
- 实验显示，廉价恢复与升级具有互补的成功模式，这支持一个离散的成本—质量前沿，而不是按恢复能力严格单调排列的恢复阶梯。
- 在可交换性、有界成本和可行性假设下，形式化的 CRC 结果保证期望恢复成本不超过请求的预算；实际解题率的变化仍取决于数据集和路由器。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19338v1](https://arxiv.org/abs/2607.19338v1)
