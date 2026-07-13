---
source: arxiv
url: https://arxiv.org/abs/2607.08028v1
published_at: '2026-07-09T01:08:33'
authors:
- Joongho Ahn
- Moonsoo Kim
topics:
- llm-agents
- harness-engineering
- code-intelligence
- auditable-ai
- enterprise-software
- multi-agent-software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents

## Summary
The paper presents a code-owned harness that turns prompt-based enterprise LLM prototypes into auditable agents with source, routing, output, and trace contracts. A Korean corporate-data investment briefing system shows that these controls survive model substitution and preserve more utility than an external guardrail.

## Problem
- Prompt-dominant prototypes do not reliably enforce source boundaries, entity routing, claim eligibility, answer structure, trace completeness, or restrictions on recommendation language.
- These failures matter in enterprise settings because unsupported claims, mixed-entity evidence, leaked internal fields, and unreproducible answers can make a system unsafe to deploy or audit.

## Approach
- Register approved sources in manifests, extract evidence records, and promote only atomic, entity-scoped, provenance-linked statements into a runtime-eligible source-backed claim set.
- Move source admission, entity routing, claim selection, answer planning, follow-up filtering, trace generation, and validation into code, schemas, manifests, and validators.
- Keep the language model at a replaceable composition boundary. The model phrases a bounded claim package, while the harness checks the result and falls back to a deterministic composer when needed.
- Record both the reader-facing answer and an audit trace covering routing, source states, selected claims, validation outcomes, and fallback paths.
- Evaluate the system on 5 Korean corporate groups, 25 listed companies, 113 source-backed claims, 30 validation scenarios, 3 hosted models, and 3 repeats per scenario.

## Results
- The harness preserved source-grounding, entity-routing, trace, output-hygiene, and recommendation-language contracts across the fixed validation scenarios; fault injection caused the validators to flag deliberately broken contracts.
- All 270 live composition-boundary runs passed the harness contracts across 3 hosted models. Model-side failures were caught and recorded by the control layer.
- In the enforcement ablation, prompt instructions alone allowed recommendation-language and internal-trace-leakage violations to reach users. Code-owned enforcement blocked these violations.
- An external bolt-on guardrail achieved 88/120 utility, while the harness preserved 120/120 utility while blocking the tested violations.
- The study measures system verifiability and contract enforcement rather than investment-decision quality, and it does not provide evidence from a broad production deployment or user-quality benchmark.

## Link
- [https://arxiv.org/abs/2607.08028v1](https://arxiv.org/abs/2607.08028v1)
