---
kind: ideas
granularity: day
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- repository context
- agent evaluation
- software security
- agent memory
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-context
- topic/agent-evaluation
- topic/software-security
- topic/agent-memory
language_code: zh-CN
---

# 编码代理工作流中的仓库上下文检查

## Summary
应将仓库上下文作为运行依赖进行测试。实际可采取的改动包括：对检索进行故障注入，在代码完成前设置安全专用上下文门禁，以及在基础设施证据缺失或过时时明确升级处理。

## 对仓库检索和摘要进行故障注入
编码代理维护者需要知道，补丁在错误的仓库上下文中是否仍然有效。ACQUIRE 表明，有针对性且有证据支持的仓库问答可以提高问题解决率；AgentCheck 则发现，代理经常会自信地接受过时或损坏的工具输出。因此，仓库检索应与 API 和数据库工具一样，纳入故障模型。

为过时的文件摘要、遗漏的依赖边、错误的符号位置，以及检索文本中嵌入的指令添加可重放的扰动。记录轨迹首次出现分歧的位置，然后测试源代码引用、文件哈希检查，以及只读方式对照当前代码确认等缓解措施。

使用 50 个已解决的 SWE-bench 任务，分别测试干净上下文和经过扰动的上下文。测量 Pass@1 损失、不安全编辑和缓解措施的恢复率。设置试点决策阈值：如果扰动使 Pass@1 降低不到 5 个百分点，则停止；如果缓解措施恢复了不到一半的暴露失败案例，则修改检查方案。

### Evidence
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): ACQUIRE 报告称，在生成补丁前进行有针对性且有仓库证据支持的问答后，SWE-bench Pass@1 更高。
- [AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP](../Inbox/2026-07-13--agentcheck-a-reproduce-intervene-mitigate-workbench-for-llm-agents-over-mcp.md): AgentCheck 可以重现过时、错误、失败和遭投毒的工具响应，并发现代理经常自信地使用错误输出。
- [Retrieval-Oriented Code Representations in Agentic Bug Localization](../Inbox/2026-07-13--retrieval-oriented-code-representations-in-agentic-bug-localization.md): 文件定位研究表明，表示方式会显著改变文件检索准确率和上下文成本。

## 面向 AI 辅助拉取请求的安全 API 上下文门禁
审查 Java 拉取请求的应用安全团队需要一种可靠的检查，用于开发者在 SSL/TLS 或 OAuth API 周围使用 Copilot 的场景。一项包含 44 名开发者的研究发现，Copilot 提高了功能正确性，但没有显著提高安全 API 的使用水平；只有两名参与者在提示中明确提出安全要求。ACQUIRE 表明，编辑前提出有针对性的问题，可以补充缺失的仓库契约。

当代码中出现安全 API 时，触发一份简短的完成前问卷：适用哪项信任策略，凭据来自哪里，需要经过哪条验证路径，以及哪些仓库配置限制了这次调用。提供带有文件和符号引用的答案，然后在接受更改前运行针对该 API 的误用检查。TerraRepair 关于模式查询和重新扫描的结果支持把精确上下文与可执行验证结合起来。

使用 30 个历史安全相关拉取请求开展盲审试点。比较不安全 API 误用、功能测试通过率和审查时间。设置试点决策阈值：如果误用率的相对降幅小于 20%，则停止；如果审查时间中位数增加超过 10%，也停止。

### Evidence
- [Understanding the Impact of AI Code Assistants on Security API Usage: An Empirical Study](../Inbox/2026-07-13--understanding-the-impact-of-ai-code-assistants-on-security-api-usage-an-empirical-study.md): 开发者研究发现，使用 Copilot 后功能正确性提高，但安全 API 的总体使用水平没有显著改善。
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): 有针对性的仓库问题产生了高度有证据支持的答案，并提高了问题解决的 Pass@1。
- [TerraRepair: A Tool-Grounded LLM Agent for Infrastructure-as-Code Repair](../Inbox/2026-07-13--terrarepair-a-tool-grounded-llm-agent-for-infrastructure-as-code-repair.md): TerraRepair 从已安装模式查询、依赖检索和基于扫描器的验收检查中获得了明显收益。

## 面向 Terraform 修复的基于新鲜度的升级处理
云安全工程师需要让自动化 Terraform 修复在缺少或过时的部署证据时停止。TerraRepair 将大多数升级处理归因于缺少部署特定上下文。AgentCheck 表明，即使采用常见缓解措施，过时数据仍然难以处理，因此不能把结构上有效的提供商响应当作当前证据。

为每个拟议修复附加一份回执，记录提供商模式版本、依赖值、源提交、检索时间、扫描器版本和未解决的冲突。缺少必填字段、哈希不再匹配或来源相互矛盾时，拒绝自动应用。使用过时模式和已变化的依赖值重放已捕获的修复，测试门禁能否在打补丁前触发升级处理。

从 40 个历史发现开始，分为有效上下文和刻意过时的上下文两组。测量不安全的自动批准和不必要的升级处理。设置试点决策阈值：如果门禁捕获的过时上下文案例少于 90%，则停止；如果超过 25% 的有效案例被升级处理，则修改门禁。

### Evidence
- [TerraRepair: A Tool-Grounded LLM Agent for Infrastructure-as-Code Repair](../Inbox/2026-07-13--terrarepair-a-tool-grounded-llm-agent-for-infrastructure-as-code-repair.md): TerraRepair 使用提供商模式、依赖检索、重新扫描和结构化升级处理；缺少部署上下文是升级处理的主要原因。
- [AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP](../Inbox/2026-07-13--agentcheck-a-reproduce-intervene-mitigate-workbench-for-llm-agents-over-mcp.md): AgentCheck 报告称，处理过时工具数据仍然困难，并支持对注入故障进行精确重放。
- [Long term memory cortex for agents that maintains tensions](../Inbox/2026-07-13--long-term-memory-cortex-for-agents-that-maintains-tensions.md): Daftari 实现了确定性回执，其中包含来源信息、新鲜度、内容哈希、替代状态和未解决的矛盾。
