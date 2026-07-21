---
source: arxiv
url: https://arxiv.org/abs/2607.17686v1
published_at: '2026-07-20T08:36:54'
authors:
- Mansur Arief
- Nur Ahmad Khatim
- Ali Akarma
- Ahmad Alfan Alfian Irfan
topics:
- requirements-traceability
- verification-validation
- software-testing
- ai-compliance
- executable-specifications
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Integrating High-Level Requirements to Low-Level Tests with Machine-Readable V&V Specifications

## Summary
VNVSpec connects high-level requirements to executable tests and audit-ready verification evidence through a machine-readable specification and traceability graph. The framework targets software and AI systems that need requirement coverage, standards mapping, and continuously updated evidence in developer workflows.

## Problem
- High-level requirements and low-level tests usually live in separate tools, leaving teams unable to reliably identify uncovered requirements or determine which evidence supports a standard clause.
- This gap matters for AI-enabled and cyber-physical systems because regulators and safety standards require traceable evidence, while raw test pass/fail results lack that structure.

## Approach
- Represent requirements, hazards, contracts, standards mappings, test links, and evidence as typed, immutable objects stored in Python, YAML, or TOML.
- Decompose user requirements into module-level requirements with explicit metrics and acceptance criteria, then connect tests and other verification activities through a directed acyclic traceability graph.
- Integrate existing tools through a pytest plugin, JUnit XML ingestion for JavaScript, Java, and C++ runners, an evidence collector for analyses and formal verification, and adapters for PyTorch and HuggingFace models.
- Apply eight requirement-quality checks, conservatively roll evidence into pass, fail, or inconclusive verdicts, and export developer reports, compliance matrices, GSN assurance cases, and EU AI Act Annex IV documentation skeletons.

## Results
- In self-application, VNVSpec continuously assessed its own specification containing 36 requirements verified by 449 tests.
- The paper reports that assessment time scales linearly and that the workflow can handle up to 10,000 requirements within the stated limited-time evaluation; the excerpt does not provide the detailed runtime values.
- Five example catalogs contain 116 requirements, with 82 mapped to at least one standards clause, or 71%.
- The framework demonstrates linked evidence from ordinary pytest tests, Jest results imported through JUnit XML, and CROWN-based formal bounds for neural-network properties over continuous perturbation ranges.
- The provided text does not report a comparative benchmark against an alternative traceability or requirements-management system, nor does it give quantitative quality-checker detection rates or integration-overhead values.

## Link
- [https://arxiv.org/abs/2607.17686v1](https://arxiv.org/abs/2607.17686v1)
