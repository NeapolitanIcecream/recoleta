---
source: arxiv
url: https://arxiv.org/abs/2606.05922v1
published_at: '2026-06-04T09:26:00'
authors:
- Wenbo Pan
- Shujie Liu
- Chin-Yew Lin
- Jingying Zeng
- Xianfeng Tang
- Xiangyang Zhou
- Yan Lu
- Xiaohua Jia
topics:
- llm-agents
- harness-optimization
- self-improvement
- software-engineering-agents
- trajectory-learning
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts

## Summary
## 摘要
RHO 在没有标注验证数据的情况下，利用过去的轨迹改进 LLM agent 的 harness。它先挑出困难且多样的任务，再重新运行这些任务，让 agent 比较自己的 rollout，最后保留它提出的最佳 harness 更新。

## 问题
- LLM agent 依赖由提示、技能、工作流和工具组成的 harness，而这个 harness 在部署后需要更新。
- 许多 harness 优化方法需要带标注的验证集，但这类数据很难为未来的任务分布收集。
- 过去的轨迹里包含失败案例和有用的行为痕迹，但简单地累积记忆带来的提升更小，也不稳定。

## 方法
- RHO 先根据困难程度给过去的轨迹打分，嵌入其中的失败描述，并用 DPP coreset 选择器在实验中选出 10 个困难且多样的任务。
- 它把每个选中的任务重新运行多次，在报告的设置中组大小 G=3。
- agent 先通过 self-validation 检查每个 rollout 的错误，再通过 self-consistency 比较 rollout 之间的不一致。
- 这些诊断结果会变成生成候选 harness 的指令，候选 harness 可以加入技能、指令和可执行工具。
- RHO 采样 N=3 个候选 harness，并通过成对的 self-preference 选择那个新 rollout 比基线 rollout 更受偏好的版本。

## 结果
- 在 SWE-Bench Pro 上，RHO 将保留测试集的通过率从 Vanilla Codex 的 0.59 提升到 0.78，绝对提升 +0.19，且不需要外部评分。
- 在 Terminal-Bench 2 上，通过率从 0.71 提升到 0.76，提升 +0.05。
- 在 GAIA-2 上，通过率从 0.29 提升到 0.37，提升 +0.08。
- 在报告表格中，RHO 优于不依赖反馈的基线：Dynamic Cheatsheet 在 SWE-Bench Pro、Terminal-Bench 2 和 GAIA-2 上分别达到 0.62/0.73/0.30，ReasoningBank 达到 0.61/0.73/0.28，Sleep-time Compute 达到 0.64/0.73/0.32。
- 与 SWE-Bench Pro 上的 Meta-Harness 相比，RHO 在没有验证标签的情况下以 103 次优化阶段 agent 调用获得 0.78；Meta-Harness 在有标签、1 轮时得到 0.62、41 次调用，在有标签、10 轮时得到 0.80、320 次调用。
- 消融摘录报告的完整诊断为 0.78/0.76/0.37；去掉 self-consistency 后降到 0.56/0.75/0.27；去掉 self-validation 后降到 0.70/0.73/0.30；使用原始轨迹时为 0.60/0.75/0.29。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05922v1](https://arxiv.org/abs/2606.05922v1)
