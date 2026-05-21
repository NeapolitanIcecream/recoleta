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
## 摘要
论文提出了一个运行时流水线，为每个用户查询创建基于角色画像的智能体，使用用户画像、任务需求和会话上下文。它面向个性化多智能体工作流，但摘录中没有报告实现、基准测试或用户研究。

## 问题
- 多智能体系统常使用预设角色、通信路径和执行顺序，这使它们难以适应用户专业水平、任务上下文和偏好的交互风格。
- 这一点很重要，因为对于同一个高层请求，用户可能需要不同的解释、任务拆分和智能体行为。
- 当用户或任务发生变化时，固定的智能体设置需要修改提示词或编排方式。

## 方法
- 中央编排器接收开放式查询，并运行 ProfileEncode 来推断用户特征、意图、领域熟悉度和通信偏好。
- TaskDecompose 将查询拆分为子任务并记录依赖关系，使一些任务可以并行运行，另一些任务等待所需输出。
- PersonaCraft 为每个子任务创建一个角色画像，包含从查询和用户画像中提取的角色、领域技能、通信风格和能力。
- AgentFactory 基于每个角色画像实例化一个由 LLM 支持的智能体，然后编排器分配任务、路由中间输出，并汇总最终答案。
- 系统在会话内保留生成的角色画像和智能体，并可在后续查询中添加新的角色画像和智能体。

## 结果
- 摘录给出的定量评估结果为 0：没有报告准确率、任务完成率、延迟、成本或用户满意度数据。
- 论文声称的系统流程有 4 个阶段：Query Analysis、Agent Generation and Instantiation、Agent Assigning and Execution、Answers Aggregation and Displaying。
- 算法列出了按需生成基于角色画像的智能体的 18 个步骤，从用户查询开始，以汇总响应结束。
- 最具体的主张是架构层面的：智能体的角色、风格和协调行为在运行时根据用户画像、任务计划和会话上下文生成。
- 论文声称，会话模型通过保留先前的智能体和角色画像来提高多次查询之间的一致性，但没有提供与固定角色多智能体系统的测量对比。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27882v1](https://arxiv.org/abs/2604.27882v1)
