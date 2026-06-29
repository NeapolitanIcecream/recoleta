---
kind: ideas
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- coding-agents
- real-world-evaluation
- agent-harness
- developer-docs
- execution-based-validation
- security-testing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/real-world-evaluation
- topic/agent-harness
- topic/developer-docs
- topic/execution-based-validation
- topic/security-testing
language_code: en
pass_output_id: 103
pass_kind: trend_ideas
upstream_pass_output_id: 102
upstream_pass_kind: trend_synthesis
---

# Repository-Verified Agent Evaluation

## Summary
Coding-agent evaluation is moving closer to what teams can verify in their own repositories and pipelines. The most usable directions here are a commit-linked scorecard for kept code and review friction, a narrow `AGENTS.md` generation workflow tied to replay evals on recent PRs, and Node.js security triage that promotes only cases with executed proof-of-concept exploits.

## Commit-linked coding-agent scorecards for kept code and review friction
Teams shipping coding agents need a commit-aware scorecard that measures what developers kept, what they threw away, and how much review friction the agent created. SWE-chat gives the clearest case for this. Across about 6,000 real sessions, agent-written code survived at 50.3% overall, with collaborative sessions dropping to 44.1%. Users pushed back in 39% of turns, and vibe-coded work carried higher token cost, slower time per committed line, and more introduced vulnerabilities than collaborative work. Those numbers support a concrete product change: add post-session attribution and commit linkage to agent logs, then rank prompts, repos, and workflows by code survival, review churn, interruption rate, and security findings per committed line. The first users are teams already paying for coding agents across shared repositories and arguing about whether the output is helping. A cheap pilot is a GitHub app or CLI wrapper that links session traces to merged diffs and shows survival and rejection rates after one week of normal use.

### Evidence
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): Provides real-world metrics on code survival, user pushback, cost, and vulnerability rates across coding-agent sessions.
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): Confirms the dataset scale and the focus on linking session traces to what developers actually committed.

## Task-specific AGENTS.md generation with before-and-after PR replay
A short, task-specific `AGENTS.md` generator with an eval loop is now a practical build for teams using repository agents. The evidence is concrete enough to treat documentation as a performance input. In Augment's study, top files around 100 to 150 lines produced 10 to 15% gains, and a six-step workflow for adding a new integration cut missing wiring files from 40% to 10% while raising correctness by 25% and completeness by 20%. The same study also shows how easy it is to make things worse: architecture-heavy files pulled in about 80K irrelevant tokens and warning-only rules doubled PR time. A useful product here is not a generic doc writer. It is a repo scanner that drafts `AGENTS.md` around a narrow task class, inserts decision tables and small code examples from the local codebase, and runs before/after task replays on recent PRs. The first buyers are platform and developer productivity teams that already maintain internal setup docs but do not know which instructions agent harnesses actually read.

### Evidence
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): Gives the main quantitative findings on helpful and harmful AGENTS.md patterns, including workflow and token-loading effects.
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): Details the six-step workflow result that reduced missing wiring files and improved correctness and completeness.

## Proof-of-concept exploit confirmation for Node.js dependency triage
Node.js package security scanning can move one step closer to triage-ready output by generating and executing proof-of-concept exploits for suspected taint-style bugs. LLMVD.js is a clear signal that this is now buildable. The system confirms 84% of benchmark vulnerabilities, far above prior tools in the excerpt, and produced validated exploits for 36 of 260 recently released packages. Its pipeline matters as much as the headline number: it separates candidate finding, exploitability judgment, constraint inference, and execution-backed confirmation with class-specific oracles for path traversal, code injection, prototype pollution, and command injection. That supports a practical workflow change for registry operators, supply-chain security vendors, and larger application teams with many npm dependencies. Put exploit confirmation after static suspicion and before analyst review, so triage starts with packages that already have a reproducible artifact. A small validation step is to run this on a recent internal dependency set and measure how many scanner alerts can be collapsed into confirmed cases with runnable proofs.

### Evidence
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): Summarizes the execution-backed vulnerability confirmation pipeline and benchmark results.
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): Confirms the reported 84% benchmark confirmation rate and 36 validated exploits on recent packages.
