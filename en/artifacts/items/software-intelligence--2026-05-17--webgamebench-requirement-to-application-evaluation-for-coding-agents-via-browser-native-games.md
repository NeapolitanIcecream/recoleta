---
source: arxiv
url: https://arxiv.org/abs/2605.17637v1
published_at: '2026-05-17T20:07:12'
authors:
- Wenyu Zhang
- Guoliang You
- Tianlun
- Haotian Zhao
- Tianshu Zhu
- Haoran Wang
- Xiaoxuan Tang
- Mingyang Dai
- Jingnan Gu
- Daxiang Dong
- Jianmin Wu
topics:
- coding-agents
- software-benchmark
- browser-games
- runtime-evaluation
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games

## Summary
WebGameBench evaluates coding agents by checking whether the delivered browser game works in a real browser, not just whether the code builds. The paper shows a large gap between playable delivery and full requirement satisfaction.

## Problem
- Coding-agent benchmarks often score functions, repository patches, terminal traces, or build results, while users receive an application that may load and still fail its runtime requirements.
- Browser-native games expose many failure modes in a small app: input handling, spatial mapping, rules, state changes, scoring, win/loss conditions, restart flow, and visible feedback.
- This matters for automated software production because an agent that ships a loadable page can still miss the behavior described in the requirement.

## Approach
- The benchmark has 111 frozen Structured WebGame Specification tasks across 7 gameplay families.
- Each agent gets one standardized generation attempt, builds a browser-native source artifact, and exposes it as a local browser URL.
- A Codex-based runtime evaluator controls Chrome through Playwright, interacts with the game, and labels it Excellent, Usable, or Unusable.
- The evaluator judges observable browser behavior against the same specification used by the coding agent.
- Tasks also include functional-point metadata and D1-D4 difficulty labels based on specification structure and rule depth.

## Results
- Across 111 tasks, 12 coding agents, and 14 evaluation configurations, the best configuration, opus-4-7, reached 76.9% usable rate and 20.2% excellent rate with 93.7% coverage.
- opus-4-6 reached 73.0% usable and 19.0% excellent; gpt-5-5 reached 63.6% usable and 16.4% excellent; gemini-3.1-pro reached 63.6% usable and 15.9% excellent.
- Lower-scoring configurations ranged from 38.3% to 52.8% usable rate, with kimi-k2.5 at 38.3% usable and 8.4% excellent.
- Difficulty stratification showed pooled usable rates of 73.7% for D1, 76.1% for D2, 52.1% for D3, and 12.6% for D4.
- On a 43-artifact human-review set, binary usable-rate agreement improved with evaluator reasoning effort: Medium scored 66.7% accuracy and 65.9% macro-F1, High scored 82.1% and 80.8%, and XHigh scored 85.0% and 82.9%.
- Exact three-way agreement under XHigh was lower at 50.0% accuracy and 50.5% macro-F1, mainly due to disagreements between Excellent and Usable labels.

## Link
- [https://arxiv.org/abs/2605.17637v1](https://arxiv.org/abs/2605.17637v1)
