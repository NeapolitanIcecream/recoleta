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
ComplexMCP 是一个基于 MCP 的基准，用来评估 LLM 智能体在不断变化的软件沙箱中使用大量相互依赖工具的能力。主要结论是，即使是强力商业模型，在真实软件自动化任务中也会频繁失败：目前最好的模型成功率为 55.31%，而人类为 93.61%。

## 问题
- 它测试的是简单 API 调用和商业软件自动化之间的差距。在这类任务里，工具共享状态，依赖前面的调用，执行时还可能出错。
- 这个问题很重要，因为如果智能体跳过检查、选错前置工具，或者在出错后放弃，就可能改错软件状态，或者让任务半途而废。
- 以往的基准常用孤立工具、固定环境、AST 匹配或小型沙箱，所以抓不到由状态、依赖关系和噪声执行带来的失败。

## 方法
- ComplexMCP 使用 Model Context Protocol 暴露 300 多个工具：7 个有状态沙箱中的 150 多个相互依赖工具，加上 150 多个无状态 API。
- 这 7 个有状态沙箱是 LightOS、LightTalk、LightShop、LightWeather、LightFlight、LightStock 和 LightNews。它们保留会话状态，比如聊天记录、交易历史、购物车、权限和其他嵌套数据。
- 一个 seed 用来设置初始环境数据和执行时扰动，例如 API 失败。相同 seed 会得到可重复的运行结果，不同 seed 会改变实体、权限和失败情况。
- 这个基准有 47 个人工整理的任务。有些 gold trajectory 需要超过 30 个不同工具和超过 60 次总工具调用。
- 评估采用规则方法：比较智能体最终的嵌套环境状态和真实状态，报告完成率和异常行为率，并且只有在完成度为 100% 且异常行为率为 0% 时才算正确。

## 结果
- 在 47 个任务上的 full-context ReAct 评估中，Gemini-3-Flash 的模型成功率最高，为 55.31% ± 0.00，完成率为 85.79% ± 0.50，异常行为率为 4.39% ± 0.19。
- 使用同样的 MCP 接口和评估器，人类用户的成功率达到 93.61% ± 1.74，完成率为 97.73% ± 1.18，异常行为率为 0.81% ± 0.27。
- 其他报告的成功率包括：Gemini-3-Pro 为 44.67% ± 1.74，GLM-4.7 为 42.55% ± 0.00，Claude-Opus-4 为 41.84% ± 2.01，Claude-Sonnet-4.5 为 39.71% ± 1.00，Qwen-3-Max 为 31.20% ± 1.00。
- GPT-5.1 的成功率为 19.14% ± 1.74，完成率为 24.63% ± 1.87，异常行为率为 1.42% ± 0.47；作者报告说，它经常在 token 或工具出错后无法恢复。
- full-context 设置里，工具说明大约占用 29,964 个 prompt token。平均有 11 轮工具调用时，在不计生成内容和工具反馈的情况下，每个任务重复注入的 prompt 总量大约是 360,000 个 token。
- 作者识别出三种失败模式：随着动作空间变大，工具检索开始饱和；由于规划过于自信，智能体跳过了环境检查；出错后不去恢复，而是给失败找理由。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10787v1](https://arxiv.org/abs/2605.10787v1)
