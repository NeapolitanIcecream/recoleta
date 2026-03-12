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
---

# Show HN: Rust-First L3 Limit Order Book Backtesting Engine with Python Bindings

## Summary
这是一个以 Rust 为核心、带 Python 绑定的 L3 限价订单簿回测引擎，面向高保真、确定性回放与策略研究。它把原始 CoinAPI LIMITBOOK 数据转换为统一 parquet，并提供撮合、回放、策略接口和分析工具。

## Problem
- 解决的是 **L3 级订单簿数据回测** 的工程问题：如何从原始逐笔订单簿事件中，稳定地重建撮合过程并进行可重复的策略评估。
- 这很重要，因为低保真或非确定性的回测会误估高频/微观结构策略表现，尤其影响排队、撤单、流动性与成交模拟。
- 研究与生产常常需要同时具备高性能核心和易用的策略开发接口；单一语言栈通常难兼顾两者。

## Approach
- 用 **Rust 实现核心引擎**：包括 L3 parquet 读取、限价订单簿与撮合引擎、确定性 replay/backtesting，以及回调策略控制。
- 用 **Python 暴露通用策略绑定**，让研究者可以直接调用 `run_l3_backtest(...)`、`run_l3_backtest_with_trace(...)` 等接口，并结合 pandas/pyarrow 做分析。
- 提供 **数据标准化管线**：把本地已下载的 CoinAPI LIMITBOOK `csv.gz` 转成引擎使用的 canonical parquet，便于统一验证和复现实验。
- 提供 **内置策略与研究辅助组件**，如 QueueImbalance、FlowMicroprice、CumulativeFlowMomentum、风险画像、收益曲线、回撤、尾部损失、预测力计算等。
- 通过测试、验证脚本、可视化与 benchmark 命令，强调行为一致性、可检查性和回放调试能力。

## Results
- 文本**没有给出正式论文式定量结果**，未报告明确的收益、Sharpe、延迟、吞吐或相对基线提升数字。
- 可确认的具体能力包括：支持 **L3 parquet ingestion**、**limit order book and matching engine**、**deterministic replay/backtesting**、**Python strategy bindings**。
- 暴露了多种运行接口与产物，例如 `RunSummary`、`ReplayTrace`、`run_live_event_stream(...)`、`run_live_channel_runtime(...)`，表明不仅支持离线回测，也面向实时事件流测试。
- 提供 `cargo bench --bench throughput` 作为吞吐基准入口，但摘录中**未提供 benchmark 数值**。
- 提供 Rust/Python 双侧测试、样例 fixture、验证脚本和回放可视化脚本，最强的实证性主张是其 **可确定性复现、可验证、可视化调试** 的研究工作流。

## Link
- [https://github.com/chasemetoyer/Backtesting-Engine](https://github.com/chasemetoyer/Backtesting-Engine)
