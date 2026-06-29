---
source: arxiv
url: https://arxiv.org/abs/2605.12078v1
published_at: '2026-05-12T13:05:02'
authors:
- Oleg Solozobov
topics:
- agent-observability
- decision-reconstruction
- software-agents
- runtime-tracing
- ai-governance
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes

## Summary
This pilot tests whether traces from agent SDKs contain enough evidence to reconstruct agent decisions at the property level. It finds large gaps in what can be recovered, especially reasoning evidence, but the study uses one worked-example anchor per SDK and no production corpus.

## Problem
- Agent failures need post-hoc reconstruction: what action occurred, who authorized it, which policy applied, and what reasoning led to it.
- Current agent traces vary by SDK, adapter, operator instrumentation, and stored artifacts, so a downstream investigator may see different evidence for the same kind of decision.
- The paper matters for agent operations and governance because missing trace properties can block incident analysis after harmful actions such as tool calls or state mutations.

## Approach
- The paper applies the existing Decision Trace Reconstructor v0.1.0 without modification.
- It evaluates 7 Decision Event Schema property classes across 6 vendor SDK regimes: AWS Bedrock Agents, LangSmith/LangChain, Anthropic Claude tool use, OpenAI Agents/Assistants, OpenTelemetry GenAI/Vertex Agent Engine, and MCP.
- It adds 2 comparator columns: the author’s Operational Evidence Plane as a ceiling reference and a public-record reconstruction of the Replit DROP DATABASE incident.
- Each property is classified as fully fillable, partially fillable, structurally unfillable, or opaque.
- The inputs are pinned worked-example anchors, one per cell, with checksum-verifiable outputs in a reproducibility package.

## Results
- The main quantitative claim is that strict-governance-completeness splits into 3 tiers across the anchor set, ranging from 42.9% to 85.7%.
- The paper reports 1 regime-independent gap: reasoning trace evidence is missing or unusable across most surveyed regimes.
- It reports 4 regime-dependent gaps and 1 Mixed property, meaning most gaps change by SDK evidence shape rather than appearing uniformly.
- The study covers 6 vendor SDK regimes, 2 comparator columns, 7 property classes, and 1 worked-example anchor per cell.
- The method is deterministic on the pinned inputs; the paper states each anchor has at most 50 fragments and runs in under 10 seconds per anchor on a consumer laptop.
- The evidence is pilot-scale: single annotator, worked examples rather than captured production traces, and no statistical test of SDK interchangeability.

## Link
- [https://arxiv.org/abs/2605.12078v1](https://arxiv.org/abs/2605.12078v1)
