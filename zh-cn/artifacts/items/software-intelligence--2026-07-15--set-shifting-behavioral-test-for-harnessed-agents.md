---
source: arxiv
url: https://arxiv.org/abs/2607.13396v1
published_at: '2026-07-15T02:49:05'
authors:
- Ziwei Ye
topics:
- llm-agents
- tool-use
- agent-evaluation
- behavioral-benchmark
- adaptive-routing
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Set-shifting Behavioral Test for Harnessed Agents

## Summary
## 摘要
该论文提出了一项行为基准，用于测试使用工具的 LLM agent 是否会在持久会话中可靠工具组发生静默变化时进行适应。在对两个开放权重模型的实验中，agent 会迅速固化为重复的工具使用例程，其适应情况取决于模型行为、此前的工具使用方式，以及工具集的呈现框架。

## 问题
- 持久 agent 会话可能形成工具使用习惯；即使先前可靠的后端变得不可靠，这些习惯仍会持续。
- 现有的 set-shifting 测试无法直接衡量 agent harness 中冗余工具之间的适应能力，因为工具 schema、技能和此前的调用会保留在上下文中。
- 这很重要，因为即使存在等效的可靠能力，agent 仍可能继续选择不可靠的工具，从而降低任务完成率。

## 方法
- 该基准加载冗余的工具-技能集合。这些工具执行等效操作，但属于不同的工具组，其可靠性会随阶段变化且对 agent 隐藏。
- 在静默边界处，可靠工具组发生变化；每次变化都配有一个不发生变化的对照，工具反馈仅限于成功或失败。
- 研究使用 Hermes Agent，搭配 mimo-v2.5 和 deepseek-v4-pro，测试环境包括调度、DevOps 事件分诊和多云存储。
- 研究将 set-shifting accuracy 计算为变化后各窗口中目标工具调用占比的乘积，同时测量路由类别和任务完成率。
- 实验改变此前使用工具所承担的角色、策略提示词和集合框架，包括将工具描述为相互竞争或相互补充。

## 结果
- 主要的分支实验使用 3 个工具组、2 个分支层级、90 个回合、3 个边界、9 个端点，以及每个单元格 16 个前缀。
- 两个模型通常都会在隐藏变化后的几个回合内形成重复例程；目标工具调用占比集中在离散的路由模式附近，而不是平滑地适应变化。
- 对于 mimo-v2.5，报告端点上的累计 set-shifting accuracy 为 0.02 至 0.33，任务完成率为 0.50 至 1.00。其表现高度依赖目标工具此前承担的角色。
- 对于 deepseek-v4-pro，累计 set-shifting accuracy 为 0.17 至 0.82，任务完成率为 0.46 至 0.92。该模型表现出更高的方差和双峰模式，通常要么转向新的工具组，要么避开该工具组。
- 报告的失败模式有所不同：mimo-v2.5 表现为在单元格层面固守中等范围的例程，而 deepseek-v4-pro 表现为在前缀层面固守目标工具占比接近 0 或 1 的例程。
- 摘录指出，集合框架会改变路由动态，但未在此处提供相应的定量干预结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13396v1](https://arxiv.org/abs/2607.13396v1)
