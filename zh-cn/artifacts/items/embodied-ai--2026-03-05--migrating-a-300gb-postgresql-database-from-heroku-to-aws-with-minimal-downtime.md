---
source: hn
url: https://argos-ci.com/blog/heroku-to-aws-migration
published_at: '2026-03-05T23:19:37'
authors:
- neoziro
topics:
- postgresql-migration
- aws-rds
- heroku-postgres
- logical-replication
- minimal-downtime
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Migrating a 300GB PostgreSQL database from Heroku to AWS with minimal downtime

## Summary
这是一篇工程迁移复盘，介绍如何将一个接近 300GB 的 PostgreSQL 生产库从 Heroku 迁移到 AWS，并将写停机时间压到约 1 分钟级别。核心贡献不是新算法，而是一套可复用的两阶段迁移方案：先用 EC2 承接 Heroku 的 WAL 恢复，再用逻辑复制迁入 RDS。

## Problem
- 解决的问题：如何把一个约 **300GB**、含约 **2.5 亿行**大表的 PostgreSQL 生产数据库从 **Heroku** 平滑迁到 **AWS**，同时尽量减少业务停机。
- 为什么重要：数据库是核心生产系统，迁移若出错会导致数据丢失、长时间停服或主键冲突；同时 Heroku 在该规模下存在**成本高、调优受限、复制路径受限**等问题。
- 具体难点：Heroku 不直接提供简单的 publication/subscription 迁移路径；RDS 又**不支持物理 WAL 流复制**，因此必须设计中间桥接方案。

## Approach
- 采用**两阶段迁移**：先在 **EC2** 上恢复 Heroku 的 base backup 和 WAL，追平后把 EC2 提升为主库，并让 Heroku 应用先切到 EC2。
- 第二阶段从 EC2 到 **RDS** 使用 PostgreSQL **logical replication**：在 EC2 建 publication，在 RDS 建 subscription，先全量复制再持续同步增量。
- 为了让 Heroku 备份可恢复，团队用 **wal-e/wal-g** 从 S3 拉取数据，并从 Heroku 的 sentinel JSON 中**重建 `backup_label` 和 `tablespace_map`**，这是恢复成功的关键步骤。
- 切换时通过两个维护窗口冻结写入，分别在 **Heroku→EC2** 和 **EC2→RDS** 进行最终追平；由于逻辑复制**不复制 sequence 值**，最后额外运行脚本同步序列，避免主键冲突。

## Results
- 迁移数据规模：生产库接近 **300GB**，其中 `screenshots` 表约 **2.5 亿行**。
- 基础备份拉取耗时：从 Heroku S3 下载约 **300GB** 数据到 EC2 用时约 **45 分钟**。
- RDS 全量复制耗时：通过 logical replication 将约 **300GB** 数据从 EC2 复制到 RDS 用时约 **8 小时**，之后进入仅同步增量的 replicating 状态。
- 停机时间：整个迁移拆成 **两个维护窗口**，每次约 **1 分钟**；文中还提到 Heroku→EC2 这一关键切换仅需**几分钟**，实现了最小化停机。
- 资源配置：RDS 使用 **db.m6g.xlarge（4 vCPU, 16GB RAM）**；桥接 EC2 使用 **t3.xlarge（4 vCPU, 16GB RAM, 300GB io1）**。
- 结论性收益：作者声称迁移后获得了**更好的性能、更低的成本和更强的运维控制权**；但文中**没有提供**如延迟下降百分比、吞吐提升或成本节省比例等严格量化对比数据。

## Link
- [https://argos-ci.com/blog/heroku-to-aws-migration](https://argos-ci.com/blog/heroku-to-aws-migration)
