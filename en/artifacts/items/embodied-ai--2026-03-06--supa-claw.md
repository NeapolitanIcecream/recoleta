---
source: hn
url: https://github.com/vincenzodomina/supaclaw
published_at: '2026-03-06T23:41:42'
authors:
- rmason
topics:
- supabase-native
- agent-infrastructure
- serverless-workers
- sql-scheduling
- secure-automation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Supa Claw

## Summary
Supa Claw is an agent/automation system built around Supabase-native capabilities, emphasizing minimal infrastructure, self-hosting, and security with auditability. It is not a robotics or embodied intelligence paper, but rather an engineering architecture description for production-oriented agent workflows.

## Problem
- The problem it addresses is how to deploy a runnable, persistent, and auditable AI agent system **without introducing extra complex infrastructure** (such as a separate queue, always-on scheduler, dedicated daemon, or additional cloud services).
- This matters because agent systems often involve credential security, reliable task execution, message/job persistence, rollback capability for destructive actions, and the complexity of later self-hosting and operations.
- The text also emphasizes security: agents should be able to perform operations **while exposing credentials as little as possible**, and dangerous actions should retain audit/rollback capability.

## Approach
- The core method is simple: **push as much of the agent system's control plane as possible into Supabase-native components**, such as the database, storage, authentication, logs, scheduled jobs, and edge runtime, instead of assembling an extra layer of infrastructure.
- Inbound events are first **persisted and queued**, then processed by workers; the system uses retries and idempotency semantics to improve reliability.
- Scheduled execution does not rely on a self-built always-on scheduler, but uses **Postgres's pg_cron** for SQL-driven scheduling; webhook ingestion and agent execution run via edge functions.
- At the data layer, messages, jobs, and tasks are all stored directly in SQL, making them easy to inspect, debug, and audit in the Supabase Dashboard; it also supports memory tables and hybrid search (FTS + pgvector).
- Security mechanisms include JWT/RLS access control, audit/rollback protections for destructive actions, a restricted/sandboxed Bash environment, and database backups as system snapshot backups.

## Results
- The text **does not provide standard paper-style quantitative results**; it does not report benchmark datasets, success rates, error metrics, throughput, latency, or numerical comparisons with systems such as OpenClaw.
- The most concrete quantifiable engineering claim is: **"Get SupaClaw running in under 5 minutes"**, i.e. it claims deployment can be completed **within 5 minutes**.
- The core architectural claim is: **rapid cloud deployment can be achieved using only Supabase**, without any other cloud provider or extra infrastructure; at the same time, it also supports later full self-hosting.
- Claimed capabilities include **core architecture, Supabase integration, multi-channel support, memory tables + hybrid search, file/web tools, skills, cron tool, in-memory bash tool**, etc., but these are feature lists rather than experimental metrics.
- Compared with a "more full-featured" system (the text mentions OpenClaw), the project's claimed differentiator is not stronger functionality, but rather being **Supabase-native, low-ops-overhead, persistently reliable, and security/audit-friendly**.

## Link
- [https://github.com/vincenzodomina/supaclaw](https://github.com/vincenzodomina/supaclaw)
