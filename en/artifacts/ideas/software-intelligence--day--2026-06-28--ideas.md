---
kind: ideas
granularity: day
period_start: '2026-06-28T00:00:00'
period_end: '2026-06-29T00:00:00'
run_id: 96fa2386-9d17-4cea-86b6-13a09fa33b1c
status: succeeded
topics:
- AI agents
- credential security
- coding agents
- agent workspaces
- model routing
- software economics
tags:
- recoleta/ideas
- topic/ai-agents
- topic/credential-security
- topic/coding-agents
- topic/agent-workspaces
- topic/model-routing
- topic/software-economics
language_code: en
pass_output_id: 289
pass_kind: trend_ideas
upstream_pass_output_id: 288
upstream_pass_kind: trend_synthesis
---

# Controlled engineering agent workflows

## Summary
Agent adoption is getting most practical where permissions, task scope, and review are part of the workflow. The clearest near-term changes are credential aliases for agent execution, small engineering tasks assigned through team tools, and operator queues for developers running several coding-agent sessions.

## Credential aliases for agent and MCP tool execution
Security teams should test an agent credential layer before giving agents broad access to internal tools. The concrete change is to stop placing reusable API keys, OAuth tokens, session tokens, and build credentials in MCP configs, IDE plugins, CI jobs, local files, or agent runtime contexts. Agents receive a scoped alias or isolated identifier; the real credential stays in controlled infrastructure that can sign payloads, enforce scope, validate timestamps, block replay, rotate keys, and revoke a session.

The first useful check is small: inventory one agent-enabled workflow, replace its direct secrets with aliases, and run a revocation drill. The drill should record whether a blocked agent loses access within the promised window, whether legitimate runs continue, and whether the audit trail is clear enough for incident response. This matters because the cited incidents are no longer theoretical: the DevFortress piece cites 28,649,024 new secrets exposed on public GitHub in 2025, 64% of 2022 leaked credentials still active in January 2026, and 24,008 unique secrets found in MCP configuration files. It also cites a Cursor agent deleting a production database in 9 seconds after finding an unscoped Railway CLI token.

### Sources
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): Summarizes the credential-aliasing approach, scoped credentials, session monitoring, revocation claims, and incident metrics.
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): Gives the cited scale of exposed secrets and specific agent-related incident numbers.
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): Names the least agency principle for bounded agent tasks and identity/privilege risk.

## Slack and workspace assignment for small code fixes with PR review
Engineering teams can route low-risk fixes through the place where the request already appears, then keep the code merge under normal review. The useful workflow is narrow: a teammate tags an agent in Slack, a Notion page, a task, or a comment; the agent finds the relevant handler, makes a small patch, adds or updates a test, opens a GitHub PR, and posts the link back into the thread.

CrewAI’s Iris example shows why this is worth trying for small work. A settings-page bug caused copied API keys with trailing newlines to fail validation. The fix was two lines, but the human workflow would have required leaving Slack, stashing current work, creating a branch, opening the editor, running Claude Code, reviewing the diff, merging, deploying, and returning to Slack. Iris opened a PR in about three minutes and added a newline test. Notion’s /Dev product points to the same operating pattern for workspace agents: @mentions, shared permissions, visible tool calls, and review or approval points inside the team workspace.

A pilot should limit eligibility to small, reversible changes with a named reviewer and a required test. Complex engineering work should remain outside the queue until the team has measured merge rate, review time, rollback rate, and how often the agent creates extra review burden.

### Sources
- [My coworker Iris isn't a person](../Inbox/2026-06-28--my-coworker-iris-isn-t-a-person.md): Summarizes Iris as a Slack-based agent for small engineering tasks and gives the three-minute PR example.
- [My coworker Iris isn't a person](../Inbox/2026-06-28--my-coworker-iris-isn-t-a-person.md): Describes the nine-step manual workflow, the whitespace-trim bug, the PR, and the added newline test.
- [/Dev/Notion](../Inbox/2026-06-28--dev-notion.md): Describes @mentioning agents, Notion Workers, shared interfaces, permissions, and review or approval points.

## Waiting-state queues for developers running several coding-agent sessions
Developers who run several Claude Code sessions need a queue that shows which agent is blocked and lets them jump there fast. Mux gives a concrete version inside tmux: it reads Claude Code status files, matches them to live panes, opens an fzf overlay, sorts waiting sessions above working and idle ones, shows time in state and a live preview, and switches to the selected pane with Enter.

This is a buildable pattern for terminals, IDEs, and internal developer tools. The queue should expose status, repository or working directory, time since last state change, current request, and the next required human action. It should also carry simple guardrails from everyday coding-agent use: ask the agent to state a plan before editing, keep changes to one or two files when possible, and require approval before edits above 100 lines or across multiple files.

The cheap validation is to compare a week of parallel agent work with and without the queue. Useful measures are time spent in waiting state, number of missed prompts, review rework, and how often the developer kills or restarts a session.

### Sources
- [Mux – A tmux overlay for managing Claude Code sessions](../Inbox/2026-06-28--mux-a-tmux-overlay-for-managing-claude-code-sessions.md): Summarizes Mux’s queue, status sorting, live pane matching, and jump behavior for Claude Code sessions.
- [Mux – A tmux overlay for managing Claude Code sessions](../Inbox/2026-06-28--mux-a-tmux-overlay-for-managing-claude-code-sessions.md): Shows the overlay fields, waiting-first sort, live preview, and one-key pane jump.
- [The Usefulness of AI Agents](../Inbox/2026-06-28--the-usefulness-of-ai-agents.md): Lists practical coding-agent guardrails: plan before coding, focused edits, and approval for larger changes.
