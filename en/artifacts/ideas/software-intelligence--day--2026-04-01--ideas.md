---
kind: ideas
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- software-agents
- coding-llms
- evaluation
- security
- gpu-kernels
tags:
- recoleta/ideas
- topic/software-agents
- topic/coding-llms
- topic/evaluation
- topic/security
- topic/gpu-kernels
language_code: en
pass_output_id: 9
pass_kind: trend_ideas
upstream_pass_output_id: 8
upstream_pass_kind: trend_synthesis
---

# Agent workflow observability

## Summary
Software-agent work in this window points to three immediate workflow changes: track whether agent code survives after merge, publish reusable run packets for evaluation and training, and treat untrusted content isolation as part of agent security. The common thread is better visibility into what agents did, what lasted, and what the surrounding scaffold allowed.

## Post-merge churn tracking for agent-authored pull requests
Teams shipping coding agents need a post-merge review lane that measures what survives after merge, not just whether the agent opened a successful pull request. A practical build is a repository report that tags agent-authored PRs, tracks later edits on the touched lines and files for 7, 30, and 90 days, and feeds the results back into review policy. Start with repositories that already label Codex, Claude Code, Copilot, Jules, or Devin activity. Flag patterns such as repeated follow-up fixes, high rewrite rates in generated tests, or large refactors that collapse soon after merge. The point is operational: maintainers need a way to see which agent workflows create cleanup work for humans.

The evidence now supports this as a normal engineering metric. A GitHub-scale study built a dataset of 111,969 PRs across five coding agents and found that agent-authored code sees more later churn than human-authored code. A separate evaluation paper argues that software-agent results are hard to compare when work stops at final task scores and hidden runs. Joining those two lines of work yields a concrete workflow: store the run metadata for each agent PR, then compare survival and churn by model, scaffold, repository type, and review path. A cheap first check is one quarter of data from a single org with bot-authored PR detection and a simple line-survival calculation.

### Evidence
- [Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time](../Inbox/2026-04-01--investigating-autonomous-agent-contributions-in-the-wild-activity-patterns-and-code-change-over-time.md): Real-world PR dataset across five agents with higher later churn in agent-authored code.
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): Argues for reproducible agent evaluation with exact versions, prompts, and trajectory logs beyond final scores.

## Standardized run packets with searchable Thought-Action-Result logs
Agent teams should add a mandatory trace package to every benchmark or internal bake-off: exact model version, prompts, temperature, tool settings, and a summarized Thought-Action-Result log for each run. This is a buildable support layer for evaluation, not a research nicety. Without it, failures cannot be inspected, baseline claims are hard to verify, and teams end up rerunning expensive experiments to answer basic questions about why one scaffold beat another.

The current evidence points to a narrow, useful format. One review of 18 software-engineering agent papers found that only 1 compared against a relevant agentic baseline. The same paper recommends publishing TAR trajectories or summaries so later analysis can recover concrete failure modes and verification behavior. STITCH adds a second reason to keep richer traces: its gains come from filtering long runs down to decision-critical segments, with up to 63.16% relative improvement on SWE-bench Verified and 61.31% compilation pass rate on HarmonyOS ArkTS using less than 1K training trajectories. That combination makes a small internal tool credible: collect runs once, compress them into searchable decision segments, and use the same store for both evaluation review and later fine-tuning.

### Evidence
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): Calls for exact reporting details and TAR logs; finds weak baseline practice in recent papers.
- [Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs](../Inbox/2026-04-01--yet-even-less-is-even-better-for-agentic-reasoning-and-coding-llms.md): Shows that filtering traces to decision-critical segments can materially improve coding-agent training.

## Attachment and workspace quarantine for high-privilege personal agents
Personal agents with file, email, browser, and shell access need an attachment and workspace quarantine layer before prompt-injection defenses inside the model. The concrete build is a pre-execution gate that classifies incoming email, downloaded files, web content, and local skill files by trust level, strips instruction-like content from low-trust sources, and requires explicit approval before those sources can influence tool calls or credential access. Teams can test it in sandboxes with seeded malicious documents and long-context sessions.

This is now an operational requirement for high-privilege agents. ClawSafety runs 2,520 trials across 120 attack scenarios and reports attack success rates from 40.0% to 75.0% depending on model, with skill-file injection averaging 69.4% and scaffold choice changing outcomes for the same model. The supporting case study on Claude Code adds a related exposure path: minified JavaScript bundles can leak prompts, endpoints, telemetry names, and environment variables in plain text, with 147,992 strings extracted from a 13MB bundle in 1.47 seconds. If agent builders assume hostile instructions and internal logic are both easy to recover, the safer default is to isolate untrusted content before the agent reads it and to move sensitive logic out of client-visible code.

### Evidence
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md): Benchmark quantifies prompt-injection success across vectors, models, and scaffolds in high-privilege agents.
- [Obfuscation is not security – AI can deobfuscate any minified JavaScript code](../Inbox/2026-04-01--obfuscation-is-not-security-ai-can-deobfuscate-any-minified-javascript-code.md): Case study shows minified client-visible JavaScript exposes prompts and internal details to fast extraction.
