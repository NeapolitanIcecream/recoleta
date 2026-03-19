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
language_code: en
---

# Migrating a 300GB PostgreSQL database from Heroku to AWS with minimal downtime

## Summary
This is an engineering practice article describing how Argos migrated a nearly 300GB PostgreSQL database from Heroku to AWS while keeping downtime extremely low. Its core value is providing a reusable large-scale database migration approach, especially suited to constrained migration scenarios from Heroku to RDS.

## Problem
- The team needed to migrate a production PostgreSQL database of nearly **300GB**, including large tables with about **250 million rows**, from Heroku to AWS while minimizing impact on the live service.
- Heroku has significant limitations at scale: it is difficult to directly use publication/subscription replication, configuration and upgrade control are insufficient, and the scaling and cost model is inflexible.
- This problem matters because the database is a core production system, and a failed migration or excessive downtime would directly affect user writes, business continuity, performance, and cost.

## Approach
- They used a **two-stage migration**: first restoring Heroku WAL archives onto a temporary **EC2 PostgreSQL** instance, then using **PostgreSQL logical replication** from EC2 to **AWS RDS**.
- In the first stage, they used `wal-e` to pull the base backup and logs from the S3 WAL archives exposed by Heroku, and manually rebuilt the missing `backup_label` and `tablespace_map` so EC2 could enter recovery and catch up with Heroku.
- Once EC2 had caught up, they briefly blocked writes during a maintenance window, **promoted** EC2 to primary, and switched the Heroku application's `DATABASE_URL` to EC2, achieving a low-downtime cutover from Heroku to EC2.
- In the second stage, they created a publication on EC2 and a subscription on RDS, first copying the full dataset and then continuously syncing incremental changes; finally, in a second maintenance window, they confirmed there was no replication lag and switched to RDS.
- Because logical replication does not copy sequence values, the author additionally ran a script on RDS to execute `setval()` on each sequence to prevent primary key conflicts.

## Results
- They successfully migrated a production PostgreSQL database of nearly **300GB**, including a `screenshots` table with about **250 million rows**.
- Downloading the roughly **300GB** base backup from Heroku S3 took about **45 minutes**; RDS completed the roughly **300GB** initial copy via logical replication in about **8 hours**.
- The overall cutover was split into **two maintenance windows**, each about **1 minute**; the article explicitly says the main Heroku → EC2 cutover took only **a few minutes**, achieving “minimal downtime.”
- After the migration, the author claims **better performance, lower costs, and stronger operational control**, but the article **does not provide** quantified before-and-after performance or cost-savings data.
- The article’s strongest concrete contribution is not a new algorithm, but an executable playbook: **restore Heroku WAL archives to EC2 + use EC2 as a bridging primary + logically replicate into RDS + manually sync sequences**.

## Link
- [https://argos-ci.com/blog/heroku-to-aws-migration](https://argos-ci.com/blog/heroku-to-aws-migration)
