---
source: arxiv
url: http://arxiv.org/abs/2604.16529v1
published_at: '2026-04-16T17:39:33'
authors:
- Joongwon Kim
- Wannan Yang
- Kelvin Niu
- Hongming Zhang
- Yun Zhu
- Eryk Helenowski
- Ruan Silva
- Zhengxing Chen
- Srinivasan Iyer
- Manzil Zaheer
- Daniel Fried
- Hannaneh Hajishirzi
- Sanjeev Arora
- Gabriel Synnaeve
- Ruslan Salakhutdinov
- Anirudh Goyal
topics:
- agentic-coding
- test-time-scaling
- code-intelligence
- multi-agent-software-engineering
- swe-bench
- terminal-bench
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Scaling Test-Time Compute for Agentic Coding

## Summary
This paper improves agentic coding by spending test-time compute on multiple full agent rollouts, then selecting and reusing the useful parts of those attempts. The main idea is to replace long noisy trajectories with short structured summaries that support both better selection and better refinement.

## Problem
- Agentic coding tasks produce long action-observation traces across many terminal steps, so standard test-time scaling methods from math or single-shot code generation do not transfer well.
- Raw trajectories are hard to compare and hard to reuse because they mix useful clues with repeated logs, errors, and dead ends.
- This matters because benchmarks such as SWE-Bench Verified and Terminal-Bench v2.0 depend on long-horizon debugging and editing, where a better way to spend inference compute can raise pass rates without changing the base model.

## Approach
- The method converts each rollout into a compact structured summary that records the key diagnosis, attempted fixes, progress, and failure modes.
- For parallel scaling, it uses **Recursive Tournament Voting (RTV)**: run **N=16** rollouts, summarize them, compare summaries in small groups, and repeat until one rollout remains. The default setup uses pairwise groups (**G=2**) and **V=8** comparison votes.
- For sequential scaling, it adapts **Parallel-Distill-Refine (PDR)** to agentic coding: build a refinement context from **K=4** summaries from the previous iteration, then launch a fresh new rollout in a reset environment conditioned on those summaries.
- The full pipeline is: iteration-0 rollouts, **RTV** select-top-**K**, iteration-1 refined rollouts, then final **RTV** selection.
- Ablations show that structured summaries work better than full traces for selection, pairwise recursive comparisons work better than flat many-way comparisons, and refining from multiple prior summaries works better than refining from one.

## Results
- Main full-pipeline gains on **SWE-Bench Verified**: Claude-4.5-Opus **70.94% → 77.60%** (+6.66), Gemini-3.1-Pro **72.25% → 76.60%** (+4.35), Claude-4.5-Sonnet **67.41% → 75.60%** (+8.19), Gemini-3-Flash **70.79% → 76.00%** (+5.21), GPT-5-0825 **61.41% → 69.80%** (+8.39).
- Main full-pipeline gains on **Terminal-Bench v2.0**: Claude-4.5-Opus **46.95% → 59.09%** (+12.14), Gemini-3.1-Pro **52.49% → 64.77%** (+12.28), Claude-4.5-Sonnet **40.62% → 56.82%** (+16.20), Gemini-3-Flash **37.93% → 48.86%** (+10.93), GPT-5-0825 **31.32% → 38.64%** (+7.32).
- **RTV** alone already helps. Example: Claude-4.5-Sonnet improves on SWE-Bench Verified **67.4% → 73.6%** and on Terminal-Bench v2.0 **40.6% → 54.6%** with **N=16, G=2, V=8**.
- In sequential refinement on 100 sampled SWE-Bench Verified tasks, Gemini-3.1-Pro improves from **72.69% → 73.75%** with single-rollout refinement, **72.69% → 76.94%** with random-**K** refinement, and **72.69% → 79.25%** with **RTV**-selected **K=4** summaries. Claude-4.5-Sonnet reaches **78.06%** with select-**K** refinement.
- Context quality predicts next-iteration success. With **K=4** selected prior rollouts, iteration-1 pass rates rise to about **97.3%** for Claude-4.5-Sonnet and **99.7%** for Gemini-3.1-Pro when the refinement context contains **4/4** passing rollouts.
- Sequential refinement also reduces average agent steps by about half in Table 4 while improving pass@1, and the paper states the method solves some tasks that none of the initial **16** rollouts solved.

## Link
- [http://arxiv.org/abs/2604.16529v1](http://arxiv.org/abs/2604.16529v1)
