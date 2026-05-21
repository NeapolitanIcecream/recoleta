---
source: arxiv
url: https://arxiv.org/abs/2605.08647v1
published_at: '2026-05-09T03:35:09'
authors:
- Aritra Mazumder
- Shubhashis Roy Dipta
- Nusrat Jahan Lia
- Tanzila Khan
- Kainat Raisa Hossain
- Nehaa Shri
- Shubhrangshu Debsarkar
- Humayra Tasnim
- Gour Gupal Talukder Shawon
- Debjoty Mitra
- Sumaiya Ahmed Rani
- Al Jami Islam Anik
- Al Nafeu Khan
topics:
- multi-agent-systems
- software-engineering-agents
- agent-evaluation
- llm-reliability
- collaboration-failures
- benchmarking
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators

## Summary
## 摘要
AgentCollabBench 测试多智能体 LLM 流水线在智能体相互传递消息时，能否保留约束、事实、私有上下文和带标记的信息。论文称，即使每个模型都能生成看起来有效的最终输出，通信拓扑也可能造成可靠性故障。

## 问题
- 多智能体软件、DevOps 和数据工程工作流可能丢失硬性约束，或传播错误前提，同时仍返回完整的最终产物。
- 只看结果的基准会漏掉过程故障，例如约束丢失、错误信念传播、跨任务泄漏和多跳信息丢失。
- 这会影响已部署的智能体团队，因为有效的 Kubernetes 清单、代码补丁或数据流水线可能遗漏必需的安全或合规条件。

## 方法
- 该基准包含 900 个经人工验证的任务，覆盖软件工程、DevOps 和数据工程。
- 每个任务针对四类风险之一：指令衰减率（Instruction Decay Rate，IDR）、放射性示踪耐久性（Radioactive Tracer Durability，RTD）、共识污染率（Consensus Pollution Rate，CPR）和跨任务泄漏控制（Cross-task Leakage Containment，CLC）。
- 它改变五种通信拓扑：线性链、分支树、汇聚型 DAG、全连接和自定义图。
- 该方法注入受控产物，例如硬性约束、唯一示踪字符串、错误事实或私有字符串，然后检查它们是否被保留、传播或泄漏。
- RTD 和 CLC 使用确定性字符串检查；IDR 和 CPR 使用 LLM 评审，并通过人工验证，Cohen's kappa >= 0.69，一致率为 84.4-89.3%。

## 结果
- 在 900 个任务上，Qwen-3.5-35B-A3B 的示踪耐久性和指令稳定性最好：RTD 为 94.0%，IDR 为 0.9%。
- GPT 4.1 mini 的泄漏和错误信念传播最低：CLC 为 2.6%，CPR 为 17.7%，其 RTD 为 80.3%。
- Llama 3.1 8B Instruct 在三项指标上最弱：IDR 为 10.1%，CPR 为 40.3%，RTD 为 62.6%；引言还报告其跨任务泄漏为 4.9%。
- Qwen 仍在 20.7% 的下游回复中传播注入的错误信念，CLC 为 4.7%，因此单一风险上的强表现不能覆盖所有风险。
- 拓扑解释了多跳信息保留方差的 7-40%，其中汇聚型 DAG 节点比线性链更常丢失少数分支携带的约束。
- 扰动测试按预期方向变化：随着拓扑隔离增强，IDR rho 为 0.211，CPR rho 为 0.411，CLC rho 为 0.146，RTD rho 为 -0.313。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08647v1](https://arxiv.org/abs/2605.08647v1)
