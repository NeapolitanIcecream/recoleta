---
source: arxiv
url: https://arxiv.org/abs/2607.14573v1
published_at: '2026-07-16T05:08:20'
authors:
- Shiyu Ying
- Xuejie Cao
- Yingfan Ma
- Yuanhao Dong
- Wenyu Chen
- Bowen Song
- Lin Zhu
topics:
- coding-agents
- software-engineering-benchmarks
- payment-integration
- repository-level-evaluation
- secure-software
- agent-skills
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents

## Summary
Alipay-PIBench is a repository-level benchmark for testing whether coding agents can implement secure, reliable, end-to-end Alipay payment integrations in realistic business applications. It evaluates functional completion and risk hardening across nine product-specific projects and 18 task instances.

## Problem
- General coding benchmarks often miss domain requirements such as server-side credential protection, signature verification, asynchronous notification handling, and consistency between payment and local business states.
- Payment integration errors can create fund-safety risks, incorrect fulfillment, duplicate state transitions, and unsafe refunds, so source-level code completion alone is insufficient.

## Approach
- The benchmark pairs nine Alipay payment products and business repositories with two progressive scenarios: Basic Functional Payment Completion and Advanced Risk-Aware Payment Hardening.
- Tasks require repository-level changes across frontend, backend, payment APIs, configuration, and business-state logic; advanced tasks test idempotency, abnormal transactions, notification authenticity, repeated confirmations, and refund safeguards.
- Scenario-specific rubrics generate deterministic static, unit, integration, and end-to-end checks, supplemented by LLM-assisted assessment for semantic properties such as product fit and state consistency.
- A weighted Rubric Pass Rate (RPR) gives integration and end-to-end checks weight 2, while static, unit, and LLM-assisted checks receive weight 1.
- Paired trials compare six models with and without the official alipay-payment-integration skill under fixed task and environment conditions.

## Results
- Across six models and 18 task instances, mean with-skill RPR ranges from 68.58% to 91.37%.
- Access to the skill improves mean RPR by 10.31 percentage points on average, with gains in 101 of 108 model-product-scenario comparisons.
- The average improvement is larger for Basic tasks (+11.27 percentage points) than for Advanced tasks (+9.35 percentage points).
- The benchmark separates source-level completion, executable payment behavior, and payment-domain requirements, showing why multiple evaluation signals and progressive scenarios are needed.
- The excerpt does not provide complete per-model, per-product, or without-skill score tables, so it supports aggregate skill-effect conclusions more strongly than detailed model rankings.

## Link
- [https://arxiv.org/abs/2607.14573v1](https://arxiv.org/abs/2607.14573v1)
