---
source: arxiv
url: http://arxiv.org/abs/2603.28653v1
published_at: '2026-03-30T16:40:11'
authors:
- Kaushitha Silva
- Srinath Perera
topics:
- llm-code-generation
- program-synthesis
- bayesian-inference
- test-generation
- co-evolution
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# BACE: LLM-based Code Generation through Bayesian Anchored Co-Evolution of Code and Test Populations

## Summary
BACE improves LLM code generation by treating generated tests as noisy evidence instead of ground truth. It co-evolves code and test populations with Bayesian belief updates, while keeping the search tied to public example cases.

## Problem
- LLM-generated code often has logic errors that single-pass prompting misses, so systems use feedback loops with generated tests.
- Generated tests are unreliable: wrong code can pass weak tests, and correct code can be pushed into wrong edits by faulty assertions.
- Recent systems such as MapCoder and CodeSIM avoid test generation because of this failure mode, which leaves useful execution signal on the table.

## Approach
- BACE keeps a **population** of candidate programs and a **population** of generated tests instead of relying on one code sample and one test suite.
- Each code candidate and each test gets a Bayesian belief score: the probability it is correct or valid. Pass/fail outcomes update those beliefs as noisy observations rather than hard truth.
- The noise model uses three pass probabilities for misleading cases: false pass for valid code on broken tests ($\alpha$), accidental pass for wrong code on valid tests ($\beta$), and coincidental pass for wrong code on broken tests ($\gamma$).
- Public input/output examples from the prompt are fixed as high-confidence anchors. Code that fails an anchor gets belief driven to zero; code that passes anchors gets a strong positive update.
- BACE alternates evolution of tests and code, and keeps diverse high-belief individuals through behavior-based elitism and differential testing.

## Results
- On **LiveCodeBench v6 (post-March 2025)**, BACE outperforms **CodeSIM** by **3.8%** with **GPT-5-Mini**.
- On the same benchmark, BACE outperforms **CodeSIM** by **5.0%** with **Qwen2.5-Coder-7B**.
- The paper claims better performance than leading multi-agent frameworks across both proprietary models and open-weight small language models.
- The excerpt does not provide full absolute scores, pass@k values, variance, or a complete baseline table.
- The authors also state that **AgentCoder underperformed direct prompting on medium problems with GPT-5-Mini**, but the excerpt gives no number for that gap.

## Link
- [http://arxiv.org/abs/2603.28653v1](http://arxiv.org/abs/2603.28653v1)
