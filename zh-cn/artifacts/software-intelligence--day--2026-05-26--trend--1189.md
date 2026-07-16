---
kind: trend
trend_doc_id: 1189
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
topics:
- coding agents
- software verification
- program repair
- agent testing
- security benchmarks
- RAN automation
- AI cost control
run_id: materialize-outputs
aliases:
- recoleta-trend-1189
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/program-repair
- topic/agent-testing
- topic/security-benchmarks
- topic/ran-automation
- topic/ai-cost-control
language_code: zh-CN
---

# 编码代理正在被要求证明、审计并为自己的工作买单

## 概览
当天的研究把编码代理当作需要审计轨迹、可执行检查和预算控制的系统。TrajAudit、EviACT 和 Verus-SpecGym 说明了重点：必须定位失败，证据必须过关，规范必须按用户意图接受测试。

## 研究发现

### 基于证据门控的修复与故障诊断
仓库级编码代理正在按其对执行证据的使用情况接受评估。TrajAudit 面向失败的代理运行，预测最早的决定性错误步骤。它的 RootSE 基准包含 93 个失败实例、超过 4,500 个执行步骤，以及约 2,700 万字符。论文报告说，在比基线至少少用 18% token 的情况下，定位准确率提升超过 24.4 个百分点。

EviACT 在自动程序修复（APR）中采用同样的方法。它把失败测试证据带入定位阶段，在测试验证前拒绝格式错误或无法构建的补丁，并在完整回归前重新运行最初失败的测试。使用 GPT-4o 时，它在 Defects4J 2.0 和 SWE-bench 变体上给出领先的修复率；在有基线成本可比时，每个 bug 的 API 成本低 70.1–88.6%。

MocklessTester 为 Java 测试加入了同类思路的更底层版本。它挖掘真实的依赖使用，编译并运行生成的 JUnit 测试，并在符号和类型状态约束下修复失败。它在 Defects4J 上报告的平均行覆盖率为 88.82%，分支覆盖率为 83.74%，执行到的真实依赖代码比基于 mock 的基线更多。

#### 资料来源
- [TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems](../Inbox/2026-05-26--trajaudit-automated-failure-diagnosis-for-agentic-coding-systems.md): TrajAudit summary, RootSE scale, localization gain, and token reduction.
- [EviACT: An Evidence-to-Action Framework for Agentic Program Repair](../Inbox/2026-05-26--eviact-an-evidence-to-action-framework-for-agentic-program-repair.md): EviACT evidence gates, benchmark results, and API cost reductions.
- [LLM-based Mockless Unit Test Generation for Java](../Inbox/2026-05-26--llm-based-mockless-unit-test-generation-for-java.md): MocklessTester method and coverage results on Defects4J and Deps4J.

### 可执行规范与机器检查的软件
验证工作把规范视为失败来源。Verus-SpecGym 测试语言模型代理能否把非正式编程任务翻译成忠实的 Verus 规范。这个基准有 581 个来自 Codeforces 的任务。表现最强的模型解出 77.8%，而 LLM-as-a-judge 评估器漏掉了 26% 被可执行检查捕获的失败。

ConVer 使用大语言模型（LLM）编写 C 函数契约和循环不变量，然后让 ESBMC 作出通过或失败的判断。它的结果随基准难度而变：45 个 Frama-C 程序的成功率为 82–96%，一个较小的 X.509 解析器基准为 33–50%，LF-Hard 程序转换为 C 后为 67%。

这篇面向 Lean 的验证文章给出了更广泛的理由。它认为 AI 生成的软件需要独立的证明检查器，因为审查和测试跟不上生成代码的规模。文中的例子包括基于 Claude 的 zlib 形式化，以及 Lean 的 Mathlib，后者被引用为拥有超过 200,000 个形式化定理。

#### 资料来源
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): Verus-SpecGym benchmark design, model scores, and judge miss rate.
- [ConVer: Using Contracts and Loop Invariant Synthesis for Scalable Formal Software Verification](../Inbox/2026-05-26--conver-using-contracts-and-loop-invariant-synthesis-for-scalable-formal-software-verification.md): ConVer contract synthesis method and benchmark success rates.
- [When AI Writes the Software, Who Verifies It?](../Inbox/2026-05-26--when-ai-writes-the-software-who-verifies-it.md): Argument for machine-checked proofs and Lean-based examples.

### 长时间代理运行的安全与工作流测试
SEC-bench Pro 用真实的 JavaScript 引擎漏洞提升了安全代理评估门槛，并提供可复现的有漏洞、已修复和最新镜像。数据集在 V8 和 SpiderMonkey 上共有 183 个已验证漏洞。表现最强的单代理配置在 V8 任务上解出 32.0%，在 SpiderMonkey 任务上解出 38.8%。只按崩溃评分的评测器会把成功数多算 43.6%，所以目标归因会改变分数。

测试代理工作流加入了结构视角。所提方法把代理工作流转成一个由代理、工具、允许调用、受限调用和委派边组成的图。在 10 个从 SDK 派生的工作流上，生成的场景覆盖了 75 个允许工具义务中的 54 个，以及 48 个委派义务中的 36 个。对受限工具的探测在 248 个受限工具义务中发现了 23 次违规。

Keyblind 给密钥加了一道实用防线。它给代理提供假的 `.env` 值，只在命令运行时注入真实密钥。这里的证据来自产品而不是基准，但威胁很具体：项目提到，2025 年有超过 100,000 次暴露密钥的 LLM 对话被搜索引擎收录。

#### 资料来源
- [SEC-bench Pro: Can Language Models Solve Long-Horizon Software Security Tasks?](../Inbox/2026-05-26--sec-bench-pro-can-language-models-solve-long-horizon-software-security-tasks.md): SEC-bench Pro dataset, scoring method, agent results, and crash-only overcount.
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): Structural coverage criteria and evaluation results for agent workflows.
- [Keyblind – encrypted secrets vault that hides API keys from AI agents](../Inbox/2026-05-26--keyblind-encrypted-secrets-vault-that-hides-api-keys-from-ai-agents.md): Keyblind secret-handling design and stated incident scale.

### 领域专用代理系统与成本压力
GENESIS 展示了专用代理系统如何为技术领域而构建，在这些领域里，一个小小的 API 或规范错误就可能让部署失败。对于无线接入网（RAN）工作，它把意图路由到合成、测试、加固、优化、发现或安全流水线。验证通过仿真、模拟和空口测试床进行。论文报告两个功能实现案例研究都达到 100% 成功，而使用 Opus 4.7 的 Claude Code 在这些案例中没有给出可工作的实现。

企业成本信号没有那么技术化，但很难忽视。Uber 据报在 4 个月内花完了 2026 年 AI 编码工具预算。其 COO 说，公司目前还不能把 Claude Code 的使用与有用消费功能的可测增长明确对应起来。这让按 token 计费的代理使用同时成了管理问题和工程问题。

#### 资料来源
- [GENESIS: Harnessing AI Agents for Autonomous 6G RAN Synthesis, Research, and Testing](../Inbox/2026-05-26--genesis-harnessing-ai-agents-for-autonomous-6g-ran-synthesis-research-and-testing.md): GENESIS pipelines, validation tiers, and RAN case-study results.
- [Uber blows through its AI budget in 1 quarter](../Inbox/2026-05-26--uber-blows-through-its-ai-budget-in-1-quarter.md): Uber budget exhaustion, adoption claims, and uncertainty about product impact.
