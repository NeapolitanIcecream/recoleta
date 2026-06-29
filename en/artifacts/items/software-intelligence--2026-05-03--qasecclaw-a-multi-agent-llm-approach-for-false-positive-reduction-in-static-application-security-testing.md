---
source: arxiv
url: https://arxiv.org/abs/2605.01885v1
published_at: '2026-05-03T14:05:52'
authors:
- Mohd Ruhul Ameen
- Md Takrim Ul Alam
- Akif Islam
topics:
- code-intelligence
- sast
- llm-agents
- software-security
- false-positive-reduction
- multi-agent-software-engineering
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing

## Summary
QASecClaw uses Semgrep to find candidate security issues, then uses a coding-focused LLM agent to suppress likely false positives after reading code context. On OWASP Benchmark v1.2, it reports much higher precision and F1 than standalone Semgrep, with a small recall drop.

## Problem
- SAST tools often flag safe code as vulnerable when they match a risky pattern but miss nearby context such as sanitization, encoding, validation, or parameterized APIs.
- False positives waste developer and security-review time, reduce trust in scanner output, and can cause real vulnerabilities to be ignored.
- The paper targets false positive reduction while keeping SAST as the high-recall source of candidate findings.

## Approach
- QASecClaw runs Semgrep first and treats its alerts as candidate vulnerabilities rather than asking an LLM to search the whole codebase.
- A SAST Filter Agent sends each finding, CWE type, file location, and source-code context to Qwen 3.5 Plus and asks for a true-positive or false-positive judgment.
- A Mission Orchestrator coordinates agents for test planning, Semgrep-based validation, evidence correlation, LLM filtering, and report generation.
- The system processes findings in batches of 15 files and validates the LLM response as structured JSON.
- If the LLM fails, times out, or returns malformed JSON, QASecClaw keeps the original Semgrep finding to avoid hiding a possible real issue.

## Results
- Evaluation uses the full OWASP Benchmark v1.2: 2,740 Java test cases across 11 CWE categories, with 1,415 vulnerable cases and 1,325 safe cases.
- QASecClaw reports F1 = 90.93% versus 78.39% for standalone Semgrep, a gain of about 12.54 percentage points.
- False positives fall from 560 with Semgrep to 64 with QASecClaw, an 88.6% reduction, while recall drops by 3.1%.
- Aggregate metrics in the paper show QASecClaw at precision 0.951, recall 0.871, F1 0.909, false positive rate 0.048, and Youden’s J 0.823; Semgrep scores precision 0.695, recall 0.900, F1 0.784, false positive rate 0.423, and Youden’s J 0.477.
- Per-CWE results cited in the abstract include SQL Injection F1 = 94.05%, Cross-Site Scripting F1 = 89.58%, and Weak Cryptography F1 = 99.61%.

## Link
- [https://arxiv.org/abs/2605.01885v1](https://arxiv.org/abs/2605.01885v1)
