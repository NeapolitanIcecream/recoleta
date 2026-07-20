---
kind: trend
trend_doc_id: 2013
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u4EE3\u7406\u8BC4\u4F30"
- "\u8F6F\u4EF6\u6D4B\u8BD5"
- "\u8FD0\u884C\u65F6\u9A8C\u8BC1"
- "\u4EE3\u7801\u4ED3\u5E93\u4E0A\u4E0B\u6587"
- "\u8F6F\u4EF6\u5B89\u5168"
run_id: materialize-outputs
aliases:
- recoleta-trend-2013
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u4EE3\u7406\u8BC4\u4F30"
- "topic/\u8F6F\u4EF6\u6D4B\u8BD5"
- "topic/\u8FD0\u884C\u65F6\u9A8C\u8BC1"
- "topic/\u4EE3\u7801\u4ED3\u5E93\u4E0A\u4E0B\u6587"
- "topic/\u8F6F\u4EF6\u5B89\u5168"
language_code: zh-CN
---

# 编码代理控制通过定向上下文和可执行证据提升了精确性

## 概览
本周进一步强化了为期三周的证据积累：编码代理的性能取决于模型周围的系统。新的信号在于精确性：系统针对已识别的知识缺口获取上下文，同时将声明绑定到变更代码、确切的源状态或领域风险。结果覆盖基准测试和原型，但广泛部署证据仍然有限。

## 研究发现

### 最低充分的代码仓库上下文
两项研究都支持选择性获取上下文，而不是穷举式探索。ACQUIRE 在修复前提出针对代码仓库的问题，使 SWE-bench Verified 上的 Pass@1 最高提升 4.4 个百分点。E3 估计任务范围，从最小可行执行路径开始，仅在验证失败后扩展；在其受控基准测试中，它保持了 100% 的成功率，同时将 token 数减少了 91%。两项研究共同表明，上下文获取应作为有预算约束的干预措施，而不是默认的全仓库扫描。不过，E3 最强的数值来自模拟器，因此其效率提升仍需更广泛的验证。

#### 资料来源
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): 报告了 ACQUIRE 的定向问答方法、最高 4.4 个百分点的 Pass@1 提升，以及代码仓库 grounding 结果。
- [Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution](../Inbox/2026-07-14--do-ai-agents-know-when-a-task-is-simple-toward-complexity-aware-reasoning-and-execution.md): 报告了 E3 的失败后扩展策略，以及在保持 100% 成功率的同时将成本降低 85%、token 数降低 91% 的受控结果。

### 感知执行框架、绑定源状态的门控
执行框架如今同时构成测量声明和安全声明的一部分。AgentCompass 发现，改变执行框架会改变基准分数和轨迹失败情况。一项供应链研究同样表明，同一个模型是否识别或安装攻击，取决于其执行框架；而确定性的安装前检查则弥补了大多数已观察到的缺口。Proof-or-Stop 增加了更严格的生命周期边界：只有在新鲜证据经过认证并绑定到当前源状态时，代理的声明才会推进。其测试阻止了虚假完成和被篡改的回执，但评估仅覆盖一个模型系列和一个自托管语料库。

#### 资料来源
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): 展示了不同执行框架之间的分数差异，并记录了多个基准测试中依赖执行框架的失败模式。
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): 展示了软件包安装攻击对执行框架和模型的依赖性，以及在执行前检查依赖项名称、来源和版本所产生的影响。
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): 定义了绑定源状态的证据门控，并报告了 10/10 个生命周期场景均无 false-done，以及对 18 类篡改的拒绝。

### 面向相关失败面的验证
可执行检查正变得更聚焦，同时覆盖更完整的领域要求。DiffTestGen 将测试引向变更函数，并在 463 个拉取请求中的 78.2% 中暴露了行为差异。GapForge 针对未覆盖的编译器区域，在报告的基线之上增加了数万行覆盖代码，并发现了 12 个真实失败。Alipay-PIBench 将同样的逻辑应用于支付集成，测试端到端行为、签名和通知处理、幂等性、退款以及业务状态一致性。这些结果表明，当真正有意义的失败面是代码差异、覆盖缺口或领域不变量时，通用的通过信号并不足够。

#### 资料来源
- [DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences](../Inbox/2026-07-17--difftestgen-change-directed-llm-based-testing-for-exposing-behavioral-differences.md): 报告了变更导向的测试生成、78.2% 的行为差异暴露率，以及覆盖 463 个拉取请求时 90.7% 的平均联合覆盖率。
- [GapForge: Directed Compiler Fuzzing via Coverage-Gap Analysis](../Inbox/2026-07-17--gapforge-directed-compiler-fuzzing-via-coverage-gap-analysis.md): 报告了覆盖缺口导向的编译器模糊测试、GCC 和 LLVM 的额外覆盖，以及发现的 12 个失败。
- [Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents](../Inbox/2026-07-16--alipay-pibench-a-realistic-payment-integration-benchmark-for-coding-agents.md): 定义了支付领域专用的静态、单元、集成和端到端检查，覆盖 18 个代码仓库级任务，并包括风险强化要求。
