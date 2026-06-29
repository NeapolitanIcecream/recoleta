---
source: arxiv
url: https://arxiv.org/abs/2605.18332v1
published_at: '2026-05-18T12:49:18'
authors:
- Wei Ma
- Zhi Chen
- Jingxu Gu
- Tianling Li
- Shangqing Liu
- Lingxiao Jiang
topics:
- software-engineering-agents
- swe-bench
- behavioral-analysis
- code-intelligence
- llm-evaluation
- agent-frameworks
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Same Signal, Different Semantics: A Cross-Framework Behavioral Analysis of Software Engineering Agents

## Summary
The paper tests whether behavioral rules for software engineering agents transfer across agent configurations. Its main finding is that many rules fail to transfer because the framework changes what the same observable behavior means.

## Problem
- Prior studies often infer success rules from one agent framework or a small group of similar frameworks, so their external validity is unclear.
- This matters for SWE-bench agents because developers may choose the wrong fix, such as changing the LLM when the framework workflow causes the behavior.
- The paper asks whether behavior-outcome links, such as error rate or testing after modification, keep the same sign across frameworks and LLMs.

## Approach
- The study analyzes 64,380 SWE-bench Verified trajectories from 126 framework-LLM configurations across 43 frameworks.
- It separates framework effects from LLM effects with two slices: 3 tracer LLMs each run across 6-8 frameworks, and 33 LLMs run on one fixed framework, mini-swe-agent.
- It parses logs with 45 parsers, maps actions into 6 categories, detects 15 error types, and builds continuous trajectory features plus 7 binary behavior patterns from prior work.
- Each configuration contributes one behavior-outcome effect size. The authors compare effect direction, heterogeneity with Higgins' I2, and variance explained by framework identity versus LLM family.

## Results
- Error rate has split semantics: 47 configurations resolve more issues when error rate is lower, while 48 resolve more when error rate is higher.
- Six continuous features and 3 of 7 binary behavior patterns show direction-divided effects across the 126 configurations.
- For mean turns, framework identity explains 64% of between-configuration variance, while LLM family explains 10%.
- Across 7 features that pass the permutation diagnostic, framework identity explains 2.1x to 6.4x the variance explained by LLM family.
- Direction-stable signals include shorter trajectories, fewer revisits, lower entropy, and lower backtrack rate, with at least 88% of configurations agreeing on the sign.
- The preprocessing pipeline reports Cohen's kappa greater than 0.85 on 500 manually annotated turns across 5 frameworks, with median unknown-action rate of 0.4% per configuration.

## Link
- [https://arxiv.org/abs/2605.18332v1](https://arxiv.org/abs/2605.18332v1)
