---
source: arxiv
url: https://arxiv.org/abs/2606.18976v1
published_at: '2026-06-17T12:00:21'
authors:
- Marco Becattini
- "Niccol\xF2 Caselli"
- Matteo Minin
- Roberto Verdecchia
- Enrico Vicario
topics:
- multi-agent-llm
- software-architecture
- automated-feedback
- software-engineering-education
- evidence-grounding
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# CAPRA: Scaling Feedback on Software Architecture Deliverables with a Multi-Agent LLM System

## Summary
CAPRA is a multi-agent LLM tool that reviews student software architecture reports and produces evidence-checked LaTeX feedback. It targets architecture documentation, where manual review is slow and ordinary automated grading has weak support.

## Problem
- Software architecture deliverables mix requirements, UML diagrams, tests, design rationale, and traceability, so instructors need substantial time to review them.
- Existing automated assessment works better for code because code has tests and static checks; architecture reports are open-ended and multi-modal.
- LLM feedback can mislead students when it invents issues or gives generic comments without source evidence.

## Approach
- CAPRA parses a student PDF with PyMuPDF for text and gpt-4o vision for UML and other diagrams, then inserts diagram descriptions into the document text.
- Specialized agents inspect the same enriched document for requirements, use cases, architecture, tests, required course features, and traceability links.
- Each issue must carry a quote, a severity, and a confidence score.
- A deterministic evidence anchoring step checks each quote against the source text with fuzzy matching based on normalized Levenshtein distance; matches below 0.45 are discarded and findings below 0.65 confidence are filtered out.
- A ConsistencyManager agent merges duplicate findings, and fixed LaTeX templates generate the final PDF feedback report.

## Results
- On 10 evaluation reports, CAPRA passed 88.8% of the eight binary criteria under strict aggregation, where both raters had to mark a criterion as pass.
- Under lenient aggregation, the pass rate was 91.9% across the same 8 criteria and 10 reports.
- The two human raters agreed on 75 of 80 decisions, a raw agreement rate of 93.75%, with Cohen's kappa of 0.582.
- CAPRA processed each report in slightly over 4 minutes at about $0.44 per report.
- The paper compares this with an estimated 30-45 minutes for a thorough manual review of one architecture report.
- The study used 10 high-scoring reports to build the feature knowledge base and a separate set of 10 reports for evaluation, so the evidence is preliminary.

## Link
- [https://arxiv.org/abs/2606.18976v1](https://arxiv.org/abs/2606.18976v1)
