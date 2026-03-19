---
source: arxiv
url: http://arxiv.org/abs/2603.02512v3
published_at: '2026-03-03T01:46:41'
authors:
- "Szil\xE1rd Enyedi"
topics:
- software-supply-chain
- module-repositories
- ai-assisted-development
- provenance
- secure-composition
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Human-Certified Module Repositories for the AI Age

## Summary
This paper proposes **Human-Certified Module Repositories (HCMR)** as a trustworthy module infrastructure for AI-assisted/automated software construction. The core idea is to make human review, supply-chain provenance, and composable interface constraints the **security foundation** for AI-assembled software.

## Problem
- Modern software increasingly depends on deep dependency trees, automated builds, and external modules, but common repositories lack **clear provenance, systematic security review, and constraints on compositional behavior**.
- This amplifies supply-chain risk; the paper uses incidents such as **SolarWinds (about 18,000 downstream organizations)**, **Log4Shell**, and the **XZ backdoor** to show how the compromise of a single upstream component or maintainer can trigger ecosystem-wide cascading effects.
- As AI-generated code and multi-component orchestration become more common, if AI assembles systems from untrustworthy modules, the results will be difficult to audit, difficult to predict, and difficult to assign accountability for.

## Approach
- Proposes **HCMR**: a curated module repository in which modules must include **strong provenance metadata, explicit interface contracts, and security review**, and where appropriate, formal or semi-formal assurances.
- Uses a **human-machine certification workflow**: first perform automated admission checks (dependency hygiene, reproducible builds, provenance integrity, interface-contract consistency), then conduct manual security review and behavioral validation, and finally publish a certified version.
- Introduces **multi-level assurance tiers**: lower tiers emphasize engineering discipline and provenance, while higher tiers add static analysis, formal reasoning, or stronger contract checking.
- Enables IDEs or AI agents to follow **secure-by-default composition rules** during assembly: only modules satisfying compatibility, dependency integrity, and provenance verification requirements may be combined.
- The design draws on supply-chain attestation and signing mechanisms such as **SLSA/Sigstore**, as well as practices from highly governed module ecosystems like **Azure Verified Modules**.

## Results
- This paper is primarily an **architectural/conceptual proposal** and **does not provide new experimental benchmarks, accuracy, success-rate, or performance figures** to validate HCMR itself.
- The strongest quantitative support in the paper comes from motivating cases rather than method evaluation: **SolarWinds** affected about **18,000** downstream organizations; analysis related to **XZ** says its impact approached **30,000** Debian/Ubuntu packages; research on **IFTTT** shows that **more than half** of services in its ecosystem are related to IoT.
- It provides a **reference architecture**, certification workflow, threat-surface analysis, and a comparison table with existing ecosystems; in that table, **HCMR** is positioned as stronger than **IFTTT / Node-RED / AVM** in **governance, provenance, and certification**, but this is a conceptual comparison rather than an empirical benchmark result.
- The main breakthrough claim is that by combining **human certification + machine-readable contracts + verifiable provenance** within a module repository, it is possible to provide greater **predictability, auditability, and accountability** for **AI-constructed software systems**; however, the paper does not report real-world deployment or quantified benefits.

## Link
- [http://arxiv.org/abs/2603.02512v3](http://arxiv.org/abs/2603.02512v3)
