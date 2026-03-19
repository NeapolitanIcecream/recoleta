---
source: hn
url: https://github.com/chasemetoyer/Backtesting-Engine
published_at: '2026-03-06T23:17:29'
authors:
- chasemetoyer
topics:
- rust
- limit-order-book
- backtesting
- python-bindings
- market-microstructure
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Show HN: Rust-First L3 Limit Order Book Backtesting Engine with Python Bindings

## Summary
This is a Rust-core L3 limit order book backtesting engine with Python bindings, aimed at high-fidelity, deterministic replay and strategy research. It converts raw CoinAPI LIMITBOOK data into a unified parquet format and provides matching, replay, strategy interfaces, and analysis tools.

## Problem
- It addresses the engineering problem of **L3 order book data backtesting**: how to reliably reconstruct the matching process from raw order-level book events and perform repeatable strategy evaluation.
- This matters because low-fidelity or non-deterministic backtests can misestimate the performance of high-frequency/microstructure strategies, especially affecting queue position, cancellations, liquidity, and fill simulation.
- Research and production often need both a high-performance core and an easy-to-use strategy development interface at the same time; a single-language stack usually struggles to optimize for both.

## Approach
- Uses **Rust to implement the core engine**: including L3 parquet reading, limit order book and matching engine, deterministic replay/backtesting, and callback policy controls.
- Uses **Python to expose generic strategy bindings**, allowing researchers to directly call interfaces such as `run_l3_backtest(...)` and `run_l3_backtest_with_trace(...)`, and combine them with pandas/pyarrow for analysis.
- Provides a **data standardization pipeline**: converting locally downloaded CoinAPI LIMITBOOK `csv.gz` files into the canonical parquet used by the engine, making validation and experiment reproduction easier.
- Provides **built-in strategies and research helper components**, such as QueueImbalance, FlowMicroprice, CumulativeFlowMomentum, risk profiles, equity curves, drawdown, tail loss, predictive power computation, and more.
- Emphasizes behavioral consistency, inspectability, and replay debugging through tests, validation scripts, visualization, and benchmark commands.

## Results
- The text **does not provide formal paper-style quantitative results**; it does not report explicit figures for returns, Sharpe, latency, throughput, or improvement over baselines.
- The specific confirmed capabilities include support for **L3 parquet ingestion**, **limit order book and matching engine**, **deterministic replay/backtesting**, and **Python strategy bindings**.
- It exposes a variety of runtime interfaces and artifacts, such as `RunSummary`, `ReplayTrace`, `run_live_event_stream(...)`, and `run_live_channel_runtime(...)`, indicating that it supports not only offline backtesting but also real-time event stream testing.
- It provides `cargo bench --bench throughput` as the entry point for throughput benchmarking, but the excerpt **does not include benchmark numbers**.
- It includes Rust/Python tests, sample fixtures, validation scripts, and replay visualization scripts; its strongest empirical claim is a research workflow that is **deterministically reproducible, verifiable, and visually debuggable**.

## Link
- [https://github.com/chasemetoyer/Backtesting-Engine](https://github.com/chasemetoyer/Backtesting-Engine)
