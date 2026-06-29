---
kind: trend
trend_doc_id: 1103
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
topics:
- coding agents
- software engineering
- agent evaluation
- test generation
- trajectory training
- self-evolving agents
- pull requests
run_id: materialize-outputs
aliases:
- recoleta-trend-1103
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/test-generation
- topic/trajectory-training
- topic/self-evolving-agents
- topic/pull-requests
language_code: en
pass_output_id: 182
pass_kind: trend_synthesis
---

# Coding agents are being judged by the evidence they leave behind

## Overview
Current emphasis: coding-agent work is tying progress to inspectable evidence. P2T curates repair steps, SWE-Mutation tests whether generated tests catch real bugs, and MOSS replays production failures before source-level updates.

## Clusters

### Trajectory evidence for training coding agents
P2T treats a developer patch as private curation data, then builds a process graph of facts, milestones, edits, and validation steps. The student agent sees only grounded trajectory prefixes. This targets a common failure in supervised fine-tuning: copying long teacher traces that contain repeated file views, loops, or unsupported reasoning.

The reported gains are practical. On SWE-bench Verified, P2T reports up to a 10.8 point Pass@1 gain over outcome-filtered supervised fine-tuning, while lowering average inference cost by about $15 per instance. ACC takes a related path for long-context training. It compiles completed Search, software engineering, and SQL agent runs into question-answer examples built from scattered tool outputs. Fine-tuning Qwen3-30B-A3B-Thinking with those compiled contexts raises MRCR from 50.19 to 68.28 and GraphWalks from 69.92 to 77.51.

#### Evidence
- [From Patches to Trajectories: Privileged Process Supervision for Software-Engineering Agents](../Inbox/2026-05-21--from-patches-to-trajectories-privileged-process-supervision-for-software-engineering-agents.md): P2T summary, method, and SWE-bench results.
- [ACC: Compiling Agent Trajectories for Long-Context Training](../Inbox/2026-05-21--acc-compiling-agent-trajectories-for-long-context-training.md): ACC trajectory compilation method and long-context benchmark gains.

### Generated tests face harder checks
SWE-Mutation separates executable tests from useful tests. Each issue is paired with mutants derived from the golden fix, and generated tests must reproduce the original bug, pass on the fix, and detect faulty variants. The gap is large: DeepSeek-V3.1 with Mini-Swe-Agent reaches 88.20% Pass@1 on Python test generation, but only 10.20% verification and 36.15% mutant detection.

VeriScale applies a similar pressure to Lean-based verifiable code generation. It expands Verina into VerinaPlus with many more expected cases, unexpected inputs, and adversarial unexpected outputs. Under the stronger suite, GPT-5.5 SpecGen falls from 68.78% to 44.44%, and CodeGen falls from 96.83% to 86.24%. The shared lesson is concrete: test suites need adversarial coverage, not just runnable cases.

#### Evidence
- [SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?](../Inbox/2026-05-21--swe-mutation-can-llms-generate-reliable-test-suites-in-software-engineering.md): SWE-Mutation benchmark design and model results.
- [VeriScale: Adversarial Test-Suite Scaling for Verifiable Code Generation](../Inbox/2026-05-21--veriscale-adversarial-test-suite-scaling-for-verifiable-code-generation.md): VeriScale test-suite scaling method and score drops.

### Production failures are becoming update inputs
MOSS tests whether a deployed agent can repair its own source code after repeated user-facing failures. It batches weak or missing dialogue chunks, runs ordered stages for locating, planning, editing, reviewing, evaluating, and verdicts, then tests candidate images in trial-worker containers. Promotion still requires user consent through `moss evo apply`, health probes, and rollback.

On OpenClaw, one evolution cycle raises the four-task mean grader score from 0.25 to 0.61 without human code edits. The interesting part is the scope of repair: MOSS edits harness code as well as prompts, skills, and memory, so failures in routing, hook ordering, session state, dispatch, and concurrency are within reach.

#### Evidence
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): MOSS design, deployment safeguards, and OpenClaw score change.

### Review records and patch structure matter
Two studies show why final pass or merge labels are too coarse for coding agents. The agentic pull-request study inspects 11,048 closed PRs and manually codes 717 cases. Among rejected PRs, only 35.7% are clear agent failures; workflow constraints and unknown rationale account for the rest. Among merged PRs, 15.4% include explicit review feedback or reviewer-applied commits.

Refactoring Runaway looks inside the patch itself. In 3,691 valid Java agent patches, tangled refactorings appear in 21.43% of agent patches and are linked to lower compilability. RefUntangle checks whether refactorings are needed and safe, then removes or repairs risky ones. Average compilation success rises from 19.34% to 38.33%, and 2.79% of previously unresolved patches pass all tests.

#### Evidence
- [Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study](../Inbox/2026-05-21--why-are-agentic-pull-requests-merged-or-rejected-an-empirical-study.md): Agentic PR dataset, manual coding, and merge/rejection findings.
- ["Refactoring Runaway": Understanding and Mitigating Tangled Refactorings in Coding Agents for Issue Resolution](../Inbox/2026-05-21--refactoring-runaway-understanding-and-mitigating-tangled-refactorings-in-coding-agents-for-issue-resolution.md): Tangled refactoring study and RefUntangle results.
