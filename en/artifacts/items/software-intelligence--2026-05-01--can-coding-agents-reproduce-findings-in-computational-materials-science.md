---
source: arxiv
url: https://arxiv.org/abs/2605.00803v1
published_at: '2026-05-01T17:42:12'
authors:
- Ziyang Huang
- Yi Cao
- Ali K. Shargh
- Jing Luo
- Ruidong Mei
- Mohd Zaki
- Zhan Liu
- Wyatt Bunstine
- William Jurayj
- Somdatta Goswami
- Tyrel McQueen
- Michael Shields
- Jaafar El-Awady
- Paulette Clancy
- Benjamin Van Durme
- Nicholas Andrews
- William Walden
- Daniel Khashabi
topics:
- coding-agents
- scientific-reproducibility
- materials-science
- agent-benchmark
- code-intelligence
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Can Coding Agents Reproduce Findings in Computational Materials Science?

## Summary
AutoMat tests whether coding agents can reproduce claim-level results from computational materials science papers. The main finding is negative: the best tested agent succeeds on 54.1% of 85 claims, and paper-only workflow recovery is the hardest case.

## Problem
- Coding agents that pass software engineering benchmarks may fail in computational science because papers omit procedure details, require domain tools, and need scientific judgment.
- The problem matters because an agent can run code and produce plausible files while using the wrong method or evidence.
- Computational materials science is a hard test case because workflows can involve DFT, molecular dynamics, ML models, custom code, HPC jobs, and post-processing.

## Approach
- The authors build AutoMat with 85 claims curated by materials science subject matter experts from real papers.
- Each task gives an agent a claim, paper, metadata, and optional artifacts; hidden expert reproduction steps are kept for evaluation.
- Tasks cover from-paper reproduction, from-artifact reproduction, and from-artifact interpretation.
- Five agent settings are evaluated: an AutoMat-specific orchestrated agent using Claude Sonnet 4.6, Claude Code with Claude Opus 4.6, Claude Code with Claude Sonnet 4.6, Claude Code with Kimi K2.5, and Codex CLI with GPT-5.4.
- A separate evaluator agent inspects traces, logs, files, and reports, then scores runs on a 1-5 scale; success means a score of 4 or 5.

## Results
- Claude Code with Opus 4.6 is best overall, with a mean reproducibility score of 3.52 and a 54.1% success rate across 85 claims.
- Codex CLI with GPT-5.4 is weakest overall, with a mean score of 2.44 and a 23.5% success rate.
- From-paper reproduction has mean scores of 1.5 to 2.2 and near-zero success rates across systems.
- From-artifact reproduction is easier, with mean scores of 3.1 to 4.1 and success rates of 39% to 77%.
- From-artifact interpretation remains uneven, with success rates of 33% to 50%.
- The LLM evaluator is calibrated on 40 SME-scored runs, reaching quadratic-weighted kappa 0.69 and within-1 score accuracy 0.80.

## Link
- [https://arxiv.org/abs/2605.00803v1](https://arxiv.org/abs/2605.00803v1)
