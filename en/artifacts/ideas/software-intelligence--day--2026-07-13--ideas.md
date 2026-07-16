---
kind: ideas
granularity: day
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-14T00:00:00'
run_id: 6d7c0900-977c-4d46-bcca-f0ffd56a1405
status: succeeded
topics:
- coding agents
- repository context
- agent evaluation
- software security
- agent memory
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-context
- topic/agent-evaluation
- topic/software-security
- topic/agent-memory
language_code: en
pass_output_id: 325
pass_kind: trend_ideas
upstream_pass_output_id: 324
upstream_pass_kind: trend_synthesis
---

# Repository context checks for coding-agent workflows

## Summary
Repository context should be tested as an operational dependency. The practical changes are fault injection for retrieval, security-specific context gates before code completion, and explicit escalation when infrastructure evidence is missing or stale.

## Fault injection for repository retrieval and summaries
Coding-agent maintainers need to know whether a patch survives bad repository context. ACQUIRE shows that targeted, evidence-backed repository answers improve issue resolution, while AgentCheck finds that agents often accept stale or corrupted tool output confidently. Repository retrieval therefore belongs in the fault model, alongside API and database tools.

Add replayable mutations for stale file summaries, omitted dependency edges, incorrect symbol locations, and instructions embedded in retrieved text. Record the first trajectory divergence, then test mitigations such as source citations, file-hash checks, and read-only confirmation against current code.

Run 50 resolved SWE-bench tasks with clean and mutated context. Measure Pass@1 loss, unsafe edits, and mitigation recovery. Use a pilot decision threshold: stop if mutations reduce Pass@1 by under 5 percentage points, or revise the checks if they recover under half of the failures they expose.

### Sources
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): ACQUIRE reports higher SWE-bench Pass@1 after targeted, repository-evidenced question answering before patch generation.
- [AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP](../Inbox/2026-07-13--agentcheck-a-reproduce-intervene-mitigate-workbench-for-llm-agents-over-mcp.md): AgentCheck reproduces stale, incorrect, failed, and poisoned tool responses and finds frequent confident use of bad output.
- [Retrieval-Oriented Code Representations in Agentic Bug Localization](../Inbox/2026-07-13--retrieval-oriented-code-representations-in-agentic-bug-localization.md): The localization study shows that representation choice materially changes file retrieval accuracy and context cost.

## Security API context gate for AI-assisted pull requests
Application-security teams reviewing Java pull requests need a reliable check when developers use Copilot around SSL/TLS or OAuth APIs. In a 44-developer study, Copilot improved functional correctness without a significant gain in secure API usage, and only two participants raised security explicitly in their prompts. ACQUIRE suggests that focused questions can supply missing repository contracts before editing.

Trigger a short pre-completion questionnaire when a security API appears: which trust policy applies, where credentials originate, what validation path is required, and which repository configuration constrains the call. Supply answers with file and symbol citations, then run API-specific misuse checks before accepting the change. TerraRepair’s schema lookup and rescanning results support this combination of exact context and executable verification.

Pilot on 30 historical security-related pull requests using blinded review. Compare insecure API misuse, functional test passage, and review time. Use a pilot decision threshold: stop if misuse falls by less than 20% relative or median review time rises by more than 10%.

### Sources
- [Understanding the Impact of AI Code Assistants on Security API Usage: An Empirical Study](../Inbox/2026-07-13--understanding-the-impact-of-ai-code-assistants-on-security-api-usage-an-empirical-study.md): The developer study finds improved functional correctness but no significant overall improvement in secure API usage with Copilot.
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): Targeted repository questions produced highly evidence-supported answers and improved issue-resolution Pass@1.
- [TerraRepair: A Tool-Grounded LLM Agent for Infrastructure-as-Code Repair](../Inbox/2026-07-13--terrarepair-a-tool-grounded-llm-agent-for-infrastructure-as-code-repair.md): TerraRepair gains substantially from installed-schema lookup, dependency retrieval, and scanner-based acceptance checks.

## Freshness-aware escalation for Terraform repair
Cloud-security engineers need automated Terraform repair to stop when deployment evidence is absent or obsolete. TerraRepair attributes most escalations to missing deployment-specific context. AgentCheck shows that stale data remains difficult even after common mitigations, so a structurally valid provider response cannot be treated as current evidence.

Attach a receipt to every proposed repair with provider-schema version, dependency values, source commit, retrieval time, scanner version, and unresolved conflicts. Refuse automatic application when required fields are missing, hashes no longer match, or sources disagree. Replay captured repairs with stale schemas and changed dependency values to test whether the gate escalates before patching.

Start with 40 historical findings split between valid and deliberately stale context. Measure unsafe auto-approvals and unnecessary escalations. Use a pilot decision threshold: stop if the gate catches under 90% of stale-context cases, or revise it if more than 25% of valid cases are escalated.

### Sources
- [TerraRepair: A Tool-Grounded LLM Agent for Infrastructure-as-Code Repair](../Inbox/2026-07-13--terrarepair-a-tool-grounded-llm-agent-for-infrastructure-as-code-repair.md): TerraRepair uses provider schemas, dependency retrieval, rescanning, and structured escalation; missing deployment context dominates escalations.
- [AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP](../Inbox/2026-07-13--agentcheck-a-reproduce-intervene-mitigate-workbench-for-llm-agents-over-mcp.md): AgentCheck reports persistent difficulty handling stale tool data and supports exact replay of injected faults.
- [Long term memory cortex for agents that maintains tensions](../Inbox/2026-07-13--long-term-memory-cortex-for-agents-that-maintains-tensions.md): Daftari implements deterministic receipts containing provenance, freshness, content hashes, supersession state, and unresolved contradictions.
