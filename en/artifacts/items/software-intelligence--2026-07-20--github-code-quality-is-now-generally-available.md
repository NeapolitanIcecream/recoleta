---
source: hn
url: https://github.blog/changelog/2026-07-20-github-code-quality-is-now-generally-available/
published_at: '2026-07-20T23:45:53'
authors:
- andsoitis
topics:
- code-intelligence
- software-quality
- ai-assisted-development
- code-analysis
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# GitHub Code Quality is now generally available

## Summary
GitHub Code Quality is generally available on GitHub Enterprise Cloud and GitHub Team as a paid product for detecting maintainability, reliability, and test-coverage issues in pull requests. It combines deterministic CodeQL analysis, AI-assisted detection, and Copilot Autofix so teams can review and address quality findings before merging.

## Problem
- AI-generated code increases the volume of code teams must review, making maintainability and reliability problems harder to catch before release.
- Teams need quality checks and coverage thresholds integrated into pull requests so they can ship code they trust.

## Approach
- Combine CodeQL's deterministic analysis with AI-assisted detection for maintainability and reliability findings.
- Use Copilot Autofix to suggest fixes that developers review before merging.
- Provide organization-level dashboards, pull-request coverage metrics from Cobertura XML reports, and quality gates through GitHub rulesets.
- Expose APIs for repository enablement and finding retrieval, with evaluate mode for gradual rollout.

## Results
- In GitHub's own engineering organization, teams resolve 67.3% of Code Quality findings before merging pull requests.
- More than 10,000 enterprises used Code Quality during the public preview.
- General availability began on July 20, 2026 for GitHub Enterprise Cloud and GitHub Team; it was not available on GitHub Enterprise Server at launch.
- Pricing is $10 per active committer per month, plus metered AI-assisted work and GitHub Actions compute for CodeQL analysis.
- The excerpt reports adoption and an internal resolution rate, but no independent benchmark or comparison with other code-quality tools.

## Link
- [https://github.blog/changelog/2026-07-20-github-code-quality-is-now-generally-available/](https://github.blog/changelog/2026-07-20-github-code-quality-is-now-generally-available/)
