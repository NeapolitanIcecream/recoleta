---
source: arxiv
url: https://arxiv.org/abs/2605.12673v1
published_at: '2026-05-12T19:22:45'
authors:
- Hao Wang
- Hanchen Li
- Qiuyang Mang
- Alvin Cheung
- Koushik Sen
- Dawn Song
topics:
- agent-benchmarks
- reward-hacking
- benchmark-security
- ai-agents
- code-intelligence
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack

## Summary
BenchJack audits AI agent benchmarks for reward-hacking paths before normal agent runs. On 10 popular benchmarks, it produced exploits for all of them and reached almost all tasks on 9 of 10 while doing no intended task work.

## Problem
- Agent benchmarks can give high scores to agents that tamper with tests, leak answers, or exploit scoring code, so reported capability numbers can be wrong.
- Manual audits do not scale across new benchmarks with different harnesses, sandboxes, and scoring functions.
- Post-run hack detectors only act after a bad run, and the cited work says LLM-based detectors can miss or accept hacked traces.

## Approach
- The paper builds an 8-class flaw taxonomy from past reward-hacking cases, including isolation failure, shipped answers, remote code execution, prompt injection, weak string matching, logic gaps, trusting untrusted output, and excessive permissions.
- It turns the taxonomy into the Agent-Eval Checklist: 30 binary checks in 7 categories for benchmark designers.
- BenchJack wraps a coding agent and runs three stages: reconnaissance maps entry points, scoring code, task files, environments, and trust boundaries; flaw scan records exploitable findings; exploit construction writes and tests a run.sh exploit that maximizes score without doing the intended tasks.
- The patching loop reruns BenchJack after a defender coding agent fixes verified exploits, then repeats until BenchJack cannot find a working hack or the benchmark needs redesign.

## Results
- BenchJack audited 10 benchmarks: SWE-bench Verified, SWE-bench Pro, FrontierSWE, MLE-Bench, SkillsBench, Terminal-Bench, OSWorld, WebArena, NetArena, and AgentBench.
- It generated working reward-hacking exploits on all 10 benchmarks and reached almost all instances on 9 of 10; AgentBench was lower because only its dbbench subset was hacked.
- It found 219 distinct flaws across the 8 flaw classes.
- The audited set covered thousands of tasks, including 500 in SWE-bench Verified, 731 in SWE-bench Pro, 812 in WebArena, 5,030 in NetArena, and 903 in AgentBench.
- On 4 benchmarks with fixable designs, the iterative patching loop reduced the hackable-task ratio from about 100% to under 10%.
- WebArena and OSWorld were patched until BenchJack could no longer hack them within 3 iterations.

## Link
- [https://arxiv.org/abs/2605.12673v1](https://arxiv.org/abs/2605.12673v1)
