---
source: hn
url: https://github.com/muralibasani/streamlens
published_at: '2026-03-06T23:05:37'
authors:
- muralibasani
topics:
- kafka-observability
- natural-language-query
- prometheus-metrics
- topology-visualization
- ai-assistant
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Show HN: Natural language queries for Prometheus Kafka metrics (StreamLens)

## Summary
StreamLens is a visualization and question-answering tool for Apache Kafka that combines cluster topology exploration, real-time metrics queries, and natural-language interaction. Its core value is helping operators and developers understand Kafka system state faster and obtain actionable information directly from Prometheus/JMX.

## Problem
- Kafka clusters contain many kinds of objects, including topics, producers, consumers, connectors, schemas, and ACLs. The structure is complex, and manually investigating topology and dependencies is costly.
- Monitoring metrics are typically scattered across Prometheus/JMX, requiring users to hand-write query expressions, making it hard to quickly answer questions such as “What is the current throughput?” or “Are there any under-replicated partitions?”
- In large clusters, node discovery, producer identification, consumer lag troubleshooting, and topic configuration inspection often require switching between multiple tools, reducing operational efficiency.

## Approach
- Build a frontend-backend system: the frontend uses React Flow to display Kafka cluster topology, while the backend uses FastAPI to connect to Kafka, Schema Registry, Kafka Connect, Prometheus, and JMX data sources.
- Automatically discover Kafka resources, including topics, consumer groups, producers, connectors, schemas, and ACLs, and merge schemas that share the same Schema Registry ID into a single display node.
- Provide an automatic fallback chain for producer detection: first read producer metrics aggregated by client_id and topic from Prometheus; if unavailable, fall back to broker-side topic metrics; if that also fails, use JMX/offset-change detection.
- Introduce the AI assistant StreamPilot, which maps natural-language questions to queries over a predefined set of Kafka broker metrics, and highlights relevant nodes in the graph and zooms to the results.
- Support interactive capabilities such as topic details, recent message viewing, consumer per-partition lag, connector configuration inspection, and sample client code generation.

## Results
- The text does not provide standard benchmark tests, offline evaluations, or quantitative comparisons with existing systems, so there are **no reportable quantitative performance improvement figures**.
- It proposes support for querying **17 broker metrics** across **5 categories**, and supports asking about real-time Kafka broker metrics in natural language.
- Supports multiple AI providers: **OpenAI, Gemini, Anthropic, Ollama**.
- Supports multiple Kafka connection/authentication methods: **SASL_SSL, SSL, PLAINTEXT**, as well as **OAUTHBEARER, SCRAM-SHA-512, SCRAM-SHA-256, PLAIN**.
- Example questions it can answer directly include current message throughput, under-replicated partitions, average produce request processing time, and partition counts, but the original text does not provide accuracy or latency data for these Q&A capabilities.

## Link
- [https://github.com/muralibasani/streamlens](https://github.com/muralibasani/streamlens)
