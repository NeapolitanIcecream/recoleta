---
source: hn
url: https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data
published_at: '2026-03-12T23:06:59'
authors:
- boxer_shorts
topics:
- bigquery-ml
- anomaly-detection
- data-quality
- timeseries-monitoring
- dbt
relevance_score: 0.02
run_id: materialize-outputs
---

# Catching silent data loss using BigQuery's native ML and Write API

## Summary
这篇文章提出了一个仅依赖 BigQuery 原生能力与 dbt 的数据量异常检测方案，用于发现“流水线成功但数据悄悄少了”的静默数据丢失。核心价值是在不引入外部监控、不过度配置、也不自训模型的前提下，批量监控数百张表的写入量异常。

## Problem
- 解决的问题是：数据管道即使执行成功，也可能只写入了部分数据甚至 0 行，而这类**部分丢失**往往比完全中断更难被发现。
- 这很重要，因为仪表盘仍然能显示、数值看起来也“合理”，企业可能在数天内持续基于错误数据做决策。
- 作者需要一个可扩展方案，能对 **200+ BigQuery Pub/Sub subscriptions** 背后的数百张表自动检测写入量偏离，而不需要逐表写规则、外部监控系统或自定义 ML 训练。

## Approach
- 核心机制很简单：直接利用 BigQuery 自动提供的 `INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT` 作为每张表的“写入量信号”，把每次写入的时间、表名、行数、错误码等物化成 dbt 增量表。
- 然后为每张表建立固定时间窗（1/2/3/4/6/8/12/24 小时）的**稠密时间网格**，即使某个窗口完全没有数据，也强制生成一行并记为 `actual_rows = 0`，避免“没数据就看不见”的盲区。
- 在这些窗口化后的时间序列上，调用 BigQuery 原生 `AI.DETECT_ANOMALIES`，使用 **TimesFM 2.5** 做异常检测；输入是按表分组的 `log_volume = LOG10(raw_volume + 100)`，并采用 **28 天训练窗口**学习每张表的周期模式。
- 系统采用三层配置：默认参数、BigQuery table labels、seed overrides；同时自动做表画像（如 `history_days >= 21`、`cv_score`、`liveness_score`、`max_gap_hours`），为不同表选择合适窗口和阈值。
- 为减少误报，作者只检测“下降”不检测“上升”，并叠加节假日抑制、绝对差异过滤（低于峰值 **0.1%** 忽略）、相对差异过滤（低于 **25%** 忽略）、逐表阈值（默认 **0.99**）以及连续窗口确认机制。

## Results
- 文中给出的部署规模是：在 Nordnet 环境中监控 **200+ Pub/Sub BigQuery subscriptions** 和**数百张 BigQuery 表**，并以**单个 dbt 模型**小时级运行完成检测。
- 训练与检测设置上，系统要求表至少有 **21 天历史** 才有资格进入检测；模型使用 **28 天训练窗口**，按小时增量运行，并在每次运行时回看最近 **2 天** 以修正延迟到达数据。
- 监控延迟方面，作者称最快检测时延约为 **1–2 小时**：一个窗口先结束，再由下一次小时级调度完成评估；更大窗口会带来更长延迟。
- 误报控制方面，默认使用 BigQuery `AI.DETECT_ANOMALIES` 的全局 `anomaly_prob_threshold = 0.95`，再叠加逐表默认阈值 **0.99**、相对偏差 **25%**、绝对偏差 **0.1% peak volume** 等规则，以“宁可漏报一些，也要显著压低误报”为设计目标。
- 成本与工程复杂度方面，作者明确声称该方案**不需要外部监控服务、不需要自定义模型训练/托管、不需要额外基础设施**，仅依赖 BigQuery + dbt 即可落地。
- 文中**没有提供标准数据集上的定量精度指标**（如 precision/recall/F1、AUC）或与其他方法的系统性对比；最强的结果声明是该方案已在生产中以低成本、零外部基础设施方式覆盖数百表，并能检测上游中断、部分交付和 schema change 引发的量变异常。

## Link
- [https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data](https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data)
