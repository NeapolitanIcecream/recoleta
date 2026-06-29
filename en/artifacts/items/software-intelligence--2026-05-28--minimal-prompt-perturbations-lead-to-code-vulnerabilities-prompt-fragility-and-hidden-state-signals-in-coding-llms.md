---
source: arxiv
url: https://arxiv.org/abs/2605.29737v1
published_at: '2026-05-28T10:30:28'
authors:
- Alexander Sternfeld
- Andrei Kucharavy
- Ljiljana Dolamic
topics:
- coding-llms
- code-security
- prompt-fragility
- hidden-state-probing
- cweval
- software-foundation-models
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs

## Summary
This paper shows that tiny prompt edits can make coding LLMs generate vulnerable code. It also finds that some vulnerability types can be predicted from prompt hidden states before code generation.

## Problem
- LLM coding assistants are used to write code that may ship, but ordinary prompt variation can change whether generated code is secure.
- Prior prompt-perturbation work mainly measured functional correctness, leaving the security effect of typos and token edits unmeasured.
- A security test alone can mislead because code that fails to implement the task may look safe, so the paper evaluates functionality and security together.

## Approach
- The study uses CWEval, which pairs each task with a functional test and a security-specific test, covering 31 CWE types across C, C++, Go, JavaScript, and Python.
- It tests CodeLlama-70B, DeepSeek-Coder-33B, and Qwen3-Coder-30B at temperature 0.
- It mutates prompts with single-character substitutions, three-character substitutions inside one token, and whole-token replacements chosen by token-embedding similarity.
- It trains logistic-regression and two-layer MLP probes on the last-token hidden state from a transformer layer to predict whether a generation will be functional and jointly functional-secure.
- Probe training uses an 80% development split with 5-fold cross-validation and a 20% held-out test split.

## Results
- On original prompts, Qwen3-Coder-30B has the best func-sec rates: 33.3% in C, 52.4% in C++, 38.6% in Go, 43.5% in JavaScript, and 56.0% in Python. CodeLlama-70B is lower: 10.0%, 19.0%, 14.0%, 26.1%, and 40.0% on the same languages.
- A single-character mutation can flip secure code to vulnerable code. In one DeepSeek-Coder-33B Python CWE-022 case, changing “otherwise,” to “otherwiseV” at token 26/102 removed the path-traversal guard around tar.extractall, allowing entries such as ../../etc/passwd to write outside the destination path.
- Temperature-0 generation was almost stable: only 2 of 324 model-CWE cases had non-uniform evaluation across three completions.
- Hidden-state probes reach about 0.70 mean held-out AUC for the joint functional-secure target across models.
- Input-handling vulnerabilities are easier to predict than secure-defaults vulnerabilities: mean AUC 0.753 ± 0.038 versus 0.674 ± 0.037, with Mann-Whitney U = 68 and p = 0.009.
- High per-CWE probe AUCs include resource exhaustion at 0.857, command injection at 0.830, and SQL injection at 0.780. Low AUCs include weak crypto (DSA) at 0.584 and signature verification at 0.588.

## Link
- [https://arxiv.org/abs/2605.29737v1](https://arxiv.org/abs/2605.29737v1)
