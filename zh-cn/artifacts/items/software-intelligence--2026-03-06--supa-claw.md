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
language_code: zh-CN
---

# Supa Claw

## Summary
Supa Claw 是一个基于 Supabase 原生能力构建的代理/自动化系统，目标是在尽量少的基础设施组件下提供可部署、可审计、相对安全的多渠道智能代理运行环境。它强调用数据库、存储、认证、定时、日志和边缘函数直接组成控制平面，而不是再引入额外队列、守护进程或云服务。

## Problem
- 它要解决的是：如何部署一个**可运行智能代理/自动化工作流**的后端系统，同时避免复杂基础设施、凭证暴露和高运维负担。
- 这很重要，因为很多代理系统虽然功能强，但往往依赖额外队列、常驻调度器、独立主机或多云组件，导致部署慢、调试难、审计弱、安全面更大。
- 文中还特别强调安全与可控性问题：代理需要“能做事”，但又不能直接拿到敏感凭证或执行不可回滚的破坏性操作。

## Approach
- 核心方法是**把代理控制平面尽可能全部放进 Supabase**：数据库、存储、认证、日志、cron、边缘运行时都使用 Supabase 自带原语。
- 事件先持久化入库再排队处理，worker 负责消费，并提供**retry + idempotency** 语义，以提高系统耐久性和恢复能力。
- 调度不使用自定义常驻 scheduler，而是用 **Postgres pg_cron** 做 SQL 驱动调度；Webhook 接入和代理执行则运行在 edge functions 上，cron 作为可靠兜底。
- 数据层面把 messages、jobs、tasks 直接存成 SQL 可检查对象，便于在 Supabase Dashboard 中排查、审计和调试。
- 安全机制上，声明采用 JWT、RLS、白名单/模拟 Bash、VM sandbox，以及对删除类操作要求审计/回滚选项，从而在不给代理底层凭证的前提下允许其执行任务。

## Results
- 文本**没有提供标准论文式定量实验结果**，没有给出 benchmark、准确率、成功率、成本或延迟数字对比。
- 最明确的可量化部署主张是：**“under 5 minutes”** 可完成启动部署；安装流程列出了 `supabase start`、`supabase db push --local`、`ngrok`、`supabase functions serve` 等步骤。
- 架构层面的具体能力声明包括：**1 个控制平面**统一管理 database/storage/auth/logs/cron/edge runtime，减少额外基础设施组件。
- 功能覆盖声明包括多渠道支持（Telegram、Slack、Teams、Discord 等）、memory tables + **hybrid search (FTS + pgvector)**、文件工具、网页工具、cron、内存文件系统 Bash。
- 安全方面的核心宣称是：**代理无凭证访问权但仍可执行操作**，并且对破坏性操作增加审计/回滚约束；但文中未给出渗透测试、事故率或安全评测数据。
- 相比 OpenClaw，它的突破点更像是**Supabase-native、低运维、可自托管**的工程集成，而不是在模型能力或智能体算法上提出新 SOTA。

## Link
- [https://github.com/vincenzodomina/supaclaw](https://github.com/vincenzodomina/supaclaw)
