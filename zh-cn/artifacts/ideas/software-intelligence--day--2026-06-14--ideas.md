---
kind: ideas
granularity: day
period_start: '2026-06-14T00:00:00'
period_end: '2026-06-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- formal methods
- agent memory
- sandbox security
- AI UX
- generative video
tags:
- recoleta/ideas
- topic/coding-agents
- topic/formal-methods
- topic/agent-memory
- topic/sandbox-security
- topic/ai-ux
- topic/generative-video
language_code: zh-CN
---

# Controlled Coding Agent Workspaces

## Summary
代理采用正在撞上当前开发工具常被当作事后补救的控制点：凭据放在哪里、项目事实如何持久化、审查者如何拿到生成代码遵守本地不变量的证据。最实际的做法，是围绕无密钥工作区、带成本测量的项目级代理记忆，以及面向证明的审查检查，做几个小试点，先放在那些对正确性要求很高的代码库里。

## Secretless Kubernetes workspaces for AI coding agents
想让编码代理接触内部数据库、SSH 主机、HTTP API、Kubernetes 集群或 mTLS 服务的团队，需要一种工作区模式，让代理可以在某个身份下执行，而不拿到长期有效的密钥。Cordium 给出了一个具体设计：无 root 的 Kubernetes 工作区、声明式环境定义，以及由 Octelium 介导的访问，让 API 密钥、密码、SSH 私钥和 kubeconfig 都留在身份感知代理里。

一个可行的试点做法，是把一个代理工作流和一个人类远程开发工作流放到同一套沙箱环境里，然后检查每次内部请求是否都绑定到工作区身份和策略决策。这个测试范围要窄：代理能否在不把任何密钥复制进容器的情况下，对内部服务执行真实的维护任务，同时安全团队还能拿到每次请求的 OpenTelemetry 日志。Cordium 还声称 VolumeSnapshot 模板能缩短重环境的冷启动时间，所以试点还应把启动延迟和访问控制覆盖率一起测出来。

### Evidence
- [Show HN: Cordium – FOSS identity-based sandbox platform with zero-trust access](../Inbox/2026-06-14--show-hn-cordium-foss-identity-based-sandbox-platform-with-zero-trust-access.md): Cordium summary describes rootless Kubernetes workspaces for developers, AI agents, and CI jobs, with identity-based secretless access and OpenTelemetry audit logs.
- [Show HN: Cordium – FOSS identity-based sandbox platform with zero-trust access](../Inbox/2026-06-14--show-hn-cordium-foss-identity-based-sandbox-platform-with-zero-trust-access.md): Cordium content states that workspaces can access databases, SSH servers, HTTP APIs, Kubernetes clusters, and mTLS services without credentials reaching the workspace.

## Per-project agent memory with cost checks for repeated coding tasks
当决策、API 事实和之前的结论只存在于聊天记录里时，编码代理就会重复劳动。Raidho 提供了一个可以直接测试的实现：把 subject-relation-object 事实按项目存到磁盘里，在后续运行时重新载入，只在需要时把相关事实召回到提示词中。它的 Vector Symbolic Architecture 内存是实现细节；工作流上的变化是，项目事实变成了持久的本地工件。

这个工具还给出了一个成本测量样式。在一个使用同一模型的真实 API 任务上，Raidho 报告确定性流程成本为 $0.05，context-first 混合方案为 $0.116，纯工具循环为 $0.301。它的自动蒸馏结果更窄：在小数据上的重复多步骤工作，每次重复成本下降了 9.6 倍，而一次数据量很大的审计几乎没有省下什么，因为费用主要来自文件内容。团队可以把这套方法放到依赖审计、发布说明检查或 API 迁移扫描等重复仓库任务上，只在测出来的节省能撑过几轮重复运行时保留记忆和蒸馏出来的流程。

### Evidence
- [Show HN: Coding agent with algebraic memory (VSA) instead of RAG](../Inbox/2026-06-14--show-hn-coding-agent-with-algebraic-memory-vsa-instead-of-rag.md): Raidho summary describes separate reasoning, execution, durable memory, auto-distillation, and reported cost comparisons.
- [Show HN: Coding agent with algebraic memory (VSA) instead of RAG](../Inbox/2026-06-14--show-hn-coding-agent-with-algebraic-memory-vsa-instead-of-rag.md): Raidho content explains per-project durable memory using subject-relation-object facts and VSA-based recall.
- [Show HN: Coding agent with algebraic memory (VSA) instead of RAG](../Inbox/2026-06-14--show-hn-coding-agent-with-algebraic-memory-vsa-instead-of-rag.md): Raidho content reports the 9.6x repeated-task cost drop and the case where data-heavy work saved almost nothing.

## Proof-oriented review checks for agent-generated code
代理生成的代码可能满足了需求变更，却漏掉测试覆盖不到的代码库不变量。Jane Street 的形式化方法文章把这件事描述成审查负担：生成代码有用，但审查者仍要花时间确认它能否发布、是否符合本地约束。

一个具体的落地步骤，是把面向证明的检查加到高不变量模块的审查路径里。第一批目标不需要把整个应用做完全验证。可以先从更强的类型约束、基于性质的测试、小型模块化规格，或者围绕接口的不证明义务开始，只要这些接口上的不变量已经明确。代理可以先起草规格，再根据这些检查的反馈修代码，然后再交给人工审查者看补丁。合适的衡量指标是审查时间和缺陷逃逸率，范围只看一小组模块，因为 Jane Street 这篇文章给的是战略判断和旧的成本基线，不是新基准。

### Evidence
- [Formal Methods and the Future of Programming](../Inbox/2026-06-14--formal-methods-and-the-future-of-programming.md): Jane Street summary argues that formal methods can reduce review burden for agent-generated code and give agents better feedback.
- [Formal Methods and the Future of Programming](../Inbox/2026-06-14--formal-methods-and-the-future-of-programming.md): Jane Street content cites the seL4 verification cost baseline of 25 person-years for 8,700 lines of C.
- [Formal Methods and the Future of Programming](../Inbox/2026-06-14--formal-methods-and-the-future-of-programming.md): Jane Street content describes agent-generated code missing codebase invariants and creating verification work for reviewers.
