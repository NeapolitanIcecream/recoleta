---
source: hn
url: https://arxiv.org/abs/2605.18747
published_at: '2026-06-24T23:14:13'
authors:
- matt_d
topics:
- software-foundation-models
- code-intelligence
- agentic-ai
- multi-agent-software-engineering
- human-ai-interaction
- devops-automation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Code as Agent Harness

## Summary
## 摘要
这篇综述认为，代码正在成为 AI 智能体的 harness：智能体在这一层进行推理、行动、保存状态、调用工具并验证工作。这个观点关系到软件工程、操作系统自动化、DevOps 和多智能体工作流，因为这些系统需要可执行的状态和检查，而不只需要生成的文本。

## 问题
- LLM 智能体经常需要执行长任务、使用工具、记住上下文并检查自己的工作；普通聊天输出无法提供足够的控制和可追踪性。
- 智能体系统需要更安全的方式，把推理与软件仓库、GUI、操作系统、企业工作流和科学工作中的行动连接起来。
- 多智能体系统需要共享制品和一致状态，让智能体能够协作、审查并验证彼此的工作。

## 方法
- 这篇论文是一篇综述，不是新的模型论文或基准论文。
- 它的核心机制很简单：把代码视为智能体 harness，也就是由代码保存智能体的状态、工具调用、计划、环境模型和执行检查。
- 它把主题组织为 3 层：harness 接口、harness 机制，以及从单智能体系统扩展到多智能体系统。
- 它回顾了规划、记忆、工具使用、反馈驱动控制、优化、协作、审查和验证的方法。
- 它把这一思路映射到编码助手、GUI 和操作系统自动化、具身智能体、科学发现、个性化、DevOps 和企业工作流等场景。

## 结果
- 摘录没有报告基准分数、数据集、消融研究或实测性能提升。
- 主要的具体主张是对基于代码的智能体 harness 做出 3 层组织：接口、机制和多智能体扩展。
- 它提出了 6 个开放工程问题：超越最终任务成功率的评估、不完整反馈下的验证、无回归的 harness 改进、一致的共享状态、安全关键行动中的人工监督，以及多模态扩展。
- 它覆盖了摘要中点名的 7 个应用领域：编码助手、GUI/OS 自动化、具身智能体、科学发现、个性化和推荐、DevOps，以及企业工作流。
- 它声称的贡献是面向可执行、可验证、有状态智能体系统的综述级综合，而不是量化突破。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18747](https://arxiv.org/abs/2605.18747)
