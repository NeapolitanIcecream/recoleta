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
- swe-bench
- trajectory-learning
- reinforcement-learning
- code-repair
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# SWE-Fuse: Empowering Software Agents via Issue-free Trajectory Learning and Entropy-aware RLVR Training

## Summary
SWE-Fuse is a training framework for software repair agents whose core goal is to reduce the misleading effects of low-quality issue descriptions in real-world software problems. By combining trajectory data with issue descriptions and without issue descriptions, together with entropy-aware RLVR training, it improves solve rates on SWE-bench Verified.

## Problem
- The paper addresses the fact that in real-world software repair data, **issue descriptions often do not match the actual patches**, which can lead automated software agents astray and cause debugging and patch generation to fail.
- This matters because current SWE agents rely heavily on issue text as the task entry point; once the description is noisy, missing, or misleading, the agent may search in the wrong direction even if it has strong coding ability.
- Data scale and quality are also limited. For example, the paper notes that in SWE-smith, **18,033 / 59,136 (30.49%)** of samples have empty problem descriptions, indicating that relying only on high-quality issue supervision is difficult to scale.

## Approach
- The core idea is simple: **do not only teach the model to read an issue and fix a bug, but also teach it to find problems through tests and debugging on its own even without a reliable issue description**.
- To do this, the authors build a hybrid training framework that fuses two types of samples: one with issue descriptions, and another consisting of **issue-free** samples that retain only tests and the environment, allowing the model to learn problem localization through multi-round debugging.
- In the supervised learning stage, the authors first use a teacher agent to generate multi-step ReAct trajectories (explicitly including reasoning and bash action), then filter them by removing trajectories with poor formatting, no intermediate reasoning, or possible cheating via git metadata, ultimately obtaining **14k** high-quality trajectory data.
- In the reinforcement learning stage, the authors propose **entropy-aware RLVR**: if the model currently has high uncertainty and the sample advantage is positive, clipping is relaxed to encourage more exploration; if the advantage is non-positive and uncertainty is high, training is made more conservative to avoid over-penalizing potentially useful exploration because of noise.
- The training and execution environment is kept relatively simple, relying mainly on basic bash tool calls and sandbox execution rather than a more complex specialized toolchain.

## Results
- On **SWE-bench Verified**, the authors report that SWE-Fuse-Qwen3-8B achieves a solve rate of **43.0%**, and SWE-Fuse-Qwen3-32B reaches **60.2%**.
- Compared with the best baselines, the paper claims that SWE-Fuse achieves solve rates of **43.0%** and **60.2%** for the **8B** and **32B** settings, respectively, and further describes these in the main text as relative improvements of **9.1%** (8B) and **11.7%** (32B).
- After adding test-time scaling **TTS@8**, the solve rates of the 8B and 32B models further increase to **49.8%** and **65.2%**.
- The paper states that the 32B open-source model reaches the best performance among same-size open-source models at the time, and has a resolved rate **1.8% higher than OpenAI-o3**, though it still trails Claude-4-Sonnet and Claude-4.5-Sonnet.
- The authors also release a trajectory dataset with **14,350** valid trajectories, covering **14,329** instances and **111** projects; the total number of interaction rounds is **401,958**, with an average of **28.05** rounds and average token consumption of **19,676.08**.

## Link
- [http://arxiv.org/abs/2603.07927v1](http://arxiv.org/abs/2603.07927v1)
