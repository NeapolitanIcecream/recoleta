---
source: hn
url: https://policycortex.com
published_at: '2026-03-07T23:24:40'
authors:
- policycortex
topics:
- cloud-compliance
- autonomous-remediation
- ai-agent
- cloud-security
- audit-automation
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Show HN: PolicyCortex – AI agent that autonomously remediates cloud misconfigs

## Summary
PolicyCortex is an AI agent platform for cloud compliance and security operations, focused on continuous detection of cloud misconfigurations, audit evidence collection, and controlled autonomous remediation. It targets highly regulated environments such as defense contractors and DOE labs, emphasizing “continuous compliance” rather than last-minute audit prep.

## Problem
- Compliance requirements in cloud environments such as **CMMC / NIST 800-171 / CIS** often rely on manual checks, fragmented tools, and temporary audit preparation, causing misconfigurations to persist and evidence collection to remain inefficient.
- Highly sensitive organizations (such as defense contractors and federal agencies) need to continuously monitor 110+ controls across **multi-cloud environments** and connect findings, remediation, audit documentation, and approval workflows.
- Alerts alone do not solve the problem; automatic remediation without constraints can also accidentally impact production systems, so a “controlled autonomy” remediation mechanism is needed.

## Approach
- The platform first integrates with **AWS / Azure / GCP**, automatically discovers resources, policy assignments, and applicable compliance frameworks, and performs continuous scanning and real-time compliance monitoring.
- It maps compliance findings to **MITRE ATT&CK** and provides executable remediation paths; for AI assets, it also maps to **MITRE ATLAS** for AI-specific observability and threat detection.
- Its core mechanism is the patent-pending **Safety Sandwich**: **pre-execution guardrails → AI decision layer (Xovyr) → post-execution validation**. In simple terms, it first checks risk boundaries, then lets AI plan/generate remediation actions, and finally validates the changes while preserving rollback capability.
- Autonomous remediation supports multiple execution paths: direct fixes, pushing PRs to **CI/CD**, creating **Jira** tickets, or sending **Slack** notifications, while recording audit logs and rollback IDs; production resources require explicit approval by default.
- Beyond remediation, the system also automates generation of audit materials such as **SSP, POA&M, ATO**, as well as FinOps recommendations based on **60–90 day** usage patterns.

## Results
- The text **does not provide standard paper-style quantitative evaluation** (such as false positive rate, remediation success rate, comparison with baseline tools, or results on public datasets).
- The explicitly stated coverage includes support for **12+ compliance frameworks**, **3 cloud providers**, mapping to **110+ NIST controls**, and **4 deployment models/form factors** (the text describes SaaS, Private Cloud, and Air-Gapped in detail, while the page separately states 4 deployment models).
- The FinOps module claims to generate resource right-sizing recommendations based on **60–90 day** usage patterns rather than only the previous month's invoice.
- At the target-market level, the page claims to address CMMC needs for **80,000+ defense contractors** and says it is trusted by defense contractors, but does not provide customer count, conversion rate, or audit pass rate.
- The key product claim is that it can discover cloud resources and policies “within minutes,” perform **continuous monitoring**, **automatic evidence collection**, and **autonomous remediation with rollback**, and support **air-gapped** on-prem inference deployment.

## Link
- [https://policycortex.com](https://policycortex.com)
