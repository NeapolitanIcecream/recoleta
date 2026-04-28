---
source: arxiv
url: http://arxiv.org/abs/2604.16790v1
published_at: '2026-04-18T02:35:05'
authors:
- Zixiao Zhao
- Amirreza Esmaeili
- Fatemeh Fard
topics:
- llm-as-a-judge
- code-intelligence
- software-engineering
- evaluation-bias
- agentic-workflows
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering

## Summary
This paper audits LLMs used as judges for code evaluation and shows that their verdicts can change a lot when the prompt adds superficial cues. The authors argue that judge accuracy alone is not enough; studies should also report bias sensitivity and repeatability.

## Problem
- LLM judges are used to rank code candidates when human review or executable tests are limited, especially in agent-based software engineering workflows.
- A judge can flip its decision across repeated runs or after small prompt edits, even when the code itself does not change.
- That matters because prompt artifacts can change benchmark conclusions, model rankings, and patch selection decisions.

## Approach
- The paper studies pairwise code judging on three tasks: code generation, code repair, and unit test generation.
- It uses a measurement-first setup: keep the candidate code fixed, then change only the judge prompt to inject one bias at a time.
- The bias suite contains 12 prompt-level interventions such as position/order, verbosity, authority/provenance, distraction, chain-of-thought, self-enhancement, and refined-version cues.
- The authors evaluate two properties: micro-accuracy under each bias condition, and test-retest consistency rate when the same case is judged twice under the same prompt.
- They test open-source Qwen-based judges and also report a similar pattern for a closed-source GPT-based judge.

## Results
- Main claim: judge decisions are highly sensitive to prompt bias even when the underlying code snippet is unchanged.
- The paper says some prompt biases improve accuracy when they favor the gold answer, but reduce accuracy a lot when they favor the wrong answer; these shifts are large enough in some settings to change task-level conclusions and relative model rankings.
- The largest concrete swing reported for a closed-source GPT-based judge is on TestGen: distraction lowers accuracy from 77.46% to 62.51%.
- Response reliability also varies by judge model: Qwen2.5-Coder-3B returns the required A/B verdict on about 99% of inputs, while a generic Qwen setup does so on about 44% and often produces free-form text until the context limit.
- The abstract and excerpt say code repair tends to have high judge accuracy, but they do not provide a full table of task-by-task accuracy numbers here.
- The paper recommends explicit controls such as A/B order swapping and controlled prompt perturbations, and it says bias sensitivity should be reported alongside accuracy.

## Link
- [http://arxiv.org/abs/2604.16790v1](http://arxiv.org/abs/2604.16790v1)
