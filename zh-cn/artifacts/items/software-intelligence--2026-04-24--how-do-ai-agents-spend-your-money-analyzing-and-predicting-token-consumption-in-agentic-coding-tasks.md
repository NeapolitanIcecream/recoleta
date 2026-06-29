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
本文研究编码代理在真实软件任务中如何消耗 token，以及它们能否在执行前预测这些成本。结果显示，代理式编码的成本远高于代码聊天或代码推理，同一任务上的成本波动很大，而当前前沿模型对自身 token 用量的预测也很差。

## 问题
- 论文提出三个问题：代理式编码的 token 成本来自哪里、哪些模型更省 token、以及代理能否在开始前估算自己的 token 账单。
- 这个问题重要，是因为编码代理按 token 用量计费，用户通常无法提前知道最终成本，而且失败的运行也会产生成本。
- 成本控制很难，因为代理式编码包含长轨迹、反复使用工具，以及大量向前携带的上下文。

## 方法
- 作者使用 **OpenHands** 代理框架，分析了 **SWE-bench Verified** 上来自 **8 个前沿 LLM** 的完整执行轨迹。
- 每个问题在每个模型上运行 **4 次**，并提取 token 数量、token 类型拆分、金钱成本，以及文件查看和编辑等细粒度动作轨迹。
- 他们把 **代理式编码** 与 **代码推理** 和 **代码聊天** 比较，衡量长时程代理工作流到底贵多少。
- 他们研究不同任务和重复运行之间的方差，将 token 成本与任务成功情况联系起来，并在共享成功和共享失败子集上比较不同模型的 token 效率。
- 他们还定义了一个 **执行前 token 预测任务**，要求代理在解决任务前估计自己的输入和输出 token 用量。

## 结果
- **代理式编码贵得多**：它使用的 token 约为单轮代码推理的 **3500 倍**，约为多轮代码聊天的 **1200 倍**。论文指出，这一差距主要由 **输入 token** 驱动。
- **token 用量波动很大**：在 **500 个问题** 上，最贵的实例比最便宜的实例多消耗大约 **700 万** 个 token。对同一个问题，重复运行的总 token 用量最多可相差 **30 倍**，而在图 2 所示的模型/问题设置中，最贵运行平均约为最便宜运行的 **2 倍**。
- **更多 token 不等于更好结果**：准确率通常在中等成本区间达到峰值，之后在更高成本下趋于饱和或下降。昂贵的失败运行会出现更多重复的文件查看和编辑，作者把这与低效搜索和冗余动作联系起来。
- **模型效率差异很大**：在相同任务上，**Kimi-K2** 和 **Claude Sonnet-4.5** 平均比 **GPT-5** 多消耗 **150 万以上** 的 token。在共享失败任务上，**GPT-5/GPT-5.2** 的 token 用量增加 **不到 50 万**，而 **Kimi-K2** 约增加 **200 万**。
- **人类难度标签对成本的预测力很弱**：专家标注的任务难度与 token 消耗只有中等偏弱的相关性（**Kendall τb = 0.32**）。此外，**6.7%** 的 **<15 分钟** 任务消耗的 token 比平均 **>1 小时** 任务还多，而 **11.1%** 的 **>1 小时** 任务消耗的 token 比平均 **<15 分钟** 任务还少。
- **自我预测效果也弱**：前沿模型与实际 token 用量只有 **弱到中等** 的相关性，最高报告相关系数到 **0.39**，而且它们在执行前会 **系统性低估** 真实 token 成本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22750v1](http://arxiv.org/abs/2604.22750v1)
