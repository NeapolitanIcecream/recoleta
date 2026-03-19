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
- ai-ops
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: Natural language queries for Prometheus Kafka metrics (StreamLens)

## Summary
StreamLens is a visualization and AI assistant tool for Apache Kafka that supports querying real-time Prometheus/JMX metrics in natural language and interactively exploring cluster topology. It is more like an engineering system/open-source product release than a traditional research paper.

## Problem
- Topics, consumer groups, producers, connectors, schemas, and ACLs in Kafka clusters are scattered across multiple systems, making troubleshooting and understanding topology costly.
- Operators usually need to hand-write PromQL/JMX queries or switch between multiple consoles, making it difficult to answer questions about throughput, backlog, partition issues, replica anomalies, and more in a timely manner.
- In large-scale clusters, the number of nodes is high and relationships are complex; lacking a unified visualization and natural-language entry point reduces troubleshooting efficiency.

## Approach
- Build a frontend-backend system: the frontend uses an interactive graph to display Kafka topology, and the backend automatically discovers topics, consumer groups, producers, connectors, schemas, and ACLs from the live cluster.
- Introduce the AI assistant StreamPilot, which maps users' natural-language questions to a set of **pre-curated** Prometheus broker metrics / PromQL queries, and highlights and zooms relevant nodes in the interface.
- Producer detection uses an automatic fallback chain: prefer Prometheus client-level metrics; if unavailable, fall back to broker-side topic metrics; if that also fails, use Broker JMX.
- Supports operational features such as Schema Registry, Kafka Connect, consumer lag, topic details, sample client code generation, message production, search/navigation, and paginated loading.
- Compatible with OpenAI, Gemini, Anthropic, and Ollama, and supports multiple Kafka authentication/connection methods (such as SASL_SSL, SSL, PLAINTEXT).

## Results
- The text **does not provide formal experiments, benchmarks, or paper-style quantitative results**, so it is not possible to report accurate SOTA or percentage improvements.
- The clearest numerical claim given is that the AI assistant can query **17** curated broker metrics covering **5 categories** of metrics.
- Example questions the system can answer include current message throughput, under-replicated partitions, average processing time for produce requests, number of partitions, etc., but no answer accuracy or latency is reported.
- Specific functional claims include support for automatically discovering topology elements, viewing consumer lag by partition, merging schema nodes based on Schema Registry ID, and paginated topic loading in large clusters.
- Compared with the traditional approach of "manually writing PromQL/JMX + switching across multiple tools," the main improvement is integrating visualization, real-time metrics, and natural-language Q&A into a single UI, but the text provides no user study or efficiency-gain data.

## Link
- [https://github.com/muralibasani/streamlens](https://github.com/muralibasani/streamlens)
