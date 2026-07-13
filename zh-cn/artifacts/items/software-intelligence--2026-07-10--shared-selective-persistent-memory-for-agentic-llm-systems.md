---
source: arxiv
url: https://arxiv.org/abs/2607.09493v1
published_at: '2026-07-10T15:07:00'
authors:
- Sanjana Pedada
- Aditya Dhavala
- Neelraj Patil
topics:
- agentic-llm-systems
- persistent-memory
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Shared Selective Persistent Memory for Agentic LLM Systems

## Summary
## 摘要
论文提出了一种面向智能体 LLM 系统的共享记忆架构。该架构保留可复用的工作区上下文，同时丢弃特定于会话的轨迹。在企业和公共数据集评估中，该架构实现了更高的任务完成率、更低的 token 用量、更快的执行速度，并支持对模式兼容的数据更新进行零 token 刷新。

## 问题
- 智能体 LLM 会话会丢弃任务规则、数据模式、工具设置和输出要求，导致用户在重复任务中反复说明这些内容。
- 保存完整对话历史会带入无关的推理过程和工具调用轨迹，可能影响后续生成并降低质量。
- 这一问题会影响重复生成仪表板、报告、数据更新和协作式制品开发，因为反复说明需求会增加时间、token 用量和出错风险。

## 方法
- 为每个工作区保存四类可复用上下文：任务规格、数据模式、工具配置和输出约束。
- 不将推理轨迹、工具日志、临时文件、失败的恢复路径、未经批准的编辑和原始数据写入持久化记忆。
- 将结构化记忆注入每个新会话，并使用紧凑的统计模式提供数据，而不是提供原始数据集。
- 要求生成的制品通过运行时注入点读取数据，使兼容的数据变更无需再次调用 LLM。
- 增加带有基于角色的访问控制的共享工作区、由 git 支持的制品版本、草稿隔离和回滚功能。

## 结果
- 在 24 个企业重复生成任务中，选择性记忆的完成率达到 96%，没有记忆时为 79%，使用完整历史时为 71%。
- 使用选择性记忆时，平均用户交互轮数降至 1.4 轮；没有记忆时为 4.3 轮，使用完整历史时为 3.1 轮。平均耗时降至 68 秒，而另外两种方式分别为 285 秒和 310 秒。
- 选择性记忆使用 3.4K 个输入 token 和 4.1K 个输出 token；使用完整历史时分别为 18.7K 和 9.6K。论文报告称，与注入原始数据相比，基于摘要的生成将 token 成本降低了 97 倍。
- 对于模式兼容的企业任务，18 个任务全部成功完成零 token 刷新。在报告的部署场景中，重复任务耗时减少了 14 倍。
- 在四个公共数据集的 36 次试验中，选择性记忆在 12 次刷新试验中全部完成任务，且使用零个 LLM token；没有记忆时的完成率为 83%，使用完整历史时为 75%。
- 报告中最突出的一项局限是：在跨文件连接语义任务上，选择性记忆失败，因为模式摘要没有捕获这类语义。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09493v1](https://arxiv.org/abs/2607.09493v1)
