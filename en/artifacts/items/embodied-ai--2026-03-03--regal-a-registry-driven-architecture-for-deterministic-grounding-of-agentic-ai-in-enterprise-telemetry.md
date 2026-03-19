---
source: arxiv
url: http://arxiv.org/abs/2603.03018v1
published_at: '2026-03-03T14:13:39'
authors:
- Yuvraj Agrawal
topics:
- llm-systems
- enterprise-telemetry
- mcp-tools
- deterministic-grounding
- data-governance
relevance_score: 0.07
run_id: materialize-outputs
language_code: en
---

# REGAL: A Registry-Driven Architecture for Deterministic Grounding of Agentic AI in Enterprise Telemetry

## Summary
REGAL proposes an architecture for enterprise telemetry that constrains LLM agents through deterministic data computation and registry-driven tool compilation, rather than letting models process raw logs directly. Its focus is not on new learning algorithms, but on turning “semantic interfaces” and “governance” into versionable, auditable system infrastructure.

## Problem
- Enterprise engineering systems generate massive, heterogeneous, and continuously evolving telemetry data, and handing it directly to LLMs leads to **context overflow and high token costs**.
- Many critical semantics are defined internally within organizations (such as P1, release-candidate, regression); without deterministic binding, LLMs are prone to **semantic ambiguity and hallucinations**.
- Handwritten tools/APIs **drift** as schemas and metric definitions evolve, leading to misinterpretation, audit difficulty, and governance risk.

## Approach
- Use **Medallion ELT** to deterministically transform raw data from version control, CI/CD, issue tracking, and observability systems into replayable, versioned Gold semantic artifacts, rather than exposing raw event streams to the model.
- Introduce a **metrics registry** as the single source of truth: metric semantics, retrieval logic, scope, caching policy, and access-control metadata are declared there.
- Through **registry-driven compilation**, automatically compile these declarative metrics into MCP tools, so tool descriptions, implementations, ACLs, and caching policies all come from the same definition, thereby reducing tool drift.
- Enforce **deterministic → probabilistic** layering: the LLM may only consume Gold artifacts and the compiled finite tool set, and cannot in turn affect data computation; the paper expresses this with the non-interference property \\(\\partial \\mathcal{D} / \\partial \\mathcal{P} = 0\\).
- At the interaction level, support both **pull** (historical queries) and **push** (event-driven triggers based on Gold artifact updates), but both share the same semantic interface, avoiding semantic divergence between active and passive workflows.

## Results
- The paper reports a **prototype validation and case study**; the core conclusion is that the architecture is feasible in practice, but **the excerpt does not provide systematic benchmark tables or complete quantitative comparison results on datasets**.
- The clearest quantitative statement in the paper is that, in the prototype deployment, when Gold artifacts fit in memory, **aggregated metric retrieval remains sub-second (less than 1 second) under moderate concurrency**, while **cache hits are nearly instantaneous**; in this setting, overall interaction latency is dominated by **model inference** rather than data retrieval.
- The paper claims the design can deliver **lower token consumption**, because the model processes pre-aggregated, semantically compressed Gold artifacts rather than raw logs; however, the excerpt **does not provide specific token savings percentages or absolute values**.
- The paper claims improvements in **governance and auditability**: access control, TTL/caching, and tool definitions are applied uniformly at the compilation boundary; at the same time, because the action space is restricted to a finite registry tool set, the **hallucination surface and operational risk are reduced**, but the excerpt **does not provide quantitative data on hallucination-rate reduction**.
- The novelty claim is not algorithmic SOTA, but a systematic proposal to treat the **registry as the single source of truth**, **semantic compilation as the execution mechanism for constraining agent action spaces**, and combine this with **end-to-end deterministic ingestion/versioned Gold artifacts**. The authors describe this as the first systematic formalization and end-to-end implementation of this pattern.

## Link
- [http://arxiv.org/abs/2603.03018v1](http://arxiv.org/abs/2603.03018v1)
