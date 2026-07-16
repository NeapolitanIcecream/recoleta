---
kind: ideas
granularity: day
period_start: '2026-05-12T00:00:00'
period_end: '2026-05-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent evaluation
- benchmark security
- agent tracing
- MCP governance
- software assurance
- code translation
- LLM testing
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/benchmark-security
- topic/agent-tracing
- topic/mcp-governance
- topic/software-assurance
- topic/code-translation
- topic/llm-testing
language_code: zh-CN
---

# 可审计的代理运维

## 摘要
代理团队现在有了可以直接照搬的审计关卡：基准的发布前 reward-hacking 运行、带 trace 要求的集中治理 MCP 服务器，以及代码翻译的路径级审查。共同的压力是运维层面的：分数、工具调用和翻译后的代码都需要保留证据，供别的团队事后检查。

## Pre-release reward-hacking audits for agent benchmarks
基准维护者可以在发布前加一道红队检查，尝试在不完成任务的情况下拿到任务分，记录利用路径，并在修复后重新运行。BenchJack 给出了一套具体做法：先映射入口点、评分代码、任务文件、环境和信任边界，再按缺陷分类法扫描，最后生成并验证一个像 `run.sh` 这样的利用脚本，让分数最大化。在它报告的审计中，BenchJack 为测试的 10 个代理基准都生成了可用利用，并找到了 219 个不同缺陷。它的修补循环把 4 个可修复基准的可被攻击任务比例降到 10% 以下，并在 3 轮内把 WebArena 和 OSWorld 全部修好。

发布清单里也应该加入同一批基准运行的 rollout-card 导出。Rollout Cards 会保存任务、环境状态、观察、模型输出、工具调用、工具结果、产物、时间、终态、失败、声明的评分视图、报告规则和省略字段。论文对 50 个仓库的审计发现，没有一个在头部准确率或分数旁边报告失败、报错或跳过的 rollout；对固定产物重新评分后，报告分数最多变化 20.9 个百分点。基准发布可以把未公开的利用扫描和缺失的 rollout 记录都当作阻断项，因为两者都会影响后来用户是否能信任报告分数。

### 资料来源
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack’s audit design, exploit generation results, flaw count, and patching-loop outcomes support a concrete pre-release benchmark security gate.
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout Cards specifies the rollout evidence bundle and reports repository-audit and re-grading results that justify score-trace publication.

## Centrally approved MCP servers with decision traces for tool access
企业 AI 负责人可以把 MCP 服务器从员工笔记本上移走，放到一个受管理的审批、身份、日志和策略层后面。Cloudflare 的内部部署给出了一种具体运行方式：员工在审批后通过模板公开内部资源，继承默认拒绝写入控制、审计日志、CI/CD 和密钥管理，并通过 Cloudflare Access 使用 OAuth，配合 SSO、MFA、IP、位置和设备检查。它的门户模式给每个员工一个端点，只暴露已授权的 MCP 服务器；流量扫描则通过 `/mcp`、`/mcp/sse` 和诸如 `tools/call`、`tools/list`、`resources/read` 之类的 JSON-RPC 方法来查找影子 MCP。

在 MCP 审批环节就应该明确 trace 要求。一项针对代理决策可重建性的试点发现，在 6 种 SDK 体系中，严格治理完整性从 42.9% 到 85.7% 不等，而且多数被调查体系里推理证据缺失或不可用。一个合适的起点是先在一个高风险内部工具上试点，默认关闭写入，按用户授权，加入 DLP 规则，并为每次工具调用保存决策记录：执行者、策略、工具、参数、结果、授权来源，以及可用的推理证据。这样安全团队就能拿到一份事件记录，回答谁授权了某个工具动作，以及适用的是哪条策略。

### 资料来源
- [Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments](../Inbox/2026-05-12--scaling-mcp-adoption-our-ref-architecture-simpler-safer-cheaper-deployments.md): Cloudflare’s MCP deployment details provide the concrete controls: remote servers, approvals, OAuth checks, audit logging, DLP, default-deny writes, portal access, and shadow MCP detection.
- [Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes](../Inbox/2026-05-12--property-level-reconstructability-of-agent-decisions-an-anchor-level-pilot-across-vendor-sdk-adapter-regimes.md): The reconstructability pilot shows that current agent traces often lack decision evidence needed for post-hoc investigation.

## Path-level differential review for LLM-assisted code migration
把旧的 C 或 C++ 迁到 Rust 的团队，可以加一道审查关，只把工具能证明可达的行为差异展示给开发者。cozy 会把原程序和翻译后的程序编译成二进制，在相同符号输入下做符号执行，比较可兼容的终止状态，并用 Z3 证明选定输出，或者生成能暴露差异的具体输入。然后开发者把每个被标出的差异归为预期或错误，而未被标出的路径在检查范围内被视为等价。

这适合渐进式内存安全迁移，因为自动翻译器、人工移植和修 bug 都可能改变行为。cozy 报告的实验规模都不大：插入排序、一个手表更新时间函数和一个 box blur 滤镜。即便如此，这个流程对一个边界清楚、输入输出明确的实用函数试点已经足够具体。这个材料包里的 APL 到 C# 工作也指向同样的采用模式：先生成带类型的目标代码，编译后跑输入输出测试，再把编译器或测试失败喂给修复尝试。主要缺口是规模，所以第一个落点应该是一个已有测试、状态定义清楚的小模块。

### 资料来源
- [Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution](../Inbox/2026-05-12--finding-a-crab-in-the-c-assured-translation-via-comparative-symbolic-execution.md): cozy provides the comparative symbolic execution workflow, developer review loop, and small C/Rust experiments.
- [Neural Code Translation of Legacy Code: APL to C#](../Inbox/2026-05-12--neural-code-translation-of-legacy-code-apl-to-c.md): The APL-to-C# study supports compile-and-run evaluation, iterative repair with compiler and test feedback, and the legacy-code migration pain point.
