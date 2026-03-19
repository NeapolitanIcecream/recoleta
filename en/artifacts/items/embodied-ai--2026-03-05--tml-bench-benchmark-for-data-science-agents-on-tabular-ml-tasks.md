---
source: arxiv
url: http://arxiv.org/abs/2603.05764v1
published_at: '2026-03-05T23:48:41'
authors:
- Mykola Pinchuk
topics:
- benchmark
- data-science-agents
- tabular-ml
- llm-agents
- kaggle-style-evaluation
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# TML-Bench: Benchmark for Data Science Agents on Tabular ML Tasks

## Summary
TML-bench is a benchmark for data science agents on tabular machine learning tasks, with a focus on measuring **performance, reliability, and stability under time constraints** in Kaggle-style end-to-end workflows. The paper evaluates 10 open-source LLMs under a unified protocol, repeating runs across 4 competitions and 3 time budgets and scoring them on a private holdout set.

## Problem
- Many existing agent evaluations focus only on isolated coding ability and fail to capture key failure modes in real data science workflows: reading data, feature processing, training, iteration, and generating a valid submission file.
- A single “lucky successful run” does not represent practical value; in real use, what matters more is **whether the agent can reliably produce a valid submission within the time limit and achieve a good score**.
- Different tasks use different metrics (such as AUC and RMSE), and time budgets are constrained, making cross-task and cross-model comparisons difficult to keep fair and reproducible, which is important for real-world model selection.

## Approach
- Introduces **TML-bench**: a strict Kaggle-style tabular ML benchmark using 4 competitions and 3 time budgets (240s, 600s, 1200s), with a unified agent instruction template and a single execution harness (Kilo Code).
- For each `(competition, model, budget)` combination, it takes the **first 5 successful runs**, and uses their median as the final score for that setting; success is defined as producing a **properly formatted submission** and obtaining a valid score on **private holdout labels invisible to the agent**.
- To address the incomparability of metrics across tasks, scores are first converted to a unified “higher is better” direction, then **min-max normalized** within each `(competition, budget)` to build an overall leaderboard.
- The main leaderboard uses an aggregation method of “**for each competition, take the model’s best budget**, then average across the 4 competitions”; it also reports success rate, IQR stability, cross-competition consistency, and scaling with changing time budgets.
- To reduce contamination risk, internet access is disabled during runs, and only models with a **knowledge cutoff earlier than the competition start time** are selected.

## Results
- The paper evaluates **10 OSS LLMs** across **4 competitions × 3 time budgets = 12** settings; each setting requires **5 successful runs**, so each included model must complete full coverage.
- **MiniMax-M2.1-TEE** achieves the **best overall performance across the four competitions** under the paper’s main aggregation metric; the abstract and results section do not provide a single overall numeric score, but explicitly identify it as the aggregate leader.
- Longer time usually helps, but not always monotonically: among **40 model×competition scaling curves**, only **23/40 = 57.5%** satisfy non-degradation from **240s→600s→1200s**; by model median, the share of monotonic competitions is **62.5%**.
- On the specific task `bank-customer-churn-ict-u-ai`, the strongest median at 1200s is **AUC = 0.928000** (GPT OSS 120B TEE), while the strongest median at 240s is **AUC = 0.926671** (MiniMax-M2.1-TEE); on the same task, one weak setting reaches only **0.813105** (NVIDIA-Nemotron-3-Nano, 1200s).
- For `foot-traffic-wuerzburg-retail-forecasting-2-0`, MiniMax-M2.1-TEE is best at all three budget levels, with **RMSE = 0.066846 / 0.065770 / 0.065489** (240s/600s/1200s); GLM 4.7 Flash shows clear instability at 1200s, with **median 0.107502, IQR 0.070186..0.221725**.
- For `playground-series-s5e10`, results are very close at 1200s, with the best **RMSE = 0.056190** (GLM-4.6-FP8). For `playground-series-s6e1`, MiniMax-M2.1-TEE leads at 1200s with **RMSE = 8.699779**; TNG-R1T2-Chimera shows an anomaly at 600s, with **median 10.199380, IQR 9.088197..13.444163**.

## Link
- [http://arxiv.org/abs/2603.05764v1](http://arxiv.org/abs/2603.05764v1)
