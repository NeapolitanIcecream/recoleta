---
source: arxiv
url: http://arxiv.org/abs/2603.10057v1
published_at: '2026-03-09T19:11:45'
authors:
- Petar Radanliev
- Carsten Maple
- Omar Santos
- Kayvan Atefi
topics:
- sbom
- aibom
- multi-agent-systems
- software-supply-chain-security
- reproducibility
- vex-csaf
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# SBOMs into Agentic AIBOMs: Schema Extensions, Agentic Orchestration, and Reproducibility Evaluation

## Summary
This paper extends static SBOMs into agentic AIBOMs with contextual reasoning capabilities, so that software bills of materials not only record components, but also combine runtime evidence and policy outputs to produce auditable vulnerability exploitability determinations. Its core contributions are multi-agent orchestration, minimal schema extensions to CycloneDX/SPDX, and evaluation centered on reproducibility and stability of vulnerability explanations.

## Problem
- Traditional SBOMs describe only static dependencies and cannot reflect runtime behavior, environment drift, dynamic loading, or real exploitability, making them insufficient for high-trust software supply-chain security and reproducible auditing.
- In the context of massive numbers of CVEs, component “presence” does not equal vulnerability “exploitability”; without contextual filtering, security teams are overwhelmed by large numbers of non-exploitable vulnerabilities.
- Regulated or high-assurance analysis environments need to bind software composition, execution context, and audit evidence together; otherwise, even if code and data remain unchanged, environmental differences can undermine result reproducibility and compliance judgments.

## Approach
- Proposes an agentic AIBOM framework: transforming the SBOM from a passive inventory into an active provenance object that outputs structured exploitability statements aligned with CSAF v2.0 / VEX, rather than directly executing blocking actions.
- Uses three types of multi-agent collaboration: MCP handles baseline environment reconstruction, A2A handles runtime dependency and environment drift monitoring, and AGNTCY performs vulnerability/VEX reasoning by combining policy, mitigations, and execution evidence.
- Applies “minimal and compatible” schema extensions to CycloneDX and SPDX, adding execution context, dependency evolution timelines, agent decision provenance, and advisory evidence fields while preserving interoperability.
- Establishes runtime dependency ground truth through pre/mid/post multi-stage snapshots, import hooks, and package manager instrumentation, and evaluates using Capture Rate, FPR, FNR, semantic/exact reproduction rate, latency, and overhead.
- To ensure high assurance, the system adds fail-closed behavior, cross-snapshot consistency checks, segmented signing, and integrity thresholds; for example, if components with missing or incorrect hashes exceed **2%**, it triggers an integrity violation and requires human adjudication.

## Results
- The paper explicitly claims that, across heterogeneous analysis workloads, agentic AIBOM improves **runtime dependency capture**, **reproduction fidelity**, and **stability of vulnerability explanations** compared with existing provenance systems such as ReproZip, SciUnit, and ProvStore, while maintaining relatively low computational overhead.
- The paper also claims that ablation experiments show each of the three agents provides unique capabilities that cannot be replaced by deterministic automation, supporting the necessity of its multi-agent design.
- The paper gives quantifiable evaluation definitions and thresholds: exact reproduction uses **SHA-256** byte-level consistency; semantic reproduction tolerances are **ε=1e-12** for deterministic tasks and **ε=1e-6** for floating-point ML tasks.
- The reliability mechanism specifies a clear rule: if cross-stage validation finds that **more than 2%** of expected components are missing or have incorrect hashes, the workflow is blocked from proceeding and escalated for human review.
- The background data emphasizes the scale of the problem: at the time of writing, there were more than **191,633** CVEs, later surpassing **200,000**; **32,760 in 2022** and **about 22,000 in 2021**; about **11%** are classified as critical; and vulnerabilities in about **95%** of SBOM components are typically not exploitable in products.
- The provided excerpt **does not include a direct final benchmark table** (such as specific percentage improvements, absolute dataset scores, or overhead in milliseconds), so more detailed quantitative comparative results cannot be extracted from the excerpt.

## Link
- [http://arxiv.org/abs/2603.10057v1](http://arxiv.org/abs/2603.10057v1)
