---
kind: trend
trend_doc_id: 1648
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
topics:
- coding agents
- software engineering
- program repair
- agent governance
- recommender systems
- security evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-1648
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/program-repair
- topic/agent-governance
- topic/recommender-systems
- topic/security-evaluation
language_code: zh-CN
---

# 编码代理正受到可追溯性、成本检查和生产验证的约束

## Overview
这一时期将大型语言模型（LLM）代理视为可运行的软件。Rel(AI)Build 像管理供应链工件一样管理代理配置，CodeAnchor 为仓库导航加入静态结构，AgentX 将代理工作连接到在线推荐系统实验。

## Clusters

### 代理配置与协作控制
Rel(AI)Build 针对编码代理使用中的一个实际弱点：定义提示词、权限和工具行为的文件，通常缺少来源记录或审查历史。它的语料库研究发现，在按 fork 调整后，10.1% 的跟踪案例中存在完全重复的代理配置路径，75.5% 的重复克隆对跨越组织边界。论文提出的控制平面加入了哈希、锁文件、审计日志、权限层级、工具调用前检查，并可编译到七个 IDE 目标。

Knowledge-Based Pull Requests (KPR) 将类似的控制思路用于协作。外部代码、测试、日志和清理后的代理轨迹会成为经过审查的知识包。随后，项目所属的代理在接收方仓库内重新生成候选代码。试点覆盖七个已合并的公开 pull request，因此证据仍处早期，但这个工作流指出了一个真实的审查问题：维护者在接受代理辅助的改动前，需要了解意图、风险和来源。

#### Evidence
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build 设计、仓库普及率研究、重复配置率、权限边界发现和一致性结果。
- [Knowledge-Based Pull Requests: A Trusted Workflow for Agent-Mediated Knowledge Collaboration](../Inbox/2026-06-25--knowledge-based-pull-requests-a-trusted-workflow-for-agent-mediated-knowledge-collaboration.md): KPR 工作流、信任边界模型、证据包设计和七个 PR 的试点范围。

### 仓库导航与执行预算
CodeAnchor 表明，简单的静态事实可以让优先使用 grep 的代理更容易检查。它把调用、导入、继承、配置、数据流、I/O 和测试链接作为注释放在代码旁边。在 SWE-bench Lite 上，轻量级拓扑将 Func@5 提高了 2.2 个百分点，并将导航缩短了 1.6 轮交互，代价是输入 token 增加约 10%。

执行成本研究质疑了一种常见的修复循环。在 7,745 条公开 SWE-bench 轨迹中，代理平均每个任务运行测试 8.8 次。在 3,000 次受控尝试中，商业代理在不受限执行条件下的解决率只提高了 1.25 个百分点，差异没有统计显著性。Claude Code 在无执行条件下解决了 63%，在不受限执行条件下解决了 64%；无执行设置节省了 56% 的 token 和 48% 的墙钟时间。

#### Evidence
- [How Much Static Structure Do Code Agents Need? A Study of Deterministic Anchoring](../Inbox/2026-06-25--how-much-static-structure-do-code-agents-need-a-study-of-deterministic-anchoring.md): CodeAnchor 方法，以及报告的 SWE-bench Lite 定位、轨迹、方差和 token 成本结果。
- [To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair](../Inbox/2026-06-25--to-run-or-not-to-run-analyzing-the-cost-effectiveness-of-code-execution-in-llm-based-program-repair.md): 公开轨迹分析、受控执行访问研究、解决率差距，以及 token/时间节省。

### 修复成功需要更强的 oracle
两篇修复论文提醒，不应只依赖单一汇总分数或单一扫描器结果。量化研究发现，较小或经过量化的 LLM 最多可减少 85% 的内存占用，但许多设置会增加推理时间或能耗。一些量化变体修复的 bug 多于基础模型，其中 DeepSeek-Coder-6.7B 的一个结果将 Defects4J 合理修复数从 43 提高到 82。相近的通过数量常常来自不同的已解决问题集合，因此作者加入了一个 Jaccard 风格的一致性度量。

TerraProbe 将 Terraform 安全修复中的判定 oracle 问题具体化。Gemini 在 83.3% 的首次修复中清除了目标 Checkov 发现，但完整 Checkov 清洁率降至 10.4%。在经过 plan 比较的真实 TerraDS 修复中，71.4% 是欺骗性修复：它们通过了自动检查，却让目标漏洞仍然存在。论文的分层评估加入了 `terraform validate`、`terraform plan`、JSON plan 比较和人工标签。

#### Evidence
- [Smaller Models, Unexpected Costs: Trade-offs in LLM Quantization for Automated Program Repair](../Inbox/2026-06-25--smaller-models-unexpected-costs-trade-offs-in-llm-quantization-for-automated-program-repair.md): 量化实验设计、内存节省、修复数量变化、已解决集合一致性和 Pareto 发现。
- [Empirical Software Engineering TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform](../Inbox/2026-06-25--empirical-software-engineering-terraprobe-a-layered-oracle-framework-for-detecting-deceptive-fixes-in-llm-assisted-terraform.md): TerraProbe 分层 oracle、Checkov 与完整验证结果对比、欺骗性修复率和 Terraform plan 比较。

### 生产环境中的推荐系统代理
AgentX 和 NOVA 给出了当天最清楚的工业部署案例。AgentX 运行一个四阶段推荐系统循环：生成提案、基于仓库进行代码变更、安全 A/B 发布，以及根据轨迹更新 harness。在为期三周的快手 App 部署中，三个 worker 生成了 374 个想法和 10 个可上线发布。报告的在线收益为用户 app 使用时长提升 0.561%，被护栏否决的 A/B 反馈会保存为可复用的实验知识。

NOVA 关注一个服务超过 10 亿用户的广告推荐系统中的架构变更。它记录候选模型图和特征设置，在训练前检查语义有效性，并把失败方向写回搜索过程。报告的 L3 Literature-to-Production 有效通过率为 60.0%，超过论文中人工专家循环基线的两倍。选定的在线测试在三个 pCVR 目标上分别将 GMV 提高了 1.25%、1.70% 和 2.02%。

#### Evidence
- [AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems](../Inbox/2026-06-25--agentx-towards-agent-driven-self-iteration-of-industrial-recommender-systems.md): AgentX 生产部署、分阶段代理循环、上线数量、吞吐量声明和在线 app 使用时长结果。
- [NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems](../Inbox/2026-06-25--nova-a-verification-aware-agent-harness-for-architecture-evolution-in-industrial-recommender-systems.md): NOVA 具备验证感知的 harness、工业推荐系统部署、有效通过率、人工参与时间减少和在线 GMV 结果。
