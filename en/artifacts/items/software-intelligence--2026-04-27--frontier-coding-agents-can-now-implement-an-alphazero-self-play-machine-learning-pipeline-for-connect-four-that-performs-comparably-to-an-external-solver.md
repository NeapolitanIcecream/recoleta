---
source: arxiv
url: https://arxiv.org/abs/2604.25067v2
published_at: '2026-04-27T23:48:30'
authors:
- Joshua Sherwood
- Ben Aybar
- Benjamin Kaplan
topics:
- coding-agents
- code-intelligence
- ml-pipeline-automation
- alphazero
- benchmarking
- ai-safety
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Frontier Coding Agents Can Now Implement an AlphaZero Self-Play Machine Learning Pipeline For Connect Four That Performs Comparably to an External Solver

## Summary
Coding agents can now build a working AlphaZero-style self-play training pipeline for Connect Four within 3 hours on one consumer GPU. The paper uses this as a benchmark for autonomous ML research implementation and reports that Claude Opus 4.7 came close to the Pascal Pons solver in the tested setting.

## Problem
- The paper asks whether coding agents can implement an end-to-end ML pipeline from a short task description, rather than copying a full prior work description.
- This matters for AI safety forecasting because autonomous replication of past AI research may appear before agents can speed up current AI research work.
- Existing broad benchmarks such as METR time horizon and Epoch Capabilities Index may miss narrow capability jumps in agentic ML research implementation.

## Approach
- The task asks each agent to build an AlphaZero-style Connect Four system using neural-network-guided MCTS and self-play training.
- The agents receive a minimal prompt and a 3-hour budget on a consumer desktop with an RTX 5060 Ti GPU, 32 GB RAM, and an AMD Ryzen 7 9700X CPU.
- The main experiment tests Gemini 3.1 Pro Preview, Claude Opus 4.6, Claude Opus 4.7, and GPT-5.4, with 8 trials per agent.
- The evaluation runs a round-robin tournament against all trial outputs and the Pascal Pons Connect Four solver, then fits Bradley-Terry ratings anchored with Pons at 2000.
- A separate 16-trial GPT-5.4 probe changes prompts and container context to test whether low time use could be evaluation-aware underperformance.

## Results
- Claude Opus 4.7 won as first mover against the Pascal Pons solver in 7 of 8 main trials.
- No other tested agent exceeded 2 wins out of 8 as first mover against Pons.
- The main experiment used 4 agents × 8 trials, for 32 primary agent outputs.
- The full tournament evaluated 49 players: 48 agent outputs plus the Pascal Pons solver.
- Each player faced each other player as both first and second mover twice, giving 4 games per matchup.
- GPT-5.4 used much less than the 3-hour budget in the main runs; in a 16-trial probe, shorter and less evaluation-coded prompts increased its time-budget usage, while Bradley-Terry ratings changed only directionally.

## Link
- [https://arxiv.org/abs/2604.25067v2](https://arxiv.org/abs/2604.25067v2)
