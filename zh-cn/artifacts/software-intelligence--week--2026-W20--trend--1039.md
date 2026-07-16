---
kind: trend
trend_doc_id: 1039
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- "\u4EE3\u7801\u667A\u80FD\u4F53"
- "\u667A\u80FD\u4F53\u8BC4\u4F30"
- "\u53EF\u6267\u884C\u53CD\u9988"
- "\u8F6F\u4EF6\u5DE5\u7A0B\u57FA\u51C6"
- "\u8FD0\u884C\u65F6\u8F68\u8FF9"
- "\u667A\u80FD\u4F53\u5B89\u5168"
run_id: materialize-outputs
aliases:
- recoleta-trend-1039
tags:
- recoleta/trend
- "topic/\u4EE3\u7801\u667A\u80FD\u4F53"
- "topic/\u667A\u80FD\u4F53\u8BC4\u4F30"
- "topic/\u53EF\u6267\u884C\u53CD\u9988"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B\u57FA\u51C6"
- "topic/\u8FD0\u884C\u65F6\u8F68\u8FF9"
- "topic/\u667A\u80FD\u4F53\u5B89\u5168"
language_code: zh-CN
---

# 代码智能体需要可执行证明、有边界的工作循环和可审计轨迹

## 概览
本周的代码智能体研究提高了有用工作的评测门槛。SWE-Cycle 和 SaaSBench 对设置、集成、测试和交付行为评分。Rollout Cards 为智能体运行增加报告规范。共同要求很直接：智能体需要拿出证据，证明任务是在真实运行约束下完成的。

## 研究发现

### 端到端软件交付基准
基准开始把编码当成完整工作周期来评测。SWE-Cycle 让智能体在 489 个 GitHub issue 实例中设置仓库、修改代码并编写验证测试。Phoenix-bench 加入硬件工程仓库和可执行 EDA 检查；智能体在这些任务上的迁移效果差，因为领域工具链和项目结构会影响结果。SaaSBench 和 WebGameBench 把同一标准推进到交付应用：企业 SaaS 系统和可玩的浏览器游戏按运行时行为、配置和跨组件集成来评判。

#### 资料来源
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): 条目摘要将 SWE-Cycle 描述为一个包含 489 个实例的端到端 GitHub issue 基准，涵盖环境设置、代码修改和验证测试。
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): 条目摘要描述了 Phoenix-bench 及其面向 Verilog/SystemVerilog 仓库 issue 的可执行 EDA 检查。
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): 条目摘要描述了 SaaSBench 在设置、配置和跨组件集成方面的失败。
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): 条目摘要描述了 WebGameBench 通过真实浏览器可玩性和需求满足度进行评估。

### 用于训练和任务设计的可执行反馈
多篇论文把执行结果用作监督来源或任务约束。DuST 使用测试时扩展过程中产生、并带有执行标签的候选代码来训练。FrontierSmith 把封闭式编码任务转成开放式优化问题，DIO-Agent 在代码发现过程中使用执行错误。Orchard 增加了可复用的沙箱基础设施，让智能体可以在软件工程、浏览器使用和助手场景中运行任务。实际方向一致：评分、错误和沙箱状态正在成为数据流水线的一部分。

#### 资料来源
- [FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale](../Inbox/2026-05-14--frontiersmith-synthesizing-open-ended-coding-problems-at-scale.md): 条目摘要描述了 FrontierSmith 用于训练 LLM 编码器的开放式优化型编码问题。
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): 条目摘要描述了 Orchard 基于 Kubernetes 的沙箱基础设施，用于跨任务领域的智能体训练。

### 基准、轨迹和工具访问的可审计性
本周的研究也把智能体分数当作需要检查的对象。BenchJack 在常规运行前审计基准中的奖励黑客路径，并在 10 个热门基准中发现了可利用点。Rollout Cards 要求智能体论文发布 rollout 记录、视图、报告规则和省略字段，以便重新检查分数。Model Context Protocol (MCP) 在企业工具中的部署提出了同样的控制问题：访问、权限和第三方技能需要审查路径，之后智能体才能在生产环境中执行操作。

#### 资料来源
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): 条目摘要描述了 BenchJack 在热门智能体基准中发现的利用方式。
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): 条目摘要描述了 Rollout Cards 以及发布 rollout 记录和报告规则的要求。
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): 条目摘要描述了无载荷第三方技能可能导致编码智能体生成并运行恶意代码。

### 已验证的漏洞修复循环
安全修复工作集中在运行时证据和可复用修复知识上。ContraFix 比较崩溃执行和安全执行，以推断补丁必须强制满足的条件，然后存储成功的修复规格和输入变异策略。MemRepair 为仓库级漏洞修复增加持久记忆，并报告了在 SEC-Bench、PatchEval 和 Multi-SWE-bench C++ 上的提升。这些系统把过去的修复和具体执行作为下一次修复尝试的输入，使评估既依赖轨迹质量，也依赖补丁文本。

#### 资料来源
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): 条目摘要描述了 ContraFix 配对使用崩溃执行和安全执行，并存储修复规格。
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): 条目摘要描述了 MemRepair 的持久修复记忆及其报告的基准提升。
