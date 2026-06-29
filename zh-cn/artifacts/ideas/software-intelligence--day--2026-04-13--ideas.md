---
kind: ideas
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- execution-verification
- software-analysis
- bug-validation
- traceability
tags:
- recoleta/ideas
- topic/coding-agents
- topic/execution-verification
- topic/software-analysis
- topic/bug-validation
- topic/traceability
language_code: zh-CN
---

# 可运行的验证工件

## Summary
可执行检查正在进入编码和分析工作流的交付工件。眼下最清楚的落地方向，是给代理生成的补丁加 CI 凭证、给安全报告分流加 PoC 验证器，以及给难配置的分析工具加分阶段 runbook 代理，用可复现的证据把它们跑起来。

## CI 执行凭证，面向代理生成的补丁
仓库级编码代理应该返回补丁，以及证明它有效的精确执行记录。AgentForge 最能支持把这件事当作产品要求，而不是研究层面的附带优化：每次代码变更都会先在网络隔离的 Docker 沙箱中运行，系统在 SWE-bench Lite 上达到 40.0% 的解决率，比单代理基线高 26 到 28 个百分点。这里更实用的交付物是一个面向 CI 的执行凭证层，保存补丁、生成的测试、沙箱配置、stdout 和 stderr，以及每次尝试的 fail-to-pass 和 pass-to-pass 结果。

这适合已经在试仓库代理、又被评审时间拖慢的团队。评审者不需要再看一段“为什么这个修复应该有效”的总结；他们需要的是可回放的记录，能看出实际运行了什么、有没有引入回归。第一个便宜的测试范围要收窄：先要求代理在一种任务上附带执行凭证，比如 flaky test 修复或小型 bug 修复，再把评审通过率和合并时间，和只提供文本与 diff 的代理输出做对比。AnalysisBench 从另一个角度支持同样的边界。它的最佳代理只有在出现工具特定证据后才停止，而自验证仍把成功率高报了 15%，这说明不能让代理在没有外部工件检查的情况下自己宣布完成。

### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge requires sandbox execution for every patch and reports 40.0% resolution with a large gain over single-agent baselines.
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench shows evidence-based completion checks matter and self-validation overstated success by 15%.

## 用于 bug 报告分流的可执行 proof-of-concept 验证
安全团队可以在 LLM 找 bug 和人工分流之间加一道可执行 PoC 门禁。AnyPoC 说明了这层为什么有用。它接收候选 bug 报告，要么生成一个带日志、可重复运行的 proof-of-concept，要么直接拒绝该报告，而且能覆盖 Chromium、Firefox、LLVM、OpenSSL、SQLite、FFmpeg 和 Redis 在内的 12 个大型系统。报告中的收益很实际：对真实 bug 报告，能产出 1.3 倍更多有效 PoC；对假阳性，能拒绝 9.8 倍更多；还把 45 个生成的 PoC 采纳为正式回归测试。

最直接的交付物是一个验证服务：接收代理生成的 bug 报告，在隔离环境中启动目标项目，尝试生成并重放 PoC，然后写回两种结果之一，确认并附上可运行工件，或拒绝并附上失败证据。这对内部 AppSec 团队和维护者很有用，他们已经收到太多只靠文字描述、不能直接相信的报告。一个简单的首发版本可以先选一个代码库里的一个 bug 类，接入稳定 CI，再比较每个确认发现的分析工时，以及那些本来会进入人工评审的被拒绝报告比例。

### Evidence
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC validates bug reports by generating and re-running executable PoCs, with large gains in valid confirmations and false-positive rejection.

## 面向首次工具配置的分析 runbook 代理
采用分析器、fuzzer、符号执行工具或 profiler 的团队，需要的是能完成完整设置并展示工具特定输出的代理，而不是在构建完成或帮助页之后就停下来的代理。AnalysisBench 对失败模式说得很直接：基线代理混淆了阶段，在长日志里丢掉了根因，还会在只看到表面信号后就宣布成功。定制的 AnalysisAgent 在 35 个工具-项目任务上达到 94% 的验证成功率，而最佳基线是 77%，方法是使用明确的工作流阶段、每轮只做一个动作、确定性的日志压缩，以及基于证据的完成检查。

这指向一个面向平台工程和开发效率团队的具体支持产品：一个 analysis-runbook 代理，负责安装工具、准备项目、记录精确命令和环境，并在预期的分析工件出现之前拒绝结束。第一个便宜的检查方式是选两个内部难工具，它们 adoption 低是因为设置脆弱，然后测量这个 runbook 代理是否能提高从未配置过这些工具的工程师的首次成功率。价值不在模型有多聪明，而在每个阶段都足够清楚，环境配置失败时可以直接排查。

### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench identifies end-to-end setup and evidence capture as the core bottleneck and reports higher verified success from staged workflows.
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge independently supports mandatory execution checks before the system can accept work as complete.
