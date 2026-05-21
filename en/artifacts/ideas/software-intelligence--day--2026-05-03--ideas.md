---
kind: ideas
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: 15787cf9-193c-4087-b517-2963b8b2e48b
status: succeeded
topics:
- LLM software engineering
- static analysis
- vulnerability repair
- refactoring correctness
- agent context
- AI reliability
tags:
- recoleta/ideas
- topic/llm-software-engineering
- topic/static-analysis
- topic/vulnerability-repair
- topic/refactoring-correctness
- topic/agent-context
- topic/ai-reliability
language_code: en
pass_output_id: 127
pass_kind: trend_ideas
upstream_pass_output_id: 126
upstream_pass_kind: trend_synthesis
---

# Bounded LLM Review Gates

## Summary
LLM adoption looks most credible where the input is already bounded: one scanner alert, one workflow file checked against a fixed list, or one before-and-after refactoring pair. The practical pattern is a small review layer with explicit fallback rules and a local accuracy check before it touches production gates.

## LLM false-positive filtering for Semgrep security alerts
Security teams that already run Semgrep can add an LLM review step after the scanner, using the Semgrep finding, CWE label, file location, and nearby source context as the only input. The output should be a structured true-positive or false-positive judgment plus a short reason. If the model times out or returns malformed JSON, the workflow should keep the original Semgrep alert open.

QASecClaw gives this shape a useful test case. On OWASP Benchmark v1.2, it cut Semgrep false positives from 560 to 64 while recall dropped by 3.1%. That is enough evidence for a limited pilot on noisy rule families such as injection, XSS, and weak cryptography. The first local check should compare model-filtered alerts against recent human triage decisions and report both false-positive reduction and missed real findings.

### Evidence
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw uses Semgrep findings plus code context for LLM judgment and reports false-positive, recall, precision, and F1 results.
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): The abstract states the OWASP Benchmark evaluation, false-positive reduction from 560 to 64, and 3.1% recall reduction.

## Checklist audit queue for GitHub Actions workflow compliance
Teams with many GitHub Actions workflows can turn documented CI practices into a fixed audit checklist and route only uncertain cases to humans. The useful unit is one workflow file checked against specific YES, NO, or NOT APPLICABLE questions, such as least-privilege permissions, pinned actions, secrets handling, caching, and failure notifications.

The GitHub Actions audit study shows why the queue needs disagreement handling. Four open-weight models had only fair agreement on 95 Java workflows, with Fleiss’ kappa at 0.28. The study accepted unanimous or near-unanimous answers, sent split cases to GPT-5, and used targeted human review for unresolved items. That process reduced verification effort by 81% while keeping 87% agreement with expert judgment. A practical rollout can start as a weekly report on permission controls, since the study found only 4% compliance there.

### Evidence
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): The study defines a 30-item GitHub Actions compliance checklist, reports model agreement, and describes GPT-5 plus human review.
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): The abstract describes workflow risks, the 30 criteria, fair model agreement, and compliance results.
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): The paper explains why linters such as actionlint and yamllint miss documented best-practice violations.

## Before-and-after LLM checks for Java refactoring correctness
IDE vendors and Java teams can test an LLM review pass for risky refactorings by giving the model only the original code, the refactored code, and a correctness question. The check fits refactoring because the evidence is paired and concrete, and the model can return a short explanation for developer inspection.

The refactoring-oracle study built 226 real Java refactoring bug cases across 47 refactoring types, including compilation-error and behavior-change cases. GPT-5.4 reached 93.8% first-run accuracy, and GPT-OSS-20B reached 80.5%. A useful adoption test is a non-blocking warning on high-volume refactorings such as Move Method, Inline Method, Pull Up Method, Extract Local Variable, and Rename Method, compared against compiler results, existing tests, and developer accept-or-dismiss behavior.

### Evidence
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): The paper reports the 226-case Java refactoring dataset, 47 refactoring types, model accuracies, and validation approach.
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): The abstract excerpt gives GPT-OSS-20B and GPT-5.4 accuracy and describes lightweight triage use in development workflows.
