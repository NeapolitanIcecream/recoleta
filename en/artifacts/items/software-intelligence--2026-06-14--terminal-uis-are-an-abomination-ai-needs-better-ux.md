---
source: hn
url: https://medium.com/@balajibal/terminal-uis-are-an-abomination-so-are-chatbots-ai-needs-better-ux-c7ee7b5a0018
published_at: '2026-06-14T23:22:19'
authors:
- rafaepta
topics:
- human-ai-interaction
- ai-ux
- terminal-ui
- agentic-workflows
- code-intelligence
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Terminal UIs Are an Abomination. AI Needs Better UX

## Summary
The piece argues that terminal UIs and chat are poor interfaces for modern AI because AI work is now multi-step, stateful, and branching. It calls for interfaces that expose provenance, dependencies, and control, rather than a scrolling transcript.

## Problem
- AI tools are still being wrapped in chat panes and terminal streams because they are cheap to build, not because they fit the work.
- Transcript-style interfaces make users reconstruct state, causality, and failures from memory, which raises cognitive load.
- This gets worse in agentic coding and other long-running tasks where the work has branches, retries, and dependencies.

## Approach
- The argument separates the model or agent engine from the user interface.
- It treats AI work as graph-shaped rather than linear, with state, branches, replay, rollback, and visible dependencies.
- It proposes different surfaces for different tasks, such as code graphs for coding, claim maps for research, and approval queues for operations.

## Results
- No quantitative results are reported; this is a position piece, not an experimental paper.
- The strongest concrete claim is that terminal and chat interfaces create adoption friction because they force users into operator mode instead of outcome-focused workflows.
- It claims agentic coding should be surfaced as a temporal change graph with nodes for edits, tests, retries, plans, and decisions, rather than as logs or diffs alone.
- It argues that better AI adoption depends on interfaces that support auditability, visibility, rollback, reproducibility, and governance.

## Link
- [https://medium.com/@balajibal/terminal-uis-are-an-abomination-so-are-chatbots-ai-needs-better-ux-c7ee7b5a0018](https://medium.com/@balajibal/terminal-uis-are-an-abomination-so-are-chatbots-ai-needs-better-ux-c7ee7b5a0018)
