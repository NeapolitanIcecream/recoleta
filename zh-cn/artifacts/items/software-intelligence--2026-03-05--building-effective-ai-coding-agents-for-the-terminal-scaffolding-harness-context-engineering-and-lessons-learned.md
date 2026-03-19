---
source: arxiv
url: http://arxiv.org/abs/2603.05344v2
published_at: '2026-03-05T16:21:08'
authors:
- Nghi D. Q. Bui
topics:
- coding-agents
- terminal-agents
- context-engineering
- tool-using-llms
- software-engineering
- agent-safety
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

## Summary
本文介绍了 OpenDev，一个面向终端的开源 AI 编码代理系统，重点不在提出新算法，而在总结如何把终端代理做得更安全、可扩展、能长期运行。论文的核心价值是把脚手架、运行时编排、上下文工程和安全机制整理成一套可复用的工程蓝图。

## Problem
- 终端原生编码代理虽然更接近开发者真实工作流，但在**长时任务**中会遇到上下文窗口耗尽、推理质量下降和行为漂移。
- 这类代理能直接执行 shell、修改文件、运行进程，如果缺少系统化约束，容易产生**破坏性操作**，因此安全问题比普通 IDE 补全更关键。
- 代理还需要支持越来越多工具和能力，但把所有工具/说明都塞进提示词会造成**prompt 膨胀**，影响成本、延迟和效果；这对软件基础模型与自动化软件生产很重要，因为真实软件工程任务往往跨多步、跨会话、跨工具链。

## Approach
- 提出 **OpenDev**：一个终端优先的开源命令行编码代理，采用四层架构（UI、Agent、Tool & Context、Persistence），将构建期的 **scaffolding** 与运行期的 **harness** 分离。
- 使用**复合 AI 系统**设计：不同工作流/阶段可绑定不同 LLM；同时采用**双代理/双模式**结构，把只读规划（Plan Mode）与可执行修改（Normal Mode）分开，以降低风险并平衡成本、延迟、能力。
- 扩展标准 ReAct：在动作前加入显式 **thinking** 和可选 **self-critique** 阶段，并把**自适应上下文压缩**直接嵌入循环，在上下文接近上限时逐步压缩旧观察。
- 通过**条件化提示组装**、**事件驱动系统提醒**、**跨会话记忆**和**惰性工具发现**来控制上下文负担：只在相关时注入指令/技能/工具，减少 prompt 冗余并缓解 instruction fade-out。
- 采用**五层纵深防御安全架构**：提示级护栏、schema 级工具限制、运行时审批、工具级校验、生命周期 hooks，多层独立拦截危险操作。

## Results
- 论文**没有给出明确的定量实验结果或基准分数**；摘录中未报告如 SWE-bench、Terminal-Bench、LongCLI-Bench 的准确率、通过率、成本或延迟数字。
- 最强的具体主张是：OpenDev 提供了一个**开源、终端原生、交互式**编码代理的系统化技术报告，作者声称这在公开文献中是首次较完整披露此类系统的工程设计。
- 系统层面的具体产出包括：**4 层总体架构**、**5 个模型角色**、**6 阶段执行循环**、**5 层安全机制**，以及会话→代理→工作流→LLM 的**4 级层次化组织**。
- 作者声称这些机制带来几类工程收益：更好的成本/延迟/能力权衡、更安全的终端执行、更高的上下文效率，以及跨会话积累项目知识；但摘录中**未提供可验证的数字对比**来证明优于 Claude Code、Aider、OpenHands 或 SWE-Agent。

## Link
- [http://arxiv.org/abs/2603.05344v2](http://arxiv.org/abs/2603.05344v2)
