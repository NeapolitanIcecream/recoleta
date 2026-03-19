---
source: hn
url: https://github.com/vincenzodomina/supaclaw
published_at: '2026-03-06T23:41:42'
authors:
- rmason
topics:
- agent-infrastructure
- supabase-native
- multi-agent-platform
- workflow-automation
- secure-tool-use
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Supa Claw

## Summary
Supa Claw is an agent/automation system built on Supabase-native capabilities, aiming to provide a deployable, auditable, and relatively secure multi-channel agent runtime environment with as little infrastructure as possible. It emphasizes composing the control plane directly from the database, storage, authentication, scheduling, logs, and edge functions, rather than introducing additional queues, daemons, or cloud services.

## Problem
- It aims to solve this: how to deploy a **backend system capable of running intelligent agents/automated workflows** while avoiding complex infrastructure, credential exposure, and high operations burden.
- This matters because many agent systems, while powerful, often depend on extra queues, always-on schedulers, dedicated hosts, or multi-cloud components, leading to slower deployment, harder debugging, weaker auditability, and a larger security surface.
- The text also specifically emphasizes security and controllability: agents need to "get things done" without directly obtaining sensitive credentials or performing destructive actions that cannot be rolled back.

## Approach
- The core approach is to **put as much of the agent control plane as possible inside Supabase**: database, storage, authentication, logs, cron, and edge runtime all use Supabase's built-in primitives.
- Events are first persisted to the database and then queued for processing; workers consume them and provide **retry + idempotency** semantics to improve durability and recovery.
- Scheduling does not use a custom always-on scheduler; instead it uses **Postgres pg_cron** for SQL-driven scheduling. Webhook ingestion and agent execution run on edge functions, with cron serving as a reliable fallback.
- At the data layer, messages, jobs, and tasks are stored directly as SQL-inspectable objects, making troubleshooting, auditing, and debugging easier in the Supabase Dashboard.
- On security, it states the use of JWT, RLS, whitelisted/simulated Bash, VM sandboxing, and audit/revert requirements for delete-type actions, allowing agents to perform tasks without being given underlying credentials.

## Results
- The text **does not provide standard paper-style quantitative results**; it does not present benchmark, accuracy, success-rate, cost, or latency comparisons.
- The clearest quantifiable deployment claim is that startup can be completed in **"under 5 minutes"**; the setup flow lists steps such as `supabase start`, `supabase db push --local`, `ngrok`, and `supabase functions serve`.
- Specific architecture-level capability claims include **one control plane** that centrally manages database/storage/auth/logs/cron/edge runtime, reducing additional infrastructure components.
- Claimed functional coverage includes multi-channel support (Telegram, Slack, Teams, Discord, etc.), memory tables + **hybrid search (FTS + pgvector)**, file tools, web tools, cron, and an in-memory filesystem Bash.
- The core security claim is that **agents have no credential access but can still perform operations**, with added audit/revert constraints on destructive actions; however, the text does not provide penetration-test results, incident rates, or security evaluation data.
- Compared with OpenClaw, its main contribution is better understood as **Supabase-native, low-ops, self-hostable** engineering integration, rather than a new SOTA in model capability or agent algorithms.

## Link
- [https://github.com/vincenzodomina/supaclaw](https://github.com/vincenzodomina/supaclaw)
