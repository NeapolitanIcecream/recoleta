---
source: arxiv
url: http://arxiv.org/abs/2603.10063v1
published_at: '2026-03-09T22:13:00'
authors:
- Fan Zhang
- Daniel Kreuter
- Javier Fernandez-Marques
- BloodCounts Consortium
- Gregory Verghese
- Bernard Butler
- Nicholas Lane
- Suthesh Sivapalaratnam
- Joseph Taylor
- Norbert C. J. de Wit
- Nicholas S. Gleadall
- "Carola-Bibiane Sch\xF6nlieb"
- Michael Roberts
topics:
- federated-learning
- healthcare-ai
- privacy-governance
- access-control
- auditability
- secure-infrastructure
relevance_score: 0.23
run_id: materialize-outputs
language_code: en
---

# Building Privacy-and-Security-Focused Federated Learning Infrastructure for Global Multi-Centre Healthcare Research

## Summary
This paper proposes FLA^3, a “governance-aware” infrastructure for healthcare federated learning that directly embeds authentication, authorisation, and accounting (AAA) into the federated learning orchestration layer to satisfy privacy and compliance requirements across institutions and jurisdictions. Its focus is not on improving the accuracy of a new model, but on making real-world healthcare federated learning deployable, auditable, and still able to maintain performance close to centralised training under strict governance constraints.

## Problem
- Multi-centre healthcare research requires joint training across institutions, but cross-border sharing of raw data is often restricted by regulations such as GDPR and HIPAA, preventing many models from being trained on sufficiently large and diverse datasets.
- Existing federated learning frameworks largely remain at the prototype-validation stage, typically assuming trusted participants and lacking runtime-enforceable governance mechanisms: **who can join, which study they can participate in, within what time window, what operations they can perform, and how actions are logged for accountability**.
- In healthcare settings, even if data never leaves the hospital, continuing computation after approval has expired or within an unapproved study still constitutes unauthorised processing, which can make the entire study non-compliant or even invalid. This makes the problem important.

## Approach
- Proposes **FLA^3 (FL with AAA)**: adding governance controls to the federated learning orchestration layer rather than relying only on data localisation or encryption techniques.
- Uses **XACML-compatible attribute-based access control (ABAC)** for runtime policy decisions, enforcing five categories of governance requirements: institutional authentication, study-scope authorisation, role-based least privilege, time validity, and audit traceability.
- Adopts a **fail-closed** mechanism: if policy evaluation fails, contextual attributes are missing, or approval has expired, participation or execution is denied by default, preventing “allow by default”.
- Introduces **study-scoped federation**: each study is an independent federation with its own participant set, authorisation policies, and validity period, allowing multiple studies to run concurrently on the same platform.
- Combines **cryptographically signed audit logs** with a Flower-based implementation; and shows that it can work together with the personalised federated learning method **FedMAP** while maintaining performance on non-IID healthcare data.

## Results
- **Real deployment feasibility**: the platform has been deployed to **5 BloodCounts! Consortium institutions** across **4 countries** (the United Kingdom, the Netherlands, India, and The Gambia); the authors claim that governance policies execute correctly under real network and regulatory constraints.
- **Clinical data scale**: simulated federated experiments were conducted on the INTERVAL study using full blood count data from **54,446 samples, 35,315 subjects, and 25 centres**.
- **Performance claim**: the authors state that under strict governance constraints, FLA^3 achieves predictive performance **comparable to centralised training**, and **significantly improves compared with individual training**.
- **Governance compatibility claim**: the authors explicitly state that after introducing policy-driven governance, **personalised federated learning performance is not reduced when integrated with FedMAP**.
- **No specific accuracy values provided in the excerpt**: the excerpt does not provide explicit metrics such as AUROC, AUPRC, or accuracy, nor percentage-point differences versus specific baselines, so further quantitative comparison is not possible.
- **Additional evidence**: the authors also cite their systematic review showing that only about **5%** of healthcare FL work involves real deployments, and that in their prior review **87/89 (98%)** of methods lacked node authentication and **0 papers** provided an openly implementated governance system suitable for peer review, underscoring that the practical breakthrough of this work lies in “enforceable governance infrastructure”.

## Link
- [http://arxiv.org/abs/2603.10063v1](http://arxiv.org/abs/2603.10063v1)
