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
language_code: en
---

# Migrating a 300GB PostgreSQL database from Heroku to AWS with minimal downtime

## Summary
This is an engineering migration retrospective describing how to move a nearly 300GB PostgreSQL production database from Heroku to AWS while reducing write downtime to about 1 minute. The core contribution is not a new algorithm, but a reusable two-stage migration plan: first use EC2 to take over Heroku's WAL recovery, then use logical replication to migrate into RDS.

## Problem
- Problem addressed: how to smoothly migrate a PostgreSQL production database of about **300GB**, including a large table with about **250 million rows**, from **Heroku** to **AWS** while minimizing service downtime as much as possible.
- Why it matters: the database is a core production system, and migration mistakes can lead to data loss, prolonged downtime, or primary key conflicts; meanwhile, at this scale Heroku also has issues such as **high cost, limited tuning flexibility, and restricted replication paths**.
- Specific difficulty: Heroku does not directly provide a simple publication/subscription migration path, while RDS **does not support physical WAL streaming replication**, so an intermediate bridging solution had to be designed.

## Approach
- Adopt a **two-stage migration**: first restore Heroku's base backup and WAL on **EC2**; after catching up, promote EC2 to primary, and have the Heroku application switch to EC2 first.
- In the second stage, use PostgreSQL **logical replication** from EC2 to **RDS**: create a publication on EC2 and a subscription on RDS, perform the initial full copy, and then continuously sync incremental changes.
- To make Heroku backups restorable, the team used **wal-e/wal-g** to pull data from S3, and **reconstructed `backup_label` and `tablespace_map`** from Heroku's sentinel JSON, which was the key step for successful recovery.
- During cutover, writes were frozen through two maintenance windows to perform final catch-up for **Heroku→EC2** and **EC2→RDS** respectively; because logical replication **does not replicate sequence values**, they finally ran an extra script to synchronize sequences and avoid primary key conflicts.

## Results
- Migration data size: the production database was nearly **300GB**, with the `screenshots` table containing about **250 million rows**.
- Base backup retrieval time: downloading about **300GB** of data from Heroku S3 to EC2 took about **45 minutes**.
- RDS full replication time: using logical replication to copy about **300GB** of data from EC2 to RDS took about **8 hours**, after which it entered a replicating state that synced only incremental changes.
- Downtime: the entire migration was split into **two maintenance windows**, each about **1 minute**; the article also mentions that the key **Heroku→EC2** cutover required only **a few minutes**, achieving minimized downtime.
- Resource configuration: RDS used **db.m6g.xlarge (4 vCPU, 16GB RAM)**; the bridging EC2 instance used **t3.xlarge (4 vCPU, 16GB RAM, 300GB io1)**.
- Concluding benefits: the author claims the migration delivered **better performance, lower costs, and stronger operational control**; however, the article **does not provide** strictly quantified comparison data such as latency reduction percentage, throughput improvement, or cost savings ratio.

## Link
- [https://argos-ci.com/blog/heroku-to-aws-migration](https://argos-ci.com/blog/heroku-to-aws-migration)
