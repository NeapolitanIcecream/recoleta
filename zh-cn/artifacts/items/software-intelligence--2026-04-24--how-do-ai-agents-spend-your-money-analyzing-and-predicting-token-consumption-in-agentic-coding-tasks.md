---
source: arxiv
url: http://arxiv.org/abs/2604.22750v1
published_at: '2026-04-24T17:54:47'
authors:
- Longju Bai
- Zhemin Huang
- Xingyao Wang
- Jiao Sun
- Rada Mihalcea
- Erik Brynjolfsson
- Alex Pentland
- Jiaxin Pei
topics:
- llm-agents
- agentic-coding
- token-efficiency
- cost-prediction
- swe-bench
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks

## Summary
## 摘要
这篇论文研究编程智能体在真实软件任务中如何消耗 token，以及它们能否在执行前预测这些成本。论文发现，智能体式编程比代码对话或代码推理贵得多，即使是同一个任务，成本波动也很大，而且当前前沿模型很难准确预测自己的 token 用量。

## 问题
- 论文关注三个问题：智能体式编程中的 token 成本来自哪里、哪些模型使用 token 更高效，以及智能体能否在开始前估算自己的 token 账单。
- 这很重要，因为编程智能体通常按 token 用量计费，用户往往事先不知道最终成本，而且即使运行失败也会产生费用。
- 成本控制很难，因为智能体式编程涉及很长的执行轨迹、反复调用工具，以及不断累积并传递的上下文。

## 方法
- 作者使用 **OpenHands** 智能体框架，分析了 **SWE-bench Verified** 上 **8 个前沿 LLM** 的完整执行轨迹。
- 对每个模型上的每个问题，他们都运行 **4 次**，并提取 token 数量、token 类型拆分、货币成本，以及文件查看和编辑等细粒度动作轨迹。
- 他们将 **agentic coding** 与 **code reasoning** 和 **code chat** 进行比较，以衡量长时程智能体工作流到底贵多少。
- 他们研究了不同任务和重复运行之间的方差，将 token 成本与任务成功率联系起来，并在共同成功和共同失败的任务子集上比较不同模型的 token 效率。
- 他们还定义了一个 **执行前 token 预测任务**，要求智能体在解决任务前先估计自己的输入和输出 token 用量。

## 结果
- **智能体式编程贵得多**：它消耗的 token 大约是单轮代码推理的 **3500×**，约是多轮代码对话的 **1200×**。论文指出，这个差距主要由 **输入 token** 推动。
- **token 用量波动很大**：在 **500 个问题** 中，最贵的实例比最便宜的多消耗约 **700 万** token。对于同一个问题，重复运行的总 token 用量最多可相差 **30×**；在图 2 展示的模型/问题设置中，最贵的一次运行平均约是最便宜的一次的 **2×**。
- **更多 token 不等于更好的结果**：准确率通常在中等成本水平达到峰值，随后在更高成本下趋于饱和或下降。成本高但失败的运行会出现更多重复的文件查看和编辑，作者将这与低效搜索和冗余操作联系起来。
- **模型效率差异很大**：在相同任务上，**Kimi-K2** 和 **Claude Sonnet-4.5** 平均比 **GPT-5** 多消耗 **超过 150 万 token**。在共同失败任务上，**GPT-5/GPT-5.2** 的 token 用量增加 **不到 0.5M**，而 **Kimi-K2** 增加了约 **2M** token。
- **人工难度标签对成本的预测能力较弱**：专家评定的任务难度与 token 消耗只有较弱相关性（**Kendall τb = 0.32**）。此外，被标为 **<15 min** 的任务中有 **6.7%** 消耗的 token 比平均 **>1 hour** 任务还多；而被标为 **>1 hour** 的任务中有 **11.1%** 消耗的 token 比平均 **<15 min** 任务还少。
- **自我预测能力较弱**：前沿模型对实际 token 用量的预测相关性只有 **弱到中等**，报告中的最佳相关性最高为 **0.39**，而且它们在执行前会 **系统性低估** 真实 token 成本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22750v1](http://arxiv.org/abs/2604.22750v1)
