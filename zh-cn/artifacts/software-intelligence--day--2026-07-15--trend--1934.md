---
kind: trend
trend_doc_id: 1934
granularity: day
period_start: '2026-07-15T00:00:00'
period_end: '2026-07-16T00:00:00'
topics:
- agent evaluation
- coding agents
- software security
- agent governance
run_id: materialize-outputs
aliases:
- recoleta-trend-1934
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/coding-agents
- topic/software-security
- topic/agent-governance
language_code: zh-CN
---

# 工具编排选择会改变智能体得分、工具习惯和安全结果

## 概览
近期关于工程化上下文和可执行检查的证据，正在工具编排框架层面变得更加具体。今天的研究表明，交互协议会改变基准得分，持久会话可能使智能体固守过时的工具使用流程，而有针对性的探索可以改善安全分析。部署仍不成熟：观察到的编码智能体使用并不普遍，而且通常由一个人监督。

## 研究发现

### 依赖工具编排框架的评估
AgentCompass 将基准、工具编排框架和执行环境分离开来，并显示同一模型的结果会随工具编排框架而变化。在 SWE-bench-Pro 上，Claude-Opus-4.8 使用 Mini-SWE-agent 得分 66.21，使用 OpenHands 得分 73.87。另一项集合转换基准发现，智能体会很快形成重复的工具使用流程，并可能在后端静默更换后继续使用不可靠的工具组。这些研究共同表明，交互历史和工具编排配置应被视为测量能力的一部分，而不是无关紧要的测试基础设施。

#### 资料来源
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): 报告了依赖工具编排框架的 SWE-bench-Pro 得分，以及涵盖七个模型的轨迹级失败分析。
- [Set-shifting Behavioral Test for Harnessed Agents](../Inbox/2026-07-15--set-shifting-behavioral-test-for-harnessed-agents.md): 测量了隐藏的工具可靠性变化后的适应情况，并发现重复出现、部分已经过时的路由流程。

### 面向软件安全的针对性证据
当探索由具体假设驱动时，安全智能体能获得更好的效果。DREA 的规划器向轻量级探索器请求仓库证据；DeepSeek-V3.2 的成对正确率从 19% 提升到 42%，同时超过 93% 的 token 在本地处理。ProfMalPlus 也会将不确定的软件包判断路由到静态、注册表或沙箱证据，并报告 98.1% 的 F1 和 597 个新识别的恶意 NPM 软件包。VisualRepair 将同样的选择性关注原则应用于截图，解决了 SWE-bench Multimodal 测试中的 196 个问题，比其最佳基线多 10 个。共同结果是有条件的：更聚焦的证据收集确有帮助，但 DREA 仍发现 26–55% 的真正例背后存在有缺陷的推理依据。

#### 资料来源
- [DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection](../Inbox/2026-07-15--drea-decoupled-reasoning-and-exploration-agents-for-repository-level-vulnerability-detection.md): 报告了仓库引导的探索收益、本地 token 卸载情况，以及由有缺陷的推理依据支持的正确标签比例。
- [ProfMalPlus: Agent-Coordinated Detection of Malicious NPM Packages via Static-Dynamic Analysis Synergy](../Inbox/2026-07-15--profmalplus-agent-coordinated-detection-of-malicious-npm-packages-via-static-dynamic-analysis-synergy.md): 结合静态、动态和注册表证据，并报告了 98.1% 的 F1 以及 597 个已确认的恶意软件包。
- [VisualRepair: Dynamic Tool Calling and Region Focusing for Visual Software Issue Repair](../Inbox/2026-07-15--visualrepair-dynamic-tool-calling-and-region-focusing-for-visual-software-issue-repair.md): 使用特定类型的视觉工具和动态区域聚焦，在 SWE-bench Multimodal 上解决了 196 个测试问题。

### 早期运营治理
现实世界的采用仍以人工监督为中心。在 2,361 个 GitHub 仓库中，项目中位数在三个月内仅产生一到两个智能体拉取请求；单人工作流占观察案例的 88.7%。在这一有限的部署基础上，治理方案也开始出现。EBAE 通过针对具体操作、绑定时间周期的授权，将智能体提案与受保护的执行分离；DNSid 则将智能体身份与互联网域名和加密注册记录关联起来。两种机制的验证仍然有限：EBAE 没有提供定量评估，DNSid 报告了未具名的试验，但没有给出结果。

#### 资料来源
- [Early Adoption of Agentic Coding Tools by GitHub Projects](../Inbox/2026-07-15--early-adoption-of-agentic-coding-tools-by-github-projects.md): 基于 25,264 个智能体拉取请求，测量了项目层面的低采用率和以单人监督为主的情况。
- [EBAE: A protocol for bounding the real-world authority of autonomous agents](../Inbox/2026-07-15--ebae-a-protocol-for-bounding-the-real-world-authority-of-autonomous-agents.md): 规定了绑定时间周期、针对具体操作的授权，但没有报告定量评估。
- [Vint Cerf is working on a plan to unleash AI agents on the open internet](../Inbox/2026-07-15--vint-cerf-is-working-on-a-plan-to-unleash-ai-agents-on-the-open-internet.md): 描述了与域名关联的智能体身份和加密注册历史，并提到试验但没有公布结果。
