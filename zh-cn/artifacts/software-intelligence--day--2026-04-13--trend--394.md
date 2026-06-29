---
kind: trend
trend_doc_id: 394
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
topics:
- coding-agents
- execution-verification
- software-analysis
- bug-validation
- traceability
run_id: materialize-outputs
aliases:
- recoleta-trend-394
tags:
- recoleta/trend
- topic/coding-agents
- topic/execution-verification
- topic/software-analysis
- topic/bug-validation
- topic/traceability
language_code: zh-CN
---

# 可执行证明正在成为编码代理的标准输出

## Overview
这一天最清楚的信号是，编码代理工作正在收紧到可执行证明上。AgentForge、AnyPoC 和 AnalysisBench 都把模型输出当作草稿，要求它先通过具体检查：沙箱执行、可复现的分析输出，或重新运行的概念验证。这种重点与近期关于控制面和验证的一批论文一致，但这组工作更明确地指向最终必须存在的工件：一个通过的补丁、一个有效的分析结果，或一个能触发漏洞的测试。

## Clusters

### Verification in the loop
执行现在成了代理主张的门槛。AgentForge 要求每个补丁先在网络隔离的 Docker 沙箱里运行，才能继续推进，并报告在 SWE-bench Lite 上达到 40.0% 的解决率，比单代理基线高出 26 到 28 个百分点。AnalysisBench 在另一个场景里得到同样的结论：代理需要明确的阶段和基于证据的停止规则，因为自我验证仍把成功率高估了 15%。AnyPoC 把这个模式用到安全报告上，先生成并重新运行可执行的概念验证测试，再拒绝未通过检查的漏洞报告。

#### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge makes sandbox execution mandatory and reports benchmark gains.
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench shows evidence-based completion checks and measured self-validation error.
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC uses executable PoCs and independent re-execution to validate bug reports.

### Structured control and traceability
最强的系统在写清工作流边界，而不只是增加模型容量。AnalysisAgent 在 35 个工具项目任务上采用每个周期一个动作、确定性的日志压缩，以及对工具特定输出的人工验证。CodeTracer 研究这些边界缺失或变弱时会发生什么。它把运行过程重建成状态转换树，然后找出最早导致失败的阶段和步骤。在 GPT-5 轨迹上，步骤级 F1 从轻量基线的约 19 提高到 48.02，而 token 使用量从 44.8k 到 58.5k 降到 31.1k。直接的信息很清楚：明确的阶段有助于执行，也有助于诊断。

#### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisAgent shows staged orchestration and verified outcomes on end-to-end analysis tasks.
- [CodeTracer: Towards Traceable Agent States](../Inbox/2026-04-13--codetracer-towards-traceable-agent-states.md): CodeTracer quantifies failure localization gains and lower token use from structured traces.

### Operational proof across tougher tasks
这一时期也把可执行检查从编码基准扩展到了更难的真实场景。AnyPoC 覆盖 12 个大型软件系统，包括 Chromium、Firefox、LLVM、OpenSSL、SQLite、FFmpeg 和 Redis。它报告对真实漏洞报告生成的有效 PoC 多出 1.3 倍，驳回的假阳性多出 9.8 倍，还有 45 个生成的 PoC 被采用为官方回归测试。ORBIT 在另一个翻译场景中把项目级编排和编译、测试修复结合起来，在 24 个 CRUST-Bench 程序上报告 100% 的编译成功率和 91.7% 的测试成功率。共同点是操作性证明：编译、测试、轨迹和可复现工件正在成为被接受的输出，而不只是看起来合理的文本。

#### Evidence
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC provides concrete multi-system results and adoption of generated PoCs as regression tests.
- [OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems](../Inbox/2026-04-13--oom-rl-out-of-money-reinforcement-learning-market-driven-alignment-for-llm-based-multi-agent-systems.md): Additional evidence in the period shows hard external constraints and executable checks matter in deployed agent systems.
