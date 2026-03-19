---
source: arxiv
url: http://arxiv.org/abs/2603.02601v1
published_at: '2026-03-03T04:59:25'
authors:
- Varun Pratap Bhardwaj
topics:
- ai-agent-testing
- regression-testing
- non-deterministic-systems
- behavioral-fingerprinting
- sequential-analysis
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# AgentAssay: Token-Efficient Regression Testing for Non-Deterministic AI Agent Workflows

## Summary
AgentAssay proposes a regression testing framework for **non-deterministic AI agent workflows**, replacing traditional binary testing with probabilistic testing backed by statistical guarantees, while specifically addressing the problem of excessive testing cost. The paper’s core selling point is that, while preserving statistical rigor, it dramatically reduces token cost through behavioral fingerprinting, sequential testing, and offline trace analysis.

## Problem
- Existing software testing assumes that **the same input produces the same output**, but LLM agents can exhibit different behaviors across repeated runs even with the same prompts, tools, and model, so ordinary assertions and one-off evaluations cannot reliably detect whether the system has “regressed.”
- Traditional **pass/fail** binary conclusions are not suitable for stochastic systems; a single failure may be just noise, and a single success may be luck, so a decision method with confidence intervals and error-rate control is needed.
- Statistical regression testing for agents is expensive: the paper gives an example where detecting a regression of magnitude 0.10 requires about **100 runs per scenario**; for 50 scenarios that becomes **5,000 calls**, which on frontier models could cost **$25,000–$75,000**, hindering CI/CD adoption.

## Approach
- Proposes a **three-valued stochastic test semantics**: test outcomes are defined as **Pass / Fail / Inconclusive**, with decisions based on pass rates over multiple runs, Wilson/Clopper-Pearson confidence intervals, and significance/power parameters to determine whether the system truly passes or has regressed.
- Uses **SPRT sequential probability ratio testing** instead of fixed-sample testing: when sufficient evidence is obtained, testing stops early, reducing the number of agent trials required.
- Defines an agent-specific testing toolbox: **5-dimensional coverage** (tool/path/state/boundary/model), **4 classes of mutation operators** (prompt/tool/model/context), and **metamorphic relations** suited to multi-step agents, enabling more systematic testing beyond just checking the final answer.
- Introduces **behavioral fingerprinting**: compressing an execution trace into a low-dimensional behavioral vector and then applying multivariate statistical tests; intuitively, this means “do not compress a complex trace into a single pass/fail bit, but retain more behavioral information,” improving information yield per sample.
- Proposes **adaptive budget optimization** and **trace-first offline analysis**: the former dynamically determines how many trials are needed based on actual behavioral variance, while the latter performs coverage, contract, metamorphic-relation, and some mutation analysis directly on pre-recorded production traces, enabling offline testing at zero additional token cost.

## Results
- The paper claims this is the first **token-efficient regression testing** framework for non-deterministic AI agent workflows, and reports an evaluation across **5 models, 3 scenarios, and 7,605 trials** at a total cost of **$227**.
- **SPRT** reduced the number of trials by **78%** across all scenarios while maintaining unchanged statistical guarantees.
- **behavioral fingerprinting** achieved **86% detection power** for regression detection, whereas binary pass/fail testing was **0%** under the corresponding setup.
- **adaptive budget optimization** reduced the number of required trials by **4–7×** for stable agents.
- The overall token-efficient pipeline achieved **5–20× cost reduction**; the abstract also claims that **trace-first offline analysis** can deliver **100% cost savings** for some test types.
- The models involved include **GPT-5.2、Claude Sonnet 4.6、Mistral-Large-3、Llama-4-Maverick、Phi-4**; the scenarios include **e-commerce、customer service、code generation**.

## Link
- [http://arxiv.org/abs/2603.02601v1](http://arxiv.org/abs/2603.02601v1)
