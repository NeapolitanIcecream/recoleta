---
kind: ideas
granularity: day
period_start: '2026-06-26T00:00:00'
period_end: '2026-06-27T00:00:00'
run_id: 2afc8250-7a5a-466d-9565-4e3834e87ff9
status: succeeded
topics:
- coding agents
- developer tools
- terminal UI
- ratchets
- regex
- code quality
tags:
- recoleta/ideas
- topic/coding-agents
- topic/developer-tools
- topic/terminal-ui
- topic/ratchets
- topic/regex
- topic/code-quality
language_code: en
pass_output_id: 285
pass_kind: trend_ideas
upstream_pass_output_id: 284
upstream_pass_kind: trend_synthesis
---

# Coding Agent Workflow Guardrails

## Summary
Agent-heavy development needs controls inside the daily workflow: counters for forbidden code patterns, persistent views over parallel agent sessions, and a narrow regex-engine test for Rust rule scanners that need lookaround.

## Ratchet checks for agent-created type-checker suppressions
Teams letting coding agents edit production code can add a ratchet check for suppressions such as `# pyrefly: ignore`. The check keeps the current count as the ceiling, fails when an agent adds a new instance, and leaves any increase to a planning agent or human reviewer with broader context.

This is a cheap guardrail because it avoids long style prompts and does not require an LLM judge. It fits places where a quick suppression may be valid in rare cases, yet harmful when used as the default path. A small trial can start with one rule in CI, report the current count, and block only new instances on agent-written branches.

### Sources
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): The summary describes ratchets as counters for forbidden patterns, notes coding-agent style violations, and names `# pyrefly: ignore` as a target case.
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): The source text explains the type-checker suppression example and the workflow where only a planning agent can raise the ratchet.

## Persistent terminal workspaces for parallel coding-agent sessions
Developers running several coding-agent CLIs can test a full-screen terminal workspace that keeps each agent, shell, open file, and working-tree diff visible in one place. The adoption test is practical: run two or three agents on separate tasks, restart the UI during a session, and check whether the operator can reattach without losing process state or track of file changes.

Workbench is a concrete example of this pattern. It uses a private tmux server for persistent agent and terminal panes, supports Claude Code, Gemini, Goose, OpenCode, and Cursor, and adds read-only file viewers plus a live git diff per workspace. The available evidence gives product details, not task-success benchmarks, so the first check should measure operator-visible failures: lost sessions, wrong workspace edits, missed diffs, and time spent switching between tools.

### Sources
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): The summary states that Workbench is a full-screen TUI for multiple coding-agent CLIs with tmux persistence, file viewers, shell panes, and git diff tracking.
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): The source text describes persistent sessions on a private tmux server and the live git changes tab.
- [Workbench: A TUI for parallel coding agents](../Inbox/2026-06-26--workbench-a-tui-for-parallel-coding-agents.md): The source text gives the saved state path and private tmux socket, supporting the persistence claim.

## Resharp benchmark for Rust rule scanners that need lookaround
Maintainers of Rust-based rule scanners can run a contained Resharp evaluation when regex rules need lookaround, especially for comment-style checks that are awkward to express through AST queries. The test should use the project’s real rules, record absolute runtime, rule count, hardware, and repeated-run variance, and include compatibility failures because Ratchets v0.4.0 is a breaking engine change.

The Ratchets report gives one useful starting point: after replacing Rust’s `regex` crate with Resharp, the author saw about a 15% speed gain on the Sculptor codebase with no other code changes. The more reliable reason to test is functional coverage, since the motivating gap was proper lookaround support for regex-based rules.

### Sources
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): The source text reports the Ratchets v0.4.0 engine change, the 15% speed gain on Sculptor, and the original need for lookaround assertions.
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): The source text explains why some rules remained regex-based, especially comment-style rules, and says Rust's `regex` crate lacked proper lookaround.
- [Speeding Up Ratchets with Resharp](../Inbox/2026-06-26--speeding-up-ratchets-with-resharp.md): The summary records the limits of the reported result: one codebase, no absolute runtime, no variance, and no hardware details.
