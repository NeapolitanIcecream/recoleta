---
kind: ideas
granularity: day
period_start: '2026-06-12T00:00:00'
period_end: '2026-06-13T00:00:00'
run_id: 16e62330-adbd-48dd-a14c-903ad1f0f166
status: succeeded
topics:
- coding agents
- agent harnesses
- AI workflow
- engineering judgment
- blockchain state
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-harnesses
- topic/ai-workflow
- topic/engineering-judgment
- topic/blockchain-state
language_code: en
pass_output_id: 253
pass_kind: trend_ideas
upstream_pass_output_id: 252
upstream_pass_kind: trend_synthesis
---

# Bounded Coding Agent Control

## Summary
Coding-agent work is moving toward smaller rule surfaces, narrower action sets, and scheduled human review. The useful changes are migration tools for agent configs, restricted command surfaces for safe local coding, and checkpoint prompts that force scope review during long AI sessions.

## MCP-backed scoped rule harness for team coding agents
Teams using Claude Code or similar agents can turn growing instruction files into scoped rule directories and an MCP server that exposes only the context needed for the current task. The concrete build is a migration and audit tool: scan a large `CLAUDE.md`, split rules by topic and project path, flag contradictory rules, then publish lookups such as `get_context(topic)` plus resources for verification status and budget.

The pain is easy to recognize: a single agent config becomes too long to remember, rules apply to projects where they do not belong, and teams have no clean update path for shared defaults. A small pilot can use one active repo, move project-specific rules into path-scoped files, and compare agent mistakes before and after the split. The check should look for rule conflicts, irrelevant context loaded into sessions, and failed verification steps, since the source example reports better behavior after contradictory rules stopped living in one file but gives no benchmark numbers.

### Evidence
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): Describes the move from a 1,800-line `CLAUDE.md` to scoped files and `keystone-mcp`, including context lookup, scaffolding, verify, and budget resources.
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): Shows the operational failure: the author could not remember rules in a large config, wrote contradictory rules, then split the file by topic.
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): Shows path-scoped activation for project- and language-specific rules, with the global file shrinking after irrelevant rules moved into repos and subtrees.

## No-shell Rust coding agent for constrained local changes
A constrained coding agent is practical for routine Rust work where shell access is the main adoption blocker. The concrete test is a Rust-only TUI agent that can edit files and run Rust-specific actions, while blocking arbitrary terminal commands. That gives maintainers a safer setting for small refactors, diagnostics, and test-driven edits on local machines.

Agent Joe is an early example: it removes shell access, narrows the action set to Rust operations, and is described as usable, while still behind Codex because its prompts are weaker and it lacks a plan mode. A useful next step is to add an explicit plan step before edits, then run the same issue set through Agent Joe and a general CLI agent. Track completed tasks, user interventions, unwanted command attempts, and failed `cargo` checks. The value comes from making the safety tradeoff visible enough for teams that currently avoid CLI agents on their own machines.

### Evidence
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): Summarizes Agent Joe as a Rust-only terminal coding agent with no shell access, fewer actions, and an admitted quality gap versus Codex.
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): The author states the tool only works with Rust, blocks shell access, reduces actions to Rust-specific ones, and lacks a plan mode.

## Thirty-minute goal review in AI-assisted coding sessions
AI coding sessions need a visible stop point when the user is still prompting after the original task has drifted. A lightweight implementation can sit in an IDE, terminal wrapper, or agent chat: capture the user’s stated goal at session start, pause the agent every 30 minutes, hide the prompt box, and ask the engineer to review the goal without model output on screen.

The checkpoint should ask for three decisions: whether the current work still fits the user problem, whether the architecture is getting more complex than the task requires, and whether the level of testing or cleanup matches the blast radius. Those questions match the human judgment described in the engineering “taste” piece: product thinking, system thinking, and quality calibration. The first validation can be a small team trial that compares scoped tasks with and without the pause, measuring extra files changed, unplanned refactors, abandoned branches, and whether the original issue was closed.

### Evidence
- [AI Doesn't Just Save Time. It Removes the Pauses](../Inbox/2026-06-12--ai-doesn-t-just-save-time-it-removes-the-pauses.md): Identifies the failure mode: AI removes pauses, encourages continuous prompting, and can turn a short task into hours of scope expansion.
- [AI Doesn't Just Save Time. It Removes the Pauses](../Inbox/2026-06-12--ai-doesn-t-just-save-time-it-removes-the-pauses.md): Gives the specific habit: every 30 minutes, stop prompting, walk, and review what the user is trying to build without the model.
- [What Do Engineers Mean When We Say "Taste"?](../Inbox/2026-06-12--what-do-engineers-mean-when-we-say-taste.md): Breaks engineering judgment into product thinking, system thinking, and quality-as-calibration as the human contribution as AI handles more mechanical coding.
