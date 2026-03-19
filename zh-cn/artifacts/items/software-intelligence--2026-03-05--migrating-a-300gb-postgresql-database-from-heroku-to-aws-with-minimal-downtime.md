---
source: hn
url: https://argos-ci.com/blog/heroku-to-aws-migration
published_at: '2026-03-05T23:19:37'
authors:
- neoziro
topics:
- postgresql-migration
- heroku-to-aws
- logical-replication
- minimal-downtime
- database-operations
relevance_score: 0.29
run_id: materialize-outputs
language_code: zh-CN
---

# Migrating a 300GB PostgreSQL database from Heroku to AWS with minimal downtime

## Summary
这是一篇工程实践型文章，介绍 Argos 如何将接近 300GB 的 PostgreSQL 从 Heroku 迁移到 AWS，并把停机时间压到极低。核心价值在于给出一个可复用的大规模数据库迁移方案，尤其适用于 Heroku 到 RDS 的受限迁移场景。

## Problem
- 需要把一个接近 **300GB**、包含约 **2.5 亿行**大表的生产 PostgreSQL 数据库从 Heroku 迁到 AWS，同时尽量避免影响线上服务。
- Heroku 在大规模场景下限制较多：难以直接做 publication/subscription 复制、配置与升级控制不足、扩容与成本模型不灵活。
- 该问题重要，因为数据库是核心生产系统，迁移失败或停机过长会直接影响用户写入、业务连续性、性能和成本。

## Approach
- 采用 **两阶段迁移**：先把 Heroku 的 WAL 归档恢复到一台临时 **EC2 PostgreSQL**，再从 EC2 用 **PostgreSQL logical replication** 同步到 **AWS RDS**。
- 第一阶段通过 `wal-e` 从 Heroku 暴露的 S3 WAL 归档拉取基设备份与日志，并手动重建缺失的 `backup_label` 与 `tablespace_map`，使 EC2 能进入 recovery 并追平到 Heroku。
- 当 EC2 追平后，在维护窗口内短暂阻塞写入，将 EC2 **promote** 为主库，并把 Heroku 应用的 `DATABASE_URL` 切到 EC2，从而实现从 Heroku 到 EC2 的低停机切换。
- 第二阶段在 EC2 上创建 publication，在 RDS 上创建 subscription，先复制全量数据，再持续同步增量变更；最终在第二个维护窗口中确认无复制延迟后切换到 RDS。
- 由于 logical replication 不复制 sequence 值，作者额外运行脚本在 RDS 上对各序列执行 `setval()` 校准，避免主键冲突。

## Results
- 成功迁移了一个接近 **300GB** 的 PostgreSQL 生产库，其中 `screenshots` 表约 **2.5 亿行**。
- 从 Heroku S3 下载约 **300GB** 基设备份耗时约 **45 分钟**；RDS 通过 logical replication 完成约 **300GB** 初始复制耗时约 **8 小时**。
- 整个切换被拆成 **两个维护窗口**，每次大约 **1 分钟**，文中明确称 Heroku → EC2 的主切换仅用 **几分钟**，实现了“minimal downtime”。
- 迁移后作者声称获得了 **更好的性能、更低的成本、以及更强的运维控制力**，但文中**没有提供**迁移前后性能或成本节省的量化对比数据。
- 文章的最强具体贡献不是新算法，而是一个可执行 playbook：**Heroku WAL 归档恢复到 EC2 + EC2 作为桥接主库 + 逻辑复制入 RDS + 手动同步 sequences**。

## Link
- [https://argos-ci.com/blog/heroku-to-aws-migration](https://argos-ci.com/blog/heroku-to-aws-migration)
