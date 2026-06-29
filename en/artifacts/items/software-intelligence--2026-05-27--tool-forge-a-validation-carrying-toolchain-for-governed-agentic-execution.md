---
source: arxiv
url: https://arxiv.org/abs/2605.28000v1
published_at: '2026-05-27T05:45:58'
authors:
- Swanand Rao
topics:
- agentic-tooling
- mcp
- tool-routing
- code-generation
- software-governance
- multi-agent-software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Tool Forge: A Validation-Carrying Toolchain for Governed Agentic Execution

## Summary
Tool Forge is an open-source toolchain for turning natural-language tool requests into validated agent tools and routing those tools through MCP with less schema context.

## Problem
- Agents need tools to call APIs, edit files, and run workflows, but generated tools can have missing validation, bad dependencies, weak tests, or unclear credential needs.
- Large tool catalogs create token cost and selection noise when every full schema is loaded into the model context.
- This matters for production agent systems because tool execution affects security, reliability, auditability, latency, and cost.

## Approach
- Tool Forge treats each tool as a capsule containing intent, contract, code, dependencies, tests, docs, validation evidence, lifecycle state, credentials, and routing metadata.
- The generation path converts intent into a capability contract, grounds API details in documentation when available, generates code or a bundle, applies deterministic scaffolding, runs review and tests, then validates execution in a sandbox.
- The Router exposes a small MCP surface for search, resolve, describe, call, and profile listing, then loads full schemas only for the selected tools.
- Governance profiles filter tools by approval state, credential mapping, tenant, lifecycle state, and task session.

## Results
- Router benchmark: 83 cases across lite, realistic, and adversarial suites; aggregate micro-F1 is 0.908.
- Token exposure: estimated task-flow tool context is reduced by 99.49% versus naive full-catalog schema exposure.
- End-to-end generation probe: 25 of 25 requested tool bundles are generated across L1 smoke, L2 realistic, and L3 adversarial local-tool tasks.
- Artifact-pattern scoring: micro-F1 is 0.940 against deterministic acceptance patterns.
- Live sandbox validation: 23 of 25 generated tools pass.
- Reported failures include negation handling, semantically confusable tools, and edge-case validation; the authors frame the benchmark as an early open-source systems result, not a state-of-the-art comparison.

## Link
- [https://arxiv.org/abs/2605.28000v1](https://arxiv.org/abs/2605.28000v1)
