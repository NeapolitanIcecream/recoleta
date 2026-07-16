---
kind: ideas
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
run_id: de086bd3-22dd-425a-8e8b-efdc6623baee
status: succeeded
topics:
- coding agents
- repository reasoning
- agent memory
- software verification
- prompt injection
- AI security
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-reasoning
- topic/agent-memory
- topic/software-verification
- topic/prompt-injection
- topic/ai-security
language_code: en
pass_output_id: 207
pass_kind: trend_ideas
upstream_pass_output_id: 206
upstream_pass_kind: trend_synthesis
---

# Coding Agent Control Layers

## Summary
Reusable setup memory, repository-structure checks, and prompt-injection command tests are ready for small trials in coding-agent workflows. The common pattern is simple: keep the main coding model fixed, add a narrow control layer around the work it already does, and measure whether the layer improves pass rate, file selection, or command safety.

## Repository setup memory with container rollback and independent pass/fail checks
Teams that use coding agents on many repositories can start by saving failed setup repairs as structured records, then retrieving them during future setup runs. A useful record would include the error text, package or toolchain signals, the repair commands, the repository type, and the later pass/fail result. The agent should try retrieved fixes inside a disposable container snapshot, roll back failed installs, and keep the final verdict separate from the agent that attempted the repair.

SETUPX gives this workflow a concrete shape. Its eXPerience Units store setup signals, plain-language guidance, executable actions, and telemetry; retrieval combines similarity, historical success, and an LLM reranker; Docker snapshots support rollback; and a Prosecutor-Judge check separates failure evidence from the final verdict. On 100 Python repositories from EnvBench, SETUPX with memory reports a 92% pass rate, 10 points above its no-memory variant. CODESKILL points in the same operational direction for broader coding tasks: compact Markdown skills with trigger conditions and action steps improved average success for frozen coding policies across EnvBench, SWE-Bench Verified, and Terminal-Bench 2.

A cheap trial would run this only on repository bootstrapping in CI or developer onboarding. The pass condition is concrete: documented commands and tests run in a clean container, the repair history is reusable, and harmful dependency changes can be rolled back.

### Sources
- [SetupX: Can LLM Agents Learn from Past Failures in Functionality-Correct Code Repository Setup?](../Inbox/2026-05-25--setupx-can-llm-agents-learn-from-past-failures-in-functionality-correct-code-repository-setup.md): SETUPX describes XPUs, Docker rollback, Prosecutor-Judge verification, and the 92% pass rate with a 10-point memory gain.
- [SetupX: Can LLM Agents Learn from Past Failures in Functionality-Correct Code Repository Setup?](../Inbox/2026-05-25--setupx-can-llm-agents-learn-from-past-failures-in-functionality-correct-code-repository-setup.md): The paper abstract defines the XPU representation, LIFO Docker snapshot stack, and Prosecutor-Judge Verification Protocol.
- [CODESKILL: Learning Self-Evolving Skills for Coding Agents](../Inbox/2026-05-25--codeskill-learning-self-evolving-skills-for-coding-agents.md): CODESKILL reports compact skill-bank management and pass-rate gains for frozen coding agents.

## Repository-structure pre-pass for multi-file issue fixes
Coding-agent evaluations should include a check for whether the agent found the files that explain the issue before it edits code. A practical workflow is to require a repository-structure pre-pass for issue tickets that mention imports, runtime targets, configuration constants, generated files, or cross-module behavior. The pre-pass should produce a short map of likely call paths, re-exports, configuration sources, and tests before the fix attempt begins.

RepoMirage shows why this is worth testing. It keeps SWE-Bench Verified issue behavior the same, then changes how the relevant context is exposed through dependency indirection, runtime-target masking, and externalized constants. Across eight models, average resolved rate falls from 66.80% to 49.78%, while accessed files rise from 4.77 to 13.24. On RepoMirage-Extend, average success is 25.25%, with multi-file issue resolution at 17.86% and proxy-chain recovery at 17.19%. The file-access analysis also shows a narrow search pattern in solved cases: GPT-5 inspected one file in 53.8% of solved cases and no more than three files in 88.0%.

The first adoption point is an internal benchmark gate. Take a set of real tickets, add behavior-preserving perturbations that move constants, mask runtime targets, or insert proxy chains, and compare agent outcomes with and without the structure pre-pass. The useful metric is whether the agent identifies the same task-relevant files under both layouts.

### Sources
- [RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations](../Inbox/2026-05-25--repomirage-probing-repository-context-reasoning-in-code-agents-with-perturbations.md): RepoMirage reports the perturbation method, file-access findings, score drops, and low results on explicit multi-file tasks.
- [RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations](../Inbox/2026-05-25--repomirage-probing-repository-context-reasoning-in-code-agents-with-perturbations.md): The abstract defines repository context reasoning and describes the large drop on RepoMirage-Extend.
- [RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations](../Inbox/2026-05-25--repomirage-probing-repository-context-reasoning-in-code-agents-with-perturbations.md): The paper explains why issue resolution often requires tracing calling relationships and execution constraints across files.

## Prompt-injection regression tests for coding assistant shell commands
Security teams can test coding assistants as command executors with developer privileges. The concrete test is to seed normal repositories with poisoned coding-rule files, skill files, MCP configuration, or documentation comments, assign ordinary development tasks, and record every shell command, file edit, network access, and credential path the assistant touches.

AIShellJack provides a starting test design. The study added poisoned coding-rule files to normal tasks and measured Cursor v1.2.2 and GitHub Copilot v1.102 on five real codebases. Across 314 payloads covering 70 MITRE ATT&CK techniques, reported attack success rates ranged from 41% to 84%. The paper also maps injection sources beyond repository files, including shared skills, MCP servers, IDE settings, websites, APIs, and messaging tools. The cited vulnerabilities include cases where execution happened before trust dialogs or bypassed command allowlists.

A useful internal control is a regression suite that fails when an assistant executes commands unrelated to the user task, reads credential files, changes authentication files, installs persistence, or sends data to unapproved endpoints. The suite should run against tool upgrades and model-backend changes, because the risk sits in the full assistant workflow, not only in the model response.

### Sources
- [How Agentic AI Coding Assistants Become the Attacker's Shell](../Inbox/2026-05-25--how-agentic-ai-coding-assistants-become-the-attacker-s-shell.md): The AIShellJack summary reports the payload set, tested tools, attack success rates, MITRE coverage, injection sources, and CVE evidence.
- [How Agentic AI Coding Assistants Become the Attacker's Shell](../Inbox/2026-05-25--how-agentic-ai-coding-assistants-become-the-attacker-s-shell.md): The paper gives concrete CVE examples and explains that hidden markdown in an imported skill file can trigger credential exfiltration.
- [How Agentic AI Coding Assistants Become the Attacker's Shell](../Inbox/2026-05-25--how-agentic-ai-coding-assistants-become-the-attacker-s-shell.md): The paper explains why autonomous command execution, file editing, and network access increase the impact of prompt injection.
