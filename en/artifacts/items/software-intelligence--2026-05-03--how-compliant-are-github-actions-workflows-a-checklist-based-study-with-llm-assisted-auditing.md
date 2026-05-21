---
source: arxiv
url: https://arxiv.org/abs/2605.02091v1
published_at: '2026-05-03T23:21:13'
authors:
- Edward Abrokwah
- Taher A. Ghaleb
topics:
- github-actions
- ci-compliance
- llm-auditing
- software-engineering
- code-intelligence
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing

## Summary
The paper studies whether LLMs can audit GitHub Actions workflows against documented best practices. Its main claim is that LLMs can scale measurement, but reliable audits still need GPT-5 dispute resolution and human checks.

## Problem
- GitHub Actions workflows can pass syntax checks while still violating security, maintainability, and performance practices, such as broad permissions, hardcoded secrets, unpinned actions, and missing failure notifications.
- Existing tools such as actionlint and yamllint catch malformed YAML and invalid action references, not whether a workflow follows GitHub documentation.
- This matters because CI workflow mistakes can expose secrets, expand token access, slow builds, and make failures harder to diagnose.

## Approach
- The authors derive a 30-item compliance checklist from official GitHub Actions documentation, covering 4 workflow sections and 8 themes.
- They convert each checklist item into a YES, NO, or NOT APPLICABLE audit question.
- They test 4 open-weight LLMs on 95 real-world Java GitHub Actions workflows, giving 2,850 checklist assessments per model and 11,400 model outputs total.
- They accept unanimous and near-unanimous model votes, send split cases to GPT-5, and use targeted human review for unresolved cases.

## Results
- The checklist contains 30 criteria: 3 workflow-level, 11 job-level, 15 step-level, and 1 permissions-level criterion.
- Across 2,850 checklist questions, 4-model agreement was unanimous for 758 cases (27%), near-unanimous for 1,104 cases (39%), and split for 988 cases (35%).
- Inter-model agreement was only fair, with Fleiss' kappa = 0.28.
- The GPT-5 plus human review process reduced verification effort by 81% while keeping 87% agreement with expert judgment.
- At scale, overall workflow compliance was 28%; permission controls had 4% compliance, Security had 26%, and Clarity had 68%.
- The paper claims LLMs are useful for large compliance scans, but security-sensitive and structure-dependent judgments still need adjudication and expert review.

## Link
- [https://arxiv.org/abs/2605.02091v1](https://arxiv.org/abs/2605.02091v1)
