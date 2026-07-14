---
source: arxiv
url: https://arxiv.org/abs/2607.11348v1
published_at: '2026-07-13T10:08:24'
authors:
- Zahra Mousavi
- Chadni Islam
- M. Ali Babar
- Alsharif Abuadbba
- Kristen Moore
topics:
- code-intelligence
- software-security
- security-api-misuse
- developer-study
- human-ai-interaction
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Understanding the Impact of AI Code Assistants on Security API Usage: An Empirical Study

## Summary
The study examines how GitHub Copilot affects professional developers using security APIs. Across 44 developers and two Java tasks, Copilot improved functional correctness but did not produce a significant improvement in secure API usage.

## Problem
- Security APIs such as SSL/TLS and OAuth are complex, and misuse can enable vulnerabilities such as certificate-validation bypasses and unauthorized access.
- Prior research mainly tested AI-generated code with fixed prompts, leaving the effects of developers accepting, changing, or rejecting suggestions unclear.
- The study addresses whether Copilot changes correctness, security API misuse, and developers’ ability to recognize insecure results.

## Approach
- The researchers ran a within-subject study with 44 professional Java developers. Each developer completed one task with Copilot and another without AI assistance, with task order and Copilot access counterbalanced.
- The tasks used Java Secure Socket Extension for SSL/TLS communication and Google OAuth for delegated Gmail access.
- Researchers manually reviewed final code for security API misuse and functional correctness, then compared the conditions with logistic regression. The two reviewers reached strong agreement, with Cohen’s kappa of 0.97.
- The study also analyzed Copilot prompts and post-task self-assessments to measure security awareness.

## Results
- Copilot improved functional correctness, especially on the more complex security API task, compared with unaided development.
- Copilot marginally reduced some insecure patterns but did not significantly improve overall secure API usage.
- Only 2 of 44 participants explicitly considered security in their Copilot prompts, and many participants failed to recognize that their final code remained insecure even though security evaluation had been disclosed.
- Targeted security-focused prompts helped address some misuses in a post-study analysis, but Copilot still did not prevent all security API errors.
- The excerpt does not provide exact correctness rates, misuse rates, or statistical effect sizes for the main comparisons; it reports the study size, reviewer agreement of 0.97, and the qualitative direction of the findings.

## Link
- [https://arxiv.org/abs/2607.11348v1](https://arxiv.org/abs/2607.11348v1)
