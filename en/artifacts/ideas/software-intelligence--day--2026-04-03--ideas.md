---
kind: ideas
granularity: day
period_start: '2026-04-03T00:00:00'
period_end: '2026-04-04T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- coding-agents
- evaluation
- software-engineering
- security
- benchmarks
- competitive-programming
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/software-engineering
- topic/security
- topic/benchmarks
- topic/competitive-programming
language_code: en
pass_output_id: 13
pass_kind: trend_ideas
upstream_pass_output_id: 12
upstream_pass_kind: trend_synthesis
---

# Repository Agent Safety Gates

## Summary
Coding-agent evaluation is moving into real repository state, real user failure traces, and real extension security checks. The clearest near-term changes are an internal replay suite built from support failures, a stateful pull-request sequence benchmark with repository health scoring, and a quarantine step for third-party skills before they reach developer machines or CI.

## Repository-grounded replay suites from coding-agent support failures
Teams adopting coding agents for repository work need a regression harness built from their own failure history, not only benchmark prompts. ABTest shows a practical recipe: take confirmed user-reported failures, abstract them into reusable workflow patterns and action types, then replay them as executable tests inside real repositories with expected file states and trace checks. The numbers justify treating this as a product requirement. From 400 confirmed failures, the paper generated 647 repository-grounded cases and surfaced 642 new true anomalies across Claude Code, Codex CLI, and Gemini CLI.

A concrete build is an internal replay suite that starts with issue tracker tickets, Slack incident reports, and support escalations for one coding agent deployment. The first version does not need model-based fuzzing. It can cover a narrow set of recurring workflow breaks such as editing the wrong file, leaving partial changes after rollback, claiming success with stale workspace state, or running the wrong command sequence. Run that suite on every agent upgrade, every tool-permission change, and every scaffold change. For teams already exposing agents to production repositories, this is a cheaper gate than waiting for user reports to pile up in live use.

### Evidence
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): ABTest converts 400 confirmed failure reports into 647 executable repository-grounded cases and confirms 642 new anomalies across major coding agents.
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): The paper describes practical workflow failures such as wrong-file edits and unintended side effects during real repository interaction.

## Stateful pull-request sequence evaluation with repository health scoring
Evaluation stacks for coding agents now need multi-PR sequences with persistent state and repository health checks. SWE-STEPS gives a clear reason. When evaluation moves from isolated pull requests to dependent sequences, reported success drops sharply: Claude Sonnet 4.5 falls from 66.25% to 43.75% on one split, and Gemini 3 Flash falls from 56.52% to 36.59%. The paper also reports worse repository health under agent-written code, including higher cognitive complexity and technical debt than human baselines.

A concrete workflow change is to add one stateful track beside existing single-task benchmarks. Start with a small chain of historical pull requests from one active repository, preserve workspace state across steps, and score both functional correctness and post-change maintainability signals such as static analysis warnings or complexity growth. This kind of test is useful for platform teams deciding whether an agent can handle backlog work over several days, and for buyers comparing agents whose leaderboard scores come from clean resets that remove the consequences of earlier mistakes.

### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): SWE-STEPS reports that isolated PR evaluation can overstate success by up to 20 points and gives concrete drops under continuous evaluation.
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): The paper states that previous inefficient or buggy code causes spillover effects and degrades repository health through higher complexity and technical debt.

## Skill-ingestion quarantine for coding-agent documentation and templates
Organizations loading third-party skills into coding agents need a skill-ingestion gate that inspects documentation examples and configuration templates before installation. The new supply-chain paper shows why this belongs in the setup path. Its attack hides malicious logic inside ordinary-looking skill documentation so the agent copies and executes it during normal setup or coding work. Across 1,070 adversarial skills, bypass rates reach 11.6% to 33.5% across four frameworks and five models. Static analysis blocks most attacks, but 2.5% still evade both static checks and model alignment, and the authors report four confirmed vulnerabilities.

A concrete build is a quarantine step for skills and MCP-style extensions: parse SKILL.md and related docs, extract executable snippets and config fragments, flag network destinations and shell commands, and require a clean isolated run before the skill can touch a developer workstation or CI secret scope. Teams can start with marketplace imports and high-permission internal skills. The immediate value is reducing a class of attacks that enters through examples and templates developers often treat as harmless reference text.

### Evidence
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): The paper documents documentation-driven poisoning of coding-agent skills with measured bypass rates across frameworks and models.
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): The abstract states that skill documentation functions as operational directives with system-level privilege implications for host compromise.
