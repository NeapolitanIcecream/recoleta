---
source: arxiv
url: https://arxiv.org/abs/2606.05920v1
published_at: '2026-06-04T09:24:30'
authors:
- Xin Wang
- Liangtai Sun
- Yaoming Zhu
- Shuang Zhou
- Jiaxing Liu
- Fengjiao Chen
- Lin Qiu
- Xuezhi Cao
- Xunliang Cai
- Licheng Zhang
- Zhendong Mao
topics:
- code-agents
- web-generation
- benchmarking
- iterative-refinement
- user-feedback
- browser-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement

## Summary
Asuka-Bench tests code agents on web app creation when the initial user request is vague and the agent must improve the site over several feedback rounds. It matters because many code benchmarks give complete one-shot specs, while real users reveal missing requirements after seeing a working UI.

## Problem
- It solves an evaluation mismatch: current code-generation benchmarks score one prompt and one answer, so they miss whether an agent can repair a web app after user feedback.
- The problem matters for automated software production because a generated project must handle UI elements, interaction logic, and edge cases as deployed behavior.
- The benchmark hides the full PRD from the code agent and checks browser-rendered behavior against internal criteria, which tests recovery from underspecified intent.

## Approach
- Each task starts with an underspecified web request; the hidden Clarified PRD defines the full requirements and expected behavior.
- A Code Agent builds a web project, a UI Agent deploys and tests it in a browser, and a User LLM turns pass/fail outcomes into natural-language feedback for the next round.
- Evaluation criteria are arranged as a DAG, so tests run only after prerequisite tests pass; feedback lists direct failures instead of downstream symptoms.
- The dataset has 50 web tasks across 6 categories, 784 evaluation tasks, and 2,402 expected outcomes, with presence, functionality, and robustness checks.

## Results
- Across 13 model-runtime configurations, cumulative weighted Task Pass Rate after 3 rounds ranges from 51.8% to 90.1%, a 38.3 percentage-point spread.
- The best reported 3-round result is GPT-5.4 with OpenHands: 52% Project Completion Rate, 90.1% weighted Task Pass Rate, and 95.1% weighted Criteria Pass Rate.
- Claude-4.6-Sonnet with Claude Code reaches 46% Project Completion Rate, 89.4% weighted Task Pass Rate, and 93.6% weighted Criteria Pass Rate after 3 rounds.
- The weakest reported setup is Seed-2.0-Pro with Claude Code: 8% Project Completion Rate, 51.8% weighted Task Pass Rate, and 60.9% weighted Criteria Pass Rate after 3 rounds.
- Feedback helps most in round 2: weighted Task Pass Rate gains about 25 percentage points, while round 3 adds 7 to 13 points.
- The DAG-aware evaluation protocol is reported to raise task fix rates by 10.5 percentage points on average and cut evaluation token cost by 23% to 26%.

## Link
- [https://arxiv.org/abs/2606.05920v1](https://arxiv.org/abs/2606.05920v1)
