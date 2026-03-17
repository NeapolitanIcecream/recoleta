---
source: hn
url: https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data
published_at: '2026-03-12T23:06:59'
authors:
- boxer_shorts
topics:
- bigquery
- anomaly-detection
- timesfm
- data-observability
- dbt
relevance_score: 0.58
run_id: materialize-outputs
---

# Catching silent data loss using BigQuery's native ML and Write API

## Summary
本文介绍了一个仅依赖 BigQuery 原生能力与 dbt 的数据量异常检测方案，用于发现“流水线成功但数据悄悄少了”的静默数据丢失。它面向数百张表统一工作，无需外部监控系统，也无需自训模型。

## Problem
- 解决的问题是：数据管道虽然执行成功，但实际落表行数显著低于正常水平，尤其是部分缺失（如少 20%）往往不易被发现。
- 这很重要，因为这类问题不会让仪表盘直接报废，业务仍会看到“看似合理”的数字，导致错误数据被持续消费数天。
- 需求约束包括：不能为每张表单独写规则，不能引入额外监控基础设施，也不希望训练和维护自定义 ML 模型。

## Approach
- 以 BigQuery 的 `INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT` 作为唯一核心信号源，记录每张表何时被写入、写了多少行、是否报错；再将其物化为 dbt 增量表，按小时刷新以保留更长历史并提升查询性能。
- 自动为每张表做画像，基于至少 **21 天**历史、变异系数、活跃度和最大写入间隔，决定其是否适合做检测，以及该用 **1/2/3/4/6/8/12/24 小时**中的哪种观测窗口。
- 构造“稠密时间网格”：即便某个窗口完全没有数据，也通过窗口 spine + `LEFT JOIN` + `COALESCE(...,0)` 保证生成 `actual_rows = 0`，避免零写入窗口在聚合时直接消失。
- 使用 BigQuery ML 的 `AI.DETECT_ANOMALIES` 与 **TimesFM 2.5** 做时序异常检测：对每张表独立建模（`id_cols=['table_fqn']`），采用 **28 天**训练窗口，并对输入做 `LOG10(raw_volume + 100)` 变换以压缩量级差异。
- 为减少误报，只检测“下降”不检测“上升”，并叠加节假日抑制、绝对显著性阈值（低于峰值的 **0.1%** 不报）、相对偏差阈值（低于 **25%** 不报）、表级概率阈值（默认 **0.99**）以及连续异常窗口确认机制；最终输出 `WARNING/ERROR/CRITICAL` 等严重度而非单一布尔值。

## Results
- 方案已在 Nordnet 的环境中应用于 **200+ Pub/Sub BigQuery subscriptions** 背后的 **数百张 BigQuery 表** 进行统一监控。
- 检测资格要求至少 **21 天**历史；模型采用 **28 天**历史作为训练上下文；增量任务每小时运行一次，并在每次运行时回看最近 **2 天**以修正延迟到达数据。
- 默认检测配置非常保守：BigQuery ML 全局异常概率阈值示例为 **0.95**，而表级默认阈值进一步提高到 **0.99**，以优先压低误报。
- 对高频小窗口（**1–4 小时**）数据，系统要求连续两个异常窗口才升级为正式告警；对 **6+ 小时**窗口默认不要求连续确认，以平衡灵敏度与噪声。
- 文中没有提供标准基准数据集上的精确评测指标、召回率/精确率或与其他方法的数值对比；最强的具体主张是：该方案能在**无外部服务、无自定义训练、零配置默认可用**的前提下，以**约 1–2 小时**的最快检测延迟覆盖大规模表级数据量异常。

## Link
- [https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data](https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data)
