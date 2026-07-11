---
source: arxiv
url: https://arxiv.org/abs/2607.07052v1
published_at: '2026-07-08T06:27:36'
authors:
- Arun Malik
topics:
- llm-agents
- agent-workflows
- it-operations
- workflow-automation
- cost-reduction
- deterministic-playbooks
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Progressive Crystallization: Turning Agent Exploration into Deterministic, Lower-Cost Workflows in Production

## Summary
Progressive crystallization turns repeated successful LLM-agent incident handling into hybrid or deterministic playbooks. In one cloud network operations deployment, deterministic executions reached about 45% after eight months and per-incident agent cost fell by more than 70% while incident volume roughly doubled.

## Problem
- LLM agents for IT operations re-run full inference on recurring incidents, so cost and latency scale with volume.
- Successful investigations are usually discarded as traces, which forces rediscovery and can produce different results on the same incident type.
- Traditional workflow automation needs manual engineering and cannot handle novel incidents, while fine-tuning still leaves probabilistic runtime behavior.

## Approach
- The paper defines three execution types: Type 3 agent-orchestrated runs at about 10k-50k tokens, Type 2 hybrid playbooks at about 1k-5k tokens, and Type 1 deterministic playbooks at zero runtime tokens.
- After a verified successful Type 3 run, the system extracts a reusable template from the trace: tool-call order, branch conditions, schemas, dependencies, parameterized values, and human-approval gates.
- Promotion from Type 3 to Type 2 requires at least 10 successful runs, zero safety violations, at least 90% matching action sequences, passing generated tests, and no recent human override.
- Promotion from Type 2 to Type 1 requires at least 50 successful hybrid runs, at least 99% LLM classification consistency, deterministic coverage of observed input variation, passing regression tests without the LLM, and human review.
- A circuit breaker demotes a playbook when execution fails, a safety violation occurs, or acceptance tests regress.

## Results
- In production cloud network operations handling tens of thousands of incidents per month, Type 1 executions rose from 0% to about 45% over eight months; the final mix was about 45% Type 1, 30% Type 2, and 25% Type 3.
- Per-incident agent cost fell by more than 70% during the same period while incident volume roughly doubled.
- The platform resolved over 90% of common incident categories autonomously.
- Mean time to resolution fell from hours to minutes.
- False-positive remediation stayed under 5% with no customer-visible impact reported.
- Safety metrics improve by type in the paper's taxonomy: reproducibility is about 50% for Type 3, about 90% for Type 2, and 100% for Type 1; runtime token cost moves from 10k-50k to 1k-5k to zero.

## Link
- [https://arxiv.org/abs/2607.07052v1](https://arxiv.org/abs/2607.07052v1)
