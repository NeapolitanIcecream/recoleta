---
source: arxiv
url: https://arxiv.org/abs/2605.27360v1
published_at: '2026-05-26T17:58:43'
authors:
- Tamerlan Aghayev
- Maxime Elkael
- Michele Polese
- Minh Dat Nguyen
- Gabriele Gemmi
- Andrea Lacava
- Ali Saeizadeh
- Reshma Prasad
- Paolo Testolina
- Angelo Feraudo
- Soumendra Nanda
- Pedram Johari
- Salvatore D'Oro
- Tommaso Melodia
topics:
- multi-agent-software-engineering
- code-generation
- ran-engineering
- spec-to-code
- agentic-testing
- 6g-ran
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# GENESIS: Harnessing AI Agents for Autonomous 6G RAN Synthesis, Research, and Testing

## Summary
Genesis is a multi-agent system for turning 3GPP/O-RAN intents into RAN code, tests, patches, and experiments that run on simulators, emulators, and real radios. The paper claims 100% success on two RAN feature-implementation case studies, while Claude Code with Opus 4.7 produced no working implementation.

## Problem
- RAN R&D is slow because feature synthesis, conformance testing, hardening, optimization, discovery, and security work each take months of engineering time per iteration.
- In one cited 5G stack analysis, a substantial feature took 74 days on average to reach the stable branch, with a 207-day 90th percentile.
- General LLM coding agents fail on RAN tasks because a small API error or spec misread can break interoperability with standard devices, radios, and OTA testbeds.

## Approach
- Genesis routes an intent, such as a spec clause, telemetry anomaly, or research hypothesis, into one of 6 pipelines: Synthesize, Test, Harden, Optimize, Discover, or Secure.
- The core mechanism is simple: agents decide what to do, deterministic skills run actions such as build, deploy, configure, and experiment, and hooks log events, enforce safety gates, and record provenance.
- Synapse stores curated 3GPP/O-RAN specs, research papers, reference code, lab inventory, code diffs, logs, traces, and experiment outputs, so later runs can reuse validated artifacts.
- Validation moves across 3 tiers: RFSIM simulation, Colosseum or hardware-in-the-loop emulation, and OTA deployment on production-grade testbeds such as X5G and Arena.
- The prototype uses about 23 parameterized skills and can run commercial and local models, including Claude Opus 4.7, Claude Sonnet 4.6, gpt-oss, Llama 4, Phi, and Gemma.

## Results
- Across multiple statistically independent runs, Genesis achieved 100% success implementing RRC.ConnMean KPM from 3GPP TS 28.552 and Conditional Handover with a closed-loop E2SM-RC xApp.
- The baseline, Claude Code with Opus 4.7, produced 0 working implementations on every attempt for the first 2 case studies.
- The evaluation covers 3 end-to-end case studies: RRC.ConnMean KPM synthesis and OTA propagation, CHO synthesis/testing/hardening, and autonomous RAN scheduler discovery using the ALLSTaR loop.
- The system covers the full 6-step RAN R&D cycle through 6 pipelines and validates generated changes on 3 infrastructure tiers before feeding results back into Synapse.
- The paper reports profiling across stages and says 2 of the 6 Synthesize stages, feature implementation and test execution, dominate both cost and wall-clock time.

## Link
- [https://arxiv.org/abs/2605.27360v1](https://arxiv.org/abs/2605.27360v1)
