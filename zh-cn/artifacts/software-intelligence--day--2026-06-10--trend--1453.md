---
kind: trend
trend_doc_id: 1453
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
topics:
- coding agents
- agent governance
- software engineering benchmarks
- LLM security
- code translation
- agent memory
run_id: materialize-outputs
aliases:
- recoleta-trend-1453
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-governance
- topic/software-engineering-benchmarks
- topic/llm-security
- topic/code-translation
- topic/agent-memory
language_code: zh-CN
---

# Coding agents need state, measured harnesses, and action gates

## 概览
当天最强的信号是，coding agent 正被当成需要记忆、harness 计量、gate 和 monitor 的产品。PROJECTMEM、Claw-SWE-Bench 和 CodeSpear 把一个实用议程定了下来：让 agent 保持状态，测量 harness，并测试代码特定工具引入的安全路径。

## 研究发现

### Coding-agent harnesses and skills
Claw-SWE-Bench 把 harness 本身算进分数里。使用同一个 GLM 5.1 模型时，OpenClaw 在最小 adapter 下的 Pass@1 从 19.1% 提升到完整 adapter 下的 73.4%。论文还报告，在固定模型下，harness 选择会让 Pass@1 最多相差 27.4 个百分点，而 Lite-80 集合只用约 23% 的运行成本，就能跟上完整的 350 实例基准。

几篇配套材料把 agent 运行当成需要持续维护的运行时。Loop-Harness 把 Claude Code 运行安排在隔离的 git worktree 里，然后要求第二个 Claude 会话打印 `VERDICT: PASS` 才能发出。Agents All the Way Down 更偏向把命令行界面（CLI）agent 用在产品集成里，并引用了一个匹配任务：Model Context Protocol（MCP）用的 token 约为 CLI 的 35 倍。SkillJuror 给出一个更小但有用的结果：把同样的 skill 内容改成 Progressive Disclosure 后，410 次匹配试验里的通过率从 42.0% 提高到 46.1%。

#### 资料来源
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Claw-SWE-Bench reports harness, model, Pass@1, Lite-80, and cost results.
- [Loop-Harness](../Inbox/2026-06-10--loop-harness-is-here.md): Loop-Harness describes scheduled agent runs, worktree isolation, verifier gates, and sample operational metrics.
- [Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production](../Inbox/2026-06-10--agents-all-the-way-down-a-methodology-for-building-custom-ai-agents-from-substrate-to-production.md): Agents All the Way Down gives the five-phase custom-agent method and CLI versus MCP cost examples.
- [SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior](../Inbox/2026-06-10--skilljuror-measuring-how-agent-skill-organization-changes-runtime-behavior.md): SkillJuror reports matched trials showing how skill organization changes runtime behavior and pass rate.

### Repository memory and multi-file localization
PROJECTMEM 处理编码会话里的一个常见失败模式：agent 忘记失败过的修复，然后重复做上下文重建。它把问题、尝试、修复、决策和笔记存进只追加的纯文本日志，再为 agent 生成确定性的摘要。它的 `precheck_file(path)` gate 会在修改与失败尝试、未解决问题或高变动率相关的路径之前发出警告。论文估计，重建项目上下文每个会话要花 5,000 到 20,000 个 token，不过它没有报告受控的任务成功率基准。

Exploration Structure in LLM Agents 先处理补丁之前的文件定位步骤。在 SWE-bench Pro 的 Ansible 切片上，它把 domain agent 分配到 CLI、module utilities、plugins 和 docs 等仓库区域。结果显示，小模型更适合按子系统并行搜索。同一研究还说明，受限输入很重要：在受限上下文下，一份大的源码文件从 29,895 个 token 降到 719 个，文档大文件从 14,366 个 token 降到 121 个。

#### 资料来源
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): PROJECTMEM summary covers event-sourced memory, pre-action warnings, token estimates, implementation details, and evaluation limits.
- [Exploration Structure in LLM Agents for Multi-File Change Localization](../Inbox/2026-06-10--exploration-structure-in-llm-agents-for-multi-file-change-localization.md): The multi-file localization paper reports domain-scoped agents, Ansible SWE-bench Pro setup, and token reductions from bounded I/O.

### Runtime governance and agent oversight
生产环境 agent 的安全正在动作层面被定义。五平面参考架构会在动作到达企业基础设施之前检查意图、委派链、能力集合和会话状态。它还提出了随时中止的调解机制，包括 pause、escalate、narrow、modify、defer 和 rollback，以及防篡改审计记录。论文里的证据主要是结构性的，只给了微秒级的 policy-core 计时，没有现场的完整系统基准。

同一时期还出现了两种实用变体。agent-gate 让完成默认失败关闭，除非所有必需证据字段都为真，包括确定性检查、独立审查、没有 secrets、对不可逆动作的人类批准，以及一份诚实的 receipt。Bootstrapped Monitoring 加入了一套模型监督协议：更强的未受信监控器审查动作，而更弱但受信任的模型审计监控器的原始 chain-of-thought（CoT）。效果取决于是否能看到原始 CoT；在报告的测试里，摘要化推理会明显削弱检测能力。

#### 资料来源
- [A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents](../Inbox/2026-06-10--a-five-plane-reference-architecture-for-runtime-governance-of-production-ai-agents.md): The five-plane architecture summary covers delegated-action risk, stop-anywhere mediation, composite principals, audit records, and evaluation scope.
- [Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server](../Inbox/2026-06-10--agent-gate-fail-closed-agent-gate-and-tamper-evident-receipts-as-an-mcp-server.md): agent-gate describes fail-closed gates, required checks, SHA-256 hash-chained receipts, and demo outcomes.
- [Bootstrapped Monitoring: Leveraging Transparent Reasoning to Oversee Stronger AI Agents](../Inbox/2026-06-10--bootstrapped-monitoring-leveraging-transparent-reasoning-to-oversee-stronger-ai-agents.md): Bootstrapped Monitoring reports the three-role protocol, catch-rate examples, and dependence on raw chain-of-thought.

### Code-specific safety and semantic verification
代码生成也有自己的安全失效路径。CodeSpear 表明，grammar-constrained decoding（GCD）这种强制生成语法正确代码的技术，可以把自然语言拒绝从输出空间里去掉。在 Qwen2.5-Coder-7B 这类本地模型上，这种攻击的平均成功率达到 81.82%；在测试过的模型里，它的平均表现比代表性的 jailbreak 基线高出 30 多个百分点。CodeShield 的做法是，在语法约束强制输出代码时，训练无害的代码输出。

Multisage 处理的是另一种代码特有弱点：翻译结果能编译，但程序行为变了。它从源代码里提取控制流、类型和 API 信号，生成多个语义视图，再用执行验证、代码变异和跨视图检查筛选这些视图，然后再提示翻译器。在 HumanEval-X 上，它报告的成功率提升最高达到 2.22 倍，且相对增幅在较小模型上最大。

#### 资料来源
- [Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code](../Inbox/2026-06-10--grammar-constrained-decoding-can-jailbreak-llms-into-generating-malicious-code.md): CodeSpear summary gives the GCD jailbreak mechanism, evaluated models, attack success rates, benchmarks, and CodeShield mitigation.
- [Enhancing LLM-Based Code Translation with Verified Multi-Semantic Representations](../Inbox/2026-06-10--enhancing-llm-based-code-translation-with-verified-multi-semantic-representations.md): Multisage summary reports semantic extraction, calibration checks, HumanEval-X results, and relative gains by model size.
