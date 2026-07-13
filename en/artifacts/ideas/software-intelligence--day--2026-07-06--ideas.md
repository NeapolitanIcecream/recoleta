---
kind: ideas
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
run_id: 9a4af824-3d39-421f-ba28-ab7b2a0cfc95
status: succeeded
topics:
- coding agents
- software engineering
- agent evaluation
- open-source software
- agent security
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/open-source-software
- topic/agent-security
language_code: en
pass_output_id: 309
pass_kind: trend_ideas
upstream_pass_output_id: 308
upstream_pass_kind: trend_synthesis
---

# Coding Agent Repository Controls

## Summary
Repository owners can add controls at the points where coding agents already create operational load: overlapping pull requests, mixed-trust tool data, and evaluations that miss long-running repository work. The evidence supports small, testable changes inside existing GitHub and CI workflows.

## Pre-merge conflict checks for concurrent agent pull requests
Maintainers using coding agents should add a queue or check that replays merges between open agent-authored pull requests before review. The check can run `git merge-tree` across co-active PR pairs, post a conflict summary, and block low-priority agent PRs that touch the same source files until the first PR lands or closes.

The operational pain is visible in GitHub data. In AIDev-pop, exact temporal overlap appeared in 40.2% of repositories with agent-authored PRs and covered 79.4% of agent PRs. Merge replay found textual conflicts in 19.8% of same-agent pairs and 41.7% of cross-agent pairs, with most conflicted files in source code. A first test is simple: run the check for two weeks on repositories where agents open multiple PRs, then compare conflict comments, CI reruns, and maintainer rebase work against the prior two weeks.

### Evidence
- Document 1776: Reports overlap rates for agent-authored pull requests and merge replay conflict rates across AIDev-pop.
- Document 1776: States the sampled merge replay result and that most conflicts were source-code changes.
- Document 1759: Shows maintainers perceive other people’s AI-generated code as harder to maintain, even without broad deterioration in observable repository signals.

## Typed trust boundaries for GitHub comments and tool responses used by coding agents
Teams running coding agents on issues, pull requests, and CI output should treat every external text field as untrusted data with a separate typed envelope for trusted metadata. A practical build is a tool-response adapter that passes author, resource ID, tool name, and execution history through parser-owned fields, while comments, logs, web text, and model-visible excerpts remain quoted data. The same adapter should reject or escape JSON-like delimiters, fake tags, spoofed tool-output blocks, and copied UI identifiers inside untrusted fields.

This belongs in the agent runtime, not only in prompt rules. The agent data injection paper shows attackers can place delimiters, JSON-like structure, tags, or spoofed metadata inside untrusted content so the model reads it as trusted agent data. The reported attacks include spoofed GitHub issue comments and fake tool responses for coding agents, with remote code execution and supply-chain paths shown on Claude Code, Codex, and Gemini CLI. A cheap validation pass is to replay the paper’s delimiter and metadata-spoofing cases against the team’s own GitHub issue reader and PR review tools, then fail the build if untrusted text can alter trusted fields.

### Evidence
- Document 1770: Defines agent data injection, describes spoofed GitHub comments and fake tool responses, and reports attack success rates.
- Document 1770: Reports remote code execution and supply-chain attack paths on coding agents and identifies missing isolation between trusted and untrusted data.
- Document 1770: Explains the difference between trusted metadata and untrusted content in agent inputs.

## Repository-agent evaluation runs with rebuild verification and long-horizon progress logs
Engineering teams choosing a coding agent should run candidate agents inside rebuildable repository sandboxes with real tests, hidden judge checks, and progress logs across multi-hour work. The evaluation should record whether the agent searched the right files, localized the fault, produced a patch, verified it, recovered after failure, and gave an honest status when it stalled. This can start with five to ten internal bugs that already have known fixes and test cases.

Several new results point to the same evaluation shape. KAT-Coder-V2.5 reports AutoBuilder raising executable environment construction success from 16.5% to 57.2% and filtering trajectories by exploration, localization, patch quality, verification, recovery, and honesty. EdgeBench measures agents over 12-hour executable tasks and finds that early progress can predict later performance with high fit. EvoAgentBench adds a transfer check by linking tasks through reusable procedures for search, debugging, and verification, while current automatic memory methods still show negative-transfer cases. A useful internal scorecard should include environment rebuild success, pass/fail outcome, time-to-first-valid-test, recovery after failed patches, and whether any stored procedure helped or hurt a later task.

### Evidence
- Document 1775: Describes executable environment construction, trajectory filtering, and reported AutoBuilder success gains.
- Document 1768: Describes 12-hour executable tasks, progress curves, and long-run agent evaluation design.
- Document 1766: Describes procedure-transfer testing through Ability units and reports mixed automatic transfer with negative-transfer cases.
