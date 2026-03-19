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
- software-supply-chain-security
- multi-agent-systems
- runtime-dependency-analysis
- vex-csaf
- reproducibility
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# SBOMs into Agentic AIBOMs: Schema Extensions, Agentic Orchestration, and Reproducibility Evaluation

## Summary
This paper proposes extending static SBOMs into “agentic” AIBOMs: while remaining compatible with existing standards, it incorporates runtime context, dependency drift, and vulnerability exploitability reasoning into auditable software provenance artifacts. The goal is to improve reproducibility, the stability of vulnerability interpretation, and runtime dependency capture in software supply-chain security.

## Problem
- Traditional SBOMs record only static dependency inventories and cannot reflect runtime behavior, environment drift, or whether a vulnerability is actually exploitable, making them inadequate for high-trust security assessment and reproducible auditing.
- Modern software involves dynamic loading, late binding, and federated services, so simply knowing that a component “exists” is not enough to judge risk; this matters because many vulnerabilities among the vast number of CVEs are not exploitable in specific environments.
- Existing provenance/reproducibility tools tend to focus on package replay, unit validation, or metadata graphs, but lack a mechanism to unify runtime evidence, policy constraints, and standardized VEX/CSAF semantics into a single artifact.

## Approach
- The core method is a three-agent multi-agent framework: MCP handles pre-execution environment reconstruction, A2A monitors runtime dependencies and environment drift, and AGNTCY determines vulnerability exploitability by combining policy and VEX rules.
- This framework turns the SBOM from a “passive inventory” into an “active reasoning artifact”: agents read runtime telemetry, dependency usage, and environmental mitigations, then output structured VEX assertions rather than directly enforcing blocks.
- The authors make minimal, standards-aligned schema extensions to CycloneDX and SPDX, adding execution context, dependency evolution timelines, agent decision provenance, and CSAF evidence links, while preserving interoperability with the existing ecosystem.
- The evaluation design compares the system with provenance systems such as ReproZip, SciUnit, and ProvStore, and constructs runtime dependency ground truth using pre/mid/post snapshots, import hooks, and package manager records; reproducibility is divided into exact parity and semantic parity, with thresholds set to ε=1e-12 (deterministic statistics) and ε=1e-6 (floating-point ML).
- The system also adds fault tolerance and audit mechanisms, including heartbeat checks, fail-closed behavior, cross-snapshot consistency validation, session-key signing, and an integrity violation trigger requiring human adjudication when missing or incorrect-hash components exceed 2%.

## Results
- The paper claims that on heterogeneous analysis workloads, compared with existing provenance systems, it achieves better **runtime dependency capture**, **reproducibility fidelity**, and **vulnerability interpretation stability**, while maintaining relatively low computational overhead.
- The excerpt provides several evaluation/decision thresholds and scale indicators: semantic reproducibility thresholds are ε=1e-12 (deterministic) and ε=1e-6 (floating-point ML); if expected components are missing or have hash errors **>2%**, the system triggers an integrity violation; the CVE ecosystem had about **191,633** entries in 2025 and exceeded **200,000** in 2026, with more than **30,000** new entries added annually.
- The paper also uses external background data to illustrate the scale of the problem: about **95%** of vulnerabilities in SBOMs are typically not exploitable in products; Dependency-Track requests to OSS Index increased from **202 million** per month to **270 million**; the average product contains about **135-150** third-party components; and it is estimated that at least **50,000** organizations use SBOMs for vulnerability management.
- However, in the provided excerpt, **the full main quantitative results tables are not visible** (for example, specific capture rates, FPR/FNR, reproducibility rates, latency, overhead percentages, or exact deltas versus each baseline), so the magnitude of the core improvements cannot be restated precisely.
- The strongest empirical claim visible in the excerpt is that ablation experiments show that each of the three agents provides unique capabilities that deterministic automation alone cannot replace; the system can generate four contextualized VEX states: “Not Affected / Affected: Mitigated / Affected: Requires Review / Under Investigation.”

## Link
- [http://arxiv.org/abs/2603.10057v1](http://arxiv.org/abs/2603.10057v1)
