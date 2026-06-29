---
source: arxiv
url: https://arxiv.org/abs/2606.10209v1
published_at: '2026-06-08T22:01:28'
authors:
- Abhilasha Lodha
- Mahsa Pahlavikhah Varnosfaderani
- Abir Chakraborty
- Abhinav Mithal
topics:
- tool-using-agents
- context-engineering
- context-pruning
- enterprise-automation
- mcp
- token-efficiency
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents

## Summary
## 摘要
这篇论文测试了面向长周期、使用冗长企业工具的 LLM 智能体的上下文裁剪和短摘要方法。在一个 50 任务的 D365 F&O 酒店费用处理基准上，保留最近 5 次工具交互并加上一个小摘要，在完成率和成本上都优于保留完整历史。

## 问题
- D365 F&O 的 MCP 工具响应每次会增加 500 到 3,000 个 token，所以 15 到 30 次调用会把一个任务膨胀到 50,000 到 150,000 个 token 以上。
- 保留完整对话历史会挤爆上下文窗口，抬高推理成本，还会让智能体接触到过时的表单状态。
- 费用分摊需要剩余金额精确到 $0.00；只要还有残余金额，任务就无法完成，还会留下人工跟进工作。

## 方法
- 智能体使用 GPT-5，通过 MCP 服务器连接 D365 F&O；在受控的上下文策略实验中，GPT-4.1 作为用户模型。
- 这种方法保留完整的最近工具调用/响应对，而不是逐个裁掉 token，因此保留下来的表单状态仍然完整。
- C3 只保留最近 5 组工具调用/响应对，大约覆盖两个费用分摊周期。
- C4 保留同样的最近 5 组交互，并为最近被移出的 3 次交互添加自动摘要。
- 这项研究在同样的 50 个任务上，比较了 C2 的完整历史、C3 的裁剪，以及 C4 的裁剪加摘要，并各运行 5 次。

## 结果
- C1，即没有用户模型的 GPT-5，完成了 8.0% 的任务，99.6% 的任务至少分摊了一行，平均分摊了 58.89% 的金额。
- C2，即带用户模型的完整历史，完成了 71.0% 的任务，使用了 1,480,996 个 token，用时 14.56 小时。
- C3，即只保留最近 5 次工具调用，完成了 79.0%，使用了 535,274 个 token，用时 5.39 小时；相比 C2，token 减少了 63.9%，时间减少了 63.0%。
- C4，即最近 5 次加摘要，完成了 91.6%，平均分摊了 99.64% 的金额，使用了 553,374 个 token，用时 5.79 小时。
- 与 C2 相比，C4 的完整分摊率提高了 20.6 个百分点；与 C3 相比，提高了 12.6 个百分点，而 token 只比 C3 多 3.4%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10209v1](https://arxiv.org/abs/2606.10209v1)
