---
source: arxiv
url: https://arxiv.org/abs/2606.23197v1
published_at: '2026-06-22T11:44:58'
authors:
- Sophie Corallo
- Debora Grupp
- "Dominik Fuch\xDF"
- Jan Keim
- Frederik Reiche
- Tobias Hey
- Anne Koziolek
topics:
- secure-software-engineering
- requirements-traceability
- code-intelligence
- software-architecture
- security-dataset
- ev-charging
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# The EVerest Dataset for Secure Software Engineering

## Summary
EVerest is a public dataset for end-to-end security engineering across requirements, architecture, documentation, and code in an EV charging stack. Its main contribution is artifact coverage and fine-grained security labels; the paper does not report model benchmark scores.

## Problem
- Secure verification needs links from natural-language requirements to architecture and implementation; missing links can leave flaws such as unsafe authentication-token storage unchecked.
- Prior datasets cover requirements, code, or vulnerabilities in separate resources. In the authors' survey, none provides requirements, architecture, code, and security-objective labels together.
- This matters for code intelligence and traceability research because models need ground truth that connects security intent to architectural elements and source code.

## Approach
- The authors built the dataset from EVerest, an open-source EV charging station software stack. The source snapshot is everest-core from 2024-06-03, with about 50 kloc across more than 500 files and about 40 contributors.
- They elicited initial security requirements with a questionnaire sent to the EVerest community. Seven participants submitted 67 requirements; after cleanup, 57 were retained and labeled by security objective.
- They refined coarse requirements through four 90-minute developer interviews, producing 93 component-level security requirements. A later requirement check left 84 security requirements in the dataset.
- They derived a Palladio architecture model from source code, covering 29 components, 34 interfaces, 144 service effect specifications, and 14 usage scenarios.
- Three annotators labeled 1,445 security elements, acceptance windows, references, coreferences, and architectural trace links. The annotation work took about 100 person-hours.

## Results
- The dataset contains 84 manually elicited security requirements, 1,445 fine-grained security element labels, an architecture model, source code, and natural-language documentation.
- Security element labels include 195 components, 105 data items, 41 nodes, 143 entities, 597 states, 36 connections, 51 data flows, 207 activities, and 70 control flows.
- The trace-link gold standard includes model element IDs for entity-like elements. The paper reports 77 traced component mentions, 32 traced data mentions, and 3 traced entity mentions.
- The architecture model includes 29 components, 34 interfaces, 144 service effect specifications, and 14 usage scenarios, including firmware updates, charger enable or disable operations, and limit configuration.
- During dataset construction, the authors found a real CWE-1295 weakness: authentication tokens were stored in plain text in auth_token_providerImpl.cpp in the PN532TokenProvider module. They disclosed it to PIONIX, and it was fixed.
- No accuracy, F1, MAP, or other model benchmark results are reported. The paper's evidence is dataset scale, artifact coverage compared with surveyed datasets, and the discovered security weakness.

## Link
- [https://arxiv.org/abs/2606.23197v1](https://arxiv.org/abs/2606.23197v1)
