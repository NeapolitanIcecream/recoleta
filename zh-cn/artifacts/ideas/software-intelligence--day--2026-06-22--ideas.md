---
kind: ideas
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- LLM agents
- coding agents
- enterprise benchmarks
- procedural memory
- software security
- context recovery
- SysML
- Text-to-SQL
tags:
- recoleta/ideas
- topic/llm-agents
- topic/coding-agents
- topic/enterprise-benchmarks
- topic/procedural-memory
- topic/software-security
- topic/context-recovery
- topic/sysml
- topic/text-to-sql
language_code: zh-CN
---

# 编码代理就绪检查

## Summary
编码代理采用有三个实际压力点：恢复仓库任务真正需要的文件，按已交付的 workplace 制品测试代理，并在部署前检查 AI 构建的应用。证据支持一些小的运营变更，团队可以用现有代码库、会话日志和安全评审队列来试点。

## 编码代理编辑前的任务级仓库上下文恢复
在大型代码库中使用编码代理的团队，应该在编辑前增加一个上下文恢复步骤：先从少量高置信度文件开始，再沿导入、配置绑定、依赖注入、测试和模块邻近关系扩展。输出可以是一个有边界的上下文包：可能编辑目标提供全文，支持文件提供紧凑元数据，并附上明确的链接列表，说明每个文件为什么被纳入。

这适合平台工程和开发者体验团队，尤其是已经看到代理只修改显眼文件，却漏掉注册代码、测试夹具或配置路径的团队。低成本试点可以选取最近已解决的工单，让维护者标注相关文件，然后比较当前检索栈和锚点加扩展流程在完整召回、token 成本和后续补丁成功率上的表现。DeepDiscovery 报告称，它在超过 25,000 个文件的工业代码库上取得收益，包括中等任务的完整召回率（Full Recall Rate）提升 2.5 到 7.4 个百分点，大型子项目任务提升 1.6 到 9.2 个百分点，并在 SWE-bench Verified 上带来 8.2 个百分点的解决率提升。

### Evidence
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): 概述 DeepDiscovery 的 Location-Inference 工作流、工业代码库规模、文件恢复收益，以及 SWE-bench Verified 解决率结果。
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): 描述语义检索遗漏配置注册、依赖注入、事件传播和跨模块约束的失败模式。

## 基于会话生成的 workplace 代理测试，按交付物、成本和技能迁移评分
企业团队在跨部门扩大代理使用前，应该把一部分真实代理会话转成可复现测试。每个测试应包含恢复出的输入文件、请求的交付物、硬性规则、文本或视觉评分规程，并为每个测试框架-模型组合运行一个全新的沙箱。评分应同时报告制品完成情况、质量、运行时间、token 用量、成本和工具调用。

可复用技能文件也需要同样的纪律。一次 `SKILL.md` 更新应先通过同一任务类别的留出任务，再通过跨角色或模型骨干的迁移检查，然后才能提升版本。EnterpriseClawBench 显示，在 32 个测试框架-模型组合中，最好的 Lite 结果达到 0.663，仍暴露出许多交付和质量失败。AFTER 显示，带版本的程序性技能可以提高准确率，但狭窄的技能演化在跨角色迁移时可能降低准确率。首次部署检查可以使用 30 到 50 个历史会话和一小组重复出现的技能；如果某个配置节省了时间，却交付失败或破坏迁移，就应阻止上线。

### Evidence
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): 详细说明如何把企业会话转成可复现任务，包括文件、交付物、角色标签、评分规程、沙箱执行，以及成本、运行时间和工具调用报告。
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): 解释企业评估为什么需要测试框架-模型组合、制品交付质量、时间、成本和任务类别级技能评估。
- [Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation](../Inbox/2026-06-22--managing-procedural-memory-in-llm-agents-control-adaptation-and-evaluation.md): 报告 AFTER 的带版本技能制品、细化收益、跨模型迁移结果和跨角色迁移损失。

## AI 编写 Web 应用的部署前安全评审
允许 AI 代理构建并部署 Web 应用的组织，应该增加一个发布门禁，专门检查反复出现的 AI 生成漏洞模式。评审应检查访问控制失效、密钥暴露、注入、未过滤输入、占位逻辑、加密失败和不安全部署设置。代理辅助审计的输出应先去重，再交给人工安全审查员，对面向公网的应用确认可利用性。

同一流程也可以把安全需求附加到架构和代码上，用于支付、身份或设备控制软件等需要可追溯性的系统。EVerest 显示了连接需求、架构、文档和代码的价值：其数据集包含 84 条安全需求和 1,445 个细粒度标签，构建过程还发现了一个真实的 CWE-1295 明文 token 存储弱点。vibe-coding 研究给出了采用阻力：在 200 个已部署、由 AI 编写的 Web 应用中，审查员在去重和可利用性检查后确认了 1,471 个可利用漏洞。

### Evidence
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): 报告 VibeApps 语料库、已部署 Web 应用审计流程、已验证漏洞数量、审查员一致性和反复出现的漏洞类别。
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): 描述 vibe-coded 应用中未经审计的安全关键决策，包括凭据、访问控制、数据库查询和不安全配置。
- [The EVerest Dataset for Secure Software Engineering](../Inbox/2026-06-22--the-everest-dataset-for-secure-software-engineering.md): 概述 EVerest 的安全需求、架构和代码链接、细粒度标签，以及已披露的 CWE-1295 token 存储弱点。
