---
source: hn
url: https://news.ycombinator.com/item?id=47371155
published_at: '2026-03-13T23:01:31'
authors:
- Aamir21
topics:
- test-generation
- pull-request-analysis
- e2e-testing
- traceability
- graph-based-reasoning
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Generate tests from GitHub pull requests

## Summary
This work proposes a method for automatically generating end-to-end tests from GitHub Pull Requests, aiming to fill the gap in real user scenario testing that AI coding tools often miss. It emphasizes linking code changes, dependencies, and requirement descriptions to produce traceable tests and coverage reports for each PR.

## Problem
- Although AI coding tools can generate code quickly, they usually only add unit tests or integration tests, lacking high-quality end-to-end user scenario tests.
- In the repositories the author observed, after enabling Copilot-like tools, the ratio of new code to high-quality e2e tests “dropped significantly,” making key logic paths and edge cases more likely to go untested.
- This matters because if the PR stage lacks automated tests tied to requirements, defects are exposed later, and testing responsibility becomes fragmented, left for developers or testing teams to handle separately.

## Approach
- The system directly reads the Pull Request, analyzes changed files and diffs, and identifies the code areas affected by the current submission.
- It uses a single-repo or multi-repo dependency graph to identify “uncovered logic paths,” meaning which branches and flows introduced by the current changes have not yet been tested.
- The system combines user stories, requirement descriptions, or linked Jira/TMS/CMS information in the PR to understand acceptance criteria, then generates test scenarios.
- It ultimately produces automated e2e tests and coverage reports tied to the PR, and provides traceability from code references to requirement/test IDs.
- The author mentions internally using graphRAG to assist with context retrieval, but does not elaborate on the technical details.

## Results
- The article **does not provide formal benchmark data, dataset names, or reproducible experimental metrics**, so it is not possible to confirm any quantified improvement relative to a baseline.
- The author claims that in “early experiments,” the system **consistently found edge cases missed by developers**. This is the strongest empirical conclusion, but no figures are given for discovery rate, accuracy, or coverage.
- In terms of workflow, the system can run automatically in the process of “Push PR → read diff + Jira ticket → generate missing tests and coverage report,” indicating that it is positioned as PR-level test generation rather than offline test suggestions.
- The example provided shows the granularity of requirement traceability: for example, `src/api/auth.js:45-78` corresponds to `GITHUB-234 / JIRA-API-102`, and an integration test `IT-01` is generated to verify that an “invalid token returns 400,” with status Pass.

## Link
- [https://news.ycombinator.com/item?id=47371155](https://news.ycombinator.com/item?id=47371155)
