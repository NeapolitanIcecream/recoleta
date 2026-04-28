---
source: arxiv
url: http://arxiv.org/abs/2604.11716v1
published_at: '2026-04-13T16:52:34'
authors:
- Shuquan Lian
- Juncheng Liu
- Yazhe Chen
- Yuhong Chen
- Hui Li
topics:
- software-agents
- code-intelligence
- swe-bench
- context-management
- reasoning-compression
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# SWE-AGILE: A Software Agent Framework for Efficiently Managing Dynamic Reasoning Context

## Summary
SWE-AGILE is a software agent framework for multi-step code fixing that keeps recent detailed reasoning, compresses older reasoning into short digests, and trains the model to work under that changing context. On SWE-Bench-Verified, it reports a new best result for 7B-8B open models, reaching 24.1% success with Qwen3-8B.

## Problem
- Multi-turn software engineering agents need long reasoning chains to inspect code, use tools, and handle edge cases, but keeping all past reasoning makes the context grow fast.
- Large contexts hurt agent quality through lost-in-the-middle effects, higher memory cost, and slower training and inference.
- If old reasoning is dropped completely, the agent has to re-derive the same analysis after each tool call, which wastes tokens and weakens continuity across steps.

## Approach
- The agent outputs three parts at each step: detailed reasoning, a short reasoning digest, and the next action.
- It uses a dynamic context: full observations and actions stay in history, recent reasoning stays verbatim in a sliding window, and older reasoning is replaced by per-step digests.
- Training uses trajectory snapshots so each step is learned under the same visibility limits used at inference time, instead of exposing the full past chain of thought during training.
- A hindsight backfill pipeline rewrites successful trajectories with detailed reasoning and digests, using the ground-truth future action plus the original shallow thought to synthesize better supervision.
- RL with verifiable rewards adds a trajectory-level compression reward, so the model gets rewarded only when it both solves the task and keeps the retained context short.

## Results
- On **SWE-Bench-Verified**, **SWE-AGILE (SFT+RL)** with **Qwen3-8B** reaches **24.1%** success.
- On the same benchmark, the **Qwen3-8B base model** gets **15.83%**, and **SWE-AGILE (SFT)** gets **21.45%**, a **35.5% relative improvement** over the base model.
- The paper says **24.1%** sets a new standard for the **7B-8B** class in its comparison table, beating **R2EGym 7B (19.0%)**, **SWE-smith 7B (15.2%)**, and **SWE-Gym 7B (10.6%)**; it also exceeds **SkyRL-Agent-v0 14B (21.6%)**.
- The method uses **2.2k training trajectories**, which the authors describe as **11%** of the **19.3k** trajectories used by **SWE-Dev**, while SWE-AGILE still slightly beats **SWE-Dev 7B (23.4%)** with its **24.1%** score.
- With **Qwen3-14B** and SFT only, SWE-AGILE reports **30.06%** on **SWE-Bench-Verified**, above **R2EGym 14B (26.8%)**, **SkyRL-Agent-v0 14B (21.6%)**, and **SWE-Gym 14B (16.4%)**.
- On **SWE-Bench Lite**, **SWE-AGILE-8B** reports **14.77%**, compared with **SWE-smith-7B at 11.7%** and **R2E-Gym at 11.0%**. The excerpt includes only partial ablation results for dynamic context analysis, so the full quantitative breakdown for those studies is not available here.

## Link
- [http://arxiv.org/abs/2604.11716v1](http://arxiv.org/abs/2604.11716v1)
