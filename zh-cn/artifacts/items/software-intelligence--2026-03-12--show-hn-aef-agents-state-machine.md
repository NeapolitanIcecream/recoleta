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
- ai-agents
- execution-model
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: AEF – Agents State Machine

## Summary
AEF（Agent Execution Framework）提出用有限状态机来组织 AI agent 的执行流程，把状态、事件、动作和转移明确化，可视作一种轻量级“agent 操作系统”规范。它主要是一个设计与实现框架，而不是带实验验证的研究论文。

## Problem
- 解决 AI agent 在多步交互、外部事件、超时、中断和失败场景下缺乏**清晰执行控制**的问题。
- 这很重要，因为没有显式状态与转移时，agent 容易出现流程混乱、难调试、难恢复和行为不可预测。
- 对多代理/复杂工作流系统而言，需要一种统一方式描述“当前在做什么、为什么切换、接下来做什么”。

## Approach
- 核心方法是把 agent 建模为**有限状态机**：agent 处于某个 state，收到某个 event 后执行 action，并转移到下一个 state。
- 每个状态显式定义 `Entry / Actions / Status / Exit / Default`，分别对应进入时初始化、状态内行为、当前状态标识、退出条件与默认回退状态。
- 转移以 `$STATE_A --[event]--> $STATE_B` 形式表达，并建议为每个状态定义可触发退出的事件、守卫条件以及转移时动作。
- 框架强调异常与边界情况设计，如失败、用户沉默、意外输入、外部 API 调用与中断恢复。
- 文中通过待办助手、多步任务处理器、具上下文记忆的助手等示例，说明如何从 3–5 个主状态开始搭建 agent 工作流。

## Results
- 文本**没有提供定量实验结果**，没有报告数据集、准确率、成功率、延迟或与基线方法的数值比较。
- 最强的具体主张是：Execution Framework 能明确回答 3 个问题——agent 在哪里（state）、什么触发了移动（event）、转移过程中发生了什么（action）。
- 规范给出了至少 **5 个状态字段**（Entry, Actions, Status, Exit, Default）和 **3 个核心运行元素**（state, event, action/transition），用于结构化 agent 行为定义。
- 文中建议实际设计时从 **3–5 个主状态** 起步，并覆盖失败、静默、异常输入等场景，以提升可维护性和可预测性。

## Link
- [https://github.com/mikemasam/aef-spec](https://github.com/mikemasam/aef-spec)
