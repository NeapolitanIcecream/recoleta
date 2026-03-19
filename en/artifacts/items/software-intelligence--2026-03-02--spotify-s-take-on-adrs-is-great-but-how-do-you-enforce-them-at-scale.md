---
source: hn
url: https://news.ycombinator.com/item?id=47226046
published_at: '2026-03-02T23:59:47'
authors:
- iamalizaidi
topics:
- adr-enforcement
- github-action
- code-review
- architecture-governance
- developer-workflow
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Spotify's take on ADRs is great, but how do you enforce them at scale?

## Summary
This is an open-source tool that automatically "surfaces" Architecture Decision Records (ADRs) during the pull request stage. Via a GitHub Action/CLI, it automatically shows relevant decisions when code touches protected files. It aims to solve the execution gap where ADRs get written but no one reads them when actually changing code.

## Problem
- Even when teams write ADRs, they often sit dormant in `docs/adr/`, and developers typically do not proactively consult them before submitting a PR.
- The moment when architectural decisions truly need to be seen is not during onboarding or planning meetings, but when someone is modifying code constrained by those decisions.
- `CODEOWNERS` alone can only assign reviewers; it cannot explain *why* a change must be made a certain way, making it hard to embed architectural constraints into day-to-day development workflows.

## Approach
- Write decisions in plain Markdown compatible with existing ADRs, declaring status, severity level, and the scope of protected files.
- Use a GitHub Action or CLI in CI to detect PR changes; once a modification matches a rule, the corresponding ADR is automatically posted as a comment on the PR.
- Rule matching supports glob patterns, regex, content-based rules, and boolean logic, so that "code changes" can be mapped to "architectural decisions that should be surfaced."
- Severity is tiered (Critical / Warning / Info); critical level can be used to block PRs, upgrading from "reminder" to "enforcement."
- The tool emphasizes practical engineering deployability: beyond GitHub, the CLI can integrate with GitLab/Jenkins/CircleCI/pre-commit, and it makes no external network calls.

## Results
- The text does not provide standard benchmark data, offline evaluation, or controlled experimental results, so there are **no quantitative research metrics** to report.
- Engineering claims include the ability to handle PRs with **3000+ files** without OOM.
- Quality and security claims include **109 tests**, plus **ReDoS protection** and **path traversal protection**.
- Functional comparison claims: compared with `CODEOWNERS`, it not only assigns reviewers but also explains the relevant architectural rationale; compared with `Danger.js`, it does not require writing code, and decisions can be maintained in Markdown.
- Deployment and adoption claims: the tool is **MIT licensed**, supports a one-step GitHub Action or the `npx decision-guardian` CLI, and is positioned as a low-integration-cost ADR enforcement solution.

## Link
- [https://news.ycombinator.com/item?id=47226046](https://news.ycombinator.com/item?id=47226046)
