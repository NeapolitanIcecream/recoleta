---
source: hn
url: https://blog.r-lopes.com/newsletter/2026-06-18
published_at: '2026-06-18T23:17:27'
authors:
- dovelome
topics:
- ai-code-generation
- software-security
- code-review
- spec-driven-development
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# The Line Vibe Coding Can't Cross

## Summary
This brief argues that prompt-and-ship AI coding is unsafe for production paths that handle auth, payments, secrets, or untrusted input. Its main prescription is to keep AI generation, but add specs, tests, threat modeling, review, audit trails, and named human owners.

## Problem
- Vibe coding removes SDLC checks such as specs, tests, review, CI, documentation, and audit trails, so defects can reach production without clear provenance.
- The risk matters most in systems where a bug can harm users, leak secrets, bypass authorization, or corrupt payments.
- Agent speed, non-deterministic outputs, and pressure to cut verification make review and reproduction harder after the code changes.

## Approach
- Classify work by stakes: throwaway or self-only code can use prompt-and-ship, while auth, payments, secrets, and untrusted input require engineering gates.
- Write behavior and constraints before generation, then let the agent produce code against that spec.
- Require human review, tests, threat modeling, and direct proof that the code does the right thing before merge.
- Keep an audit trail and assign a named human owner for each production change.
- Move security checks away from single points of failure, such as middleware-only authorization, and gate dependencies with CI scanning.

## Results
- The brief cites a claim that about 45% of AI-generated code contains security flaws.
- It reports defect concentration in security and logic: XSS appears at 2.74x the human baseline, and logic errors appear at 1.75x the human baseline.
- It cites Veracode telemetry linking more generative AI coding with higher vulnerability severity: 11.3% of vulnerabilities were severe, compared with 8.3% in the prior year.
- It gives two concrete failure examples: the Sakari ransomware generated an RSA key pair and discarded the private key, and a framework auth-bypass case let an attacker skip middleware with a guessable header.
- The claimed production rule is a gated path with at least 4 checks after generation: human review, tests, threat modeling, and proof before an accountable merge.

## Link
- [https://blog.r-lopes.com/newsletter/2026-06-18](https://blog.r-lopes.com/newsletter/2026-06-18)
