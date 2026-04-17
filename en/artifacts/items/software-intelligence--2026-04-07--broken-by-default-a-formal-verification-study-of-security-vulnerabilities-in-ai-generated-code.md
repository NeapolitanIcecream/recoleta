---
source: arxiv
url: http://arxiv.org/abs/2604.05292v2
published_at: '2026-04-07T00:55:42'
authors:
- Dominik Blain
- Maxime Noiseux
topics:
- code-security
- formal-verification
- llm-code-generation
- static-analysis
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code

## Summary
This paper measures how often major LLMs generate insecure code on security-sensitive programming tasks and checks exploitability with formal methods instead of keyword rules. Across 3,500 generated programs from seven models, the authors report that vulnerable code is common and often formally provable.

## Problem
- The paper studies a practical gap: AI coding assistants are used for production code, but prior evaluations often rely on pattern matching or manual review, which cannot prove that a flaw is actually exploitable.
- This matters for security-critical code because a warning from a static rule is weaker than a concrete witness input that triggers overflow, memory corruption, injection, or weak authentication behavior.
- The main question is how often current LLMs generate exploitable vulnerabilities by default, and whether prompts or standard security tools reduce that risk.

## Approach
- The authors build a benchmark of 500 security-focused prompts across five CWE groups: memory allocation, integer arithmetic, authentication, cryptography, and input handling. They query seven production LLMs at temperature 0, yielding 3,500 code artifacts.
- They analyze outputs with COBALT, which finds candidate vulnerability sites, encodes the bug condition into Z3 SMT formulas, and asks Z3 for a satisfying assignment. If Z3 returns SAT, the paper treats that as a formal proof of exploitability with a concrete input witness.
- They classify findings into Z3 SAT, pattern match, or clean, and assign severity with CVSS v3 base scores.
- They validate 7 representative cases with proof-of-concept harnesses and GCC AddressSanitizer runtime checks.
- They add three side experiments on a 50-prompt subset: secure-prompt ablation, comparison against six static analysis tools, and self-review where each model inspects its own vulnerable outputs.

## Results
- Across all 3,500 artifacts, 55.8% contain at least one COBALT-identified vulnerability. The paper reports 1,055 Z3-proven findings with satisfiability witnesses.
- Model rates on the 500-prompt benchmark range from 48.4% for Gemini 2.5 Flash to 62.4% for GPT-4o. No model reaches grade C or better; Gemini 2.5 Flash gets D at 48.4%, GPT-4o gets F at 62.4%, GPT-4.1 gets 54.0%, Mistral Large 57.8%, Llama 3.3 70B 58.4%, Llama 4 Scout 60.6%, and Claude Haiku 4.5 49.2%.
- By category, integer arithmetic has the highest mean vulnerability rate at 87%, memory allocation is 67%, input handling 56%, authentication 44%, and cryptography 25%.
- Runtime validation confirms 6 of 7 selected cases with actual faults or exploits, including heap-buffer-overflow, alloc-size-too-big, out-of-bounds read, SQL injection, and weak password hashing. One Zip Slip case was blocked by Python 3.12 at runtime even though the vulnerable pattern was generated.
- In the secure-prompt ablation on 50 prompts, the mean vulnerability rate drops from 64.8% to 60.8%, a 4-point reduction. Four of five models still receive grade F, and Llama 3.3 70B gets worse from 68% to 70%.
- In tool comparison on the 50-prompt subset, Semgrep plus Bandit flag 19 of 250 artifacts, or 7.6%. The paper says six industry tools combined miss 97.8% of Z3-proven findings, and CodeQL detects 0 of 90 formally proven cases.
- In self-review, models identify their own vulnerable code 70 out of 89 times, or 78.7%, which the paper uses to argue that models often know how to spot these bugs in review mode but still generate them during synthesis.

## Link
- [http://arxiv.org/abs/2604.05292v2](http://arxiv.org/abs/2604.05292v2)
