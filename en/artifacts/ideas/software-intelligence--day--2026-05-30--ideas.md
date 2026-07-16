---
kind: ideas
granularity: day
period_start: '2026-05-30T00:00:00'
period_end: '2026-05-31T00:00:00'
run_id: de086bd3-22dd-425a-8e8b-efdc6623baee
status: succeeded
topics:
- agent runtime
- autonomy governance
- workflow evaluation
- coding agents
- model routing
- deterministic validation
tags:
- recoleta/ideas
- topic/agent-runtime
- topic/autonomy-governance
- topic/workflow-evaluation
- topic/coding-agents
- topic/model-routing
- topic/deterministic-validation
language_code: en
pass_output_id: 217
pass_kind: trend_ideas
upstream_pass_output_id: 216
upstream_pass_kind: trend_synthesis
---

# Operational controls for workplace agents

## Summary
Agent deployments are moving into ordinary operations work: scheduled runs, secrets, sandboxes, approvals, traces, and repeatable workflow tests. The most practical moves are small control layers around existing coding agents, recipe-based acceptance tests for personal agents, and ADR drafts that keep human approval before file writes.

## Approval and audit controls for scheduled coding agents
Teams using Claude Code, Codex, OpenCode, or Cursor can treat each scheduled agent as a named process with an owner, allowed tools, secret scopes, expiry time, approval rules, and a kill switch. Lite-Harness already gives a concrete starting point: one self-hosted server, an OpenCode-compatible API, cron runs, vault keys, sandboxes, persistent sessions, and an Inbox UI for human approval before actions such as sending LinkedIn messages.

The missing piece to add around that server is a small manifest and audit layer. Every run should answer four questions without reading raw logs: who authorized the agent, which capability or secret allowed the action, which approval unblocked it, and how to stop or expire it. Autonomy Kernel gives the clean design target here: actions trace back to one principal and one authorization path, with execution, identity, authority, communication, and auditing handled below the agent.

A useful first test is a two-agent pilot inside one engineering team: one code-maintenance agent and one outreach or triage agent. Give each a manifest, require approval for external side effects, and review a week of run records for missing owner, missing grant, stale secret, or unreviewed action.

### Sources
- [Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)](../Inbox/2026-05-30--show-hn-lite-harness-self-hosted-cursor-agents-use-claude-code-opencode.md): Lite-Harness provides scheduled agent runs, secrets, sandboxes, persistent sessions, and human approval routing.
- [Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)](../Inbox/2026-05-30--show-hn-lite-harness-self-hosted-cursor-agents-use-claude-code-opencode.md): The example deployment shows cron scheduling, vault keys, a sandbox check, a test run, and approval before each send.
- [A case for an Autonomy Kernel](../Inbox/2026-05-30--a-case-for-an-autonomy-kernel.md): Autonomy Kernel defines the runtime responsibilities: execution, identity, authority, communication, auditing, stoppability, and traceable authorization.

## Recipe-based acceptance tests for personal-agent workflows
Teams deploying personal agents for calendar, email, reports, travel, finance, or web tasks need acceptance tests that run the whole configuration, including prompts, model choice, tools, memory, delegation, safety behavior, latency, and traces. HermesBench is a usable pattern: it evaluates complete Hermes configurations across 27 recipes, publishes a baseline score of 78.2, and links results to scenario definitions, score axes, deterministic checks, closure decisions, and redacted timelines.

The practical build is a local recipe pack for the workflows a team actually allows. A calendar recipe can check that the agent asks before moving an external meeting. A finance recipe can reconcile extracted invoice lines against the printed total. A report recipe can require source links and flag unsupported claims. Dimensional Design supports this shape by putting predictive steps behind deterministic pass-fail gates where exactness matters, with small recorded human checks where software cannot verify the output.

Start with five recipes tied to real failures or risky side effects. Save artifacts for each run, including prompt, model/provider, tools, trace, pass-fail checks, and reviewer notes. The score matters less than whether a maintainer can inspect why a run passed, failed, or needed a human decision.

### Sources
- [Show HN: HermesBench – workflow reliability evals for personal AI agents](../Inbox/2026-05-30--show-hn-hermesbench-workflow-reliability-evals-for-personal-ai-agents.md): HermesBench evaluates complete agent configurations with recipes, traces, deterministic checks, and a public baseline across 27 workflows.
- [Show HN: HermesBench – workflow reliability evals for personal AI agents](../Inbox/2026-05-30--show-hn-hermesbench-workflow-reliability-evals-for-personal-ai-agents.md): The site describes visible limits, redacted traces, score axes, and a single-recipe quick-start path for current configurations.
- [The Manifesto for Dimensional Design](../Inbox/2026-05-30--the-manifesto-for-dimensional-design.md): Dimensional Design argues for deterministic pass-fail gates and small recorded human review around AI outputs that need exactness.

## Architecture Decision Record drafts generated from issue analysis
Engineering teams can add an ADR draft step to architecture-labeled GitHub issues or Jira tickets before implementation starts. arch-decision shows the workflow: read the request, inspect the codebase with parallel agents, identify constraints and prior art, propose options, build a trade-off table, wait for approval, write the ADR, and link it back to the source issue.

This targets a specific source of technical debt: teams skip ADRs because a senior engineer may spend 2–4 hours researching the codebase, comparing approaches, and writing the decision record. The reported refinedev/refine run found relevant prior art, identified a package constraint, and recommended an `onParse` callback scoped to the antd wrapper; a later community PR used the same callback name, scope, and placement, according to the source.

The adoption test is simple. Run the tool on ten closed issues that should have had ADRs, hide the merged solution from the reviewer, and ask a staff engineer whether the generated options and recommendation would have improved the original review. Keep the approval gate mandatory, and store rejected drafts as useful evidence about where the agent missed project context.

### Sources
- [Arch-Decision – A multi-agent architecture tool for Claude Code](../Inbox/2026-05-30--arch-decision-a-multi-agent-architecture-tool-for-claude-code.md): arch-decision describes the ADR workflow, eight phases, parallel codebase exploration, generated options, a synthesizer, and a required human approval gate.
- [Arch-Decision – A multi-agent architecture tool for Claude Code](../Inbox/2026-05-30--arch-decision-a-multi-agent-architecture-tool-for-claude-code.md): The refinedev/refine case reports a recommendation that matched a later community PR in callback name, scope, and placement.
