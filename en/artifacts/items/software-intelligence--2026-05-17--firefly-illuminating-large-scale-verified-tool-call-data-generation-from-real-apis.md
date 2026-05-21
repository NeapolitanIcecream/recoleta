---
source: arxiv
url: https://arxiv.org/abs/2605.17558v1
published_at: '2026-05-17T17:38:17'
authors:
- Yuxuan Lu
- Ziyi Wang
- Yingzhou Lu
- Yisi Sang
- Jiri Gesi
- Xianfeng Tang
- Yimeng Zhang
- Zhenwei Dai
- Hui Liu
- Hanqing Lu
- Chen Luo
- Qi He
- Benoit Dumoulin
- Jing Huang
- Dakuo Wang
topics:
- tool-calling-agents
- verified-data-generation
- mcp-servers
- offline-rl
- api-simulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs

## Summary
FireFly generates verified tool-call training data by executing real MCP APIs first, then writing tasks from the observed outputs. The paper claims that RL on this data raises a 4B model to near Claude Sonnet 4.6 performance on its held-out tool-calling test.

## Problem
- Tool-calling agents need trajectories with correct intermediate API calls and checkable final answers, but human labeling is expensive and hard to scale across many APIs.
- Many synthetic datasets generate a user task before any known reachable outcome exists, which can produce infeasible calls, stale responses, or labels with no executed source.
- Live APIs change, fail, and hit rate limits, so repeated RL rollouts against real servers are hard to reproduce.

## Approach
- FireFly scrapes MCP servers from Smithery, then filters for stateless tools with no user authentication, clear JSON schemas, and non-trivial behavior. This leaves 240 servers and 993 tools.
- It builds a directed tool graph where LLM-judged edges mean one tool output can feed another tool input. The graph has about 83K directed edges, including 64K medium-or-higher confidence edges.
- A strong LLM explores live APIs inside sampled sub-DAGs from this graph, producing executable tool-call DAGs with recorded tool names, arguments, outputs, and data-flow edges.
- The task generator works backward from observed outputs: it writes a natural-language task and structured answer schema after the correct values already exist in executed tool results.
- A retrieval-augmented simulator caches all observed calls and returns exact cached outputs, fuzzy retrieved outputs with LLM help, or an error for unseen tools. RL then uses offline GRPO with binary rewards from field matching and LLM judging.

## Results
- The dataset contains 5,144 verified tasks and 9,749 trajectories from 240 servers and 993 tools. It uses 4,944 tasks for training and 200 for testing.
- Task statistics include 3.0 tool calls on average, a 1–10 call range, 4.6 answer fields on average, 77.0% medium tasks, and 38.5% multi-server tasks.
- On the FireFly test set, Qwen3-4B improves from 28.1% to 41.5% pass@1 after FireFly RL, a gain of 13.4 points. Pass@16 improves from 43.0% to 57.0%.
- The trained 4B model is close to Claude Sonnet 4.6 on pass@1, at 41.5% versus 42.2%, and exceeds it on pass@8, at 52.8% versus 50.3%.
- Public benchmark gains include Tau2-Bench Retail 0.491 to 0.627, Airline 0.365 to 0.525, Telecom 0.189 to 0.204, MCP-Atlas 19.4% to 26.0%, and MCPMark File System 40.0% to 60.0%, Postgres Easy 70.0% to 80.0%, Postgres Std 9.5% to 13.3%.
- During the full training run, simulator calls resolved as 42.2% exact match, 57.8% fuzzy match, and 0% no-data. Dataset generation used about 23.5B tokens and cost about $47K.

## Link
- [https://arxiv.org/abs/2605.17558v1](https://arxiv.org/abs/2605.17558v1)
