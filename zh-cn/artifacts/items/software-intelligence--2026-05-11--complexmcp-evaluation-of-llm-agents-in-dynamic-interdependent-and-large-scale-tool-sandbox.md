---
source: arxiv
url: https://arxiv.org/abs/2605.10787v1
published_at: '2026-05-11T16:20:51'
authors:
- Yuanyang Li
- Xue Yang
- Longyue Wang
- Weihua Luo
- Hongyang Chen
topics:
- llm-agents
- tool-use
- mcp
- software-automation
- agent-benchmarking
- stateful-sandboxes
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox

## Summary
## 摘要
ComplexMCP 是一个基于 MCP 的 LLM 智能体基准，要求智能体在会变化的软件沙箱中使用大量相互依赖的工具。主要发现是，强商业模型在许多真实软件自动化任务上仍会失败：报告中表现最好的模型成功率为 55.31%，人类为 93.61%。

## 问题
- 它测试简单 API 调用与商业软件自动化之间的差距。在商业软件自动化中，工具共享状态，依赖先前调用，并且可能在执行期间失败。
- 这个问题重要，因为智能体如果跳过检查、选择错误的前置工具，或在出错后放弃，可能会改错软件状态，或让任务未完成。
- 以往基准常使用孤立工具、固定环境、AST 匹配或小型沙箱，因此无法覆盖由状态、依赖关系和带噪执行造成的失败。

## 方法
- ComplexMCP 使用 Model Context Protocol 暴露 300 多个工具：7 个有状态沙箱中的 150 多个相互依赖工具，以及 150 多个无状态 API。
- 这 7 个有状态沙箱是 LightOS、LightTalk、LightShop、LightWeather、LightFlight、LightStock 和 LightNews。它们保留聊天历史、交易历史、购物车、权限以及其他嵌套数据等会话状态。
- 种子设定初始环境数据和执行时扰动，例如 API 失败。相同种子会产生可复现运行，不同种子会改变实体、权限和失败情况。
- 该基准包含 47 个手工整理的任务。一些标准轨迹需要使用 30 多个唯一工具，并进行 60 多次工具调用。
- 评估基于规则：它将智能体最终的嵌套环境状态与真实状态进行比较，报告完成率和误行为率，并且只有在完成率为 100%、误行为率为 0% 时才将任务计为正确。

## 结果
- 在 47 个任务的全上下文 ReAct 评估中，Gemini-3-Flash 的模型成功率最高，为 55.31% ± 0.00，完成率为 85.79% ± 0.50，误行为率为 4.39% ± 0.19。
- 人类用户使用相同的 MCP 接口和评估器，达到 93.61% ± 1.74 的成功率、97.73% ± 1.18 的完成率和 0.81% ± 0.27 的误行为率。
- 其他报告的成功率包括 Gemini-3-Pro 的 44.67% ± 1.74、GLM-4.7 的 42.55% ± 0.00、Claude-Opus-4 的 41.84% ± 2.01、Claude-Sonnet-4.5 的 39.71% ± 1.00，以及 Qwen-3-Max 的 31.20% ± 1.00。
- GPT-5.1 的成功率为 19.14% ± 1.74，完成率为 24.63% ± 1.87，误行为率为 1.42% ± 0.47；作者报告称，它在 token 或工具出错后常无法恢复。
- 全上下文设置用于工具描述的提示约为 29,964 个 token。按平均 11 轮工具调用计算，在计入生成内容和工具反馈前，每个任务的重复提示量约为 360,000 个 token。
- 作者识别出三类失败模式：动作空间增长导致工具检索饱和，过度自信的规划导致跳过环境检查，以及出错后为失败找理由而没有恢复。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10787v1](https://arxiv.org/abs/2605.10787v1)
