---
source: arxiv
url: https://arxiv.org/abs/2604.27882v1
published_at: '2026-04-30T14:01:06'
authors:
- Giuseppe Arbore
- Andrea Sillano
- Luigi De Russis
topics:
- multi-agent-systems
- persona-agents
- agent-orchestration
- personalization
- human-ai-interaction
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Building Persona-Based Agents On Demand: Tailoring Multi-Agent Workflows to User Needs

## Summary
这篇论文提出了一个运行时流水线，为每个用户查询创建基于人格的代理，输入包括用户画像、任务需求和会话上下文。它面向个性化的多代理工作流，但摘录中没有实现、基准测试或用户研究。

## Problem
- 多代理系统常用预设角色、通信路径和执行顺序，这让它们很难适配用户熟练度、任务上下文和偏好的交互方式。
- 这很重要，因为同一个高层请求，用户可能需要不同的解释方式、任务拆分和代理行为。
- 固定的代理设置在用户或任务变化时，需要改动提示词或编排逻辑。

## Approach
- 中央编排器接收一个开放式查询，并运行 ProfileEncode 来推断用户特征、意图、领域熟悉度和沟通偏好。
- TaskDecompose 将查询拆分为多个子任务，并记录依赖关系，这样部分任务可以并行执行，其他任务要等所需输出完成后再继续。
- PersonaCraft 为每个子任务创建一个人格，角色、领域技能、沟通风格和能力都来自查询和用户画像。
- AgentFactory 根据每个人格实例化一个由 LLM 支持的代理，然后由编排器分配任务、路由中间输出，并聚合最终答案。
- 系统会在一个会话中保留生成的人格和代理，并且可以在后续查询中添加新的实例。

## Results
- 摘录没有给出任何定量评估结果：没有准确率、任务完成率、延迟、成本或用户满意度数据。
- 文中声称的系统流程有 4 个阶段：Query Analysis、Agent Generation and Instantiation、Agent Assigning and Execution、Answers Aggregation and Displaying。
- 算法列出了 18 个按需生成基于人格代理的步骤，从用户查询开始，到聚合响应结束。
- 最明确的具体主张是架构层面的：代理角色、风格和协调行为会根据用户画像、任务计划和会话上下文在运行时生成。
- 论文声称会话模型通过保留先前的代理和人格来改善多次查询之间的一致性，但没有提供与固定角色多代理系统的实测对比。

## Link
- [https://arxiv.org/abs/2604.27882v1](https://arxiv.org/abs/2604.27882v1)
