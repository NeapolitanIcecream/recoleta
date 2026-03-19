---
source: hn
url: https://github.com/awsome-o/grafana-lens
published_at: '2026-03-06T23:37:50'
authors:
- AwesomeO3000
topics:
- observability
- grafana
- otlp
- ai-agents
- sre
- tracing
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Show HN: An OTLP observability plugin for OpenClaw AI agents in Grafana

## Summary
This is not a robotics/foundation model paper, but a Grafana observability plugin for OpenClaw AI agents. It packages metrics, logs, tracing, alerts, and security inspections into tools that agents can invoke through natural language for operations and monitoring.

## Problem
- It addresses the problem that signals across **metrics, logs, traces, alerts, and security** in AI agent platforms are fragmented and hard to troubleshoot in a unified way.
- The traditional built-in OpenClaw `diagnostics-otel` only provides basic counters/histograms, lacking **lifecycle-level tracing, log forwarding, session-level tracing, and security monitoring**, making it difficult to locate complex failures or anomalous behavior.
- This matters because once an agent system connects to tools, Webhooks, multi-turn sessions, and external data sources, problems often span metrics/logs/traces, and multi-signal investigation is a core real-world operations need.

## Approach
- Through a self-contained OpenClaw plugin, it registers **17 Grafana-related tools** for the agent, allowing users to use natural language directly to query PromQL/LogQL/TraceQL, build dashboards, set alerts, share charts, investigate incidents, and more.
- It uses **OTLP HTTP push** to send metrics to Prometheus, logs to Loki, and traces to Tempo; it does not rely on Prometheus scraping, so data is "available immediately."
- It registers **16 lifecycle hooks** in OpenClaw (such as `session_start`, `llm_input`, `before_tool_call`, `after_tool_call`, etc.), builds a session-level trace tree, and associates logs with `trace_id`, enabling click-through navigation from Loki to Tempo.
- It provides SRE-oriented analysis logic: for example, `grafana_investigate` aggregates metrics/logs/traces/context in parallel; anomaly detection uses **z-score relative to a 7-day baseline**; alert fatigue analysis identifies always-firing, flapping, and error/nodata rules.
- It provides detection-oriented security monitoring: **6 categories of checks** (prompt injection, cost anomalies, tool loops, session enumeration, webhook errors, stuck sessions), as well as **12 regex patterns** to scan for prompt injection signals, and supports automatic redacted export of sensitive tokens.

## Results
- The text **does not provide formal experiments, benchmark datasets, or paper-style comparative quantitative results**, so there is no verifiable SOTA or percentage improvement.
- Specific functional result claims include: **17 composable tools**, **12 prebuilt dashboard templates**, **16 lifecycle hooks**, **6 security checks**, and sharing support for **15+ messaging channels**.
- For anomaly analysis, it claims support for z-score severity grading based on a **7-day baseline**: `normal` (<1.5σ), `mild` (1.5–2σ), `significant` (2–3σ), `critical` (>3σ).
- For trace retrieval, it claims the ability to directly query slow traces, for example slow traces with a threshold of **>10s**, and supports filtering by error status and attributes based on TraceQL.
- The default OTLP export interval is stated as **15000 ms**, the default truncation length for content fields is **2000** characters; custom metrics support up to **100** metric definitions by default, up to **5** label keys per metric, and up to **50** unique label combinations.
- For security/privacy, it claims `redactSecrets` is enabled by default, can recognize multiple token types (such as `ghp_`, `xoxb-`, `sk-`, `glsa_`, etc.), and redact them into the `${first6}...${last4}` format.

## Link
- [https://github.com/awsome-o/grafana-lens](https://github.com/awsome-o/grafana-lens)
