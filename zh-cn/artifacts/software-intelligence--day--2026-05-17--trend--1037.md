---
kind: trend
trend_doc_id: 1037
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- vulnerability repair
- tool calling
- code review
- legacy modernization
run_id: materialize-outputs
aliases:
- recoleta-trend-1037
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/vulnerability-repair
- topic/tool-calling
- topic/code-review
- topic/legacy-modernization
language_code: zh-CN
---

# 代码智能体正按已交付系统和已验证修复循环接受评判

## Overview
当天最明确的信号是具体执行。SaaSBench和WebGameBench对已交付软件的行为打分，ContraFix和MemRepair则通过把运行时证据和先前修复保留在循环中来改进修复。当前重点偏向运行环节：搭建、集成、验证和审查控制决定智能体是否有用。

## Clusters

### 全栈交付基准
SaaSBench把企业软件交付作为测试对象。它的任务包括长篇产品需求、Docker运行时、按依赖顺序执行的验证节点、多种语言、数据库，以及前端/后端技术栈。报告中的最佳Pass@1为20.68%，超过95%的失败发生在深入业务逻辑之前，常见于搭建、配置、集成、过早停止或调试停滞阶段。

WebGameBench把同一点落实到用户可见的形式。智能体构建浏览器游戏，然后运行时评估器通过Playwright控制Chrome，并按需求检查行为。最佳配置达到76.9%的可用率，但优秀率只有20.2%。页面可以加载，但仍可能遗漏规则、输入处理、计分、重启行为，或胜负条件。

#### Evidence
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench的任务设计、验证设置和失败结果。
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): WebGameBench的运行时评估，以及可用与优秀结果。

### 使用运行时证据和记忆进行漏洞修复
两篇修复论文把漏洞修复处理成反馈问题。ContraFix比较崩溃执行和安全执行，在故障附近插入探针，并在打补丁前写出修复规格。在SEC-Bench上，它解决了200个C/C++ CVE实例中的84.0%；消融结果把27个百分点的提升归因于对比式运行时分析。

MemRepair走的是以记忆为中心的路线。它存储过去的修复、可复用的安全模式，以及从失败补丁到成功补丁的轨迹。Locator、Patcher和Verifier循环会先运行漏洞测试和回归测试，再接受代码修改。在SEC-Bench上，使用DeepSeek-v3.2的MemRepair解决了58.00%的任务，高于列出的OpenHands、SWE-agent和Aider基线。

#### Evidence
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix方法、SEC-Bench结果和消融证据。
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): MemRepair的记忆设计、验证循环和基准结果。

### 来自真实API的已验证工具调用数据
FireFly先执行真实的Model Context Protocol (MCP) API，再在已有观测输出后编写任务，用这种方式构建工具使用训练数据。该流程把Smithery服务器筛选到240个服务器和993个工具，构建有向工具图，探索线上API，并缓存观测到的调用，用于离线强化学习。

结果是一个包含5,144个已验证任务和9,749条轨迹的数据集。训练后，Qwen3-4B在FireFly测试上的pass@1从28.1%提升到41.5%，接近Claude Sonnet 4.6的42.2%。论文还报告了在Tau2-Bench、MCP-Atlas和MCPMark上的提升。

#### Evidence
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): FireFly的数据生成流程、数据集规模和模型结果。

### 由人控制的软件工作流
代码审查论文把智能体式审查视为带有人类决策点的协同拉取请求流程。它的五个阶段覆盖PR创建、PR增强、审查者选择、AI辅助审查和回顾。该论文属于愿景论文：它没有报告新的基准、原型评估、用户研究或受控实验。

AgentModernize把更可测试的结构用于遗留系统现代化。它把业务规则提取为Behavioral Specification Graph，生成Python/FastAPI代码，并通过反馈验证行为。结果仍然较低：GPT-5.3-codex达到19.4%的平均Behavioral Equivalence Rate，而单提示和思维链基线在测试场景中的得分均为0.0%。

#### Evidence
- [Rethinking Code Review in the Age of AI: A Vision for Agentic Code Review](../Inbox/2026-05-17--rethinking-code-review-in-the-age-of-ai-a-vision-for-agentic-code-review.md): 智能体式代码审查工作流，以及缺少新的实证评估。
- [AgentModernize: Preserving Business Logic in Legacy Modernization with Multi-Agent LLMs and Behavioral Specification Graphs](../Inbox/2026-05-17--agentmodernize-preserving-business-logic-in-legacy-modernization-with-multi-agent-llms-and-behavioral-specification-graphs.md): AgentModernize的规格图、验证循环和行为等价结果。
