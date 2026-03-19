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
- data-governance
- access-control
- privacy-preserving-ml
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Building Privacy-and-Security-Focused Federated Learning Infrastructure for Global Multi-Centre Healthcare Research

## Summary
FLA^3 is a governance-enhanced infrastructure for multi-centre federated learning in healthcare. Under the premise that “data never leaves the hospital,” it makes authentication, authorisation, and accounting first-class controls enforced at runtime. The paper’s main argument is that in real cross-border, regulated healthcare environments, federated learning must not only protect data, but also enforceably guarantee who can participate, when they can participate, and why they can participate.

## Problem
- Multi-institution healthcare research needs larger and more heterogeneous datasets, but cross-border sharing of patient data is strictly constrained by regulations such as GDPR and HIPAA, making many valuable AI models difficult to train.
- Most existing federated learning frameworks only address “keeping data local,” but do not enforce governance requirements at runtime, such as **authentication, study-based authorisation, time-bounded validity, and audit trails**, so real clinical deployments may still constitute unauthorised processing.
- This matters because even if raw data never leaves the hospital, if nodes with expired approvals continue participating, or unauthorised institutions join training, the entire study may become non-compliant and undermine trust among patients and institutions.

## Approach
- Proposes **FLA^3 (FL with AAA)**: directly integrating **authentication, authorisation, accounting** into the federated learning orchestration layer, rather than relying only on organisational processes or static configuration.
- Uses **XACML-compatible attribute-based access control (ABAC)**: at each key federated learning lifecycle stage, the system checks institution identity, study ID, role, approval status, and temporal validity; if policy evaluation fails or context is missing, it denies by default (fail-closed).
- Designs **study-scoped federation**: each study is treated as an independent federation, with its own set of participating institutions, policies, and time window, avoiding a situation where “approval for one study grants access to all studies.”
- Adds **cryptographic auditing/accounting**: security-relevant operations generate audit records with cryptographic signatures, making participation attributable, auditable, and accountable.
- Implementation-wise, it extends **Flower** and is compatible with the personalised federated learning method **FedMAP**, to handle the non-IID heterogeneity common in healthcare data while also fitting the outbound-only network environments often found in hospitals.

## Results
- **Real-world deployment feasibility**: the platform was deployed across **5 institutions in 4 countries** in the **BloodCounts! Consortium** (United Kingdom, Netherlands, India, and The Gambia); the paper states that governance policies were correctly enforced under realistic network limitations and regulatory constraints.
- **Clinical utility evaluation**: simulated federated experiments were conducted on **INTERVAL** data, covering **54,446 samples, 35,315 subjects, and 25 centres**.
- The paper’s core performance claim is that **FLA^3 achieves predictive performance comparable to centralised training** while strictly enforcing governance constraints.
- It also claims that after integration with **FedMAP**, the governance mechanism **does not reduce personalised federated learning performance**, and federated training **significantly outperforms single-institution standalone training**.
- **No explicit numerical metrics provided**: the excerpt does not report AUROC, accuracy, error values, or percentage relative improvements, nor does it provide detailed numerical comparisons against specific baselines; the strongest quantitative evidence is mainly the deployment scale (5 institutions / 4 countries) and data scale (54,446 samples / 25 centres).

## Link
- [http://arxiv.org/abs/2603.10063v1](http://arxiv.org/abs/2603.10063v1)
