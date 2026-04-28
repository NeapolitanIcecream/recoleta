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

# 可执行证明正在成为编码 agents 的标准输出

## Overview
这一天最明确的信号是，编码 agent 的研究正在收紧到可执行证明上。AgentForge、AnyPoC 和 AnalysisBench 都把模型输出当作草稿，必须通过具体检查才能成立：沙箱执行、可复现的分析输出，或重新运行的概念验证。这个重点与近期关于控制面和验证的一系列论文一致，但这一组工作更明确地指出了最终必须产出的对象：能通过的补丁、有效的分析结果，或能触发漏洞的测试。

## Clusters

### 环路中的验证
执行现在成了检验 agent 声称是否成立的关口。AgentForge 要求每个补丁都必须先在网络隔离的 Docker 沙箱中运行，才能进入下一步；它在 SWE-bench Lite 上报告了 40.0% 的问题解决率，比其单 agent 基线高出 26 到 28 个百分点。AnalysisBench 在另一类场景中得出相同结论：agent 需要明确的阶段划分和基于证据的停止规则，因为自我验证仍把成功率高估了 15%。AnyPoC 把这一模式用到安全报告上，方法是生成并重新运行可执行的概念验证测试，然后剔除未通过该检查的漏洞报告。

#### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge 强制要求沙箱执行，并报告了基准测试提升。
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench 展示了基于证据的完成检查，并测量了自我验证误差。
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC 使用可执行 PoC 和独立重跑来验证漏洞报告。

### 结构化控制与可追踪性
最强的系统在明确写出工作流边界，而不是只增加模型容量。AnalysisAgent 在每个周期只执行一个动作，使用确定性的日志压缩，并在 35 个工具-项目任务上对工具专属输出进行人工验证。CodeTracer 研究了这些边界缺失或薄弱时会发生什么。它把运行过程重建为状态转移树，然后定位最早导致失败的阶段和步骤。在 GPT-5 的轨迹上，步骤级 F1 从较轻量基线的大约 19 提升到 48.02，同时 token 使用量从 44.8k 到 58.5k 降到 31.1k。实际含义很直接：明确的阶段划分同时有助于执行和诊断。

#### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisAgent 展示了分阶段编排，以及端到端分析任务上的已验证结果。
- [CodeTracer: Towards Traceable Agent States](../Inbox/2026-04-13--codetracer-towards-traceable-agent-states.md): CodeTracer 量化了结构化轨迹在失败定位提升和 token 用量降低上的效果。

### 更难任务中的操作性证明
这一时期也把可执行检查从编程基准扩展到了更难的真实场景。AnyPoC 覆盖 12 个大型软件系统，包括 Chromium、Firefox、LLVM、OpenSSL、SQLite、FFmpeg 和 Redis。它报告称，对真实漏洞报告生成的有效 PoC 增加了 1.3x，拒绝的假阳性增加了 9.8x，并且有 45 个生成的 PoC 被采纳为官方回归测试。ORBIT 在另一种翻译场景中，把项目级编排与编译和测试修复结合起来，在 24 个 CRUST-Bench 程序上报告了 100% 的编译成功率和 91.7% 的测试成功率。共同点是操作层面的证明：编译、测试、轨迹和可复现产物正在成为被接受的输出，而不只是看起来合理的文本。

#### Evidence
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC 提供了具体的多系统结果，并且生成的 PoC 被采纳为回归测试。
- [OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems](../Inbox/2026-04-13--oom-rl-out-of-money-reinforcement-learning-market-driven-alignment-for-llm-based-multi-agent-systems.md): 这一时期的其他证据表明，已部署 agent 系统中的硬性外部约束和可执行检查很重要。
