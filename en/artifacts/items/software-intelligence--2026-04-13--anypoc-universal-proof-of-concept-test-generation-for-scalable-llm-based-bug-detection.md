---
source: arxiv
url: http://arxiv.org/abs/2604.11950v1
published_at: '2026-04-13T18:44:02'
authors:
- Zijie Zhao
- Chenyuan Yang
- Weidong Wang
- Yihan Yang
- Ziqi Zhang
- Lingming Zhang
topics:
- llm-bug-detection
- proof-of-concept-generation
- multi-agent-systems
- software-testing
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection

## Summary
AnyPoC turns bug-report validation into executable proof-of-concept generation, so LLM bug finders can produce concrete evidence instead of text-only claims. It targets large, mixed software systems and aims to reject bad reports instead of generating plausible but fake PoCs.

## Problem
- LLM bug detectors can propose many candidate bugs, but developers still need to manually verify whether each report is real.
- Naive LLM PoC generation is unreliable: models tend to produce outputs that look successful, including non-working PoCs or hallucinated execution evidence.
- Existing PoC generators are narrow in scope. They often depend on one language, one bug class, one scaffold, or datasets that contain only true bugs.

## Approach
- AnyPoC is a multi-agent validator that takes a candidate bug report and either returns an executable PoC or rejects the report.
- An analyzer agent first fact-checks the report, checks code context and claimed bug mechanics, and filters some false reports before expensive generation starts.
- A generator agent then iteratively writes and runs a PoC, debugs it, and performs a second execution pass to collect explicit evidence such as logs and traces.
- A checker agent independently re-executes the PoC and verifies that the evidence actually demonstrates the bug, which is meant to reduce hallucinated success and reward hacking.
- A knowledge extractor and filter maintain a self-evolving knowledge base so later PoC attempts can reuse project-specific setup knowledge instead of rediscovering it each time.

## Results
- Evaluated on 12 real-world software systems across different languages and domains, including Chromium, Firefox, LLVM, OpenSSL, SQLite, FFmpeg, and Redis.
- Compared with baseline coding agents such as Claude Code and Codex, AnyPoC produces **1.3x** more valid PoCs for true-positive bug reports.
- It rejects **9.8x** more false-positive bug reports than those baselines.
- In one cited failure case for a baseline, Claude Code with Opus 4.5 produced **142** plausible PoCs for **144** bug reports, but only **26** were valid.
- The paper claims **122** new bugs found to date, with **105** confirmed by developers, **86** fixed, and **45** generated PoCs adopted as official regression tests.
- Table 1 positions AnyPoC as broader than prior systems: language-agnostic, dependency-free, able to handle false-positive filtering, and credited with **122** new bugs versus smaller or narrower prior results.

## Link
- [http://arxiv.org/abs/2604.11950v1](http://arxiv.org/abs/2604.11950v1)
