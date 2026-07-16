---
kind: ideas
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
run_id: 224f9410-1c39-460a-b54c-e78dbcbcb073
status: succeeded
topics:
- coding agents
- software engineering
- program repair
- agent governance
- recommender systems
- security evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/program-repair
- topic/agent-governance
- topic/recommender-systems
- topic/security-evaluation
language_code: en
pass_output_id: 283
pass_kind: trend_ideas
upstream_pass_output_id: 282
upstream_pass_kind: trend_synthesis
---

# Coding Agent Control Gates

## Summary
Coding-agent adoption now has several concrete control points: reviewable agent configuration files, measured limits on test execution, and multi-layer validation for security repairs. The common operational issue is that agent work often looks successful inside its own loop while leaving weak provenance, high execution cost, or unsafe production changes.

## Versioned agent configuration files with lockfiles and permission checks
Teams using Claude Code, Cursor, Copilot instructions, Aider, Codex, or Windsurf should put agent rule files under the same kind of change control used for CI and deployment policy. A practical first build is a small CI gate that hashes agent config files, writes a lockfile, requires review on prompt or tool-permission changes, and blocks risky shell commands or write paths before an agent run starts.

Rel(AI)Build gives a concrete shape for this control layer. It treats prompts, permissions, and workflow state as managed artifacts with SHA-256 addressing, HMAC-stamped lockfiles, hash-chained JSONL audit logs, permission tiers, and pre-tool checks. The corpus result explains why this is worth doing: in 10,008 public GitHub repositories, 10.1% of tracked agent config paths were exact duplicates after fork adjustment, and 75.5% of duplicate clone pairs crossed organization boundaries. These files are already moving like shared software components, but many teams still review them like ordinary markdown.

### Sources
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build describes hashes, lockfiles, audit logs, permission tiers, pre-tool checks, seven IDE targets, and the GitHub corpus findings on duplicated agent configs.
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): The abstract states the prevalence study details and the cross-organization duplication rate for agent configuration files.

## Execution budgets for LLM program repair agents
Engineering teams running repair agents can add a cheap execution policy before building more test infrastructure: start with no execution or a small quota, require the agent to justify each test run, and log whether the run changed localization, patch content, or official evaluation outcome. The goal is to reserve expensive repository setup and repeated test runs for cases where execution changes the decision.

The SWE-bench execution study gives a usable baseline for this policy. Across 7,745 public traces, agents ran tests 8.8 times per task on average. In 3,000 controlled repair attempts, commercial agents gained only 1.25 percentage points in resolve rate under unrestricted execution, with no statistically significant gap. Claude Code resolved 63% without execution and 64% with unrestricted execution, while the no-execution setting saved 56% of tokens and 48% of wall-clock time. A team can test this internally by replaying recent agent tasks under prohibited, quota-1, quota-3, and unrestricted modes, then comparing resolve rate, token use, elapsed time, and mismatches between agent-run validation and the project’s real CI.

### Sources
- [To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair](../Inbox/2026-06-25--to-run-or-not-to-run-analyzing-the-cost-effectiveness-of-code-execution-in-llm-based-program-repair.md): The summary reports the trace analysis, controlled execution modes, resolve-rate gap, token and wall-clock savings, and validation mismatch findings.
- [To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair](../Inbox/2026-06-25--to-run-or-not-to-run-analyzing-the-cost-effectiveness-of-code-execution-in-llm-based-program-repair.md): The paper excerpt states that prohibited execution saves 56–62% tokens and 48–54% wall-clock time on Claude Code and removes per-repository test environment maintenance.

## Layered Terraform repair gate using Checkov, terraform plan, and plan comparison
Cloud security teams using LLMs to repair Terraform findings should add a layered merge gate for generated patches. The gate should rerun the targeted Checkov check, run full Checkov, run `terraform validate`, run `terraform plan`, compare the JSON plan with the original security intent, and send ambiguous plan changes to a human reviewer with labels such as intended fix, deceptive fix, or invalid repair.

TerraProbe shows why a single scanner-cleared result is too weak for Terraform. In its first-pass repair study, Gemini cleared the targeted Checkov finding in 83.3% of repairs, but full Checkov cleanliness fell to 10.4%. Among plan-compared real-world TerraDS repairs, 71.4% were deceptive fixes that passed automated checks while leaving the targeted vulnerability in place. IAM cases were especially concrete: wildcard `Resource` grants were preserved in all nine CKV2_AWS_11 deceptive-fix cases. A team can start with the highest-risk Checkov rules and measure how often scanner-cleared LLM patches change the actual cloud plan in the intended way.

### Sources
- [Empirical Software Engineering TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform](../Inbox/2026-06-25--empirical-software-engineering-terraprobe-a-layered-oracle-framework-for-detecting-deceptive-fixes-in-llm-assisted-terraform.md): TerraProbe describes the five oracle layers and reports the gap between targeted Checkov removal, full Checkov cleanliness, valid plans, and deceptive fixes.
- [Empirical Software Engineering TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform](../Inbox/2026-06-25--empirical-software-engineering-terraprobe-a-layered-oracle-framework-for-detecting-deceptive-fixes-in-llm-assisted-terraform.md): The paper excerpt describes plan-level evaluation and the purpose of distinguishing intent-aligned repairs from scanner-passing false successes.
