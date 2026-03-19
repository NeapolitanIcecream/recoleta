---
source: arxiv
url: http://arxiv.org/abs/2603.07927v1
published_at: '2026-03-09T03:47:10'
authors:
- Xin-Cheng Wen
- Binbin Chen
- Haoxuan Lan
- Hang Yu
- Peng Di
- Cuiyun Gao
topics:
- software-agents
- llm-training
- trajectory-learning
- reinforcement-learning
- bug-fixing
- swe-bench
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# SWE-Fuse: Empowering Software Agents via Issue-free Trajectory Learning and Entropy-aware RLVR Training

## Summary
SWE-Fuse is a training framework for software-repair agents whose core goal is to enable models to learn step-by-step debugging and optimize stably even when issue descriptions are unreliable or entirely missing. It mixes trajectories with issue descriptions and trajectories without issue descriptions during training, then pairs this with an entropy-based RLVR update strategy, achieving strong results on SWE-bench Verified.

## Problem
- The paper aims to solve the problem that issue descriptions in real software engineering data are often misaligned with the actual fixing patches, or even empty, causing issue-based software agents to be misled.
- This matters because SWE agents rely on issue text to understand bugs, but real-world data is noisy and scalable high-quality issue-PR pairings are scarce, which directly limits repair success rates and training scale.
- The paper gives an example where the issue mentions warning handling, but the gold patch actually fixes TIFF encoding logic; in addition, 18,033/59,136 (30.49%) samples in SWE-smith have empty issue descriptions.

## Approach
- The core idea is simple: do not only teach the model to "read the issue and fix the bug," but also teach it to "find the problem through test failures and step-by-step debugging even without an issue." Accordingly, the authors fuse issue-guided samples and issue-free samples for training.
- The first component is issue-free-driven trajectory learning: multi-step reasoning+action debugging trajectories are first generated in an executable repository sandbox, then rule filtering and git-leakage prevention filtering are applied, and finally the mixed trajectories are used for SFT so the model learns to inspect code, run commands, read errors, and modify patches step by step.
- Issue-free samples remove the issue description while retaining other context and part of the tests, and use "successful trajectories" to train the model, thereby reducing interference from incorrect issue text.
- The second component is entropy-aware RLVR: during reinforcement learning, different samples dynamically adjust the clipping range according to policy entropy. When entropy is high and the advantage is positive, clipping is relaxed to encourage exploration; when entropy is high but the advantage is non-positive, clipping is tightened to avoid incorrectly penalizing potentially useful behaviors due to noise.
- Training also adopts RLOO-style relative advantage estimation and relies only on a sandbox environment with basic bash tool calls, reducing system complexity.

## Results
- On SWE-bench Verified, SWE-Fuse-Qwen3-8B reaches an issue resolve rate of **43.0%**, and SWE-Fuse-Qwen3-32B reaches **60.2%**.
- The paper claims these respectively outperform the best **8B** and **32B** baselines, with relative solve rate improvements of **43.0%** and **60.2%**; elsewhere it also states that in open-model comparisons, the relative improvements are **9.1% (8B)** and **11.7% (32B)**.
- After adding test-time scaling, under **TTS@8**, the 8B and 32B models reach solve rates of **49.8%** and **65.2%**, respectively.
- The authors claim the 32B open-source model ranks first among models of the same scale on the leaderboard, and has a resolved rate **1.8% higher than OpenAI-o3**, though it still trails Claude-4-Sonnet and Claude-4.5-Sonnet.
- In terms of training data, the authors constructed **14,350** valid trajectories covering **14,329** instances and **111** projects; the total number of interaction rounds is **401,958**, with an average of **28.05** rounds and average token consumption of **19,676.08**.
- The paper’s strongest claim is that through "issue-free trajectory learning + entropy-aware RLVR," even using only a relatively simple bash toolchain, 8B/32B software agents can reach a new open-source SOTA on real-repository repair tasks.

## Link
- [http://arxiv.org/abs/2603.07927v1](http://arxiv.org/abs/2603.07927v1)
