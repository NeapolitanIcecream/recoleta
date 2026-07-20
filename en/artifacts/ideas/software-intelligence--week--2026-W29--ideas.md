---
kind: ideas
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
run_id: ff933669-c602-4705-915e-81cbc0549a68
status: succeeded
topics:
- coding agents
- agent evaluation
- software testing
- runtime verification
- repository context
- software security
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-testing
- topic/runtime-verification
- topic/repository-context
- topic/software-security
language_code: en
pass_output_id: 339
pass_kind: trend_ideas
upstream_pass_output_id: 338
upstream_pass_kind: trend_synthesis
---

# Coding-agent controls tied to verification failures and harness changes

## Summary
Repository exploration can be deferred until verification identifies a concrete knowledge gap, reducing unnecessary context while preserving a path to deeper repair. Separately, harness upgrades need paired security regression tests because changing the interaction layer can reverse whether the same model blocks or executes an unsafe action.

## Verification-triggered repository question answering for coding-agent repair
Coding-agent teams should trigger targeted repository question answering when a minimal repair fails verification, rather than performing the same broad exploration before every edit. E3 shows that starting with the smallest viable execution path and expanding after failed verification can reduce redundant work, while ACQUIRE shows that explicit questions about repository mechanisms, dependencies, and contracts can recover otherwise failed repairs. DiffTestGen supplies a concrete escalation signal: tests aimed through public entry points at changed functions can reveal unexplained old-versus-new behavior or stalled changed-line coverage.

A practical repair loop would estimate scope, make the smallest plausible patch, and run change-directed tests. A failure would be translated into repository questions for read-only agents; their file- and function-cited answers would then inform the next patch. The cheapest useful evaluation is an ablation on the same issue set comparing always-on question answering, no question answering, and verification-triggered question answering, measuring resolved issues, tokens, and repair rounds.

### Sources
- [Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution](../Inbox/2026-07-14--do-ai-agents-know-when-a-task-is-simple-toward-complexity-aware-reasoning-and-execution.md): E3 maintained 100% success on its controlled 121-edit benchmark while reducing tokens by 91%, though broader deployment performance was not established.
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): ACQUIRE raised SWE-bench Verified Pass@1 by 3.8–4.4 percentage points and reduced repair rounds by 17.1% on cases converted from failure to success.
- [DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences](../Inbox/2026-07-17--difftestgen-change-directed-llm-based-testing-for-exposing-behavioral-differences.md): DiffTestGen used changed functions, public entry points, and union-coverage feedback to expose behavioral differences in 78.2% of 463 pull requests.

## Harness-swap security tests for coding-agent releases
Coding-agent release engineers should treat a harness upgrade as a security-relevant behavior change even when the model is unchanged. AgentCompass found that harness choice changed benchmark scores and trajectory failures. In package-install experiments, swapping only the harness changed one untrusted-registry attack from 10/10 caught to 9/30 caught, while another variant moved in the opposite direction. Model-level safety claims therefore cannot substitute for testing the shipped model–harness combination.

Before releasing a harness or permission-policy change, run the current and candidate versions with the same model on fixed dependency-install attacks and benign controls, then compare whether unsafe commands are blocked before execution and inspect the recorded trajectories. The release receipt should bind the result to the harness version, tool policy, command set, and source state; Proof-or-Stop demonstrates the underlying mechanism for rejecting stale, tampered, or reconfigured evidence, while explicitly not proving semantic correctness.

### Sources
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): AgentCompass separates benchmark, harness, and environment and reports score and failure-pattern variation across harnesses.
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): With the model held fixed, a harness swap reversed detection outcomes for untrusted-registry scenarios; a deterministic pre-install check closed most observed gaps.
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): Proof-or-Stop binds evidence to source, policy, and command-set hashes and rejected 18 tested tamper classes, but was evaluated with one model family and a self-hosted corpus.
