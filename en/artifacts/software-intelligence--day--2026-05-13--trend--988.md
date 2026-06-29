---
kind: trend
trend_doc_id: 988
granularity: day
period_start: '2026-05-13T00:00:00'
period_end: '2026-05-14T00:00:00'
topics:
- coding agents
- agent evaluation
- software engineering
- verification
- runtime systems
- agent optimization
run_id: materialize-outputs
aliases:
- recoleta-trend-988
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/verification
- topic/runtime-systems
- topic/agent-optimization
language_code: en
pass_output_id: 150
pass_kind: trend_synthesis
---

# Code agents are being graded on complete, verifiable work

## Overview
The period’s clearest signal: code agents are being judged by complete, checkable work. SWE-Cycle and Phoenix-bench make setup, tests, and domain toolchains part of the score. CRANE shows model editing can raise agent pass rates when tool-call format is protected.

## Clusters

### End-to-end software work
SWE-Cycle makes the gap visible between partial progress and full issue resolution. It asks agents to rebuild the environment, implement the fix, and write verification tests in a raw repository. The best FullCycle solve rate in the excerpt is 13.50%, even though isolated environment reconstruction reaches 78.12% and isolated test generation reaches 67.28%.

AI Harness Engineering gives a systems explanation for this pattern. It treats agent performance as the result of the model, runtime harness, and repository environment together. Its proposed trace package records actions, tool use, context, verification, failure attribution, intervention, entropy, and outcome, so a successful patch must come with evidence about how it was produced.

#### Evidence
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle task design, FullCycle evaluation, and reported solve rates.
- [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](../Inbox/2026-05-13--ai-harness-engineering-a-runtime-substrate-for-foundation-model-software-agents.md): Harness responsibilities, trace classes, and verification-focused evaluation protocol.

### Domain toolchains expose transfer limits
Phoenix-bench tests software-style agents on Verilog and SystemVerilog maintenance tasks under executable Electronic Design Automation (EDA) checks. Top commercial agents resolve only 32.7% to 38.6% of tasks. The same agents lose 37 to 58 percentage points compared with SWE-bench Verified.

The failure mode is concrete. Hardware bugs propagate through ports, clocks, resets, parameters, and signal flow across instantiated modules. A file-level oracle adds only 1.4 percentage points because agents still make wrong module edits. One round of testbench-log feedback raises resolved rates to about 42% to 45%, showing that executable failure evidence is more useful than file names alone.

#### Evidence
- [Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench](../Inbox/2026-05-13--is-agentic-ai-ready-for-real-world-hardware-engineering-a-deep-dive-with-phoenix-bench.md): Phoenix-bench construction, EDA evaluation, resolved rates, transfer drop, and diagnostic interventions.

### Verification skills are becoming separate targets
PBT-Bench isolates property-based testing (PBT): the agent must infer a documented invariant and write Hypothesis input generators that reach semantic bugs. The benchmark covers 100 problems, 40 Python libraries, and 365 injected bugs. Under the PBT-guided prompt, recall spans 42.1% to 83.4% across models.

The prompt gains are uneven. Qwen 3.6 Plus gains 24.5 percentage points, Qwen 3.5-30B-A3B gains 22.9 points, and Step 3.5 Flash gains 20.3 points. DeepSeek V3.2 and Grok 4.1 Fast lose recall under the same scaffolding. This makes test-design competence a measurable agent skill, with model-specific prompt fit.

#### Evidence
- [PBT-Bench: Benchmarking AI Agents on Property-Based Testing](../Inbox/2026-05-13--pbt-bench-benchmarking-ai-agents-on-property-based-testing.md): PBT-Bench design, scale, scoring method, recall ranges, and model-specific prompt effects.

### Agent reliability is being tuned below the product surface
CRANE edits Qwen Instruct checkpoints with reasoning directions from Thinking checkpoints, then suppresses updates that would disturb tool delimiters, JSON schema tokens, and chat templates. On Roo-Eval, it reaches 66.2% pass@1 at 30B compared with 46.7% for the Instruct baseline, and 81.5% at 80B compared with 72.8%.

Other work tunes the surrounding machinery. CANTANTE assigns per-agent prompt credit from system-level scores and reports the best average rank across MBPP, GSM8K, and HotpotQA. SkillOps maintains reusable agent skills as typed contracts with validators and compatibility links, reaching 79.5% task success on ALFWorld with a 200-skill library. 1Password’s monolith refactor shows the production version of the same lesson: agents helped after engineers supplied deterministic analyzers, manifests, stop rules, and review points.

#### Evidence
- [CRANE: Constrained Reasoning Injection for Code Agents via Nullspace Editing](../Inbox/2026-05-13--crane-constrained-reasoning-injection-for-code-agents-via-nullspace-editing.md): CRANE method and Roo-Eval, SWE-bench-Verified, and Terminal-Bench results.
- [CANTANTE: Optimizing Agentic Systems via Contrastive Credit Attribution](../Inbox/2026-05-13--cantante-optimizing-agentic-systems-via-contrastive-credit-attribution.md): CANTANTE per-agent credit assignment and benchmark results.
- [SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems](../Inbox/2026-05-13--skillops-managing-llm-agent-skill-libraries-as-self-maintaining-software-ecosystems.md): SkillOps contract representation, maintenance actions, and ALFWorld result.
- [What we learned using AI agents to refactor a monolith](../Inbox/2026-05-13--what-we-learned-using-ai-agents-to-refactor-a-monolith.md): 1Password production refactor setup, deterministic tooling, results, and failure cases.
