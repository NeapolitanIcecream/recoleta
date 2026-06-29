---
kind: ideas
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
run_id: de086bd3-22dd-425a-8e8b-efdc6623baee
status: succeeded
topics:
- coding agents
- software verification
- code review automation
- vulnerability repair
- agent evaluation
- program analysis
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-verification
- topic/code-review-automation
- topic/vulnerability-repair
- topic/agent-evaluation
- topic/program-analysis
language_code: en
pass_output_id: 213
pass_kind: trend_ideas
upstream_pass_output_id: 212
upstream_pass_kind: trend_synthesis
---

# Generated Code Quality Gates

## Summary
Coding-agent adoption is creating review queues, weak correctness evidence, and repeated security-fix work. The practical moves are narrower gates around low-risk diffs, executable checks for generated code when tests are missing, and repair memory for vulnerability agents.

## Risk-gated auto-landing for low-risk AI-generated diffs
Teams seeing AI-generated diff volume outrun reviewer capacity can build a narrow auto-review path for low-risk changes. RADAR gives a concrete pattern: classify diffs by source, exclude sensitive files and scopes, score each diff with a risk model, run LLM review, run deterministic checks, and auto-land only within configured thresholds. Meta reports more than 535K RADAR-reviewed diffs and more than 331K landed diffs, with lower revert and production-incident rates than non-RADAR diffs in the deployment. A small version can begin with codemods, generated runbook changes, or allowlisted owners, then compare revert rate, incident rate, and review wall time against ordinary review.

### Evidence
- [Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency](../Inbox/2026-05-28--automating-low-risk-code-review-at-meta-radar-risk-calibration-and-review-efficiency.md): RADAR combines source eligibility rules, Diff Risk Score thresholds, LLM review, deterministic checks, and production results for more than 535K reviewed diffs.
- [How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions](../Inbox/2026-05-28--how-coding-agents-fail-their-users-a-large-scale-analysis-of-developer-agent-misalignment-in-20574-real-world-sessions.md): Real coding-agent sessions show frequent constraint violations and low visible self-resolution, which supports review gates that preserve developer control.

## Specification-based execution checks for generated code without trusted tests
Developers often receive generated code before they have a trusted test suite. TRAILS points to a buildable check for that gap: extract behavior categories and preconditions from the natural-language spec, generate candidate inputs, execute the candidate program, and ask an LLM to judge each input-output pair against the spec without seeing the code. The method improved Matthew correlation coefficient over zero-shot chain-of-thought baselines on LiveCodeBench and CoCoClaNeL, though it used more tokens per task. This fits code-generation surfaces where accepting a wrong function is costly and a full test suite is unavailable, such as internal scripting tools, data transforms, and generated helper functions.

### Evidence
- [Inferring Code Correctness from Specification](../Inbox/2026-05-28--inferring-code-correctness-from-specification.md): TRAILS describes the spec-to-input-output checking workflow, reports MCC gains, and documents the higher token cost.

## CWE-keyed repair memory for vulnerability-fix agents
Security teams running agentic vulnerability repair can store repair attempts as reusable experience, keyed by CVE or CWE. EvoRepair records vulnerability analysis, repair strategy, trajectory analysis, reusable rules, and follow-up notes; it retrieves related experience before patching in Docker, then scores and updates the store after each attempt. The paper reports 93.47% on PATCHEVAL and 87.00% on SEC-bench with GPT-5-mini, ahead of 12 automated vulnerability repair baselines in its comparison. A practical pilot can start with one recurring weakness class, such as path traversal or command injection, and measure whether the agent repeats fewer failed edits and reaches passing security tests in fewer turns.

### Evidence
- [EvoRepair: Enhancing Vulnerability Repair Agents Through Experience-Based Self-Evolution](../Inbox/2026-05-28--evorepair-enhancing-vulnerability-repair-agents-through-experience-based-self-evolution.md): EvoRepair provides the cyclic repair-memory workflow and benchmark results for automated vulnerability repair.
- [Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs](../Inbox/2026-05-28--minimal-prompt-perturbations-lead-to-code-vulnerabilities-prompt-fragility-and-hidden-state-signals-in-coding-llms.md): The prompt-fragility study shows that small prompt changes can flip generated code from secure to vulnerable, supporting extra security checks around generated fixes.
