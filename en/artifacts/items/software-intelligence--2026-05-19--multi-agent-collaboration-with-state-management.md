---
source: arxiv
url: https://arxiv.org/abs/2605.20563v1
published_at: '2026-05-19T23:45:33'
authors:
- Mengyang Liu
- Taozhi Chen
- Zhenhua Xu
- Xue Jiang
- Yihong Dong
topics:
- multi-agent-coding
- state-management
- conflict-detection
- llm-code-generation
- software-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Multi-agent Collaboration with State Management

## Summary
STORM is a shared-workspace state manager for LLM agents editing the same codebase. It checks whether an agent's file view is current before each write, so stale edits are rejected while the agent can still retry with fresh code.

## Problem
- Parallel software agents can edit shared files or dependent files at the same time, which can create broken interfaces, overwritten work, and failed integration.
- Git worktree isolation prevents live interference, but it hides conflicts until a final merge, where semantic conflicts are harder to diagnose and repair.
- This matters for automated software production because larger code tasks need parallel work, and poor conflict handling can erase the gains from using multiple agents.

## Approach
- STORM keeps one shared workspace and gives every file a version counter.
- Each agent has a read snapshot: the set of files it has read and the file versions it saw.
- Before a write is accepted, STORM checks that every file in the agent's read snapshot still has the same version. If any file changed, the write is rejected.
- On rejection, STORM returns the current target file, a diff for direct conflicts, and stale dependency files so the agent can retry with current context.
- Agents also leave structured intent comments in code, which gives other agents a simple way to see why nearby code was changed.

## Results
- On Commit0-Lite with Claude Sonnet 4.6, STORM scored 46.2 weighted pass rate and 82.5 macro pass rate, compared with GitWorktree at 24.6 / 63.8 and single-agent at 20.7 / 66.4.
- On PaperBench Code-Dev with Claude Sonnet 4.6, STORM scored 74.1, compared with GitWorktree at 72.7 and single-agent at 68.7.
- The paper reports STORM gains over the git-worktree multi-agent baseline of +18.7 macro points on Commit0-Lite and +1.4 points on PaperBench.
- STORM-Combined reached the best Claude Sonnet 4.6 scores: 49.2 weighted and 87.6 macro on Commit0-Lite, and 78.2 on PaperBench.
- With Qwen 3.6 Plus, STORM scored 61.4 weighted on Commit0-Lite versus GitWorktree at 16.7, and 55.0 on PaperBench versus GitWorktree at 51.6.
- In a Sonnet scaling test on Commit0-Lite, increasing the maximum engineers from 2 to 8 raised overall pass rate from 38.2% to 69.7% and macro pass rate from 71.3% to 87.1%, while cost rose from $199 to $429 and wall-clock time stayed near 13 hours.

## Link
- [https://arxiv.org/abs/2605.20563v1](https://arxiv.org/abs/2605.20563v1)
