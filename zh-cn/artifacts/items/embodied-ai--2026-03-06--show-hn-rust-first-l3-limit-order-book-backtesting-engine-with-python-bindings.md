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
language_code: zh-CN
---

# Show HN: Rust-First L3 Limit Order Book Backtesting Engine with Python Bindings

## Summary
这是一个**Rust 优先的 L3 限价订单簿回测引擎**，并提供 Python 绑定，面向高频/微观结构研究与策略回放。它强调确定性重放、订单簿撮合、数据转换与研究辅助工具的一体化工作流。

## Problem
- 解决 **L3（逐笔订单级）市场数据回测** 的工程问题：如何高效导入原始订单簿数据、准确重建撮合过程，并让研究者能稳定复现实验结果。
- 这很重要，因为高频交易和订单流策略高度依赖 **真实队列位置、撤单、成交与微观结构动态**；如果回测不精确，策略评估会失真。
- 现有研究流程常在性能、可重复性和 Python 研究便利性之间取舍，而该项目试图同时覆盖这三点。

## Approach
- 用 **Rust 实现核心引擎**：包括 L3 parquet ingestion、limit order book、matching engine 和 deterministic replay/backtesting，以获得更高性能和更可控的执行语义。
- 通过 **Python bindings** 暴露统一接口，让用户可以直接在 Python 中编写策略、调用回测、批量运行和分析结果。
- 提供 **callback policy controls** 和多种示例策略/风险配置（如 QueueImbalanceScalper、FlowMicropriceScalper、CumulativeFlowMomentum），便于快速验证微观结构信号。
- 提供 **CoinAPI LIMITBOOK 到 canonical engine parquet 的本地转换脚本**，并附带 schema 校验、回放验证、可视化、指标与风险报告工具，形成端到端研究流水线。

## Results
- 文本**没有提供正式论文式定量结果**，未报告诸如收益、Sharpe、吞吐量、延迟或与其他回测引擎的基准对比数字。
- 给出的最具体能力声明包括：支持 **L3 parquet ingestion、订单簿与撮合、确定性 replay/backtesting、Python 策略绑定、指标/绘图/研究辅助**。
- 提供了可执行基准入口 **`cargo bench --bench throughput`**，说明作者关注吞吐测试，但摘录中**没有给出具体 benchmark 数值**。
- 提供样例与验证工作流，如 **`validate_engine_run.py`**、**`run_l3_backtest(...)`**、**`run_l3_backtest_with_trace(...)`**，支持从 CoinAPI 原始 LIMITBOOK 文件构建 parquet 并进行回测验证。
- 项目还声明支持多种“实时/在线”运行接口，如 **`run_live_event_stream(...)`**、**`run_live_channel_runtime(...)`** 等，但摘录中**没有量化其实时性能或稳定性**。

## Link
- [https://github.com/chasemetoyer/Backtesting-Engine](https://github.com/chasemetoyer/Backtesting-Engine)
