---
kind: trend
trend_doc_id: 611
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
topics:
- coding-agents
- real-world-evaluation
- agent-harness
- developer-docs
- execution-based-validation
- security-testing
run_id: materialize-outputs
aliases:
- recoleta-trend-611
tags:
- recoleta/trend
- topic/coding-agents
- topic/real-world-evaluation
- topic/agent-harness
- topic/developer-docs
- topic/execution-based-validation
- topic/security-testing
language_code: en
pass_output_id: 102
pass_kind: trend_synthesis
---

# Coding-agent research is getting judged by kept code, control surfaces, and executable proof

## Overview
April 22’s research is strongest where coding work meets concrete checks from real use, project scaffolding, and direct execution. SWE-chat grounds coding-agent claims in kept code and user pushback. HARBOR and AGENTS.md show that harness and documentation choices can change results as much as model selection. WebGen-R1 and LLMVD.js extend the same pressure into website generation and security, where outputs are scored by running systems, not polished text.

## Clusters

### Real workflow evidence is now a first-class coding-agent input
Real usage evidence is getting harder to ignore. SWE-chat logs about 6,000 sessions across 200+ repositories and shows that coding agents are used for code understanding, git operations, debugging, and full code writing, not just benchmark-style patching. The useful correction is that output volume is a weak proxy for value. Agent-written code survives at 50.3% overall, and collaborative sessions fall to 44.1%. The same paper also shows clear cost and risk differences: vibe-coded work uses 204K tokens per 100 committed lines and introduces 0.76 vulnerabilities per 1,000 committed lines, versus 0.14 in collaborative sessions. That fits the recent run of papers that add execution and behavioral checks, but this one adds the missing in-the-wild layer: what developers kept, what they rejected, and how often they pushed back.

#### Evidence
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): Summary metrics on session mix, code survival, cost, and vulnerability rates.

### Docs, harnesses, and test artifacts are part of the model behavior now
The control surface around coding agents is getting more explicit. One line of work treats project documents as direct performance inputs. The AGENTS.md study reports 10 to 15% gains from short, task-specific files, a drop in missing wiring files from 40% to 10% with a six-step workflow, and large failures when docs are bloated or warning-heavy. Another line treats the harness itself as the optimization target. HARBOR shows that manual flag stacking can backfire: a baseline at 15/89 tasks improved to 17/89 with one bundle of native flags, then fell to 13/89 after adding self-evaluation and 12/89 after adding more published techniques. Shift-Up sits on the process side of the same theme. It uses requirements, architecture records, and executable tests to constrain agent work, but its evidence is still qualitative. The common emphasis is clear: teams are tuning the wrapper around the model as much as the model output.

#### Evidence
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): Concrete effects of AGENTS.md structure on real software tasks.
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): Manual harness tuning results and configuration sensitivity.
- [Shift-Up: A Framework for Software Engineering Guardrails in AI-native Software Development -- Initial Findings](../Inbox/2026-04-22--shift-up-a-framework-for-software-engineering-guardrails-in-ai-native-software-development-initial-findings.md): Process guardrails via requirements and executable tests, with noted evidence limits.

### Run it, render it, or exploit it: verification keeps moving closer to the task
Execution-backed evaluation keeps spreading into adjacent coding tasks. WebGen-R1 uses reinforcement learning for multi-page website generation, but the key detail is its reward design: a site must pass structure checks, build, serve, and render before visual scoring matters. On its reported benchmark, valid render ratio rises from 30.56% to 95.89%, while functional quality moves from 1.59% to 29.21%. Security work is using the same pattern of concrete confirmation. LLMVD.js does not stop at suspicious flows in Node.js packages; it generates and runs proof-of-concept exploits, confirming 84% of benchmark vulnerabilities and producing validated exploits for 36 of 260 recent packages. A separate OSV-based evaluation paper makes a narrower point: even scanner comparisons need version-level ground truth before numbers are trustworthy. The throughline is practical verification. Systems are being judged by what runs, renders, or exploits under direct checks.

#### Evidence
- [WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning](../Inbox/2026-04-22--webgen-r1-incentivizing-large-language-models-to-generate-functional-and-aesthetic-websites-with-reinforcement-learning.md): Execution-grounded reward design and website generation results.
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): Exploit confirmation pipeline and benchmark/package findings.
- [A Ground-Truth-Based Evaluation of Vulnerability Detection Across Multiple Ecosystems](../Inbox/2026-04-22--a-ground-truth-based-evaluation-of-vulnerability-detection-across-multiple-ecosystems.md): Need for explicit version-level ground truth in vulnerability evaluation.
