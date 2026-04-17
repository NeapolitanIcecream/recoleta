---
source: arxiv
url: http://arxiv.org/abs/2604.04812v1
published_at: '2026-04-06T16:16:24'
authors:
- Yuchen Cao
- Hanlin Zhang
- Jacky Wai Keung
- Yang Chen
- Linqi Song
topics:
- benchmarking
- code-generation
- trading-systems
- iterative-repair
- auditability
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# SysTradeBench: An Iterative Build-Test-Patch Benchmark for Strategy-to-Code Trading Systems with Drift-Aware Diagnostics

## Summary
SysTradeBench is a benchmark for turning natural-language trading strategies into governed, executable code that can be built, tested, and patched across iterations. It measures whether LLMs produce valid trading systems with audit logs, deterministic behavior, leakage checks, and limited semantic drift during repairs.

## Problem
- Existing finance and code benchmarks do not test the full strategy-to-code workflow as auditable software with execution, repair cycles, and drift control.
- A single backtest metric can hide serious failures such as look-ahead leakage, non-determinism, broken risk rules, or missing audit trails.
- This matters in trading because deployed strategy code must follow the intended rules, pass governance checks, and stay reproducible under review.

## Approach
- The benchmark gives each model a standardized strategy document plus frozen machine-checkable semantics for 12 trading strategies.
- Each submission must produce three artifacts: a strategy card, runnable Python strategy code, and structured audit logs tracing signals, risk checks, orders, positions, and P&L.
- A sandboxed executor runs hard validity gates for parsing, schema compliance, execution, determinism, anti-leakage, and audit completeness, then scores four dimensions: spec fidelity, risk discipline, reliability/auditability, and out-of-sample robustness indicators.
- The system supports up to 3 build-test-patch iterations. After each run, the model gets an evidence bundle with failures and scores, but patches are constrained to at most 50 changed lines and checked for semantic drift with checksums, invariants, and regression traces.
- The evaluation covers 17 models, uses frozen 2024-2025 market data across U.S. equities, crypto, and China A-shares, and reports cost-effectiveness alongside quality scores.

## Results
- The paper reports results on 17 models across 12 strategies.
- Top models reach at least 91.7% validity and aggregate scores in the 7.29-7.85 range.
- Evidence-driven iteration improves quality, but it also drives convergence: generated code reaches 95.4% similarity by Iter2 and becomes byte-identical by Iter3.
- The benchmark uses 5 mandatory validity gates plus audit completeness of at least 95%; submissions that fail any gate are excluded from D1-D4 scoring.
- Out-of-sample evaluation in the current paper is limited: D4 uses sampled 10-bar test windows and zero transaction costs, while full 2025 test-split evaluation with 0.1-20 bps cost sweeps is deferred because 1020 backtests would take about 450 CPU-hours.
- The main empirical claim is that LLMs are useful for rapid prototyping and shallow bug fixing, while human quantitative researchers are still needed for critical strategies that need diverse solutions and stronger robustness.

## Link
- [http://arxiv.org/abs/2604.04812v1](http://arxiv.org/abs/2604.04812v1)
