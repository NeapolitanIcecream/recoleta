---
source: arxiv
url: https://arxiv.org/abs/2606.19980v1
published_at: '2026-06-18T09:21:27'
authors:
- Wenli Xiao
- Jia Xie
- Tonghe Zhang
- Haotian Lin
- Letian "Max" Fu
- Haoru Xue
- Jalen Lu
- Yi Yang
- Cunxi Dai
- Zi Wang
- Jimmy Wu
- Guanzhi Wang
- S. Shankar Sastry
- Ken Goldberg
- Linxi "Jim" Fan
- Yuke Zhu
- Guanya Shi
topics:
- real-world-robot-learning
- robot-policy-self-improvement
- dexterous-manipulation
- coding-agents
- robot-data-scaling
- vision-language-action
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# ENPIRE: Agentic Robot Policy Self-Improvement in the Real World

## Summary
ENPIRE lets coding agents improve robot manipulation policies on real hardware by running reset, rollout, verification, and code-edit loops with little human work after setup. It reports up to 99% real-world success on dexterous tasks and faster improvement when eight robot-agent workers run in parallel.

## Problem
- Real robot policy learning still needs humans to reset scenes, judge outcomes, collect rollouts, and change training code, which slows data scaling for dexterous manipulation.
- Coding agents can improve software in digital settings, but real robots need safe execution bounds, automatic resets, and reliable success checks before agents can run experiments.
- The problem matters because robot time and human operator time become bottlenecks when training generalist policies on contact-rich tasks.

## Approach
- ENPIRE gives a coding agent task APIs for hard safety limits, automatic verification, automatic reset, rollout execution, and training-code edits.
- In the first stage, the agent builds reset and reward/checker code from short human feedback and demos; after approval, these APIs are fixed for later runs.
- In the second stage, the agent reads logs and videos, edits BC/RL/heuristic/code-policy training code, launches real robot rollouts, and keeps changes that raise measured success.
- For fleets, ENPIRE assigns one agent per robot; agents test different code branches asynchronously and share or copy successful recipes through Git.
- The paper adds Mean Robot Utilization, GPU utilization, Mean Token Utilization, tokens-to-success, and time-to-success to measure how much robot time and model-token budget the agents spend.

## Results
- The abstract claims coding agents reached 99% success on real dexterous tasks including PushT, pin-box insertion, and zip-tie cutting.
- Pin insertion uses 4 mm holes and requires 50 consecutive real-world successes in evaluation; the paper reports convergence to 100% faster than a cited human-in-the-loop method.
- In simulation on Gym-PushT, Claude Code and Codex reached 95% success in about 2 hours; Kimi Code took about twice as long.
- Fleet scaling cut Push-T time to a 1.0 normalized score from about 5 hours with 1 agent to about 2 hours with 8 agents.
- Fleet scaling cut pin-insertion time to near-perfect success from more than 1.5 hours with 1 agent to about 40 minutes with 8 agents.
- The zip-tie checker was optimized to under 150 ms latency, and RoboCasa365 results are reported as better than GR00T VLA and CaP-X, but the excerpt gives no exact success rates for that comparison.

## Link
- [https://arxiv.org/abs/2606.19980v1](https://arxiv.org/abs/2606.19980v1)
