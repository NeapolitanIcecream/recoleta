---
source: hn
url: https://github.com/mikemasam/aef-spec
published_at: '2026-03-12T23:13:19'
authors:
- mikemasam
topics:
- agent-framework
- state-machine
- workflow-orchestration
- event-driven-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: AEF – Agents State Machine

## Summary
AEF（Agent Execution Framework）提出用**状态机**来组织 AI 代理的执行流程，把“当前处于什么状态、收到了什么事件、该做什么动作”明确化。它本质上是一个面向代理运行时的规范化框架，强调可控性、可解释性和流程设计，而不是新模型或新学习算法。

## Problem
- 解决的问题是：AI agent 的执行流程常常隐式、混乱，缺少对**状态、事件、动作、转移**的清晰定义，导致行为难以预测、调试和维护。
- 这很重要，因为代理在处理用户输入、计时器、外部 API、异常、沉默用户等情况时，如果没有统一执行框架，就容易出现死循环、上下文丢失或错误恢复困难。
- 文中还隐含针对多步任务与上下文中断问题：需要让代理知道“自己现在在哪一步、为什么跳转、下一步该做什么”。

## Approach
- 核心方法是把 agent 设计成一个**有限状态机**：每个状态定义进入时做什么（Entry）、状态内动作（Actions）、当前状态标识（Status）、退出条件与目标状态（Exit）、以及默认回退状态（Default）。
- 代理接收各种**事件**（如用户输入、计时器触发、外部数据返回），事件触发从一个状态迁移到另一个状态，形式类似 `$STATE_A --[event]--> $STATE_B`。
- 框架要求在每个状态中明确三件事：哪些事件可以触发离开当前状态、需要满足哪些条件/guard、转移时要执行哪些动作。
- 它还强调**进入动作**和**退出动作**的规范化，例如初始化变量、启动/停止计时器、发送初始响应、清理资源、记录状态变化。
- 实践上建议先定义 3–5 个主状态，并为失败、用户沉默、异常输入、中断恢复等边界情况设计转移规则；文中给出待办助手、多步任务处理、上下文感知助手等示例。

## Results
- 提供的是**规范/框架说明与示例**，摘录中**没有报告定量实验结果**，没有给出数据集、指标、基线或百分比提升。
- 最强的具体主张是：Execution Framework 能明确回答三件事——**代理当前在哪里（state）**、**是什么触发了变化（event）**、**转移过程中发生了什么（action）**。
- 文中宣称该框架可用于更清晰地设计代理流程，包括多步工作流、外部 API 调用、记忆管理与中断处理，但未提供数值化验证。
- 从贡献类型看，它更像**工程设计规范/执行模型**，而非在 agent benchmark 上取得突破的新算法。

## Link
- [https://github.com/mikemasam/aef-spec](https://github.com/mikemasam/aef-spec)
