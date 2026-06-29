---
source: arxiv
url: https://arxiv.org/abs/2605.15040v1
published_at: '2026-05-14T16:35:12'
authors:
- Baolin Peng
- Wenlin Yao
- Qianhui Wu
- Hao Cheng
- Xiao Yu
- Rui Yang
- Tao Ge
- Alessandrio Sordoni
- Xingdi Yuan
- Yelong Shen
- Pengcheng He
- Tong Zhang
- Zhou Yu
- Jianfeng Gao
topics:
- agentic-llm-training
- code-intelligence
- software-agents
- reinforcement-learning
- kubernetes-sandboxes
- gui-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Orchard: An Open-Source Agentic Modeling Framework

## Summary
Orchard is an open-source agent-training system built around a thin Kubernetes environment service. It reports strong results for software-engineering, browser-use, and personal-assistant agents using reusable sandbox infrastructure plus SFT and RL recipes.

## Problem
- Agentic LLM training needs many isolated environments for code execution, web tasks, and tool use; closed or tightly coupled sandbox systems make results harder to reproduce and reuse.
- Software-engineering agents need large trajectory sets and better learning from failed attempts, because SWE-bench-style rewards are sparse.
- Open research needs lower sandbox cost and higher rollout throughput so smaller teams can train and evaluate agents at scale.

## Approach
- Orchard Env runs as a Kubernetes-native sandbox service with a REST API for sandbox creation, command execution, file I/O, network policy, and cleanup.
- It injects a lightweight in-pod execution agent into user Docker images at runtime, so task images do not need rebuilds.
- Execution requests go directly to sandbox Pod IPs, which avoids Kubernetes exec and WebSocket overhead on the hot path.
- Orchard-SWE distills 107K software-engineering trajectories, keeps useful parts of unresolved trajectories with credit-assignment SFT, and uses Balanced Adaptive Rollout for sparse-reward RL.
- Orchard-GUI and Orchard-Claw reuse the same environment layer for browser navigation and productivity-tool tasks with SFT plus RL.

## Results
- Orchard-SWE with Qwen3-30B-A3B-Thinking reaches 64.3% on SWE-bench Verified after SFT and 67.5% after SFT+RL under mini-swe-agent, claimed as a new open-source best among comparable-size models.
- Orchard-GUI trains a 4B vision-language agent with 0.4K distilled trajectories and 2.2K open-ended tasks, reaching 74.1% on WebVoyager, 67.0% on Online-Mind2Web, 64.0% on DeepShop, and 68.4% average.
- Orchard-Claw trains on 0.2K synthetic tasks and reaches 59.6% pass@3 on Claw-Eval; with the ZeroClaw harness it reaches 73.9% pass@3.
- Orchard Env reports 0.280 s average command latency, compared with 0.747 s for E2B and 2.046 s for Modal in the cited benchmark setup.
- In a 1,000-sandbox stress test, Orchard Env reports 100% success, 26 s end-to-end time, 11.75 s average create time, and 0.28 s average exec latency.
- Estimated cost for 128 parallel 2-vCPU, 8-GiB sandboxes over 240 hours is $3,362 on-demand and $673 with spot instances, compared with $7,078 for Daytona or E2B.

## Link
- [https://arxiv.org/abs/2605.15040v1](https://arxiv.org/abs/2605.15040v1)
