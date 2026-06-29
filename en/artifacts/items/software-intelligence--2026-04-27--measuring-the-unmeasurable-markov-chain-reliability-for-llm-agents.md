---
source: arxiv
url: https://arxiv.org/abs/2604.24579v1
published_at: '2026-04-27T15:05:45'
authors:
- Phat T. Tran-Truong
- Xuan-Bach Le
topics:
- llm-agents
- agent-reliability
- markov-chain
- evaluation-metrics
- trace-analysis
- multi-agent-systems
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Measuring the Unmeasurable: Markov Chain Reliability for LLM Agents

## Summary
TraceToChain turns LLM-agent execution traces into an absorbing Markov chain that estimates when a run reaches success or failure. It gives pass@k, pass^k, and reliability decay curves one success-time distribution with fit checks and uncertainty intervals.

## Problem
- LLM agents act over many steps, but benchmark reports often compress reliability into one scalar such as pass@1 or pass@k.
- A single pass rate cannot answer step-budget, fallback-tool, or mean-time-to-failure questions without another benchmark run.
- Deployment teams need evidence that a trace-derived reliability model fits held-out traces and has finite-sample uncertainty.

## Approach
- Featurize each trace step, such as reasoning, tool calls, observations, retries, and errors, then cluster steps into transient state labels using Ward clustering with silhouette-selected cluster count.
- Fit an absorbing discrete-time Markov chain M=(Q,R_success,R_failure) with Laplace-smoothed MLE, where Q models transitions among transient states and the exit vectors model success or failure.
- Treat reliability as first passage to the success absorber: R(d)=Pr(success by step d), with the fundamental matrix N=(I-Q)^-1 giving closed-form reliability quantities.
- Check whether a first-order chain is supported by traces using a first-vs-second-order AIC test and a KS test on the first-passage CDF.
- Report Dirichlet-posterior credible intervals and trace-level bootstrap intervals for transition entries and derived reliability metrics.

## Results
- On 7 controlled MAST-style setups with a strict 50/50 fit/test split, held-out empirical RDCs matched analytic RDCs with max L_inf^RDC=0.053 and median 0.048.
- A two-sample KS test accepted the fitted chain on 7/7 setups at p>0.05, with minimum p=0.78.
- Per-entry 95% posterior intervals and bootstrap intervals agreed by about 0.01 at the median.
- The method claims pass@k, pass^k, and RDC are projections of one success first-passage distribution, which makes denominator and horizon choices explicit.
- The paper states that raw SWE-bench and tau-bench trace validation remains future work because those traces need step-level feature data.

## Link
- [https://arxiv.org/abs/2604.24579v1](https://arxiv.org/abs/2604.24579v1)
