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
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# AgentAssay: Token-Efficient Regression Testing for Non-Deterministic AI Agent Workflows

## Summary
AgentAssay proposes a regression testing framework for **non-deterministic AI agent workflows**, replacing traditional binary testing with probabilistic testing backed by statistical guarantees, while specifically addressing the problem of excessively high testing costs. Its core value is that it substantially reduces the token and runtime cost required for agent regression testing while preserving significance/power guarantees.

## Problem
- The paper addresses the following issue: **the same agent can produce different results under the same input due to sampling, model updates, tool variability, and context changes**, which makes traditional testing methods based on "single run + binary pass/fail" unable to reliably detect regressions.
- This matters because agents in production may silently degrade after minor adjustments to prompts, tools, models, or orchestration logic; the paper gives an example in which customer support routing accuracy drops from **93% to 71%**, yet traditional tests and alerts may still miss it.
- Another key issue is cost: if statistical testing is done with a fixed sample size, the paper estimates that **50 scenarios × 100 trials per scenario = 5,000 agent calls**, and a single regression check on frontier models could cost **$25,000–$75,000**.

## Approach
- The core mechanism changes test semantics from "whether the output equals the expected answer" to "**whether the probability that the agent satisfies a property exceeds a threshold**," and replaces rigid binary conclusions with the three-valued outcomes **Pass / Fail / Inconclusive**.
- It runs multiple trials on the same scenario and computes the pass rate and confidence interval; if the lower bound of the interval exceeds the threshold, the result is Pass; if the upper bound is below the threshold, it is Fail; otherwise, the evidence is insufficient and the result is Inconclusive.
- To reduce cost, the paper proposes three main token-efficient methods: **behavioral fingerprinting** (compressing execution traces into low-dimensional behavioral vectors for multivariate regression detection), **adaptive budget optimization** (adaptively determining the number of trials based on actual behavioral variance), and **trace-first offline analysis** (using pre-recorded traces to perform coverage/contract/metamorphic/mutation testing offline).
- Beyond statistical decision procedures, the framework also fills out agent-testing infrastructure: **5-dimensional coverage metrics** (tool/path/state/boundary/model), **mutation testing operators** for prompt/tool/model/context, **metamorphic relations** suitable for multi-step agents, and **statistical deployment gates** for CI/CD.
- The paper also claims integration with the AgentAssert contract framework, allowing behavioral contracts to serve as formal test oracles for verifying before deployment whether the agent still satisfies requirements.

## Results
- The overall evaluation covers **5 models, 3 agent scenarios, and 7,605 trials**, with a total experimental cost of **$227**; the models include **GPT-5.2、Claude Sonnet 4.6、Mistral-Large-3、Llama-4-Maverick、Phi-4**.
- The paper claims that **SPRT sequential probability ratio testing** reduced the number of trials by **78%** across all scenarios while maintaining the same statistical guarantees.
- **Behavioral fingerprinting** achieved **86% detection power** for regression detection, whereas binary pass/fail-based testing achieved **0%** under the corresponding setup.
- **Adaptive budget optimization** can further reduce the required number of trials by **4–7×** for stable agents.
- The paper overall claims that its token-efficient techniques can achieve **5–20× cost reduction**, and under **trace-first offline analysis**, four categories of tests reach **100% cost savings / zero additional token cost**.
- The abstract also gives the overall range: while maintaining rigorous statistical guarantees, AgentAssay achieves **78–100% cost reduction**; this is its most central claimed breakthrough result.

## Link
- [http://arxiv.org/abs/2603.02601v1](http://arxiv.org/abs/2603.02601v1)
