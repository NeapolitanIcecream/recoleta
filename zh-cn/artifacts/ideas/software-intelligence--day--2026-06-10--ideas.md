---
kind: ideas
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent governance
- software engineering benchmarks
- LLM security
- code translation
- agent memory
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-governance
- topic/software-engineering-benchmarks
- topic/llm-security
- topic/code-translation
- topic/agent-memory
language_code: zh-CN
---

# Coding Agent Control Points

## 摘要
编码代理的采用正在转向具体控制点：用打分的 harness 运行来区分模型质量和 adapter 设计，用本地仓库记忆在重复失败修改前发出警告，以及为会压制拒绝的代码生成模式加入安全检查。真正有用的工作很具体：固定评估契约，把项目状态记录在聊天窗口之外，并在 decoder 设置进入开发流程之前先测试它们。

## Lite benchmark runs for coding-agent harness changes
评估编码代理的团队应该把 harness 当作产品组件来打分，而不是把它当作背景管道。Claw-SWE-Bench 说明了原因：在相同的 GLM 5.1 模型下，OpenClaw 使用最小的 direct-diff adapter 时 Pass@1 为 19.1%，使用完整 adapter 时为 73.4%。在固定模型下，harness 选择让 Pass@1 最多相差 27.4 个百分点。

一个可行的落地步骤是，在每次 harness 变更时加入一次小型、固定的基准测试。这个运行应保持任务集、Docker 工作区、提示模板、墙钟时间预算、补丁提取和预测格式不变，然后把 Pass@1、token 成本和墙钟时间一起报告。Claw-SWE-Bench Lite 提供了一个可用模式，因为它的 80 例子子集与 350 例子完整运行的结果很接近，而成本只有完整运行的约 22.9%。这让工程团队可以在把波动归因于模型之前，先发现 adapter、停止规则和补丁提取里的回归。

### 资料来源
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Reports the fixed scoring contract, adapter lifecycle, Pass@1 differences between minimal and full adapters, harness-choice spread, and Lite-80 cost and tracking results.
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Confirms the 350-instance benchmark, 80-instance Lite subset, 19.1% versus 73.4% Pass@1 result, and harness/cost accounting claim.

## Pre-merge checks that combine project memory with completion evidence
代理生成的 pull request 需要一个检查点，来拦住重复的失败修复和没有依据的完成声明。PROJECTMEM 提供状态层：它把 issue、attempt、fix、decision 和 note 记录在只追加的纯文本日志里，然后在编辑与失败尝试、未解决问题或高变更文件相关的路径前，通过 `precheck_file(path)` 发出警告。agent-gate 提供完成层：只有在所需证据字段明确为真时，`verify_gate(...)` 才会 fail closed。

一个可落地的工作流是给 AI 生成的变更加一个 pre-merge bot。在代理打开或更新 pull request 之前，它先把受影响文件和项目记忆日志对照。在 PR 被标记为 ready 之前，它要求确定性的检查、独立的反证优先审查、密钥检查、对不可逆或外向动作的人类批准，以及哈希链账本中的收据。第一个有用的指标很直接：统计这个 bot 拦住已知问题文件的重复修改，或拦住缺少测试、审查、密钥扫描、批准或收据的“已完成”声明的次数。

### 资料来源
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): Describes PROJECTMEM's append-only event log, deterministic summaries, MCP and CLI access, and `precheck_file(path)` warnings for prior failed attempts, open issues, and high-churn files.
- [Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server](../Inbox/2026-06-10--agent-gate-fail-closed-agent-gate-and-tamper-evident-receipts-as-an-mcp-server.md): Describes agent-gate's fail-closed completion checks, required default fields, independent review requirement, and SHA-256 hash-chained receipt ledger.
- [Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server](../Inbox/2026-06-10--agent-gate-fail-closed-agent-gate-and-tamper-evident-receipts-as-an-mcp-server.md): Shows the demo path where missing human approval and missing receipt block completion, and where ledger verification detects tampering.

## Safety regression tests for grammar-constrained code generation
给代码启用 grammar-constrained decoding 的团队应该为恶意代码提示加入安全回归测试套件。CodeSpear 显示，正常的编程语言语法会把自然语言拒绝从有效输出空间中移除，只剩下模型在语法上有效的代码中采样。报告中的攻击在 Qwen2.5-Coder-7B 等本地模型上的平均成功率达到 81.82%，并且在测试模型上比代表性的 jailbreak 基线平均高出 30 个百分点以上。

具体测试是：对每个模型和推理栈，都在有和没有语法约束的情况下运行恶意代码基准。只要受约束运行产生可执行有害代码的比例高于未受约束运行，门禁就应该失败。如果必须输出语法代码，CodeShield 给出一种缓解模式：针对只能输出代码的场景训练偏好行为，让模型在无法表达拒绝时输出无害代码。

### 资料来源
- [Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code](../Inbox/2026-06-10--grammar-constrained-decoding-can-jailbreak-llms-into-generating-malicious-code.md): Explains how grammar-constrained decoding can suppress refusals, lists affected deployment settings, reports attack success rates, and describes CodeShield's preference-training approach.
- [Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code](../Inbox/2026-06-10--grammar-constrained-decoding-can-jailbreak-llms-into-generating-malicious-code.md): Confirms that vLLM and SGLang support grammar-constrained decoding and describes the mechanism by which a standard code grammar can force malicious code generation.
