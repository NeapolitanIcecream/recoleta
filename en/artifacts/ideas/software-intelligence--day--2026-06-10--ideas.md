---
kind: ideas
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
run_id: dd7a0731-956b-4096-8d79-a6cad0e86b55
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
language_code: en
pass_output_id: 245
pass_kind: trend_ideas
upstream_pass_output_id: 244
upstream_pass_kind: trend_synthesis
---

# Coding Agent Control Points

## Summary
Coding-agent adoption is moving toward concrete control points: scored harness runs that separate model quality from adapter design, local repository memory that warns before repeated failed edits, and security checks for code-generation modes that can suppress refusals. The useful work is specific: fix the evaluation contract, record project state outside the chat window, and test decoder settings before they reach developer workflows.

## Lite benchmark runs for coding-agent harness changes
Teams evaluating coding agents should score the harness as a product component, not as background plumbing. Claw-SWE-Bench shows why: with the same GLM 5.1 model, OpenClaw scored 19.1% Pass@1 with a minimal direct-diff adapter and 73.4% with the full adapter. Under fixed models, harness choice changed Pass@1 by as much as 27.4 percentage points.

A practical adoption step is to add a small fixed benchmark run to every harness change. The run should keep the task set, Docker workspace, prompt template, wall-clock budget, patch extraction, and prediction format stable, then report Pass@1 beside token cost and wall-clock time. Claw-SWE-Bench Lite is a useful pattern because its 80-instance subset tracked the 350-instance run closely while costing about 22.9% of the full run. This gives engineering teams a way to catch regressions in adapters, stopping rules, and patch extraction before attributing movement to the model.

### Evidence
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Reports the fixed scoring contract, adapter lifecycle, Pass@1 differences between minimal and full adapters, harness-choice spread, and Lite-80 cost and tracking results.
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Confirms the 350-instance benchmark, 80-instance Lite subset, 19.1% versus 73.4% Pass@1 result, and harness/cost accounting claim.

## Pre-merge checks that combine project memory with completion evidence
Agent-authored pull requests need a checkpoint that catches repeated failed fixes and unsupported claims of completion. PROJECTMEM supplies the state layer: it records issues, attempts, fixes, decisions, and notes in an append-only plain-text log, then warns through `precheck_file(path)` before edits to files tied to failed attempts, open issues, or high churn. agent-gate supplies the completion layer: `verify_gate(...)` fails closed unless required evidence fields are explicitly true.

A buildable workflow is a pre-merge bot for AI-authored changes. Before the agent opens or updates a pull request, it checks touched files against the project memory log. Before the PR is marked ready, it requires deterministic checks, independent refute-first review, a secrets check, human approval for irreversible or outward actions, and a receipt in a hash-chained ledger. The first useful measurement is simple: count how often the bot blocks repeated edits to known-problem files or blocks a “done” claim with missing tests, review, secret scan, approval, or receipt.

### Evidence
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): Describes PROJECTMEM's append-only event log, deterministic summaries, MCP and CLI access, and `precheck_file(path)` warnings for prior failed attempts, open issues, and high-churn files.
- [Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server](../Inbox/2026-06-10--agent-gate-fail-closed-agent-gate-and-tamper-evident-receipts-as-an-mcp-server.md): Describes agent-gate's fail-closed completion checks, required default fields, independent review requirement, and SHA-256 hash-chained receipt ledger.
- [Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server](../Inbox/2026-06-10--agent-gate-fail-closed-agent-gate-and-tamper-evident-receipts-as-an-mcp-server.md): Shows the demo path where missing human approval and missing receipt block completion, and where ledger verification detects tampering.

## Safety regression tests for grammar-constrained code generation
Teams enabling grammar-constrained decoding for code should add a security regression suite for malicious code prompts. CodeSpear shows that a normal programming-language grammar can remove natural-language refusals from the valid output space and leave the model sampling only syntactically valid code. The reported attack reached 81.82% average success on local models such as Qwen2.5-Coder-7B and beat representative jailbreak baselines by more than 30 percentage points on average across tested models.

The concrete test is to run a malicious-code benchmark with and without the grammar constraint for each model and inference stack. The gate should fail when the constrained run produces executable harmful code at a higher rate than the unconstrained run. If grammar output is mandatory, CodeShield points to one mitigation pattern: train preference behavior for cases where only code is allowed, so the model emits harmless code when a refusal cannot be represented.

### Evidence
- [Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code](../Inbox/2026-06-10--grammar-constrained-decoding-can-jailbreak-llms-into-generating-malicious-code.md): Explains how grammar-constrained decoding can suppress refusals, lists affected deployment settings, reports attack success rates, and describes CodeShield's preference-training approach.
- [Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code](../Inbox/2026-06-10--grammar-constrained-decoding-can-jailbreak-llms-into-generating-malicious-code.md): Confirms that vLLM and SGLang support grammar-constrained decoding and describes the mechanism by which a standard code grammar can force malicious code generation.
