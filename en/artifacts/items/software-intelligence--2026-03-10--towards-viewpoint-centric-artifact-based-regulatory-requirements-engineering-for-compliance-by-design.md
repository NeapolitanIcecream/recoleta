---
source: arxiv
url: http://arxiv.org/abs/2603.09492v1
published_at: '2026-03-10T10:51:40'
authors:
- Oleksandr Kosenkov
topics:
- regulatory-requirements
- compliance-by-design
- artifact-based-re
- viewpoint-coordination
- privacy-by-design
relevance_score: 0.47
run_id: materialize-outputs
language_code: en
---

# Towards Viewpoint-centric Artifact-based Regulatory Requirements Engineering for Compliance by Design

## Summary
This paper proposes an artifact-based regulatory requirements engineering framework, AM4RRE, centered on viewpoint coordination, with the goal of enabling a more systematic implementation of “compliance by design” across the software development life cycle. Its core contribution is connecting legal, business, requirements, and architecture viewpoints through a shared artifact model, in order to reduce the ad hoc and fragmented nature of current compliance practices.

## Problem
- Regulatory compliance in software engineering is becoming increasingly complex, as the number, scope, and knowledge density of regulations continue to grow, while industry still largely relies on isolated, ad hoc compliance practices.
- Regulatory requirements differ from ordinary business requirements: they are often “post hoc” requirements derived from interpretations of regulations, can in turn affect existing requirements and architecture, and require continuous coordination across legal, requirements, architecture, and other viewpoints.
- Existing process-/activity-centered methods struggle to ensure consistency, completeness, and verifiability under agile development and real project change, making them difficult to use for demonstrable compliance by design.

## Approach
- Based on literature research and multiple empirical studies, the authors extend AMDiRE and propose the artifact model AM4RRE, organizing regulatory requirements engineering around “what artifacts should be produced” rather than “which process should be followed.”
- AM4RRE contains 5 core parts: role model, goal model, project context model, milestone model, and content model; and it is organized around 4 viewpoints: legal, business, requirements, architecture.
- Its central mechanism is to use legal specifications as the foundation: legal concepts in regulatory text are first annotated and structured, then mapped into software context, requirements, and system specifications, forming consistent cross-viewpoint relationships.
- The model is operationalized through three kinds of tailoring: regulation-specific tailoring (extracting concepts and attributes from regulations), project content tailoring (mapping legal concepts to engineering artifacts), and goal-driven tailoring (determining which content items are needed based on organizational/project goals).
- The paper also reports preliminary evidence supporting the model: systematic mapping/review, interviews, focus groups, practice studies, and an initial validation of a legal concept instantiation method in GDPR/privacy by design scenarios.

## Results
- The paper does not provide quantitative experimental results for the final overall effectiveness of AM4RRE; this is a doctoral-stage paper, and the final model is still planned to be validated with practitioners in the future.
- The literature study identified **11 categories** of regulatory requirements engineering challenges, with the most prominent issues related to the knowledge density of legal/IT/privacy-security domains, the abstract nature of regulations, and difficulties in interaction among experts.
- In practice studies related to privacy by design, among **15 participants**, only **2** used systematic methods, while most of the rest still relied on unsystematic practices, supporting the importance of the problem.
- In the review of privacy design methods, only **5 papers** were identified that explicitly covered both requirements and system design, and the authors note that **none** of the methods can be directly and systematically reused for other regulations.
- From practitioner interviews, the authors derived **11** high-level RE goals for privacy by design, and accordingly incorporated a goal model into AM4RRE to support cross-viewpoint coordination and tailoring.
- The validation conclusion for the legal viewpoint and the GDPR concept instantiation method is **overall positive/applicable**: feedback from legal expert walkthroughs was positive; practitioner validation showed that the method can be used to capture legal domain knowledge and allocate it to the requirements and system levels, but the paper does not report precise metrics or baseline comparison values.

## Link
- [http://arxiv.org/abs/2603.09492v1](http://arxiv.org/abs/2603.09492v1)
