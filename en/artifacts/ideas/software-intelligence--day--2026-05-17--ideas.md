---
kind: ideas
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
run_id: de413610-9807-4db4-a597-b3516b40c62a
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- vulnerability repair
- tool calling
- code review
- legacy modernization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/vulnerability-repair
- topic/tool-calling
- topic/code-review
- topic/legacy-modernization
language_code: en
pass_output_id: 159
pass_kind: trend_ideas
upstream_pass_output_id: 158
upstream_pass_kind: trend_synthesis
---

# Runtime Verification Loops for Coding Agents

## Summary
Teams testing coding agents should add acceptance gates that run the delivered system, preserve runtime evidence during repair, and train tool callers on API calls that have already executed. The useful work is in the verification loop around the agent: browsers, Docker runtimes, tests, crash inputs, safe inputs, and cached tool outputs become part of the work product.

## Dependency-aware runtime acceptance gates for agent-built applications
Coding-agent pilots need a release gate that starts the generated app, drives the UI, and records which requirement checks failed before a human reviews code. SaaSBench shows why this gate should cover setup and integration: its best reported result is 20.68% Pass@1, and more than 95% of failures occur before deep business logic, often in system setup, configuration, integration, premature stopping, or repeated debugging loops. WebGameBench gives a smaller pattern for user-facing behavior: a browser evaluator controls Chrome through Playwright and checks whether the delivered game actually handles inputs, rules, scoring, restart flow, and win/loss conditions.

A practical build is a harness around existing agent runs: normalize Docker startup, encode product requirements as dependency-ordered checks, use Playwright for UI behavior, and label blocked checks separately from direct failures. A team can trial it on ten recent agent-generated prototypes or internal tools. If the failed checks cluster around setup, integration, state handling, and visible behavior, the harness gives engineering managers a concrete acceptance signal before agent output enters normal code review.

### Sources
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench reports low Pass@1 and identifies setup, configuration, integration, premature stopping, and debugging loops as the dominant failure points.
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): WebGameBench evaluates delivered browser apps with Playwright-driven runtime checks and reports a large gap between usable and excellent delivery.

## Crash-and-safe execution loops for vulnerability repair agents
Security teams can wrap vulnerability-repair agents in a loop that compares crashing Proof-of-Concept inputs with nearby safe inputs, inserts probes near the fault, and asks the model to write a repair specification before editing source. ContraFix reports 84.0% resolution on 200 C/C++ SEC-Bench CVE instances, with a 27-point ablation gain attributed to contrastive runtime analysis. The mechanism is concrete: mutate the PoC, split executions into crashing and non-crashing groups, compare recorded state near the fault, then patch against a safety condition.

MemRepair points to the support layer this loop needs in a real repository: store prior fixes, security patterns, and failed-patch-to-success trajectories, then verify each candidate patch with vulnerability and regression tests. A product security team can start with recent fixed CVEs and store sanitizer reports, stack traces, probe logs, accepted patch summaries, failed patch summaries, CWE, language, and project identifiers. The verifier should accept only patches that compile and pass both the original crash case and the regression suite.

### Sources
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix uses paired crashing and safe executions, runtime probes, repair specifications, and verified patching; its ablation credits contrastive runtime analysis with a large gain.
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): MemRepair describes persistent repair memory and a Locator, Patcher, Verifier loop that runs vulnerability and regression tests before accepting edits.

## Executed-output datasets for internal MCP tool callers
Teams training agents to use internal MCP servers can generate tasks after successful API exploration has produced concrete outputs. FireFly filters real MCP tools, builds a directed tool graph, runs APIs, caches observed calls, and then writes natural-language tasks with answer schemas tied to those observed results. This order reduces infeasible tool trajectories and stale labels because the expected answer already exists in recorded execution data.

An internal version can start with stateless staging tools that have clear JSON schemas and no user-specific authentication. Each successful trajectory should store tool names, arguments, outputs, and data-flow edges. Cached responses can power offline evaluation and reinforcement learning without repeated live calls against changing services. A small check is enough to test fit: select twenty internal tools, explore multi-step calls, and measure how often cached outputs can support checkable tasks with exact field-level answers.

### Sources
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): FireFly builds verified tool-call data by executing real MCP APIs first, caching outputs, and generating tasks backward from observed results.
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): The paper states that FireFly produced 5,144 verified tasks across 240 servers and 993 tools and used cached execution for reproducible offline training.
