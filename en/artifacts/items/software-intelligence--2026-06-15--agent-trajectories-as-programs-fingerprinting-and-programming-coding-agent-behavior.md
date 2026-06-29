---
source: arxiv
url: https://arxiv.org/abs/2606.16988v1
published_at: '2026-06-15T17:28:41'
authors:
- Hamidah Oderinwale
topics:
- coding-agents
- software-engineering
- agent-traces
- behavioral-fingerprinting
- swe-bench
- trace-search
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Agent trajectories as programs: fingerprinting and programming coding-agent behavior

## Summary
The paper argues that coding agents can be identified and programmed through their action traces, not just scored by task success. It introduces ProcGrep, a library for building procedural fingerprints, comparing agents, and searching past agent trajectories.

## Problem
- Benchmark scores show whether an agent solved a task, but they do not show how the agent searched, edited, tested, or failed.
- Developers need trace-level tools for model routing, monitoring, cost analysis, and debugging as coding agents take more of the software workflow.
- Natural-language plans and rationales are weak evidence for action: the paper reports low precision for several model accounts, including Claude-4 precision of 0.500 and Claude-3.7-thinking precision of 0.625.

## Approach
- The method turns agent trajectories into sequences of procedural actions such as `read_file`, `search_repo`, `edit`, `run_test`, and `submit`.
- It parses solution patches with ASTs, adds code context and model-written behavior descriptions, then induces a shared action vocabulary from recurring action subsequences.
- The main vocabulary induction method is BPE over action traces. The paper chooses `K=192` after a V-measure sweep, with a reported peak of `0.644` and a plateau across `K=128` to `K=256`.
- It compares agents with entropy, compression ratio, action-transition statistics, nearest-neighbor retrieval, and Jensen-Shannon divergence over procedural distributions.
- ProcGrep lets users write deterministic structural queries over traces, including ordered actions, counts, conditions, and missing actions.

## Results
- On SWE-bench Verified traces from 10 agents across GPT, Claude, DeepSeek, Qwen-derived, SWE-agent, Agentless, DARS, and Moatless setups, procedural fingerprints attribute an unseen trajectory to the correct agent with `85.7%` accuracy versus an `11.1%` random baseline.
- Distinct action transitions identify agents: DARS+R1 overuses `search_repo → create_file` by `31.6×`, Moatless+V3 overuses `edit → submit` by `15.7×`, and Agentless+Claude-3.5 overuses `run_test → run_test` by `12.5×`.
- ProcGrep reaches `F1=1.000` with `1.1 µs` latency per decision on episodic trace search. LLM judges are lower: Claude Sonnet 4.6 gets `F1=0.278` at `1.71 s`, GPT-4o gets `F1=0.230` at `0.66 s`, and DeepSeek-chat gets `F1=0.093` at `1.51 s`.
- Teacher-student procedural similarity is measurable: the Claude-3.7-thinking to SWE-agent-LM-32B distilled pair has `JSD=0.250`, compared with `0.518` within model family across generations and `0.533` for the same model across scaffolds.
- Procedural representations predict success better than natural-language accounts in nearest-neighbor tests: structural pattern overlap gets `F1=0.347`, action sequence distance gets `F1=0.274`, narrative description gets `F1=0.177`, and random retrieval ranges from `0.13` to `0.24`.
- Cost and behavior differ by agent: Claude-4 resolves `59.0%` of tasks at `$2.02` per resolved task, Claude-3.7-thinking resolves `50.7%` at `$1.53`, GPT-4 resolves `18.0%` at `$13.93`, and Moatless+DeepSeek-V3 resolves `30.7%` at `$0.06`.

## Link
- [https://arxiv.org/abs/2606.16988v1](https://arxiv.org/abs/2606.16988v1)
