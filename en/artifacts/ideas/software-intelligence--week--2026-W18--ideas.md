---
kind: ideas
granularity: week
period_start: '2026-04-27T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: 4b758f75-19b5-49ca-abc8-4c7c7fd6ebc0
status: succeeded
topics:
- coding agents
- software engineering
- benchmarks
- verification
- security repair
- agent infrastructure
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/benchmarks
- topic/verification
- topic/security-repair
- topic/agent-infrastructure
language_code: en
pass_output_id: 143
pass_kind: trend_ideas
upstream_pass_output_id: 142
upstream_pass_kind: trend_synthesis
---

# Checkable Coding Agent Controls

## Summary
Coding-agent adoption is moving toward smaller, checkable control points: focused file viewing, safer patch application, product-decision checks, SAST triage with fallback behavior, and evaluation records that include traces, files, tests, and state changes.

## Focused file viewing and patch application tools for repository agents
Repository agents need a thinner interface between exploration and editing. SWE-Edit gives a practical design: a Viewer returns only task-relevant code blocks for a file and query, while an Editor applies a patch from a natural-language edit instruction. The main agent keeps the bug reasoning and fix plan, with less file-search residue in its context and fewer brittle find-and-replace failures.

The reported gains are modest on issue resolution and more concrete on cost and edit reliability. On SWE-bench Verified, SWE-Edit raises resolved rate from 69.9% to 72.0%, cuts inference cost by 17.9%, and raises edit success from 93.4% to 96.9%. The Viewer returns 39.7% of requested file content on average, which is a direct way to test whether the interface is reducing code surface without hiding the needed lines.

A team running coding agents on an internal monorepo can test this without changing the model: add a file-view endpoint that takes a path and query, add a patch endpoint that accepts an edit instruction, and compare agent runs on recent bugs. Track resolved issues, failed patches, non-cached input tokens, and reviewer complaints about unrelated edits.

### Sources
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit reports the Viewer and Editor split, cost reduction, edit-success gains, token reduction, and SWE-bench Verified results.
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): The paper abstract describes the context-coupling problem and the two-subagent design.

## Decision-compliance checks for coding-agent pull requests
Coding agents can pass lint and typecheck while missing team decisions stored outside the repo. The practical build is a PR gate that turns product and engineering decisions into explicit checks: required audit logging, approved UI components, feature flags, ORM choices, auth wrappers, and deprecated patterns. The agent can receive retrieved decisions during spec drafting and mid-build review, and the final diff can be scored against the same decision list.

Context-Augmented Code Generation reports a large gain on a small clean-room benchmark: Claude Code with codebase access alone scores 46% weighted decision compliance, while Claude Code plus Brief scores 95%. The setup also changes the workflow by adding specs, acceptance criteria, and mid-build guidance, so the safer takeaway is operational: teams should measure whether their agent PRs follow stored decisions, not only whether the code compiles.

A cheap first version can cover one product area and ten recurring decisions. Store each decision with an owner, examples, and a regex or review checklist. Run the coding agent on old tickets, then compare generated diffs against the checklist before and after retrieval.

### Sources
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): The paper defines decision compliance, describes Brief, and reports the 46% to 95% compliance change plus benchmark limits.
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): The source text says product decisions may live in tools, design documents, or wikis and can be invisible in code.

## Semgrep alert triage with contextual LLM review and fail-open handling
SAST adoption is blocked by alert queues that developers stop trusting. QASecClaw points to a bounded use of a coding model: keep Semgrep as the high-recall scanner, send each finding with CWE type, file location, and source context to an LLM reviewer, and suppress only findings judged false positive. If the model times out or returns malformed JSON, keep the original Semgrep alert.

On OWASP Benchmark v1.2, QASecClaw reduces false positives from 560 to 64 and raises F1 from 78.39% to 90.93%, with recall down by 3.1%. That tradeoff is practical for security teams that already review Semgrep output, because the model is judging a known candidate alert instead of searching the full codebase.

The first deployment should run in shadow mode on existing CI alerts. Compare model-suppressed findings with human triage for a few CWE categories, keep all suppressed alerts visible in an audit view, and require structured reasons tied to nearby sanitization, validation, encoding, or parameterized APIs.

### Sources
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw uses Semgrep first, applies contextual LLM review, keeps alerts on model failure, and reports OWASP Benchmark results.
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): The abstract describes the SAST false-positive problem and the Semgrep plus coding-specialized LLM filter setup.
