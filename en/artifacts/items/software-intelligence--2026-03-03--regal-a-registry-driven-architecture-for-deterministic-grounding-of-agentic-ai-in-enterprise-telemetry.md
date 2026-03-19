---
source: arxiv
url: http://arxiv.org/abs/2603.03018v1
published_at: '2026-03-03T14:13:39'
authors:
- Yuvraj Agrawal
topics:
- agentic-ai
- enterprise-telemetry
- mcp-tools
- deterministic-grounding
- registry-driven-architecture
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# REGAL: A Registry-Driven Architecture for Deterministic Grounding of Agentic AI in Enterprise Telemetry

## Summary
REGAL proposes an agentic AI deployment architecture for enterprise telemetry: first, a deterministic data pipeline compresses raw telemetry into reproducible semantic metrics, and then the LLM accesses these results only through controlled tools compiled from a registry. Its core value lies not in new learning algorithms, but in unifying “semantic definitions, tool interfaces, and governance policies” into versionable architectural constraints.

## Problem
- Enterprise engineering telemetry comes from version control, CI/CD, defect tracking, and observability platforms; the data is large-scale, heterogeneous, and continuously evolving, so feeding raw events directly to an LLM causes **context overload and high token costs**.
- Internal organizational semantics (such as “P1,” “regression,” and “release candidate”) are locally defined; if one relies only on probabilistic retrieval or RAG, the model can easily **misinterpret semantics and hallucinate**.
- Handwritten tools/APIs can **experience tool drift** as schemas and metric definitions change, causing interface documentation, actual execution, and governance policies to fall out of sync, which affects auditing and compliance.

## Approach
- It adopts a **deterministic–probabilistic separation**: all telemetry first goes through a replayable, idempotent, versioned Medallion ELT process, transforming Bronze/Silver into Gold semantic artifacts for AI consumption; the LLM can only consume these artifacts and cannot in turn alter the computation logic.
- It introduces a **metrics registry** as the single source of truth: the registry declares metric identifiers, semantic descriptions, retrieval logic, platform scope, ACL, and caching policies.
- Through **registry-driven compilation**, declarative metric definitions are automatically compiled into MCP tools, including tool schema, descriptions, access control, and caching behavior, thereby realizing “interface-as-code” at runtime.
- Through a **bounded action space**, the agent is restricted to calling a limited set of precompiled semantic tools, rather than generating arbitrary SQL or accessing raw logs, reducing the hallucination surface and governance complexity.
- It supports dual **pull + push** paths: historical analysis pulls Gold metrics by time window through tools; real-time monitoring triggers alerts and agent workflows through Gold-layer change streams, with both sharing the same semantic boundary.

## Results
- The paper explicitly states that this is a **systems architecture and prototype validation effort**; it **does not report precise quantitative comparison results on standard benchmark datasets**, and it **does not propose new learning algorithms**.
- The prototype and case study claim to validate the architecture’s value in **feasibility, latency, token efficiency, and governance**; the most specific numerical statement in the paper is that when Gold artifacts **fit in memory** and under **moderate concurrent load**, aggregated metric retrieval can remain **sub-second**, and responses are **almost instantaneous** when the cache is hit.
- The paper further claims that in the prototype scenario above, **model inference latency rather than data retrieval latency** becomes the dominant part of end-to-end interaction, supporting its design principle of “deterministic computation first, probabilistic reasoning second.”
- The main breakthrough claim is not about SOTA metrics, but about architecture: using the **registry as the single source of truth**, using the **compilation step as the mechanism for tool consistency and governance enforcement**, and treating **deterministic Gold artifacts** as the LLM’s sole input boundary, in order to mitigate the three enterprise deployment pain points of context overload, local semantics, and tool drift.

## Link
- [http://arxiv.org/abs/2603.03018v1](http://arxiv.org/abs/2603.03018v1)
