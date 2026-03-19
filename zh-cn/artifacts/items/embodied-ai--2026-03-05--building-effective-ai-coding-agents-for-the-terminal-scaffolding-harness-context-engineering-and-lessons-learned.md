---
source: arxiv
url: http://arxiv.org/abs/2603.05344v2
published_at: '2026-03-05T16:21:08'
authors:
- Nghi D. Q. Bui
topics:
- terminal-agent
- coding-agent
- context-engineering
- agent-scaffolding
- tool-safety
- compound-ai-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

## Summary
本文介绍了 OpenDev，一个面向终端的开源 AI 编码代理系统设计报告，重点讨论如何把长时程代码任务做得更安全、更稳定、更节省上下文。它的主要贡献不是新算法，而是一套面向真实开发环境的工程化架构与经验总结。

## Problem
- 终端原生编码代理需要在**长会话**中工作，但 LLM 上下文窗口有限，容易出现上下文膨胀、遗忘早期信息和推理退化。
- 代理能够执行 shell 命令、修改文件、启动进程，若缺少保护机制，容易造成**破坏性操作**，这对真实软件开发非常关键。
- 系统还要兼顾**可扩展性、成本、延迟与能力**：工具和子代理越多，提示词越大、控制越难，实际可用性会下降。

## Approach
- 提出 OpenDev：一个**终端优先**的开源命令行编码代理，采用四层架构（UI、Agent、Tool & Context、Persistence）来分离界面、推理、工具、上下文和持久化职责。
- 使用**compound AI system**思路做按工作流选模型：把 thinking、critique、execution 等不同阶段绑定到不同 LLM，在成本、时延和能力之间做可配置权衡。
- 采用**双模式/双层代理**设计：Plan Mode 只允许只读工具做安全规划，Normal Mode 才执行读写操作；并通过子代理和工具白名单限制能力范围。
- 扩展 ReAct 循环，在动作前加入**显式思考、可选自我批评、上下文压缩**，配合事件驱动 system reminders、模块化提示词拼装、跨会话 memory，尽量在长任务中保持行为稳定。
- 通过**五层防御式安全机制**降低风险：提示层护栏、schema 级工具限制、运行时审批、工具级校验、生命周期 hooks；同时用懒发现工具/MCP 控制提示词体积。

## Results
- 论文**没有提供标准基准上的定量实验结果**，也没有报告诸如 SWE-bench、Terminal-Bench、LongCLI-Bench 上的准确率、成功率或成本对比数字。
- 文章的核心定位是**系统设计与经验报告**，明确表示“**not to present a novel algorithmic breakthrough**”，而是公开一个生产级终端编码代理的架构、设计权衡与 lessons learned。
- 具体系统性主张包括：使用**4 层系统架构**组织组件；在安全上采用**5 层独立防护层**；在执行上使用含 compaction/thinking/self-critique/action 的扩展循环；在架构层面支持**每工作流独立模型绑定**。
- 工程实现上给出较具体的可验证设计：如并发 session→agent→workflow→LLM 的**4 级层次结构**、子代理隔离、懒加载外部工具、跨会话 memory、事件驱动提醒等，作为构建终端原生 AI coding agent 的蓝图。

## Link
- [http://arxiv.org/abs/2603.05344v2](http://arxiv.org/abs/2603.05344v2)
