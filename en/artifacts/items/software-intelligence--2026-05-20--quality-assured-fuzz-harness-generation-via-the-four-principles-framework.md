---
source: arxiv
url: https://arxiv.org/abs/2605.21824v1
published_at: '2026-05-20T23:48:26'
authors:
- Ze Sheng
- Dmitrijs Trizna
- Luigino Camastra
- Zhicheng Chen
- Qingxiao Xu
- Jeff Huang
topics:
- fuzz-testing
- llm-agents
- code-generation
- software-security
- harness-generation
- program-analysis
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Quality-Assured Fuzz Harness Generation via the Four Principles Framework

## Summary
QuartetFuzz is an LLM-agent system that generates fuzz harnesses and checks them for correctness before fuzzing starts. It targets false positives caused by bad harness logic, invalid API use, private-entry bypasses, and weak entry-point choices.

## Problem
- Library fuzzing depends on harness code that maps fuzzer bytes into API calls; a bad harness can crash because of its own bug or invalid API sequence.
- Existing generators often judge harnesses by build success, short fuzzing runs, crashes, or coverage, which can miss source-level correctness errors.
- Prior work reports false-positive crash rates as high as 94%, which wastes maintainer triage time and makes LLM-scale harness generation risky.

## Approach
- QuartetFuzz defines four harness-quality checks: Logic Correctness, API Protocol Compliance, Security Boundary Respect, and Entry Point Adequacy.
- It groups targets by feature-level Logic Groups, then uses a call graph to choose public entry APIs that reach security-relevant core code.
- It researches API protocols from headers, comments, source code, and existing callers, then generates a libFuzzer harness through a build-fix loop.
- Before submission, it runs adversarial reach and run probes: the agent creates inputs meant to trigger likely harness faults, then checks behavior with tools such as ASan and LSan.

## Results
- On 23 open-source projects across C/C++, Java, and JavaScript, QuartetFuzz submitted 42 bug reports; 29 were fixed or confirmed upstream, including 3 CVEs, and 2 were rejected, giving a 4.8% false-positive rate.
- Built-in P1/P2 checks blocked 58 harness-induced crashes before they became false-positive reports: 14 in audited production harnesses and 44 in generated harnesses.
- As an auditor on 586 production OSS-Fuzz harnesses across 70 projects, it found 53 quality violations; maintainers confirmed 45 and fixed or merged 35.
- Repairs exposed 2 latent library bugs, including an OpenSSL DES stack-buffer-overread described as latent for more than 25 years.
- On a 100-harness gold dataset from 39 projects, generated harnesses matched human-written harnesses on line and branch coverage within TOST ±2 percentage points with p < 1e-10.
- Against other generators on coverage, QuartetFuzz outperformed OSS-Fuzz-Gen by 6.9-8.3 percentage points and PromeFuzz by 4.1-5.2 percentage points across line and branch coverage.

## Link
- [https://arxiv.org/abs/2605.21824v1](https://arxiv.org/abs/2605.21824v1)
