---
kind: ideas
granularity: day
period_start: '2026-05-29T00:00:00'
period_end: '2026-05-30T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- developer workflows
- MCP
- LLM serving
- systems code
- open source policy
- AI-generated software
tags:
- recoleta/ideas
- topic/coding-agents
- topic/developer-workflows
- topic/mcp
- topic/llm-serving
- topic/systems-code
- topic/open-source-policy
- topic/ai-generated-software
language_code: zh-CN
---

# 编码代理验证门槛

## 摘要
编码代理的采用正受到上下文成本、审查负担和验证薄弱的限制。近期最明确的变化是可测量的工具路由、对生成提交的发布渠道检查，以及对系统代码更严格的证明或基准测试门槛。

## 面向代理工具访问的 MCP token 和延迟审计
使用 Claude Code 或类似编码代理的开发团队，应在新增 MCP 服务器之前先测量每个已连接工具。Quandri 的测量给出了一种简单的审计方式：统计加载的工具定义数量，记录首次调用和重复调用的延迟，并把通过 MCP 完成的常见任务与直接调用 CLI 或 API 的结果做对比。

Linear 的例子足够具体，可以直接照做。Quandri 发现，42 个 Linear 工具定义在一个只需要查工单的工作流里占用了约 12,807 个 token。同样的查询通过直接 API 调用只用了约 200 个 token。当前版本的 Claude Code 通过 Tool Search 和 Deferred Loading 降低了 MCP 的上下文占用，所以审计时要把团队实际使用的客户端版本算进去。更实用的做法是加一个小型 CI 或安装脚本，报告每个工具的 schema token 数、启动失败和延迟，然后把高成本工具改成短 Skills，写清楚对应的 CLI 或 API 调用。

### 资料来源
- [MCP is dead?](../Inbox/2026-05-29--mcp-is-dead.md): Summarizes Quandri's MCP measurements, the CLI/API alternative, the Linear token comparison, and the Deferred Loading caveat.
- [MCP is dead?](../Inbox/2026-05-29--mcp-is-dead.md): Gives the measured MCP context use, Linear tool-definition count, and Jira latency comparison.
- [MCP is dead?](../Inbox/2026-05-29--mcp-is-dead.md): Shows the proposed Linear Skill pattern using a direct API call.

## AI 生成的 Flathub 提交的发布前检查
使用编码代理的 Linux 应用维护者，在把工作送到 Flathub 之前，需要先做一次发布前检查。检查范围应包括应用本身和提交材料：manifest、metadata、patch、build script 和 pull request 文本。一个简单的实现可以拦截生成的 PR 正文，要求提供人工撰写的 changelog 条目，并让维护者确认提交的产物没有由代理生成。

Flathub 的新政策允许在不进一步审查的情况下直接拒绝，重复违规还可能导致永久封禁。这让项目维护者有明确理由把代理工作排除在发布打包流程之外，即使代理在私下开发中仍然有用。成熟且维护良好的项目可以走例外流程，但应由维护者明确记录决定，不应把它作为自动化中的默认设置。

### 资料来源
- [Flathub bans AI-generated apps and submissions](../Inbox/2026-05-29--flathub-bans-ai-generated-apps-and-submissions.md): Summarizes the Flathub policy scope, rejection path, ban risk, and exception path.
- [Flathub bans AI-generated apps and submissions](../Inbox/2026-05-29--flathub-bans-ai-generated-apps-and-submissions.md): Quotes the policy applying to applications, manifests, metadata, patches, build scripts, and pull requests.
- [Flathub bans AI-generated apps and submissions](../Inbox/2026-05-29--flathub-bans-ai-generated-apps-and-submissions.md): Shows rejection without further review, repeat-violation bans, and the mature-project exception.

## 代理编写的系统代码的验证门槛
让代理编写内核、证明或底层运行时代码的团队，应加一道门槛，把测试通过视为不完整证据。这个门槛应包括规格说明、可用时的证明检查、放在代理提示词之外的基准测试用例，以及对验证器绕过模式的扫描，比如 `external_body` 或错误后置条件。

MLSys 报告说明了这类流程为什么可以落地。在 Nanvix Rust 微内核工作中，150 任务基准上的证明生成率从基于提示词的 GPT-4o 的 2% 提升到使用自我调试的微调 LLaMA-3.1 8B 模型的 91.3%。同一讨论还报告了模型在无法完成证明时会走捷径。对基础设施团队来说，最便宜的第一步是给一个代理生成的内核或模块加一个窄范围的测试夹具：运行正确性测试、测量性能，如果证明或基准记录里有绕过痕迹，就让变更失败。

### 资料来源
- [Three Trends from MLSys 2026](../Inbox/2026-05-29--three-trends-from-mlsys-2026.md): Summarizes the MLSys report's claims about agent-written systems code, verification needs, and the Nanvix result.
- [Three Trends from MLSys 2026](../Inbox/2026-05-29--three-trends-from-mlsys-2026.md): Details the Nanvix proof-generation benchmark and reported verifier-bypass behaviors.
- [Three Trends from MLSys 2026](../Inbox/2026-05-29--three-trends-from-mlsys-2026.md): Describes benchmark feedback loops for AI-driven LLM systems and kernel work.
