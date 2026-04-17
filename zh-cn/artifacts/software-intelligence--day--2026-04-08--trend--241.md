---
kind: trend
trend_doc_id: 241
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
topics:
- software-agents
- repository-engineering
- evaluation
- code-generation
- agent-infrastructure
run_id: materialize-outputs
aliases:
- recoleta-trend-241
tags:
- recoleta/trend
- topic/software-agents
- topic/repository-engineering
- topic/evaluation
- topic/code-generation
- topic/agent-infrastructure
language_code: zh-CN
---

# 软件代理工作正更明确地处理规格、检查和整个仓库级任务

## Overview
当天最强的证据支持这样一类软件代理：它们会写下任务说明，能在仓库规模上行动，并通过具体检查。ReCodeAgent和REAgent通过在生成前加入规划或需求，取得了可衡量的提升。CLI-Tool-Bench和SWD-Bench则把评估收紧到端到端行为、仓库理解和下游实用性上。

## Clusters

### 规格说明和验证位于代理循环内部
当系统自己携带计划并检查自己的输出时，仓库级编码工作的证据更强。ReCodeAgent把翻译拆分为分析、规划、翻译和验证，并报告在118个项目和四种语言对上取得99.4%的编译成功率和86.5%的测试通过率。REAgent在问题修复上采用了相同的大体模式：先构建结构化需求，用生成的测试给需求打分，再持续改进，直到需求足以驱动补丁生成。报告显示，与基线相比，已解决问题的增幅为9.17%到24.83%。共同点很直接：当规格说明和验证成为循环中的一等步骤，而不是最后补上的清理环节时，仓库代理的表现会提高。

#### Evidence
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): 多代理规划和验证在仓库级翻译中带来了很强的结果。
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): 需求生成和评估改善了问题解决结果。

### 基准正在测试完整的仓库任务，而不只是代码片段
基准设计正越来越接近开发者实际要求代理完成的工作。CLI-Tool-Bench从空工作区开始，根据命令行为、输出和文件系统影响来评估完整的CLI工具。即使是最好的模型，整体成功率也低于43%。SWD-Bench评估文档时，看的不是文档写得是否漂亮，而是它是否有助于回答开发问题、定位功能文件，以及恢复整个仓库中的实现细节。它还报告称，在使用更好的文档时，SWE-Agent的问题解决能力下游提升了20%。这一时期的评估工作不太关心润色过的局部输出，更关心代理能否完成一个可由另一套系统验证的仓库任务。

#### Evidence
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): 0到1的CLI基准衡量端到端仓库构建，并发现成功率较低。
- [Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development](../Inbox/2026-04-08--evaluating-repository-level-software-documentation-via-question-answering-and-feature-driven-development.md): 文档基准将质量与仓库问答任务和下游代理性能联系起来。

### 代理基础设施正在成为产品层
产品工作正把代理运行时本身打包成交付物。Claude Managed Agents提供托管循环，包含工具、代码执行、网页访问、持久会话和服务端事件历史。这意味着运行时控制、行为引导和环境配置由平台侧承担，而不是应用团队。这里的证据来自产品文档，不是基准数据，因此这个判断比研究论文更窄一些。不过，它仍然符合当天的主题：团队想要的是已经接好执行、状态和控制界面的代理行为。

#### Evidence
- [Claude Managed Agents Overview](../Inbox/2026-04-08--claude-managed-agents-overview.md): 托管运行时产品把自主代理所需的执行、工具、状态和引导打包在一起。
