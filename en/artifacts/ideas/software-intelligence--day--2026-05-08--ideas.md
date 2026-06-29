---
kind: ideas
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
run_id: 33eb08d1-934b-4c2e-83b2-87023d83f83a
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- formal verification
- agent governance
- repository automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/formal-verification
- topic/agent-governance
- topic/repository-automation
language_code: en
pass_output_id: 137
pass_kind: trend_ideas
upstream_pass_output_id: 136
upstream_pass_kind: trend_synthesis
---

# Coding Agent Control Points

## Summary
Teams adopting coding agents can add three concrete controls now: a pre-edit abstention check for stale issues, a repository configuration audit for agent instructions and permissions, and a proof-focused lane for code that needs machine-checked correctness.

## Pre-edit abstention checks for stale and duplicate bug reports
Agent-maintained issue workflows should add a required pre-edit step that proves the reported bug still exists before the agent changes executable code. A cheap version is a small harness that asks the agent to reproduce the failure, inspect recent commits touching the same area, and return a signed “no code change” result when the repository already satisfies the issue.

FixedBench gives a concrete reason to test this. In already-fixed SWE-bench Verified tasks, agents still made unwanted executable-code edits in 35% to 65% of cases. A direct “Abstain or Fix” prompt improved abstention for some models, but it also caused heavy under-repair on partially fixed issues, with GPT-5.4 mini incorrectly abstaining 93.6% of the time in that setting. The check should therefore score two cases together: stale reports where the right result is no patch, and partial fixes where a patch is still needed.

The first users are teams letting agents open or update maintenance PRs from issue queues. The workflow change is small: require a reproduction note and a “why no edit is safe” path before the agent can push a code diff. Human reviewers still keep merge authority, which matches current GitHub evidence: in 29,585 AI-agent-related PRs, agent-approved PRs totaled only 14 and stayed below 0.1% per tool.

### Evidence
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench measures unwanted edits on already-fixed issues and shows the prompt tradeoff on partially fixed issues.
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): The paper frames stale and duplicate bug reports as a routine repository condition where agents should abstain.
- [Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles](../Inbox/2026-05-08--collaborator-or-assistant-how-ai-coding-agents-partition-work-across-pull-request-lifecycles.md): The PR lifecycle study shows humans almost always retain merge authority in AI-agent PR workflows.

## Repository configuration audits for coding-agent instructions, hooks, and permissions
Repositories using Claude Code, GitHub Copilot, Cursor, Gemini, OpenAI Codex, or AGENTS.md should maintain an agent configuration inventory in CI. The inventory should list context files, skills, subagents, commands, rules, settings, hooks, and MCP connections; record which files affect every session; and flag permissions or hooks that can run before human review.

The new GitHub configuration dataset shows that this is already ordinary repository material. It found 15,591 configuration artifacts across 4,738 repositories, with context files appearing in 4,463 repositories. These files are no longer side notes in a developer setup; they are part of how teams steer agents.

Security work points to the checks the inventory should run first. Subagent systems need bounded memory inheritance, role-scoped resource access, lifecycle controls, and safe termination rules. Runtime governance work adds a practical placement model: pre-action gates for blocked operations, action-time monitors for risky tool use, post-action auditors for trace review, and escalation routing when a policy cannot be decided automatically. A CI audit can start with static detection and move the high-risk items into runtime checks where the agent acts.

### Evidence
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): The dataset quantifies repository-level agent configuration artifacts across tools and configuration mechanisms.
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): The paper defines context files, skills, subagents, commands, rules, settings, hooks, and MCP configurations.
- [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](../Inbox/2026-05-08--when-child-inherits-modeling-and-exploiting-subagent-spawn-in-multi-agent-networks.md): The subagent security paper identifies memory inheritance, resource access, stale state, and termination-control vulnerabilities.
- [SARC: A Governance-by-Architecture Framework for Agentic AI Systems](../Inbox/2026-05-08--sarc-a-governance-by-architecture-framework-for-agentic-ai-systems.md): SARC specifies runtime enforcement sites for constraints inside agent execution.

## Proof-focused coding lanes for code with correctness obligations
Teams writing security-sensitive libraries, parsers, payment logic, or protocol code should separate ordinary code generation from proof work. A practical first build is an internal Rust/Verus lane for a narrow set of functions: the agent proposes code, a developer or verifier reviews the specification, and the system requires machine-checked proofs plus positive and negative tests before merge.

VeriContest shows why this should be scoped narrowly. GPT-5.5 reached 92.18% pass@1 on natural-language-to-code generation, then fell to 48.31% on specification generation, 13.95% on proof generation, and 5.29% end-to-end verified generation. All evaluated models stayed below 6% end-to-end. The gap is large enough that proof generation should be treated as its own review workload with dedicated failure reports, not as a hidden add-on to a passing test suite.

The useful adoption test is small: choose ten functions with clear preconditions and postconditions, require Verus checks, and track where the agent fails: missing specification, incomplete postcondition, invalid invariant, or wrong code. VeriContest’s use of Post2Exe and large negative test suites also gives a concrete pattern for catching weak specifications before they are trusted.

### Evidence
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest reports the benchmark composition and the large drop from ordinary code generation to verified generation.
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): The paper reports the pass@1 split across code, specification, proof, and end-to-end verified generation.
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): The content describes Verus specifications, executable Rust code, loop invariants, assertions, and proof structure.
