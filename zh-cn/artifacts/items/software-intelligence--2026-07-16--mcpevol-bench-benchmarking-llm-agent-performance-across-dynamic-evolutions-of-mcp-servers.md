---
source: arxiv
url: https://arxiv.org/abs/2607.14642v1
published_at: '2026-07-16T07:09:49'
authors:
- Huanxi Liu
- Kun Hu
- Jiaqi Liao
- Qiang Wang
- Pengfei Qian
- YuanZhao Zhai
- Dawei Feng
- Bo Ding
- Huaimin Wang
topics:
- software-foundation-model
- code-intelligence
- agent-network
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers

## Summary
## 摘要
MCPEvol-Bench 评估了当 MCP 工具接口和功能发生演变时，LLM 智能体能否维持任务性能。在 12 个模型中，服务器演变导致性能显著下降，表明静态工具使用基准会高估智能体在变化环境中的可靠性。

## 问题
- 现有 MCP 和工具使用基准主要在静态工具集上评估智能体，因此无法衡量智能体对工具、参数、描述或服务器功能变化的适应能力。
- 这一点很重要，因为 MCP 服务器在实际使用中会持续演变：远程服务器的可用率在 12 周内从 72.7% 降至 52.0%，分析的初始工具中有 54.6% 被修改或弃用。

## 方法
- 该基准包含 123 个 MCP 服务器、1,272 个工具，以及覆盖九个领域的 201 个多工具任务；每项任务都在原始服务器，以及经过三轮和五轮变异后演变出的服务器版本上进行测试。
- 作者根据观察到的 MCP 演变归纳出 11 种变异算子，涵盖工具、参数和描述变化，例如新增、替换、删除、约束变异和描述更新。
- 一个由 LLM 驱动的流程使用基于 AST 的代码锚定技术，对源代码仓库应用变异，验证语法和功能，并部署生成的多版本 MCP 服务器。
- 智能体采用 1–10 分制的任务完成度（Task Fulfillment）和规划有效性（Planning Effectiveness）进行评估，此外还使用演变能力得分（Evolutionary Competency Score），奖励高性能和较低的跨版本方差。

## 结果
- 在演变后的 MCP 服务器上，GPT-5.4 的任务完成度性能下降了 13.7%，Claude-Sonnet-4-6 下降了 14.4%；该研究在 201 项任务上评估了 12 个 LLM。
- 在分析的智能体轨迹中，服务器演变使规划错误增加了 34.1%，推理错误增加了 35.6%。
- 工具新增和修改导致了最明显的性能损失，而删除冗余工具或参数对原始工作流执行的影响可以忽略不计。
- 基准中的模拟演变与现实世界的版本更新表现出较高的语义相似度，并与人工评估结果高度一致，但摘录没有提供相应的相似度或一致性数值。
- 添加反思、规划和记忆模块提高了智能体的适应能力，但摘录没有报告这些改进的定量增益，也没有提供完整的逐模型基线表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14642v1](https://arxiv.org/abs/2607.14642v1)
