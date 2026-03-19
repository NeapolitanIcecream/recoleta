---
source: arxiv
url: http://arxiv.org/abs/2603.06029v1
published_at: '2026-03-06T08:28:44'
authors:
- Jie Ma
- Ningyu He
- Jinwen Xi
- Mingzhe Xing
- Liangxin Liu
- Jiushenzi Luo
- Xiaopeng Fu
- Chiachih Wu
- Haoyu Wang
- Ying Gao
- Yinliang Yue
topics:
- api-testing
- differential-testing
- ethereum
- llm-for-testing
- software-reliability
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# When Specifications Meet Reality: Uncovering API Inconsistencies in Ethereum Infrastructure

## Summary
This paper presents APIDiffer, a specification-guided differential testing framework for Ethereum infrastructure, designed to automatically discover inconsistencies among API implementations across different Ethereum clients. Its core value lies in directly converting official API specifications into tests and combining that with large language models to filter false positives, thereby uncovering a large number of high-value defects in real production clients.

## Problem
- The paper addresses the following issue: although multiple independently implemented Ethereum client APIs are supposed to follow the same specification, their actual behavior often differs, which can lead to incorrect asset displays, degraded user experience, and risks to network reliability.
- This matters because the Ethereum ecosystem secures more than **$381 billion** in assets, and ordinary users, wallets, block explorers, and Web3 libraries almost all interact with the chain through client APIs rather than running their own nodes.
- Existing testing methods mainly rely on manual effort, DSLs, or templates, making it difficult to keep up with rapid protocol evolution; at the same time, differential testing results contain many "acceptable differences" and environmental differences, making it hard to distinguish real bugs from false positives.

## Approach
- APIDiffer’s core method is simple: **use the official API specification as input to the test generator**, automatically generate test requests for execution-layer (EL) and consensus-layer (CL) clients, and then send the same request to multiple implementations for comparison.
- It first performs **syntax-guided generation**: automatically constructing valid and invalid requests based on JSON schema to cover both correctness and robustness scenarios.
- It then performs **semantics-aware filling**: using auxiliary APIs to fetch real-time on-chain data and replacing parameters such as addresses and blocks with actually existing on-chain objects, avoiding meaningless tests that are syntactically correct but semantically invalid.
- To reduce false positives, it uses **specification-aware filtering**: first applying heuristic rules to remove environmental differences and acceptable differences, then using an LLM to classify response fields as must-identical / may-divergent / must-divergent, and to identify results that are "semantically equivalent but textually different."
- The full workflow covers 11 major Ethereum clients, runs them simultaneously in a controlled local test network, and produces bug reports that can be submitted to developers.

## Results
- APIDiffer found **72 bugs** across **all 11 major Ethereum clients**.
- Of these, **90.28%** have already been **confirmed or fixed** by developers, indicating that most findings are not noise.
- It also found **1 critical error in the official API specification itself**, showing that the problem exists not only in implementations but also at the specification level.
- Compared with existing tools, APIDiffer improves code coverage by up to **89.67%**.
- It reduces the false positive rate by **37.38%**.
- In terms of community feedback, developers have already integrated its test cases, and **1 bug** was escalated for discussion at the official Ethereum Project Management meeting.

## Link
- [http://arxiv.org/abs/2603.06029v1](http://arxiv.org/abs/2603.06029v1)
