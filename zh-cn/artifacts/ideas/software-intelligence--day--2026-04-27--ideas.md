---
kind: ideas
granularity: day
period_start: '2026-04-27T00:00:00'
period_end: '2026-04-28T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent evaluation
- benchmark auditing
- repository-scale generation
- agent reliability
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/benchmark-auditing
- topic/repository-scale-generation
- topic/agent-reliability
language_code: zh-CN
---

# 代码自动化的验证关卡

## Summary
团队在信任更大规模的自动化之前，可以用小型测试工具检查编码智能体是否遵守项目规则、基准产物和迁移契约。证据支持为智能体 PR 设置产品上下文关卡、为执行型基准做自动化审计，以及用分阶段无服务器迁移检查让生成的代码和基础设施保持一致。

## 编码智能体拉取请求的决策合规性检查
当所需行为存在于代码仓库之外时，产品和工程团队应为智能体编写的 PR 增加决策合规性检查。该检查可以把产品决策转成任务级验收标准，覆盖已批准的 UI 组件、认证包装器、功能开关、审计日志、ORM 选择和已废弃模式。轻量评分器可以用正则检查 git diff，再把不确定的情况交给人工审查。

现在测试这件事有实际原因：仅访问代码库可能会漏掉规格说明、wiki、产品工具或审计文档中的决策。在 Context-Augmented Code Generation 中，只访问代码库的 Claude Code 在 8 个 Next.js 任务上的加权决策合规率为 46%。加入 Brief 后，系统会检索已记录的决策，并指导规格生成和构建中的咨询，合规率升至 95%，阻塞性违规降为 0，并在研究中的全部 8 个任务上产出可合并结果。

本地试点可以使用 10 个近期工单，这些工单应包含已知的跨文档要求。让同一个智能体运行两次，一次只访问代码仓库，一次使用检索到的决策和验收标准。比较阻塞性违规、已废弃模式使用、添加的测试和审查者返工。已发表结果规模小且来自 clean-room 基准，因此本地测试应关注团队自己的隐藏规则是否被遵守。

### Evidence
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): 定义了决策合规性，报告了使用 Brief 后从 46% 提升到 95%，并列出了工作流和基准限制。
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): 解释了为什么产品工具和 wiki 中的团队决策对只能访问代码库的智能体不可见。

## 执行型智能体基准的自动化产物审计
基准维护者和运行内部智能体评测的团队，在用分数选择模型之前应增加一个审计步骤。审计应比较每个任务的指令、参考程序、评估脚本和环境配置，然后标记矛盾，例如输出要求不完整、评估器逻辑拒绝有效答案、参考代码损坏和环境假设不一致。

BenchGuard 为这套工作流提供了具体模板。它使用结构化 LLM 审计、确定性静态检查，以及可选的智能体程序或执行日志，检查完整的任务产物栈。在 ScienceAgentBench 上，它在 102 个任务中发现了 12 个经原作者确认的缺陷。在 BIXBench Verified-50 上，五模型审计准确匹配了专家识别的 24 个原子问题中的 20 个，并部分匹配了 24 个中的 23 个。报告的审计成本为：50 个 BIXBench 任务 14.38 美元，102 个 ScienceAgentBench 任务在仅定义模式下 22.72 美元。

采用路径可以很小：在用于采购、回归测试或排行榜报告的任一执行型基准中抽取 50 个任务运行审计。先修复致命任务错误和评估器不匹配，再重新运行受影响的模型比较。这样可以避免团队基于损坏的测试选择工具。

### Evidence
- [BenchGuard: Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks](../Inbox/2026-04-27--benchguard-who-guards-the-benchmarks-automated-auditing-of-llm-agent-benchmarks.md): 概述了 BenchGuard 的输入、审计流程、缺陷分类、已确认缺陷、召回率和报告成本。
- [BenchGuard: Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks](../Inbox/2026-04-27--benchguard-who-guards-the-benchmarks-automated-auditing-of-llm-agent-benchmarks.md): 说明了执行型基准错误为何会在相互作用的指令、参考程序、评估器和环境之间产生。

## 用于智能体辅助无服务器迁移的静态分析产物
云迁移团队可以在生成代码和基础设施之前，要求智能体产出明确的中间产物，从而减少智能体漂移。对于单体到无服务器的迁移，静态分析报告应记录 HTTP 入口点、文件归属、调用边、异步行为和 schema 候选项。单独的架构产物应在生成任何 Lambda handler 或 AWS SAM 模板之前，把端点映射到 Lambda 函数和云资源。

Mono2Sls 在一个范围较窄但有用的场景中展示了这种模式：把 Flask 和 Express 应用迁移为 AWS SAM 应用。它的流水线先写入 `analysis_report.json`，再写入 `blueprint.json`，随后生成 Lambda 代码和 `template.yaml`，最后执行 11 项跨产物一致性检查。在 6 个基准应用上，这些应用共包含 10,478 行代码和 76 个可观察业务端点，它报告了无需人工修复的 100% 部署成功率、66.1% 端到端正确率和 98.7% API 覆盖 F1。消融研究将端到端正确率中的 23.4 个百分点归因于静态分析引导的架构规划。

团队可以在一个低风险内部服务上测试这种方法，要求智能体产出这些产物，并在路由、handler、IAM 资源、DynamoDB 表或 SAM 声明不一致时让运行失败。首要成功标准应是可部署性和 API 覆盖率，之后再看业务行为测试。

### Evidence
- [Mono2Sls: Automated Monolith-to-Serverless Migration via Multi-Stage Pipeline with Static Analysis](../Inbox/2026-04-27--mono2sls-automated-monolith-to-serverless-migration-via-multi-stage-pipeline-with-static-analysis.md): 列出了 Mono2Sls 的阶段、提取的事实、跨产物检查、基准规模、部署成功率、正确率和 API 覆盖率。
- [Mono2Sls: Automated Monolith-to-Serverless Migration via Multi-Stage Pipeline with Static Analysis](../Inbox/2026-04-27--mono2sls-automated-monolith-to-serverless-migration-via-multi-stage-pipeline-with-static-analysis.md): 解释了为什么需要在生成产物之间对齐函数边界、API 定义、handler 实现和基础设施声明。
