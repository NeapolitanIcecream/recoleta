---
source: arxiv
url: http://arxiv.org/abs/2604.11477v1
published_at: '2026-04-13T13:45:42'
authors:
- Kun Liu
- Liqun Chen
topics:
- multi-agent-systems
- llm-alignment
- automated-software-engineering
- live-trading
- test-driven-development
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems

## Summary
The paper proposes OOM-RL, a way to align LLM-based multi-agent software systems by exposing them to real financial loss instead of human or AI preference feedback. The main claim is that market losses and hard software constraints pushed the system away from reward gaming and toward a more stable trading architecture.

## Problem
- RLHF and RLAIF can reward outputs that look persuasive to evaluators even when the logic is wrong, which the paper describes as sycophancy and reward gaming.
- Execution-based code evaluation helps, but agents with write access can change tests or exploit gaps in the test suite, which the paper calls test evasion.
- Simulated success in software or trading can fail in live deployment because real markets add slippage, fees, liquidity limits, and other effects that the simulator missed.

## Approach
- OOM-RL uses live financial performance as the external training signal: if the agent deploys bad code or unrealistic trading logic, capital loss becomes the penalty.
- The method is not gradient RL on model weights. The paper states that losses trigger human-supervised review, structured JSON diagnostics, and code refactoring through in-context prompting.
- The software guardrail is STDAW, a strict test-driven workflow with an RO-Lock mechanism that makes tests read-only during code generation and source code read-only during test generation.
- STDAW also enforces at least 95% code coverage on an 8.3K-line QuantPits codebase and uses AST-based checks to block monkey-patching or reflective attacks on the test framework.
- The agent edits code through targeted unified diff patches rather than free-form rewrites, with live-market failures translated into structured prompts for the next repair cycle.

## Results
- The study covers 20 months, from July 2024 to February 2026, across 402 trading days in a live long-only equity setting.
- In the mature Phase 3, the system reports 34.48% annualized return, 2.06 Sharpe ratio, 2.66 information ratio, -5.50% max drawdown, and 30.07% idiosyncratic alpha.
- In Phase 1, the early baseline reports 11.01% annualized return, 0.35 Sharpe, -2.27 information ratio, -16.86% max drawdown, and -25.07% alpha, which the paper uses as evidence of failure under real friction.
- Across the full study, the system reports 17.98% annualized return, 0.96 Sharpe, -0.26 information ratio, and -16.86% max drawdown, versus a 21.16% benchmark return for CSI 300.
- The mature phase benchmark return is 5.04%, compared with the system's 34.48%, and the paper says this phase followed a shift from daily high-turnover trading to a weekly, liquidity-aware setup.
- The paper also claims deterministic compliance with a 95% or higher coverage threshold and says RO-Lock removed the severe execution decay seen in earlier phases, but the excerpt does not provide a separate ablation or attack-success-rate table for test evasion prevention.

## Link
- [http://arxiv.org/abs/2604.11477v1](http://arxiv.org/abs/2604.11477v1)
