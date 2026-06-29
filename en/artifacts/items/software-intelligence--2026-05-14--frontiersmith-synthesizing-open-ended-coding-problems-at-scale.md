---
source: arxiv
url: https://arxiv.org/abs/2605.14445v1
published_at: '2026-05-14T06:39:42'
authors:
- Runyuan He
- Qiuyang Mang
- Shang Zhou
- Kaiyuan Liu
- Hanchen Li
- Huanzhi Mao
- Qizheng Zhang
- Zerui Li
- Bo Peng
- Lufeng Cheng
- Tianfu Fu
- Yichuan Wang
- Wenhao Chai
- Jingbo Shang
- Alex Dimakis
- Joseph E. Gonzalez
- Alvin Cheung
topics:
- code-intelligence
- coding-data-synthesis
- open-ended-coding
- llm-training
- software-foundation-models
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale

## Summary
FrontierSmith turns closed-ended competitive programming tasks into open-ended optimization-style coding problems for training LLM coders. The paper claims that 200 synthesized problems improve Qwen3.5 models on FrontierCS and ALE-bench.

## Problem
- Many real coding tasks have no known optimal solution and need continuous scoring, while most LLM coding training uses binary pass/fail tasks.
- Open-ended coding data is scarce and costly because each problem needs an objective, test cases, and a verifier that can score solution quality.
- The gap matters because open-ended benchmarks remain hard: FrontierCS reports human experts at 95.41 on algorithmic tasks versus 29.37 for Gemini 3.0 Pro, and FrontierCS and ALE-bench contain only about 240 and 40 human-curated problems.

## Approach
- FrontierSmith starts with closed-ended competitive programming problems and mutates them by changing goals, restricting valid outputs, or generalizing inputs.
- These mutations convert exact-answer tasks into optimization tasks where solvers can use different heuristics and receive continuous scores.
- A coarse LLM judge filters candidates for open-endedness, then an idea divergence metric keeps problems where sampled solutions use different core algorithms.
- The system estimates idea divergence first with pairwise LLM judgments, then with distances between verifier score vectors across generated test cases.
- Separate agents generate test cases and scoring verifiers, cross-check them, and validated problems enter the seed pool for later synthesis rounds.

## Results
- Training Qwen3.5-9B with GRPO on 200 synthesized problems improves FrontierCS by +8.82 points and ALE-bench by +306.36 Elo-rating-based performance.
- Training Qwen3.5-27B improves FrontierCS by +12.12 points and ALE-bench by +309.12.
- Compared with closed-ended HardTests, FrontierSmith training is higher by +5.24 on FrontierCS and +236.40 on ALE-bench.
- Compared with random rewards, FrontierSmith training is higher by +7.58 on FrontierCS and +256.76 on ALE-bench.
- Removing the idea-divergence filter drops FrontierCS performance by 2.05 points, which supports the filter's value in selecting training problems.
- The paper also reports that synthesized problems make agents use more turns and tokens, matching behavior seen on human-curated open-ended problems, but the excerpt does not give exact turn or token counts.

## Link
- [https://arxiv.org/abs/2605.14445v1](https://arxiv.org/abs/2605.14445v1)
