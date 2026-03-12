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
---

# Supa Claw

## Summary
Supa Claw 是一个以 Supabase 原生能力为核心构建的代理/自动化系统，强调最少基础设施、可自托管与安全可审计。它并非机器人或具身智能论文，而更像一套面向生产代理工作流的工程化架构说明。

## Problem
- 解决的问题是：如何在**不引入额外复杂基础设施**（如独立队列、常驻调度器、专用守护进程、额外云服务）的情况下，部署一个可运行、可持久化、可审计的 AI 代理系统。
- 这很重要，因为代理系统常常涉及凭据安全、任务可靠执行、消息/作业持久化、可回滚 destructive actions，以及后续自托管和运维复杂度。
- 文中还强调安全问题：代理应当在**尽量不直接暴露凭据**的前提下完成操作，并对危险动作保留审计/回退能力。

## Approach
- 核心方法很简单：**把代理系统的控制平面尽量全部压到 Supabase 原生组件里**，例如数据库、存储、认证、日志、定时任务和边缘运行时，而不是自己再拼装一套额外基础设施。
- 入站事件先被**持久化并排队**，再由 worker 处理；系统使用重试和幂等语义来提高可靠性。
- 定时调度不是靠自建常驻 scheduler，而是使用 **Postgres 的 pg_cron** 做 SQL 驱动调度；Webhook 接入和 agent 执行则通过 edge functions 运行。
- 数据层面上，消息、作业和任务都直接存储在 SQL 中，便于在 Supabase Dashboard 里检查、调试和审计；还支持 memory tables 与混合搜索（FTS + pgvector）。
- 安全机制包括：JWT/RLS 访问控制、对 destructive actions 的审计/回滚保护、受限/沙箱化 Bash 环境，以及数据库备份作为系统快照备份。

## Results
- 文本**没有提供标准论文式定量实验结果**，没有给出基准数据集、成功率、误差、吞吐、延迟或与 OpenClaw 等方案的数字对比。
- 最具体的可量化工程声明是：**“Get SupaClaw running in under 5 minutes”**，即声称可在 **5 分钟内完成启动部署**。
- 架构上的核心主张是：**只依赖 Supabase 即可完成云端快速部署**，无需其他云提供商或额外基础设施；同时也支持后续完全自托管。
- 功能声明包括：已完成 **core architecture、Supabase integration、multi-channel support、memory tables + hybrid search、file/web tools、skills、cron tool、in-memory bash tool** 等，但这些是特性列表，不是实验指标。
- 相比“更全功能”的系统（文中提到 OpenClaw），该项目宣称自己的突破点不是功能更强，而是**Supabase-native、低运维开销、持久化可靠和安全审计友好**。

## Link
- [https://github.com/vincenzodomina/supaclaw](https://github.com/vincenzodomina/supaclaw)
