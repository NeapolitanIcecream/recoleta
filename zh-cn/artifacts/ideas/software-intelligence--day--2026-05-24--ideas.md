---
kind: ideas
granularity: day
period_start: '2026-05-24T00:00:00'
period_end: '2026-05-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software factories
- formal verification
- agent guardrails
- enterprise AI
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-factories
- topic/formal-verification
- topic/agent-guardrails
- topic/enterprise-ai
language_code: zh-CN
---

# Coding Agent Control Gates

## Summary
智能体采用现在指向三类具体控制：带外部验证的受限维护任务、小型高风险代码路径的形式化证明门，以及把生成的仓库噪音挡在未来智能体上下文之外的 Pull Request 检查。

## Dependency update and CVE fix factory station
平台和安全团队可以先把一类重复的维护工作封装成一个工厂站点，再扩大智能体的使用范围。一个合适的起点是对一组已知仓库做依赖更新或 CVE 修复。每个任务都应包含通告或工单、目标仓库、允许的命令、非目标、复现步骤、验证检查、无操作规则、所需证据，以及一个固定的输出状态，例如 `PR_READY`、`NO_OP`、`ESCALATE` 或 `RETRYABLE_FAILURE`。

真正有价值的是智能体外层的包装：接收任务、分类、创建隔离工作区、实施变更、测试、收集证据、限制重试次数、进入评审队列。第一个试点可以跑 10 个仓库，统计有多少任务产出可评审的 PR、理由充分的无操作结果或升级处理。安全检查应当放在测试、日志、截图、trace、ADR 检查或其他评审者可见的证据里，因为智能体自己的解释不足以支撑涉及生产代码的维护工作。

### Evidence
- [How to build your own software factory](../Inbox/2026-05-24--how-to-build-your-own-software-factory.md): Defines task packets, external validation, terminal states, no-op rules, retry limits, and a dependency-update example across repos.
- [Don't Fear the Dark Factory](../Inbox/2026-05-24--don-t-fear-the-dark-factory.md): Describes bounded maintenance automation through a validation harness, with candidate tasks including dependency upgrades and security vulnerability mitigation.

## Dafny and Z3 proof gate for small AI-written critical functions
把智能体用于授权、支付、策略或数据访问逻辑的团队，可以在小函数上先加一道证明门，再把生成代码当成可供评审的结果。实际做法是从一个窄接口开始，写出 Dafny 风格的前置条件和后置条件，用 Z3 检查规格，生成或修改实现，并把验证结果和 Pull Request 一起保存。

这类方法最适合验证性质紧凑的代码：余额不能为负、授权规则默认拒绝、策略更新保持不变量、输入解析器拒绝未定义情况。证据只支持一个受限试点，不支持自然语言需求已经能端到端产出经过验证的生产系统这一更大的说法。需要盯住的缺口是规格生成：当前 vericoding 的结果在正式规格已经存在时最强，或者人在代码生成前能先审查生成出来的规格时更强。

### Evidence
- [Vericoding: The End of "Trust Me Bro, The AI Wrote It"](../Inbox/2026-05-24--vericoding-the-end-of-trust-me-bro-the-ai-wrote-it.md): Describes the proposed pipeline from natural-language intent to Dafny-style specs, Z3 checks, verified code, and proof artifacts, while noting no new end-to-end quantitative evaluation.
- [Vericoding: The End of "Trust Me Bro, The AI Wrote It"](../Inbox/2026-05-24--vericoding-the-end-of-trust-me-bro-the-ai-wrote-it.md): Cites a vericoding benchmark with 12,504 formal specifications and up to 82% success in Dafny using off-the-shelf LLMs.

## Pull request check for generated-file and log context growth
依赖智能体的仓库应该增加一项 PR 检查，用来拦截那些会增加未来智能体上下文成本的改动。生成的客户端、覆盖率输出、构建产物、日志、快照、第三方文件、锁文件抖动和智能体指令转储，都可能在不破坏常规测试的情况下，让后续智能体会话变慢、更贵、噪音更多。

ContextLevy 提供了一个具体实现方式：扫描 GitHub Pull Request diff，估算上下文权重，识别高风险文件，在超过阈值时发出定向评论。它可以作为 GitHub Action 或 npm CLI 运行，而且不会调用 LLM，也不会上传代码。一个低风险的上线方式是先只评论两周，调好忽略路径和阈值，再把团队已经一致认为不该进入仓库的文件类别设为阻断。

### Evidence
- [Built a small PR guardrail for token bloat, worth maintaining?](../Inbox/2026-05-24--built-a-small-pr-guardrail-for-token-bloat-worth-maintaining.md): Explains ContextLevy’s target failure mode: PRs that add low-signal files and create persistent overhead for AI coding agents.
- [Built a small PR guardrail for token bloat, worth maintaining?](../Inbox/2026-05-24--built-a-small-pr-guardrail-for-token-bloat-worth-maintaining.md): Shows the GitHub Action setup, required permissions, and behavior of reading PR diffs and commenting when thresholds are exceeded.
