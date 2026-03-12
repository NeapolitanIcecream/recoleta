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
---

# Show HN: An OTLP observability plugin for OpenClaw AI agents in Grafana

## Summary
这是一个为 OpenClaw AI 代理提供 Grafana 可观测性的社区插件，通过自然语言把监控、排障、告警、追踪和数据推送整合到代理工作流中。它的价值在于让 AI 代理具备面向 SRE/安全/运维的原生可观测能力，而不只是输出文本结果。

## Problem
- AI 代理平台通常只有基础诊断计数器，缺少**会话级 traces、日志转发、安全信号、跨指标/日志/链路的联合排障**能力。
- 运维和开发者需要在 Prometheus、Loki、Tempo、Grafana 之间手工切换，且还要写 PromQL/LogQL/TraceQL，使用门槛高。
- 对于代理系统，**提示注入、工具循环、成本异常、告警疲劳**等新型运行风险难以持续监控，这会影响可靠性、安全性和生产落地。

## Approach
- 提供一个**自包含 OpenClaw 插件**，内置 Grafana REST client，并自动注册 **17 个可组合工具**，让代理能用自然语言执行查指标、查日志、查 traces、建 dashboard、建告警、分享图表、做安全检查、做事件调查等操作。
- 通过 **OTLP HTTP push** 直接把 **metrics→Prometheus、logs→Loki、traces→Tempo** 发送到 LGTM 栈，无需 Prometheus scraping，数据可立即可见。
- 在 OpenClaw 生命周期中挂载 **16 个 hooks**（如 `llm_input`、`before_tool_call`、`session_end` 等），构建**会话级 trace 树**、生成日志记录，并补充基础诊断扩展不具备的 rich telemetry。
- 增加面向代理场景的分析能力：**7 天基线 z-score 异常检测**、季节性比较、告警疲劳分析、`grafana_investigate` 多信号并行排障，以及 **6 项安全检查**（提示注入、成本异常、工具循环等）。
- 提供 **12 个预置 dashboard 模板** 和自定义指标推送能力，可把外部数据通过对话直接写入 Grafana 体系。

## Results
- 功能性结果：系统声称提供 **17 个 agent tools**、**12 个预置 dashboard 模板**、**16 个生命周期 hooks**、**6 项并行安全检查**，覆盖查询、可视化、告警、追踪、排障和共享等完整流程。
- 可观测性范围：支持 **3 类 OTLP 信号**（metrics/logs/traces）分别接入 **Prometheus/Loki/Tempo**，并支持 **15+ 消息渠道**分享 panel 图像。
- 分析机制：异常检测基于**7 天基线**计算 z-score，严重度阈值定义为 **<1.5σ / 1.5–2σ / 2–3σ / >3σ**；慢 trace 示例阈值为 **>10s**；告警疲劳规则包含**持续触发 >24 小时**等判据。
- 安全监测：提示注入检测使用 **12 条 regex patterns**；安全总览 dashboard 含 **15 个 panels**；密钥脱敏默认开启，示例会把 token 截断为 `${first6}...${last4}`。
- 配置与运行：默认 OTLP 导出周期为 **15000 ms**，本地 LGTM 推荐以单容器方式暴露 **3000/4317/4318/9090** 端口运行。
- 定量突破说明：给定内容**没有提供标准基准数据集上的实验结果**，也没有精确的准确率、召回率、延迟或成本对比；最强的具体主张是其在 OpenClaw 中把 Grafana/LGTM 的多信号观测、调查与安全监测整合为统一的自然语言代理接口。

## Link
- [https://github.com/awsome-o/grafana-lens](https://github.com/awsome-o/grafana-lens)
