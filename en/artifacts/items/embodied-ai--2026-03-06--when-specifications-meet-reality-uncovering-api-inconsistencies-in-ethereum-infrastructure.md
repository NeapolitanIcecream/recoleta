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
- ethereum
- api-testing
- differential-testing
- blockchain-infrastructure
- llm-based-analysis
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# When Specifications Meet Reality: Uncovering API Inconsistencies in Ethereum Infrastructure

## Summary
This paper presents APIDiffer, a framework for Ethereum client APIs that combines “specification-based test generation + differential comparison + false-positive filtering” to automatically discover inconsistencies across different client implementations. Its importance lies in the fact that Ethereum infrastructure secures over $381 billion in assets, and APIs are the primary entry point for users to access the chain, so errors can directly affect balance displays, user experience, and network reliability.

## Problem
- The paper aims to solve how to systematically discover implementation inconsistencies and real bugs in Ethereum execution-layer (EL) and consensus-layer (CL) client APIs, rather than relying on manually written tests or manual judgment of differences.
- This matters because client APIs are the only/main interface through which users, wallets, block explorers, and Web3 applications access the blockchain; implementation errors may cause incorrect balances, incorrect transaction information, and inconsistent services, and may even create financial misinformation.
- Existing methods either rely on DSLs/templates/manual test cases and struggle to keep up with protocol evolution, or treat all differences as bugs, leading to high false-positive rates and making it hard to distinguish “allowed differences” from “real errors.”

## Approach
- The core method is a **specification-driven differential testing framework**: it first automatically generates test requests from official API specifications, then sends the same requests to multiple Ethereum clients, compares the returned results, and identifies inconsistencies.
- To generate inputs that can “actually test meaningful behavior,” APIDiffer does not only generate **syntactically valid/invalid** requests according to the JSON schema, but also retrieves **real-time on-chain data** through auxiliary APIs, replacing parameters such as addresses and blocks with real existing values so that requests are semantically valid as well.
- To reduce false positives, it introduces **specification-aware filtering**: combining rules and LLMs, it classifies response fields into three categories—must match, may differ, and should differ—thereby ignoring non-bug cases such as node-state differences and unique-identifier field differences.
- For results that are “superficially different but semantically the same” across clients (such as different error message text), the system further uses LLMs to judge semantic equivalence, avoiding treating semantically equivalent responses as bugs.
- The framework covers both EL and CL APIs, and executes the same batch of tests across 11 mainstream client combinations in a locally controlled test network, automatically producing bug reports.

## Results
- Across **11 mainstream Ethereum clients**, APIDiffer found **72 bugs** in total.
- Of these bugs, **90.28%** have already been **confirmed or fixed** by developers, indicating that most findings are real issues rather than noise.
- APIDiffer also discovered **1 critical error in the official API specification itself**, showing that it can uncover not only implementation bugs but also specification defects.
- Compared with existing tools, APIDiffer achieves **up to 89.67%** higher code coverage.
- It **reduces the false-positive rate by 37.38%**, directly addressing the core challenge of differential testing: “finding differences but struggling to judge whether they are real bugs.”
- The paper also provides ecosystem-side evidence: developers have already integrated its test cases, expressed willingness to adopt it, and **1 bug** was escalated to discussion at the official Ethereum Project Management meeting.

## Link
- [http://arxiv.org/abs/2603.06029v1](http://arxiv.org/abs/2603.06029v1)
