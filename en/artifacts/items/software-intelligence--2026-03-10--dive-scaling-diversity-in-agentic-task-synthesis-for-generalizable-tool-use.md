---
source: arxiv
url: http://arxiv.org/abs/2603.11076v1
published_at: '2026-03-10T20:54:23'
authors:
- Aili Chen
- Chi Zhang
- Junteng Liu
- Jiangjie Chen
- Chengyu Du
- Yunji Li
- Ming Zhong
- Qin Wang
- Zhengmao Zhu
- Jiayuan Song
- Ke Ji
- Junxian He
- Pengyu Zhao
- Yanghua Xiao
topics:
- tool-use-agents
- synthetic-data
- ood-generalization
- multi-agent-training
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use

## Summary
DIVE studies how to make tool-using LLMs generalize more robustly to unfamiliar tasks and unfamiliar toolsets. The core idea is to first execute diverse real tools to collect evidence, and then infer verifiable, executable tasks from the execution traces, thereby scaling both “diversity” and “data reliability” at the same time.

## Problem
- Existing agent task synthesis methods mostly focus on fixed task families and fixed toolsets. Although they can improve in-distribution performance, they are often brittle when the task distribution or toolset changes, and can even exhibit negative transfer.
- To improve generalization, training data must not only be abundant, but also sufficiently diverse in **tool types, tool combinations, and tool-use patterns**; however, increasing diversity can easily lead to tasks that are not executable or not verifiable.
- This matters because agents in real deployments must face open-world tool use: from general search to specialized tools in finance, medicine, biology, and software engineering, and failure directly limits practical usability.

## Approach
- DIVE adopts an **evidence-first** reverse synthesis process: instead of writing tasks first and then validating them, it **runs real tools first**, obtains real outputs and traces, and then infers question-answer tasks that are strictly entailed by the evidence.
- The core mechanism is simple: **facts and evidence come first, then the questions are created**. As a result, tasks are naturally executable (because the traces have already been executed) and verifiable (because the answers come directly from tool outputs).
- To expand structural diversity, the method scales along two axes: **tool-pool coverage** (a broader tool pool) and **per-task toolset variety** (richer tool combinations within each task).
- The authors build three decoupled resource pools: 373 validated real tools, domain seed concept pools, and query exemplars that provide only priors on task form; each round randomly samples toolsets, seeds, and exemplars.
- In the Evidence Collection–Task Derivation loop, the evidence collector executes up to 6 tool calls and iterates for K=3 rounds, gradually accumulating evidence and inducing multi-step tool-use patterns; the resulting tasks are then used to train Qwen3-8B with 48k SFT and 3.2k RL.

## Results
- On **9 OOD benchmarks**, **Qwen3-8B** trained with DIVE improves by an average of **+22 points**; relative to the “strongest 8B baseline,” it reportedly achieves a **+68%** improvement.
- In terms of data scale, training uses **48k SFT traces + 3.2k RL tasks**; the synthesis sources include a **114k task pool** and another **38k task pool**, while the tool pool covers **373 tools across 5 domains**.
- Compared with the base Qwen3-8B, Dive-8B (RL) shows significant gains on multiple OOD benchmarks: **GAIA 22.4→61.2 (+38.8)**, **HLE 6.4→17.8 (+11.4)**, **BrowseComp 1.3→16.4 (+15.1)**, **Xbench-DS 24.0→58.1 (+34.1)**.
- There are also clear gains on specialized-tool OOD benchmarks: **Finance Agent Benchmark 2.0→34.0 (+32.0)**, **MedAgentBench 38.4→57.3 (+18.9)**, **SWE-bench Verified 10.8→18.3 (+7.5)**, **Toolathlon 0.9→8.3 (+7.4)**.
- Compared with the authors’ own SFT model, RL continues to bring improvements: for example **Dive-Eval 35.4→42.5**, **GAIA 49.3→61.2**, **FinSearchComp-T3 33.0→37.3**, **FAB 28.0→34.0**.
- The paper also claims that for OOD generalization, **scaling diversity is better than simply scaling quantity**: even with **4×** less data, diversity scaling remains more effective; this is one of its most important mechanistic conclusions.

## Link
- [http://arxiv.org/abs/2603.11076v1](http://arxiv.org/abs/2603.11076v1)
