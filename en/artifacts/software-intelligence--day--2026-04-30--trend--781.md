---
kind: trend
trend_doc_id: 781
granularity: day
period_start: '2026-04-30T00:00:00'
period_end: '2026-05-01T00:00:00'
topics:
- agent evaluation
- vision-to-code grounding
- LLM supply chain
- software security
- dependency risk
run_id: materialize-outputs
aliases:
- recoleta-trend-781
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/vision-to-code-grounding
- topic/llm-supply-chain
- topic/software-security
- topic/dependency-risk
language_code: en
pass_output_id: 120
pass_kind: trend_synthesis
---

# AI engineering research is tightening evidence gates around agents and model dependencies

## Overview
The day’s strongest research treats large language models (LLMs) as dependencies that need evidence gates. C2VEval exposes visual-code shortcuts, Claw-Eval-Live grades real workflow traces, and IronCurtain ties security claims to harnesses and executable proof.

## Findings

### Benchmarks that test the work artifact
C2VEval shows how a vision-to-code benchmark can overstate capability when task text leaks the answer. In circuit-to-Verilog generation, model headers such as `sum`, `cout`, or `fsm_3state` let multimodal LLMs (MLLMs) produce plausible register-transfer-level code without reading the diagram. When the authors replace the image with a blank one, Mirage mode matches or beats real-image mode on all eight evaluated MLLMs. After anonymizing identifiers, GPT-5.4 drops from 45.51% to 24.55% Functional Pass@1, and Opus 4.6 drops from 52.69% to 11.38%.

Claw-Eval-Live applies the same evidence-first instinct to workflow agents. It grades 105 tasks using traces, audit logs, service state, post-run files, command traces, and tests. Claude Opus 4.6 leads at 66.7% pass rate, and no evaluated model reaches 70%. The result is a concrete ceiling on today’s workflow automation claims, especially for HR, management, and multi-system business tasks.

#### Sources
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): C2VEval design, Mirage failure, anonymized results, and VeriGround metrics.
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Claw-Eval-Live task construction, grading evidence, model results, and hard task families.

### Security agents need state and executable validation
IronCurtain frames vulnerability discovery as a stateful investigation. A central orchestrator reads an append-only journal, dispatches specialist agents, and keeps code search, harness creation, and validation outside a single model context. The workflow reproduced the 1998 OpenBSD TCP SACK vulnerability and used Opus 4.6 to build a fuzzer that narrowed the trigger to a two-sequence-number difference at a 32-bit signed integer boundary. A QEMU-based driver then reproduced the kernel panic.

The same report gives useful cost and access details. Opus and Sonnet runs used about 10 million tokens per investigation, with reported costs near $150 and $30. Hosted GLM 5.1 runs averaged 27 million tokens and still produced a proof-of-concept plus sanitizer-validated harness for an 18-year-old integer truncation flaw. The evidence favors security pipelines that validate reachability, not static bug reports alone.

#### Sources
- [Finding Zero Days with any model?](../Inbox/2026-04-30--finding-zero-days-with-any-model.md): IronCurtain workflow, OpenBSD reproduction, GLM 5.1 finding, validation tiers, and token costs.

### Model and package dependencies are treated as governed production risks
The LLM supply-chain paper argues for deployer-side compatibility gates before hosted model updates reach production. Its examples are practical: unit-test contracts, valid JSON requirements, code-only output rules, and risk categories such as authentication, data validation, and structured output. In a small validation over seven Claude models and 25 prompts, structured JSON tasks showed more drift than SQL and authentication tasks. One backend SQL function passed with Sonnet 4, then failed a safe-encoding test the next day.

Deptex extends the same operational lens to open-source package risk. It combines an organization graph, policy checks, code-property-graph reachability, and constrained LLM verification. In its scenario, a CVSS 9.8 issue appears in 10 repositories, but eight paths are downgraded because they sit in offline batch scripts six function hops deep, while two public unauthenticated API paths receive high exposure. The paper is mostly a design and scenario report, so its claims need measured alert-reduction results.

#### Sources
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): Production contracts, risk-category tests, Claude validation setup, and observed drift examples.
- [DEPTEX: Organization-First, Open Source Dependency Risk Monitoring](../Inbox/2026-04-30--deptex-organization-first-open-source-dependency-risk-monitoring.md): Deptex architecture, Execution Path Dominance scoring, and CVSS 9.8 scenario.

### Hardware AI work is demanding domain checks
The hardware items share a concern about models that produce convincing artifacts without enough domain grounding. VeriGround addresses that problem in circuit generation with anonymized training, blank-image refusal examples, and decision-focused preference tuning. It reaches 46.11% Functional Pass@1 on normal C2VEval inputs and 42.51% on anonymized inputs, while keeping false refusals low on valid examples.

JuliaHub’s Dyad 3.0 announcement makes a related product claim for physical-system engineering. It connects agents with physics simulation, control design, safety analysis, and embedded code generation. The release says a Scientific Machine Learning digital twin used four sensor inputs to predict pump faults with over 90% accuracy in work with Binnies and Williams Grand Prix Technologies. The announcement includes useful engineering direction, but its benchmark evidence is limited compared with the circuit-generation paper.

#### Sources
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): VeriGround training recipe, functional pass rates, and refusal metrics.
- [Building Persona-Based Agents On Demand: Tailoring Multi-Agent Workflows to User Needs](../Inbox/2026-04-30--building-persona-based-agents-on-demand-tailoring-multi-agent-workflows-to-user-needs.md): Dyad 3.0 claims, physics-grounded workflow, and pump-fault digital twin result.
