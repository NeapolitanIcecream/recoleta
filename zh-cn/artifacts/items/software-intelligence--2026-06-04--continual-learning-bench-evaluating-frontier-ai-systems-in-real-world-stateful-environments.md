---
source: arxiv
url: https://arxiv.org/abs/2606.05661v1
published_at: '2026-06-04T03:43:28'
authors:
- Parth Asawa
- Christopher M. Glaze
- Gabriel Orlanski
- Ramya Ramakrishnan
- Benji Xu
- Asim Biswal
- Vincent Sunn Chen
- Frederic Sala
- Matei Zaharia
- Joseph E. Gonzalez
topics:
- continual-learning
- llm-agents
- agent-memory
- benchmarking
- software-engineering
- stateful-evaluation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments

## Summary
## 摘要
CL-Bench 测试 LLM 代理是否会在一串相关的真实世界任务中持续改进，而不只是对孤立提示表现良好。主要发现是，在平均水平上，使用完整上下文的上下文学习优于多个记忆系统。

## 问题
- 现有的记忆、长上下文和测试时自适应评估，往往测试的是回忆、上下文压缩或静态任务准确率；它们没有衡量代理是否会随着时间学习环境中的隐含结构。
- 这对软件代理、预测代理和决策支持代理很重要，因为它们需要复用先前交互中的经验，并在概念漂移后做出调整。

## 方法
- CL-Bench 包含六个领域：软件工程、信号处理、疾病暴发预测、数据库查询、策略游戏和需求预测。
- 每个任务都是一组按顺序出现的实例，彼此共享隐藏结构，例如代码库布局、模式约定、疾病动力学或对手策略。
- 该基准比较保留先前经验的有状态运行和每个实例都从头开始的无状态运行。
- 主要指标是 gain：同一系统在同一实例上的有状态奖励减去无状态奖励。normalized gain 再用系统剩余的上限对其进行缩放。
- 任务至少由两位作者审阅，并由 2 到 3 位领域专家验证其真实感、可复用知识和可测量的学习改进。

## 结果
- 整体表现最好的系统是使用 Claude Sonnet 4.6 的完整上下文 ICL：归一化奖励 22.3% ± 4.1，归一化 gain 25.4% ± 3.6，平均 rollout 成本为 30.4 美元。
- 使用 GPT-5.4 的完整上下文 ICL 在归一化奖励上排第二：奖励 20.1% ± 9.1，gain 20.1% ± 9.1，成本 18.4 美元。
- 使用 Sonnet 4.6 的 Claude Code 在奖励上排第三，在 gain 上处于第二梯队：奖励 19.0% ± 7.1，gain 23.9% ± 5.7，成本 38.6 美元。
- 专用记忆系统落后：使用 GPT-5.4 的 Mem0 达到奖励 15.1% ± 6.4，gain 20.2% ± 5.9；使用 GPT-5.4 的 ACE 达到奖励 4.6% ± 2.7，gain 8.6% ± 2.5，成本 62.8 美元。
- 使用 Gemini 3 Flash 的 ICL 记录中的成本最低，为 7.6 美元，同时仍达到 16.4% ± 3.8 的归一化 gain。
- 按任务看，Sales Prediction 和 Blind Spectrum Monitoring 的学习曲线更清楚，Cohort Studies 的学习较弱，Database Exploration 的 gain 主要来自有状态运行避开了无状态运行中频繁出现的失败。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05661v1](https://arxiv.org/abs/2606.05661v1)
