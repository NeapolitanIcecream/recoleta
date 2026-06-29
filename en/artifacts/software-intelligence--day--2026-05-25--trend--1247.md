---
kind: trend
trend_doc_id: 1247
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
topics:
- coding agents
- repository reasoning
- agent memory
- software verification
- prompt injection
- AI security
run_id: materialize-outputs
aliases:
- recoleta-trend-1247
tags:
- recoleta/trend
- topic/coding-agents
- topic/repository-reasoning
- topic/agent-memory
- topic/software-verification
- topic/prompt-injection
- topic/ai-security
language_code: en
pass_output_id: 206
pass_kind: trend_synthesis
---

# Coding agents are being judged by memory quality, repository reasoning, and executable safety

## Overview
The day’s strongest research signal is operational control for coding agents. CODESKILL and SETUPX show measurable gains from reusable experience. RepoMirage shows that many agents still struggle when repository cues require multi-file reasoning. Security and verification papers make the same demand concrete: agent actions need bounded authority, independent checks, and machine-readable evidence.

## Clusters

### Reusable agent experience
CODESKILL treats a coding agent’s past trajectories as training data for a skill manager. It writes compact Markdown skills with trigger conditions and action steps, then keeps the bank small through generate, revise, merge, and drop operations. With Qwen3.5-35B-A3B frozen as the coding policy, it reports 39.26 average success across EnvBench-Python, EnvBench-Java, SWE-Bench Verified, and Terminal-Bench 2, compared with 29.57 without skills.

SETUPX applies the same idea to repository setup. It stores setup fixes as eXPerience Units, tries them inside Docker snapshots, rolls back harmful attempts, and uses a Prosecutor-Judge check to avoid accepting superficial success. On 100 Python repositories from EnvBench, SETUPX with experience memory reports a 92% pass rate, 10 points above its no-memory variant.

#### Evidence
- [CODESKILL: Learning Self-Evolving Skills for Coding Agents](../Inbox/2026-05-25--codeskill-learning-self-evolving-skills-for-coding-agents.md): CODESKILL approach, skill-bank operations, and benchmark results.
- [SetupX: Can LLM Agents Learn from Past Failures in Functionality-Correct Code Repository Setup?](../Inbox/2026-05-25--setupx-can-llm-agents-learn-from-past-failures-in-functionality-correct-code-repository-setup.md): SETUPX experience units, Docker rollback, prosecutor-judge verification, and pass-rate results.

### Repository context reasoning
RepoMirage isolates a failure mode that ordinary SWE-Bench scores can hide. It keeps issue behavior the same, then changes how relevant repository context is exposed through dependency indirection, runtime target masking, and externalized constants. Across eight models, average resolved rate falls from 66.80% on SWE-Bench Verified to 49.78% after perturbation, while accessed files rise from 4.77 to 13.24.

The file-access analysis explains why this matters. GPT-5 inspected one file in 53.8% of solved cases and no more than three files in 88.0%. RepoMirage-Extend makes the hidden bottlenecks explicit and reports 25.25% average success, with multi-file issue resolution at 17.86% and proxy-chain recovery at 17.19%.

#### Evidence
- [RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations](../Inbox/2026-05-25--repomirage-probing-repository-context-reasoning-in-code-agents-with-perturbations.md): RepoMirage perturbations, file-access analysis, and benchmark drops.

### Verification for generated software
Verification work in the corpus is concrete and tool-bound. SPDDwL uses Rocq, an interactive theorem prover, to generate a verified pure core and then extract C++ for host integration. In its RISC-V RV32I case study, the system completes all 47 instructions within a 30-minute budget, produces 1,859 lines of verified Rocq and 2,848 lines of C++, passes 265 generated tests, and survives 12 hours of AFL++ fuzzing with no crashes or hangs.

Production-oriented work uses contracts and independent reviewers. The meta-engineering harness turns feature requests into explicit contracts, sends work through role-specialized agents, and classifies failures as bugs, spec gaps, verifier noise, or contract ambiguity. Its early deployment covered 17 features over several weeks and caught five bugs or implementation gaps before merge. ESBMC adds a longer verification view: the survey describes a bounded model checker with nine language front ends, six SMT solver backends, k-induction, and recent links to LLM-driven repair and agentic checking.

#### Evidence
- [Trustworthy Software Project Generation : a Case Study with an Interactive Theorem Prover](../Inbox/2026-05-25--trustworthy-software-project-generation-a-case-study-with-an-interactive-theorem-prover.md): SPDDwL architecture and RISC-V case-study results.
- [Meta-Engineering Harnesses for AI-Native Software Production: A Contract-Driven Adversarial Verification Architecture with Early Deployment Report](../Inbox/2026-05-25--meta-engineering-harnesses-for-ai-native-software-production-a-contract-driven-adversarial-verification-architecture-with-early-deployment-report.md): Contract-driven harness design and early deployment evidence.
- [ESBMC: A Survey of Its Evolution, Integration, and Future Directions in Formal Software Verification](../Inbox/2026-05-25--esbmc-a-survey-of-its-evolution-integration-and-future-directions-in-formal-software-verification.md): ESBMC survey scope, verification capabilities, and LLM/agent integrations.

### Agentic coding security
The strongest security item treats coding assistants as command executors with developer privileges. The AIShellJack study adds poisoned coding-rule files to normal tasks and records what Cursor and GitHub Copilot execute. Across 314 payloads covering 70 MITRE ATT&CK techniques, reported attack success rates range from 41% to 84%.

The attack surface is larger than project files. The paper maps injection paths through shared skills, Model Context Protocol servers, IDE settings, websites, APIs, and messaging tools. It also cites 14 CVEs across Cursor, GitHub Copilot, Claude Code, Zed.dev, Codex, and Windsurf, including cases where attacks triggered before trust dialogs or bypassed command allowlists. Nerve, a self-hosted agent runtime, shows the corresponding product response: plan approval, source-ingestion warnings, script timeouts, and session logs are part of the runtime design, although it reports no accuracy or productivity benchmark.

#### Evidence
- [How Agentic AI Coding Assistants Become the Attacker's Shell](../Inbox/2026-05-25--how-agentic-ai-coding-assistants-become-the-attacker-s-shell.md): AIShellJack setup, attack payload coverage, success rates, and CVE summary.
- [Show HN: Nerve – self hosted runtime for AI agents](../Inbox/2026-05-25--show-hn-nerve-self-hosted-runtime-for-ai-agents.md): Runtime safety features for long-running agents and lack of benchmark evidence.
