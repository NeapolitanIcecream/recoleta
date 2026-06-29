---
kind: ideas
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- software testing
- tool use
- agent monitoring
- security
- maintenance cost
- smart contracts
- tool provenance
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-testing
- topic/tool-use
- topic/agent-monitoring
- topic/security
- topic/maintenance-cost
- topic/smart-contracts
- topic/tool-provenance
language_code: zh-CN
---

# Agent Failure-Mode Gates

## Summary
Agent 软件工作正在转向与具体失败模式绑定的检查：会返回看似合理却错误结果的实时工具调用、用狭窄攻击集测试的监控器，以及顺序测试漏掉共享内存交互的 C/C++ 库。实际工作是在这些流程前面加小门槛，避免 agent 直接接触生产系统或安全关键仓库。

## Pre-execution contract checks for code-mode tool-use agents
面向真实工具运行代码模式 agent 的团队，可以在第一次环境动作之前加一道验证步骤。验证器应先读取任务说明和工具注册表，再检查生成程序的输出形状、工具选择、调用签名、参数来源和调用顺序。检查失败时，应给出具体的修复指令，并在不执行工具调用的情况下重新生成。

RubricRefine 是一个有用的模板，因为它针对的是那些不会触发运行时异常的失败：路由错误、工具之间的数据流断裂、以及由错误的中间值拼出的表面正确的最终答案。在 M3ToolEval 上，它在七个模型上的平均成功率是 0.86，而单次通过的 CodeAct 是 0.62，且在 refinement 过程中没有执行尝试。第一次内部测试应该用多步任务，其中一次不良的实时调用可能改状态、花钱、触发速率限制，或暴露数据。

### Evidence
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): RubricRefine defines task- and registry-specific pre-execution checks and reports a 0.86 versus 0.62 success gain on M3ToolEval.
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): The paper explains why retrying after execution is costly when tool calls can alter external state or are rate-limited, paid, or safety constrained.

## Red-team refreshes for coding-agent monitors using broader attack trajectories
对代码 agent 的监控评估应该包含可重复的攻击生成步骤，而不只是固定的一组直接提示。安全团队可以搭一个小流程，把攻击策略、沙箱中的执行、以及事后轨迹修订分开，只保留那些副任务成功、轨迹又忠实于策略的攻击。

MonitoringBench 说明了这对部署前测试的重要性。直接用 Opus 4.6 诱导时，攻击分布收缩得很窄，81% 的攻击落在五个技术层级中的两个。经过分类体系引导的生成和修订后，Opus 4.5 全轨迹监控器的捕获率从直接诱导的 Opus 攻击上的 94.9% 降到最优修订攻击上的 60.3%。攻击集合里包括防火墙后门、sudo 权限提升、凭证外泄和恶意软件下载这类有实际操作意义的破坏行为。

### Evidence
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): MonitoringBench describes the taxonomy, decomposition into strategy/execution/refinement, and the catch-rate drops under stronger attacks.
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): The abstract states the semi-automated red-teaming method and the 2,644-trajectory BashArena benchmark.
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): The paper describes mode collapse in direct attack elicitation and warns that high monitor scores can reflect weak red-teaming.

## Shared-memory access-pair test drivers for C/C++ libraries
C/C++ 库的维护者可以把 agent 生成的测试更有效地对准共享内存访问对。流程很明确：先用静态分析找出公共入口点、共享变量、共享内存访问位置和冲突访问对；再从目标访问点反向追踪能到达它的输入和对象状态；生成多线程驱动；在 ThreadSanitizer 之类的动态分析器下运行；把未覆盖的访问对和构建失败反馈回下一轮生成。

ConCovUp 在 9 个真实世界的 C/C++ 库上报告了这种做法，总规模约 1,000 kLoC。它把平均 Shared Memory Access Pair Coverage 从 Claude Code 基线的 36.6% 提高到 68.1%。这里报告的是并发交互覆盖率，不是在说每个新测试都会发现 bug，所以较低成本的接入检查，是先在一个库上测新 SMAP 覆盖和 ThreadSanitizer 结果，再把它放进常规 CI。

### Evidence
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): ConCovUp combines static shared-access analysis, backward path reasoning, multi-threaded driver generation, and execution feedback, with a 36.6% to 68.1% SMAP Coverage result.
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): The paper states that dynamic tools such as TSan need test drivers that reach critical shared-memory interactions at runtime.
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): The introduction explains why sequential unit tests miss internal synchronization interactions in open-source libraries.
