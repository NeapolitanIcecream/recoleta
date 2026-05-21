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

# 可检查的智能体运营

## Summary
智能体团队现在有了可直接借鉴的审计关卡：面向基准的发布前奖励黑客运行、带轨迹要求的集中治理 MCP 服务器，以及面向代码翻译的路径级审查。共同的运营压力在于：分数、工具调用和翻译后的代码都需要保留证据，供另一个团队事后检查。

## 面向智能体基准的发布前奖励黑客审计
基准维护者可以在发布前加入一次红队检查：尝试在不完成任务的情况下拿到任务分数，记录利用路径，并在修复后重新运行。BenchJack 给出了一套具体做法：梳理入口点、评分代码、任务文件、环境和信任边界；按缺陷分类扫描；然后生成经过测试的利用脚本，例如一个能最大化得分的 `run.sh`。在其报告的审计中，BenchJack 为测试的全部 10 个智能体基准生成了可用的奖励黑客利用，并发现了 219 个不同缺陷。它的补丁循环在 4 个设计可修复的基准上把可被利用的任务比例降到 10% 以下，并在 3 次迭代内完全修补了 WebArena 和 OSWorld。

发布清单还应要求同一批基准运行导出 rollout card。Rollout Cards 保存任务、环境状态、观测、模型输出、工具调用、工具结果、产物、时间信息、终端状态、失败、声明的评分视图、报告规则和省略字段。该论文审计了 50 个代码库，发现没有一个在头部分数之外报告失败、报错或跳过的 rollout；对固定产物重新评分会使报告分数最多变化 20.9 个百分点。基准发布可以把未公开的利用扫描和缺失的 rollout 记录列为发布阻断项，因为两者都会影响后续用户能否信任报告分数。

### Evidence
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack 的审计设计、利用生成结果、缺陷数量和补丁循环结果支持一个具体的发布前基准安全关卡。
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout Cards 规定了 rollout 证据包，并报告了代码库审计和重新评分结果，支持发布分数对应的轨迹记录。

## 集中审批的 MCP 服务器，并为工具访问保留决策轨迹
企业 AI 负责人可以把 MCP 服务器从员工笔记本迁出，放到受管理的审批、身份、日志和策略层之后。Cloudflare 的内部部署给出了一套具体运行方式：员工在获批后通过模板暴露内部资源，继承默认拒绝写入控制、审计日志、CI/CD 和密钥管理，并通过 Cloudflare Access 使用 OAuth，同时检查 SSO、MFA、IP、位置和设备属性。它的门户模式为每名员工提供一个端点，只暴露已授权的 MCP 服务器；流量扫描则通过 `/mcp`、`/mcp/sse` 以及 `tools/call`、`tools/list`、`resources/read` 等 JSON-RPC 方法查找影子 MCP 使用。

MCP 审批时应明确要求保留轨迹。一个关于智能体决策可重建性的试点发现，在 6 种 SDK 机制中，严格治理完整度为 42.9% 到 85.7%，多数受调查机制缺失推理证据或推理证据不可用。一个有用的首批上线目标是选择一个高风险内部工具，默认禁用写入，按用户授权，启用 DLP 规则，并为每次工具调用保存决策记录：行为人、策略、工具、参数、结果、授权来源和可用的推理证据。安全团队随后可以获得一条事件记录，用来回答谁授权了工具操作以及适用了哪条策略。

### Evidence
- [Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments](../Inbox/2026-05-12--scaling-mcp-adoption-our-ref-architecture-simpler-safer-cheaper-deployments.md): Cloudflare 的 MCP 部署细节提供了具体控制：远程服务器、审批、OAuth 检查、审计日志、DLP、默认拒绝写入、门户访问和影子 MCP 检测。
- [Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes](../Inbox/2026-05-12--property-level-reconstructability-of-agent-decisions-an-anchor-level-pilot-across-vendor-sdk-adapter-regimes.md): 可重建性试点显示，当前智能体轨迹经常缺少事后调查所需的决策证据。

## 面向 LLM 辅助代码迁移的路径级差异审查
把遗留 C 或 C++ 翻译成 Rust 的团队可以增加一个审查关卡，只向开发者展示工具能够证明可到达的行为差异。cozy 将原程序和翻译后的程序编译为二进制，在相同符号输入下对两者执行符号执行，比较兼容的终止状态，并使用 Z3 证明选定输出相等，或生成能暴露差异的具体输入。开发者随后把每个标记差异归类为预期差异或错误；未标记的路径则在已检查边界内按等价处理。

这适合渐进式内存安全迁移，因为自动翻译器、人工移植和 bug 修复都可能改变行为。报告中的 cozy 实验规模较小：插入排序、手表更新函数和盒式模糊滤镜。即便如此，这个流程已经足够具体，可以先在一个输入输出清晰、有边界的工具函数上试点。同一组材料中的 APL-to-C# 工作也指向其他遗留语言的相同采用方式：生成带类型的目标代码，编译，运行输入输出测试，并把编译器或测试失败反馈给修复尝试。主要缺口是规模，因此首个采用目标应是一个已有测试且状态定义清楚的小模块。

### Evidence
- [Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution](../Inbox/2026-05-12--finding-a-crab-in-the-c-assured-translation-via-comparative-symbolic-execution.md): cozy 提供了比较符号执行流程、开发者审查循环，以及小规模 C/Rust 实验。
- [Neural Code Translation of Legacy Code: APL to C#](../Inbox/2026-05-12--neural-code-translation-of-legacy-code-apl-to-c.md): APL-to-C# 研究支持编译并运行式评估、用编译器和测试反馈进行迭代修复，以及遗留代码迁移这一痛点。
