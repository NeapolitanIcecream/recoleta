---
kind: ideas
granularity: day
period_start: '2026-07-08T00:00:00'
period_end: '2026-07-09T00:00:00'
run_id: 32dafdd4-8f69-4566-b517-7eb6bfa3b607
status: succeeded
topics:
- coding agents
- agent security
- MCP
- bug reports
- software benchmarks
- production automation
- AI personalization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-security
- topic/mcp
- topic/bug-reports
- topic/software-benchmarks
- topic/production-automation
- topic/ai-personalization
language_code: en
pass_output_id: 313
pass_kind: trend_ideas
upstream_pass_output_id: 312
upstream_pass_kind: trend_synthesis
---

# Coding Agent Control Loops

## Summary
Coding-agent adoption is running into three concrete operating problems: untrusted repositories can steer agents into running attacker code, recurring incidents keep paying full inference cost, and issue text written for humans can leave repair agents guessing. The most practical changes are execution gates for repo and MCP tool use, promotion rules that convert verified incident traces into playbooks, and issue templates that collect executable repair evidence upfront.

## Execution gate for untrusted repository commands and MCP tool calls
Security teams testing Claude Code, Codex, or MCP-based agents should add a pre-execution gate before any command, binary, script, file path, URL, database query, or terminal tool call that came from repository text or user-controlled input. The gate can be simple: label the source of each proposed argument, block auto-approved execution for unsigned local binaries and repo-suggested scripts, require a human approval reason for first-time commands, and log the exact repository file or MCP parameter that introduced the instruction.

The need is concrete. One proof of concept modified a local `geopy` repository with normal-looking project guidance, a `security.sh` script, a malicious `code_policies` binary, and a decoy source file. Claude Code and Codex inspected the files, accepted the script as safe, and ran the malicious binary in auto-mode or auto-review. The reported affected setups included several Claude Code CLI versions and Codex CLI 0.142.4.

MCP servers show the same class of failure at tool boundaries. SpellSmith’s MCP study found 43 taint-style cases among 53 vulnerability reports, with most triggered during tool invocation. Its mitigation rewrites tool descriptions with security guidance and adds a reflection step before final execution. A practical first test is to run existing agents against a small repo fixture with benign-looking README guidance that asks for a script execution, then repeat with the gate enabled and check whether the agent can still inspect code while losing the path to automatic execution.

### Sources
- Document 1794: Documents the repository-based remote code execution proof of concept against Claude Code and Codex auto-approved modes.
- Document 1799: Reports that most collected MCP server vulnerabilities were taint-style issues and describes security-aware tool descriptions plus pre-invocation reflection.

## Promotion rules that convert verified incident-agent traces into playbooks
Ops teams using agents for incident triage should keep successful agent traces as automation material. A buildable version records tool-call order, branch conditions, schemas, dependencies, parameters, and human-approval points after each verified incident run. Recurring patterns can then be promoted into a hybrid playbook after repeated safe success, and into deterministic execution after higher consistency, regression tests, and human review.

The payoff is cost and repeatability on recurring incidents. In the reported cloud network operations deployment, deterministic executions reached about 45% after eight months. The final mix was about 45% deterministic, 30% hybrid, and 25% fully agent-orchestrated. Per-incident agent cost fell by more than 70% while incident volume roughly doubled, and mean time to resolution fell from hours to minutes.

The cheap adoption check is one incident family, such as a known network alarm or routine service degradation. Capture 20 to 30 successful agent runs, cluster the action sequences, and generate one candidate playbook with explicit demotion rules for failed checks, safety violations, or acceptance-test regressions. The team learns whether the trace data is complete enough before committing to a broader incident automation program.

### Sources
- Document 1800: Describes trace extraction, promotion and demotion criteria, execution types, and production results for cloud network incident handling.

## Issue templates that collect executable evidence for repair agents
Engineering teams assigning bugs to repair agents should update issue templates to request agent-useful fields: a minimal reproduction script, expected behavior, observed error, relevant source snippet or API contract, suspected file or module, and any proposed fix direction. The template should also discourage long narrative reports that mix speculation, history, and unrelated discussion into the initial task.

The evidence points to specific fields. In 433 SWE-bench Verified issues attempted by 87 agents, fix suggestions had the largest positive association with success, with odds ratio 3.61. Repository source code, reproduction scripts, and naming the eventual patch file were also linked to higher repair odds. Longer reports correlated with lower repair odds, with odds ratio 0.49 for a one-standard-deviation increase in log report length.

A small pilot can measure the change without altering the whole tracker. Route a subset of new bugs through the revised template, run the same repair agent on matched old-style and new-style reports, and compare valid patch rate, time to first plausible patch, and number of repository-search steps. If reporters cannot provide a fix suggestion, the template can ask for the failing invariant or the file most likely to own the behavior.

### Sources
- Document 1797: Reports the SWE-bench Verified study linking fix suggestions, reproduction scripts, source-code hints, localization, and shorter reports with repair-agent success.
