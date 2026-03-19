---
source: hn
url: https://github.com/awsome-o/grafana-lens
published_at: '2026-03-06T23:37:50'
authors:
- AwesomeO3000
topics:
- observability
- grafana-plugin
- ai-agents
- opentelemetry
- sre
- trace-analysis
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Show HN: An OTLP observability plugin for OpenClaw AI agents in Grafana

## Summary
This is a community plugin that brings Grafana observability to OpenClaw AI agents, integrating monitoring, troubleshooting, alerting, tracing, and data pushing into agent workflows through natural language. Its value lies in giving AI agents native observability capabilities for SRE/security/operations, rather than just producing text outputs.

## Problem
- AI agent platforms usually only have basic diagnostic counters, lacking **session-level traces, log forwarding, security signals, and joint troubleshooting across metrics/logs/traces**.
- Operators and developers need to manually switch between Prometheus, Loki, Tempo, and Grafana, and also write PromQL/LogQL/TraceQL, creating a high barrier to use.
- For agent systems, new operational risks such as **prompt injection, tool loops, cost anomalies, and alert fatigue** are difficult to monitor continuously, affecting reliability, security, and production readiness.

## Approach
- Provide a **self-contained OpenClaw plugin** with a built-in Grafana REST client that automatically registers **17 composable tools**, allowing agents to use natural language to query metrics, query logs, query traces, build dashboards, create alerts, share charts, perform security checks, and investigate incidents.
- Use **OTLP HTTP push** to send **metrics→Prometheus, logs→Loki, traces→Tempo** directly into the LGTM stack, with no need for Prometheus scraping, so data is visible immediately.
- Attach **16 hooks** throughout the OpenClaw lifecycle (such as `llm_input`, `before_tool_call`, `session_end`, etc.) to build a **session-level trace tree**, generate log records, and add rich telemetry that basic diagnostic extensions do not provide.
- Add analysis capabilities tailored to agent scenarios: **7-day baseline z-score anomaly detection**, seasonality comparison, alert fatigue analysis, `grafana_investigate` multi-signal parallel troubleshooting, and **6 security checks** (prompt injection, cost anomalies, tool loops, etc.).
- Provide **12 prebuilt dashboard templates** and custom metric push capabilities, enabling external data to be written directly into the Grafana system through conversation.

## Results
- Functional results: the system claims to provide **17 agent tools**, **12 prebuilt dashboard templates**, **16 lifecycle hooks**, and **6 parallel security checks**, covering the full workflow of querying, visualization, alerting, tracing, troubleshooting, and sharing.
- Observability scope: supports **3 types of OTLP signals** (metrics/logs/traces) connected respectively to **Prometheus/Loki/Tempo**, and supports sharing panel images across **15+ messaging channels**.
- Analysis mechanisms: anomaly detection computes z-scores based on a **7-day baseline**, with severity thresholds defined as **<1.5σ / 1.5–2σ / 2–3σ / >3σ**; the example threshold for slow traces is **>10s**; alert fatigue rules include criteria such as **continuously firing for >24 hours**.
- Security monitoring: prompt injection detection uses **12 regex patterns**; the security overview dashboard contains **15 panels**; key redaction is enabled by default, and examples truncate tokens as `${first6}...${last4}`.
- Configuration and runtime: the default OTLP export interval is **15000 ms**, and local LGTM is recommended to run as a single container exposing ports **3000/4317/4318/9090**.
- Note on quantitative breakthrough: the provided content **does not include experimental results on standard benchmark datasets**, nor precise comparisons of accuracy, recall, latency, or cost; the strongest concrete claim is that it unifies multi-signal Grafana/LGTM observation, investigation, and security monitoring in OpenClaw into a single natural-language agent interface.

## Link
- [https://github.com/awsome-o/grafana-lens](https://github.com/awsome-o/grafana-lens)
