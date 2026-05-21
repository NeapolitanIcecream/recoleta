---
source: arxiv
url: https://arxiv.org/abs/2605.10913v1
published_at: '2026-05-11T17:50:51'
authors:
- Simon Yu
- Derek Chong
- Ananjan Nandi
- Dilara Soylu
- Jiuding Sun
- Christopher D Manning
- Weiyan Shi
topics:
- agent-runtime
- multi-agent-systems
- code-intelligence
- execution-tracing
- agent-rl
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace

## Summary
Shepherd is a runtime for meta-agents that records agent execution as a typed Git-like trace, so supervisors can inspect, fork, replay, and modify running agents. The paper reports faster branching than Docker-style snapshots and task gains in live coding supervision, workflow optimization, and RL training.

## Problem
- LLM agent systems now use meta-agents that supervise, edit, or train other agents during execution.
- Existing runtimes mostly expose transcripts, tool logs, or environment snapshots, which makes it hard to rewind, branch, replay, or intervene in a running agent with exact state.
- This matters because multi-agent coding, workflow search, and agent RL waste time when each alternative path needs a full rerun.

## Approach
- Shepherd treats an agent as a typed task with typed inputs and outputs, so a meta-agent can pass it around, call it, replace it, or compose it with other tasks.
- Every model call, tool call, filesystem write, and environment action becomes a typed effect in an append-only execution trace.
- The trace works like Git: each action is a commit, each fork is a branch, merge keeps a child branch, and discard removes it without changing the parent.
- Forking copies the agent process and filesystem together with copy-on-write isolation, so alternative continuations can run from the same past state.
- The core operations are specified with an algebraic-effects calculus mechanized in Lean, and replay preserves the exact prompt prefix for provider prompt-cache reuse.

## Results
- On Terminal-Bench 2.0 images, Shepherd forks in 134–143 ms across image sizes from 42 MB to 5.8 GB; Docker commit takes 658–725 ms, and full root filesystem copy takes up to 53,462 ms on the 5.8 GB image.
- On the 5.8 GB image, Shepherd revert takes 147 ms versus 828 ms for Docker commit and 25,943 ms for full copy.
- For K=4 branches on the 5.8 GB image, Shepherd reports 30 KB disk overhead and 25.7 MB RAM overhead, with 10 KB per-branch storage.
- Replay reaches about 95% prompt-cache hit rate on Anthropic Claude Haiku 4.5 across 8 Terminal-Bench 2.0 tasks.
- A live supervisor raises CooperBench pair coding pass rate from 28.8% to 54.7%, close to the reported 57.2% solo ceiling.
- Counterfactual meta-optimization beats MetaHarness and GEPA by up to 11 points with up to 58% lower wall-clock, and Tree-RL raises TerminalBench-2 on Qwen3.5-35B-A3B from 34.2% to 39.4%.

## Link
- [https://arxiv.org/abs/2605.10913v1](https://arxiv.org/abs/2605.10913v1)
