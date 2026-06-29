---
source: arxiv
url: https://arxiv.org/abs/2606.01508v1
published_at: '2026-06-01T00:08:03'
authors:
- Ankur Sharma
- Deep Shah
topics:
- agent-operating-system
- agentic-control-plane
- os-security
- agent-governance
- tool-mediation
- auditability
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Agent Operating Systems (AOS): Integrating Agentic Control Planes into, and Beyond, Traditional Operating Systems

## Summary
## 总结
论文将 Agent Operating System 定义为面向长运行 AI 智能体的控制平面，这些智能体需要调度、记忆、权限、策略检查和审计轨迹，超出普通进程管理的范围。这是一篇概念性的系统论文，重点在架构和评估标准，而不是基准测试结果。

## 问题
- 传统操作系统抽象，如进程、线程、文件、系统调用和静态权限，不能表达智能体意图、目标进展、委托权限、工具使用或决策来源。
- 生产环境中的智能体系统常把调度、记忆、权限、工具中介和审计放在应用代码里，这会削弱强制执行，也让事故复盘更难。
- 这个问题很重要，因为智能体可以在文件、网络、API 和服务之间执行有副作用的操作，而它们的推理仍然是概率性的，可能出错，也可能被操纵。

## 方法
- 论文提出在现有内核之上增加一层 Agent Operating System，把智能体身份、目标、任务图、能力集合、上下文状态和执行记录作为一等管理对象。
- 它把推理、执行和策略分开：模型提出动作，策略层批准或拒绝，执行层在受控环境中运行已批准的工具调用。
- 架构包括生命周期管理、面向目标的调度、上下文和记忆管理、工具和能力注册表、确定性的策略强制执行，以及只追加的审计记录。
- 它把 AOS 的部署路径对应到用户空间运行时、操作系统扩展、分布式控制平面，以及对更高层 OS 职责的部分接管，同时把分页、驱动和底层 CPU 调度等内核职责留在操作系统中。
- 设计基于现有 Linux 和 Windows 机制，包括容器、cgroups、命名空间、seccomp、SELinux/AppArmor、eBPF、Windows 策略控制和审计流。

## 结果
- 摘要中没有量化基准结果，没有原型性能数据，也没有与 Linux、Windows、Kubernetes 或智能体运行时的实测比较。
- 论文声称有 6 项主要贡献：AOS 定义、组件拆分、集成模型、Linux/Windows 映射、安全分析和评估标准。
- 它定义了 3 个分离平面：推理、执行和策略，并要求任何有副作用的动作在执行前必须经过确定性的允许决策。
- 它列出 4 条架构不变式，包括任何有副作用的动作都不能在没有确定性允许决策的情况下执行，以及策略结果要记录在只追加的审计日志中。
- 它描述了 4 种集成模型：用户空间运行时、操作系统扩展、分布式控制平面，以及对更高层 OS 职责的选择性接管。
- 它给出 4 类智能体记忆：短暂上下文、持久智能体记忆、检索知识和执行记录，每类的保留、来源和审计需求都不同。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.01508v1](https://arxiv.org/abs/2606.01508v1)
