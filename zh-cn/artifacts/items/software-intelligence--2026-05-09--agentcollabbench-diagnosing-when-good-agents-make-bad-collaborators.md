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
AgentCollabBench 测试多智能体 LLM 流水线在代理之间传递消息时，是否能保住约束、事实、私有上下文和标记信息。论文认为，即使每个模型都能给出看起来有效的最终输出，拓扑也会带来可靠性失效。

## 问题
- 多智能体的软件、DevOps 和数据工程流程，可能会丢失硬性约束，或传播错误前提，同时仍然返回完整的最终产物。
- 只看结果的基准会漏掉过程层面的失败，比如约束丢失、错误信念传播、跨任务泄漏和多跳信息丢失。
- 这会影响已经部署的代理团队，因为一个看起来有效的 Kubernetes 清单、代码补丁或数据管道，可能漏掉必须满足的安全或合规条件。

## 方法
- 该基准包含 900 个人工验证任务，覆盖软件工程、DevOps 和数据工程。
- 每个任务针对四类风险之一：Instruction Decay Rate (IDR)、Radioactive Tracer Durability (RTD)、Consensus Pollution Rate (CPR) 和 Cross-task Leakage Containment (CLC)。
- 它变化五种通信拓扑：linear chain、branching tree、converging DAG、fully connected 和 custom graph。
- 该方法注入受控工件，比如硬性约束、唯一 tracer 字符串、错误事实或私有字符串，然后检查它们是否被保留、传播或泄漏。
- RTD 和 CLC 使用确定性的字符串检查；IDR 和 CPR 使用经过人工验证的 LLM 评审，Cohen's kappa >= 0.69，且一致率为 84.4-89.3%。

## 结果
- 在 900 个任务上，Qwen-3.5-35B-A3B 的 tracer durability 和 instruction stability 最好：RTD 94.0%，IDR 0.9%。
- GPT 4.1 mini 的泄漏和错误信念传播最低：CLC 2.6%，CPR 17.7%，但它的 RTD 为 80.3%。
- Llama 3.1 8B Instruct 在三项指标上最弱：IDR 10.1%，CPR 40.3%，RTD 62.6%；引言还报告了 4.9% 的跨任务泄漏。
- Qwen 仍然在 20.7% 的下游响应中传播了注入的错误信念，CLC 为 4.7%，所以单项优势不能覆盖所有风险。
- 拓扑解释了多跳信息存活率 7-40% 的方差，converging DAG 节点比 linear chain 更容易丢掉来自少数分支的约束。
- 扰动测试朝着预期方向变化：随着 topology siloing 增强，IDR rho 0.211、CPR rho 0.411、CLC rho 0.146，而 RTD rho -0.313。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08647v1](https://arxiv.org/abs/2605.08647v1)
