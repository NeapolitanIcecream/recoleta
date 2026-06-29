---
source: arxiv
url: https://arxiv.org/abs/2606.10209v1
published_at: '2026-06-08T22:01:28'
authors:
- Abhilasha Lodha
- Mahsa Pahlavikhah Varnosfaderani
- Abir Chakraborty
- Abhinav Mithal
topics:
- tool-using-agents
- context-engineering
- context-pruning
- enterprise-automation
- mcp
- token-efficiency
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents

## Summary
This paper tests context pruning and short summaries for long-horizon LLM agents that use verbose enterprise tools. On a 50-task D365 F&O hotel-expense benchmark, keeping the last 5 tool interactions plus a small summary beats full history on both completion and cost.

## Problem
- Verbose D365 F&O MCP tool responses add 500-3,000 tokens per call, so 15-30 calls can grow a task to 50,000-150,000+ tokens.
- Full conversation history can overflow context windows, raise inference cost, and expose the agent to stale form state.
- Expense itemization needs an exact $0.00 remaining balance; any residual amount blocks completion and creates manual follow-up.

## Approach
- The agent is GPT-5 using D365 F&O through an MCP server; GPT-4.1 acts as a user model in the controlled context-policy runs.
- The method keeps whole recent tool call/response pairs instead of trimming individual tokens, so retained form state stays intact.
- C3 keeps only the last 5 tool call/response pairs, which covers about two itemization cycles.
- C4 keeps the same last 5 pairs and adds an automated summary of the 3 most recent evicted interactions.
- The study compares C2 full history, C3 pruning, and C4 pruning plus summary across 5 runs on the same 50 tasks.

## Results
- C1, GPT-5 without a user model, completed 8.0% of tasks, itemized at least one line in 99.6%, and itemized 58.89% of amount on average.
- C2, full history with user model, completed 71.0% of tasks, used 1,480,996 tokens, and took 14.56 hours.
- C3, last 5 tool calls, completed 79.0%, used 535,274 tokens, and took 5.39 hours; this is a 63.9% token reduction and 63.0% time reduction versus C2.
- C4, last 5 plus summary, completed 91.6%, itemized 99.64% of amount on average, used 553,374 tokens, and took 5.79 hours.
- C4 improved complete itemization by 20.6 percentage points over C2 and by 12.6 points over C3, with only 3.4% more tokens than C3.

## Link
- [https://arxiv.org/abs/2606.10209v1](https://arxiv.org/abs/2606.10209v1)
