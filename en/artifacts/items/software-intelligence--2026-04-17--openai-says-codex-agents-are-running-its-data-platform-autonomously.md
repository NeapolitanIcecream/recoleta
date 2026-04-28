---
source: hn
url: https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/
published_at: '2026-04-17T23:48:56'
authors:
- tanelpoder
topics:
- code-agents
- data-platform-automation
- multi-agent-software-engineering
- ai-operations
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# OpenAI Says Codex Agents Are Running Its Data Platform Autonomously

## Summary
OpenAI says Codex-based agents now handle parts of its internal data platform with limited human intervention, including incident response, release management, and validation. The main claim is that useful data agents depend less on model skill alone and more on a unified, well-maintained data foundation.

## Problem
- OpenAI’s internal data platform is large and fast-moving: more than 3,500 internal users, over 600 PB of data, about 70,000 datasets, and streaming event volume up about 50x in a year.
- Human operators struggle to keep up with pipeline failures, schema drift, release checks, and scattered operational knowledge across Slack threads, runbooks, dashboards, and code.
- Data agents fail when the underlying data estate is fragmented. Missing metadata, weak lineage, unclear ownership, and inconsistent metric definitions block reliable automation.

## Approach
- OpenAI embeds Codex-powered agents into the data platform so they can monitor throughput, latency, and data quality in real time, then investigate anomalies such as stalled jobs, malformed events, and schema drift.
- The agents work on a connected internal data foundation that includes table definitions, ownership, documentation, query history, lineage, dashboards, permissions, and production code, rather than only a code repository.
- Agents can take operational actions such as restarting jobs, reallocating resources, generating fixes, validating those fixes, preparing deployments, and generating pull requests for review.
- OpenAI describes several domain-specific agents: a release agent for Apache Spark systems, an on-call assistant that retrieves prior fixes and escalation paths, and development agents that start local services, open browser sessions, test UI changes, and validate behavior.
- Trust and review are handled by exposing assumptions, generated queries, internal citations, confidence levels, and self-checks against trusted “golden” sources such as verified dashboards.

## Results
- Scale of the deployed setting: 3,500+ internal users, 600+ petabytes of data, roughly 70,000 datasets.
- Growth pressure: streaming event volumes increased about 50x year over year.
- Codex product usage cited in the article: more than 3 million weekly users.
- Claimed operational outcomes: broken pipelines can trigger an agent instead of waiting for an engineer; some failures are investigated, debugged, and sometimes resolved before a human opens a dashboard; releases can proceed without manual orchestration. The excerpt gives no direct before/after reliability or MTTR numbers for these internal deployments.
- Claimed automation breadth: OpenAI says Codex has generated hundreds of pull requests for large-scale migrations automatically.
- Benchmark numbers mentioned for broader agent performance, not this data-platform deployment: OpenAI’s agent scores 77.3% on Terminal-Bench 2.0 versus Claude’s 65.4%; Anthropic models are described as reaching the mid-to-upper 60% range on SWE-bench verified tasks.

## Link
- [https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/](https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/)
