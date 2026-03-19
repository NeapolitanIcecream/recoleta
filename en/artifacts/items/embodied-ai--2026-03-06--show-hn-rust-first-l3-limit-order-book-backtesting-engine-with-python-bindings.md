---
source: hn
url: https://github.com/chasemetoyer/Backtesting-Engine
published_at: '2026-03-06T23:17:29'
authors:
- chasemetoyer
topics:
- limit-order-book
- backtesting-engine
- market-microstructure
- rust-python-bindings
- high-frequency-trading
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Show HN: Rust-First L3 Limit Order Book Backtesting Engine with Python Bindings

## Summary
This is a **Rust-first L3 limit order book backtesting engine** with Python bindings, aimed at high-frequency/microstructure research and strategy replay. It emphasizes an integrated workflow for deterministic replay, order book matching, data conversion, and research support tools.

## Problem
- It addresses the engineering challenges of **L3 (order-level) market data backtesting**: how to efficiently ingest raw order book data, accurately reconstruct the matching process, and enable researchers to reproduce experimental results reliably.
- This matters because high-frequency trading and order-flow strategies depend heavily on **true queue position, cancellations, fills, and microstructure dynamics**; if the backtest is inaccurate, strategy evaluation becomes distorted.
- Existing research workflows often trade off among performance, reproducibility, and Python research convenience, while this project attempts to cover all three.

## Approach
- It implements the **core engine in Rust**: including L3 parquet ingestion, limit order book, matching engine, and deterministic replay/backtesting, to achieve higher performance and more controllable execution semantics.
- It exposes a unified interface through **Python bindings**, allowing users to write strategies directly in Python, run backtests, execute batches, and analyze results.
- It provides **callback policy controls** and multiple example strategies/risk configurations (such as QueueImbalanceScalper, FlowMicropriceScalper, CumulativeFlowMomentum), making it easier to quickly validate microstructure signals.
- It includes **local conversion scripts from CoinAPI LIMITBOOK to canonical engine parquet**, along with schema validation, replay verification, visualization, metrics, and risk reporting tools, forming an end-to-end research pipeline.

## Results
- The text **does not provide formal paper-style quantitative results**; it does not report metrics such as returns, Sharpe, throughput, latency, or benchmark comparisons with other backtesting engines.
- The most specific capability claims given include support for **L3 parquet ingestion, order book and matching, deterministic replay/backtesting, Python strategy bindings, and metrics/plotting/research helpers**.
- It provides an executable benchmark entry point, **`cargo bench --bench throughput`**, indicating that the author cares about throughput testing, but the excerpt **does not provide specific benchmark numbers**.
- It includes sample and validation workflows such as **`validate_engine_run.py`**, **`run_l3_backtest(...)`**, and **`run_l3_backtest_with_trace(...)`**, supporting the construction of parquet files from raw CoinAPI LIMITBOOK files and backtest validation.
- The project also states support for multiple “live/online” runtime interfaces, such as **`run_live_event_stream(...)`** and **`run_live_channel_runtime(...)`**, but the excerpt **does not quantify their real-time performance or stability**.

## Link
- [https://github.com/chasemetoyer/Backtesting-Engine](https://github.com/chasemetoyer/Backtesting-Engine)
