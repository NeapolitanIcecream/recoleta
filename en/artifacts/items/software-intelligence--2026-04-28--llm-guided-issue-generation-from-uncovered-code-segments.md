---
source: arxiv
url: https://arxiv.org/abs/2604.26118v2
published_at: '2026-04-28T21:10:53'
authors:
- Diany Pressato
- Honghao Tan
- Mariam Elmoazen
- Shin Hwei Tan
topics:
- code-intelligence
- automated-bug-detection
- llm-agents
- software-testing
- issue-generation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# LLM-Guided Issue Generation from Uncovered Code Segments

## Summary
IssueSpecter turns uncovered Python code segments into ranked bug reports with reproduction steps and candidate fixes. The paper claims this helps find latent defects before a human files an issue.

## Problem
- Automated issue-fixing systems need a bug report before they can act, so defects in untested code may stay hidden until users hit them.
- Coverage-driven test generation can reach buggy paths, but generated assertions may encode the current wrong behavior and hide the defect.
- Raw LLM bug reports can be noisy; developers need ranking, reproduction steps, and fixes to decide what to inspect first.

## Approach
- SlipCover identifies code segments that the existing unit tests do not cover.
- GPT-5-mini reviews each uncovered segment and generates up to 3 issue reports with severity, affected operating systems, reproduction steps, and suggested code fixes.
- A rule-based selection step ranks reports by severity, operating-system impact, and description length, then keeps the top 10 issues per project.
- GPT-5-mini reranks those 10 issues by impact, scope, and urgency.
- The system runs the existing test suite on proposed fixes and lowers the rank of issues whose patches introduce new failing tests.

## Results
- On 13 active Python projects from CodaMosa, IssueSpecter generated 10,467 issue reports from uncovered segments.
- Human annotation of 130 top-ranked issues found 49 valid bugs (37.7%), 61 issues needing further investigation (46.9%), and 20 invalid reports (15.4%); valid or plausible reports totaled 84.6%.
- Annotator agreement was 80.3% on the 130 manually reviewed issues.
- LLM-based ranking beat rule-based ranking by 50% at P@3 and 41% in MRR; in the HTTPie example, MRR improved from 0.14 to 1.00 and ranked a CWE-22 path traversal issue first.
- Against CoverUp on 168 matched artifacts per tool, IssueSpecter reported a higher bug validity rate: 81.0% vs. 76.2%, using the same model and evaluation count.
- The annotated issues covered 9 of 10 bug taxonomy categories, with 43 logic or conditional bugs, 39 input-validation or boundary bugs, and 4 security-related bugs.

## Link
- [https://arxiv.org/abs/2604.26118v2](https://arxiv.org/abs/2604.26118v2)
