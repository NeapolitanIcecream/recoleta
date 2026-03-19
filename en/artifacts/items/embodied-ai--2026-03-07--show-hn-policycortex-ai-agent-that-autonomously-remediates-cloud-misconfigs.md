---
source: hn
url: https://policycortex.com
published_at: '2026-03-07T23:24:40'
authors:
- policycortex
topics:
- cloud-security
- compliance-automation
- autonomous-remediation
- misconfiguration-detection
- ai-ops
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Show HN: PolicyCortex – AI agent that autonomously remediates cloud misconfigs

## Summary
PolicyCortex is an automation platform for cloud security and compliance, focused on continuous monitoring, audit evidence collection, and autonomous remediation of cloud misconfigurations. Its core value proposition is using AI agents with deterministic guardrails and rollback capability to move from merely “finding problems” to “automatically fixing problems” without sacrificing safety.

## Problem
- Compliance requirements such as CMMC, NIST 800-171, and CIS in cloud environments typically rely on manual checks, fragmented tools, and ad hoc audit preparation, leading to low efficiency, frequent omissions, and difficulty maintaining continuous audit readiness.
- Alerts without remediation allow cloud misconfigurations to persist for long periods; but letting AI directly change production environments introduces risks of mistakes, blast radius, and compliance issues.
- This matters for defense contractors, DOE labs, and federal agencies because they face strict authorization and assessment requirements, and failure can affect business eligibility, audit outcomes, and security posture.

## Approach
- After connecting AWS, Azure, and GCP accounts, the platform automatically discovers resources, policy assignments, and applicable compliance frameworks, and continuously scans the environment.
- Detected configuration issues are mapped to CMMC, NIST 800-171, CIS, custom frameworks, and MITRE ATT&CK/ATLAS for prioritization, risk explanation, and generation of remediation paths.
- The core mechanism is the so-called **Safety Sandwich**: **pre-execution guardrail checks → AI decision layer (Xovyr) plans remediation/generates code/selects execution path → post-execution validation**, with rollback IDs preserved.
- To reduce autonomy risk, the system claims it will not touch production resources without explicit approval, while supporting multiple execution methods such as direct remediation, pushing CI/CD PRs, creating Jira tickets, or sending Slack notifications.
- In addition to remediation, it automatically collects compliance evidence, generates SSP, POA&M, and ATO packages, and integrates continuous governance, audit preparation, FinOps, and AI observability into one platform.

## Results
- The text **does not provide paper-style experimental results or benchmark tests**. It gives no quantitative comparison on false positive rate, remediation success rate, audit pass rate, latency, cost savings, or performance versus competitors or manual processes.
- The most specific coverage metrics include: support for **12+** compliance frameworks, **3** cloud providers, mapping to **110+** NIST controls, and **4** deployment models.
- Recommendations in the FinOps module are based on **60–90 days** of usage patterns rather than last month’s bill; this describes the product mechanism, not an outcome metric.
- Market-size-oriented statements include that **80,000+** defense contractors face CMMC deadline requirements; this is application-context background, not a system performance result.
- Non-research numerical claims related to the founders include that the platform is built with **600K+** lines of production code and has filed **4** U.S. patents; these indicate engineering investment and IP positioning, but cannot substitute for technical validation results.
- Therefore, the strongest verifiable claim is that the system asserts it can achieve “guardrailed autonomous remediation” and “automated audit evidence/authorization document generation” on top of continuous monitoring, but it **lacks public quantitative evidence** demonstrating the magnitude of improvement over existing approaches.

## Link
- [https://policycortex.com](https://policycortex.com)
