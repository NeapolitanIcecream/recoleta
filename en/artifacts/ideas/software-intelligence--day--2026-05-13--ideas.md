---
kind: ideas
granularity: day
period_start: '2026-05-13T00:00:00'
period_end: '2026-05-14T00:00:00'
run_id: 0382e4c2-09c9-46ad-a3c5-07b5736cf4fa
status: succeeded
topics:
- coding agents
- agent evaluation
- software engineering
- verification
- runtime systems
- agent optimization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/verification
- topic/runtime-systems
- topic/agent-optimization
language_code: en
pass_output_id: 151
pass_kind: trend_ideas
upstream_pass_output_id: 150
upstream_pass_kind: trend_synthesis
---

# Agent verification records

## Summary
Complete agent work now needs evidence that the agent set up the project, chose the right files, ran meaningful checks, and preserved existing behavior. The practical moves are concrete: add trace packages to agent PRs, feed HDL agents executable EDA failure logs, and test property-based prompts per model before asking agents to write semantic tests.

## Agent PR trace packages with setup, test, and intervention records
Software teams adopting code agents should require each agent PR to include a compact trace package: environment setup steps, files inspected, commands run, generated or changed tests, verification results, failure diagnosis, and any human intervention. This gives reviewers a stable artifact to inspect before they spend time reading a large patch.

SWE-Cycle shows why this matters. Agents can do much better on isolated setup and test-generation tasks than on full issue resolution from a raw repository; the best FullCycle solve rate in the excerpt is 13.50%, even though isolated environment reconstruction reaches 78.12% and isolated verification test generation reaches 67.28%. AI Harness Engineering gives the operational checklist for the missing evidence, including action, tool, context, verification, failure attribution, intervention, entropy, and outcome traces. 1Password’s monolith refactor shows the production version: agents worked better when engineers built deterministic analyzers, manifests, stop rules, and review points, while sequencing mistakes still required human control.

### Sources
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle reports the sharp gap between isolated setup or test tasks and full raw-repository issue resolution.
- [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](../Inbox/2026-05-13--ai-harness-engineering-a-runtime-substrate-for-foundation-model-software-agents.md): AI Harness Engineering defines trace classes and runtime responsibilities for auditable agent software work.
- [What we learned using AI agents to refactor a monolith](../Inbox/2026-05-13--what-we-learned-using-ai-agents-to-refactor-a-monolith.md): 1Password describes deterministic analyzers, manifests, stop rules, and human review during a large Go monolith refactor.

## EDA testbench-log feedback for HDL repository agents
Hardware teams testing software-style coding agents on Verilog or SystemVerilog should add an EDA feedback loop before broad adoption. A practical version runs the agent’s patch in a Docker-pinned Verilator or synthesis environment, returns the failing testbench log with module hierarchy context, and asks for one repair attempt in an isolated worktree.

Phoenix-bench reports that top commercial agents resolve only 32.7% to 38.6% of repository-level HDL issues under executable EDA checks, with drops of 37 to 58 percentage points compared with SWE-bench Verified. The failure mode is specific: agents stop at symptom files and miss signal-flow dependencies through ports, clocks, resets, parameters, and instantiated modules. File-level oracle localization adds only 1.4 percentage points, while one round of testbench-log feedback lifts resolved rates to about 42% to 45%. The cheap adoption test is a small internal benchmark of recent HDL bugs with fail-to-pass and pass-to-pass checks, scored only when the target failure passes and prior passing tests still pass.

### Sources
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Phoenix-bench summarizes repository-level HDL tasks, EDA checks, resolved rates, SWE-bench transfer drops, and the effect of testbench-log feedback.
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): The paper describes cross-hierarchy signal-flow failures and why file-level localization is too coarse for many hardware bugs.

## Model-specific property-based testing prompt trials for Python libraries
Teams asking agents to write tests for Python libraries should trial property-based testing prompts per model before adding the workflow to CI. The concrete check is small: give the agent API documentation, existing tests, and a hidden buggy version, require a `pbt_test.py` file using Hypothesis, and score tests by fail-on-buggy and pass-on-fixed behavior.

PBT-Bench isolates this skill across 100 problems, 40 Python libraries, and 365 injected semantic bugs. Under a PBT-guided prompt, recall ranges from 42.1% to 83.4% across models. The same prompt helps some models by more than 20 percentage points and hurts others, including reported drops for DeepSeek V3.2 and Grok 4.1 Fast. A team can use this pattern to decide which model and prompt are allowed to generate property tests for documented invariants, especially for APIs where boundary cases and input distributions matter more than example-based tests.

### Sources
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): PBT-Bench defines the task, benchmark size, Hypothesis output requirement, and model-by-prompt results.
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): The paper reports the recall range and model-specific gains or degradations under Hypothesis scaffolding.
