---
source: arxiv
url: http://arxiv.org/abs/2603.05764v1
published_at: '2026-03-05T23:48:41'
authors:
- Mykola Pinchuk
topics:
- benchmarking
- data-science-agents
- tabular-ml
- llm-agents
- reliability-evaluation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# TML-Bench: Benchmark for Data Science Agents on Tabular ML Tasks

## Summary
TML-bench is a benchmark for data science agents on tabular machine learning tasks, focused on evaluating models’ **correctness, reliability, and performance under time limits** in Kaggle-style end-to-end workflows. Rather than looking only at a single best result, it compares the stable capabilities of 10 open-source/open-weight LLMs in real tabular ML workflows through repeated runs, private holdout scoring, and cross-task normalization.

## Problem
- Many existing benchmarks test only local coding ability or a single lucky run, and cannot reflect whether a data science agent can truly **complete an end-to-end tabular ML workflow within a fixed time budget**.
- Different Kaggle tasks use different metrics (such as AUC and RMSE), making direct horizontal comparison difficult; meanwhile, a single result also hides **success rates and run-to-run variability**.
- This matters because in real use, users need not just agents that “sometimes get it right,” but agents that can **consistently produce valid submissions and achieve reproducible scores**.

## Approach
- The authors introduce **TML-bench**: a strict Kaggle-style benchmark for tabular tasks, covering **4 competitions × 3 time budgets (240s, 600s, 1200s)** and evaluating **10 models**.
- Each model is **repeatedly run until 5 successful samples** are obtained for each task and budget; the reported value is the **median** of the “earliest 5 successful runs,” rather than the single best run.
- Runs are executed with a unified harness via **Kilo Code**: they are run under time limits in a clean workspace, submission format is checked automatically, and scoring is performed on **private hidden labels not visible to the agent**, ensuring end-to-end correctness.
- To enable cross-task comparison, the authors first unify different metrics into a “higher is better” direction, then apply **min-max normalization** within each task/budget setting; the main leaderboard uses an aggregation method of “**take the best budget for each competition, then average across the 4 competitions**.”
- To reduce contamination risk, **internet access is disabled** during evaluation, and only models whose **knowledge cutoff predates the competition release** are selected.

## Results
- Under the main aggregate metric, **MiniMax-M2.1-TEE** delivers the best overall performance on **4/4 competitions**, making it the paper’s claimed top model on the overall leaderboard.
- Longer time budgets help overall, but the gains are not always smooth: among **40 model×competition scaling curves**, only **23/40 = 57.5%** are monotonic non-worsening; the median monotonicity rate aggregated by model is **62.5%**, indicating that “more time leads to better results” remains noisy at the current number of repetitions.
- Specific task results: on **bank-customer-churn-ict-u-ai**, the strongest median at **1200s** is **AUC = 0.928000** (GPT OSS 120B TEE), while the strongest at **240s** is **0.926671** (MiniMax-M2.1-TEE); on the same task, Nemotron-3-Nano reaches only **0.813105** at 1200s, showing a clear gap.
- On **foot-traffic-wuerzburg-retail-forecasting-2-0**, **MiniMax-M2.1-TEE** is best at all three budgets: **RMSE 0.066846 / 0.065770 / 0.065489** (240s/600s/1200s). Meanwhile, **GLM 4.7 Flash** has a median of **0.107502** at 1200s, with an IQR of **0.070186..0.221725**, showing significant instability.
- On **playground-series-s5e10**, results at **1200s** are extremely close, with the best being **RMSE 0.056190** (GLM-4.6-FP8), and many models differ by only **a few 1e-4**, indicating that the top models are already very close on this task.
- On **playground-series-s6e1**, **MiniMax-M2.1-TEE** achieves the best **RMSE 8.699779** at **1200s**; meanwhile, **TNG-R1T2-Chimera** shows a clear failure mode at **600s**, with a median of **10.199380** and IQR **9.088197..13.444163**. The paper does not provide a unified numeric table of overall leaderboard scores, but it clearly emphasizes that there is substantial divergence among **performance, success rate, and stability**.

## Link
- [http://arxiv.org/abs/2603.05764v1](http://arxiv.org/abs/2603.05764v1)
