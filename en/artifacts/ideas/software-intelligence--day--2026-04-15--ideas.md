---
kind: ideas
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
run_id: 2c820f02-ea9f-4551-985d-436f1ebff98d
status: succeeded
topics:
- coding-agents
- evaluation
- repository-context
- memory
- generalization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/repository-context
- topic/memory
- topic/generalization
language_code: en
pass_output_id: 73
pass_kind: trend_ideas
upstream_pass_output_id: 72
upstream_pass_kind: trend_synthesis
---

# Controlled agent feedback loops

## Summary
The usable pattern in this evidence is tighter control over what the agent sees, what kind of fix it attempts next, and how its output is judged. Repository tools can compress context before generation because selective compression improved quality and latency in the cited study. Test-driven coding loops can route failures into plan repair or code repair because that decision improved pass rates while cutting retries. Generated tests need mutation-score gating on unseen codebases because public-benchmark wins did not carry over to SAP HANA, and compilation feedback alone could reward weaker tests.

## Repository context compression before code generation
Repository-aware coding tools should add a context compression stage that ranks and condenses files before generation, then keep full-file retrieval as a fallback for misses. The current evidence says long prompts are carrying enough noise that a learned compressed representation can beat full-context inference on repository tasks while also cutting latency. In the repository compression study, QC-7B with text-to-vector compression at 4x reached 41.34 BLEU on Python completion versus 32.21 for full context, and the paper reports end-to-end latency cuts up to 50%. That points to a buildable editor or CI feature for teams whose agents already read too many files: compress the repo view into task-scoped memory tokens, log when the agent asks for raw files anyway, and compare acceptance rate and response time against today's full-context path. The practical bar is simple: if compressed context keeps completion quality flat or better on the team's own repositories while lowering latency, it should become the default path for repository-scale assistance.

### Evidence
- [On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation](../Inbox/2026-04-15--on-the-effectiveness-of-context-compression-for-repository-level-tasks-an-empirical-investigation.md): Shows compressed repository context can outperform full-context inference and reduce latency, with concrete QC-7B results at 4x compression.
- [On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation](../Inbox/2026-04-15--on-the-effectiveness-of-context-compression-for-repository-level-tasks-an-empirical-investigation.md): Confirms the mechanism and reported gains from latent vector compression filtering repository noise.

## Plan-repair and code-repair split in test-driven coding loops
Coding agents that already run tests should separate plan repair from code repair and store failure summaries between iterations. The CollabCoder results point to a concrete workflow change: when a run fails, classify whether the problem is in the approach, the implementation, or the alignment between them, then choose the next edit accordingly. In the paper, this structure improved Pass@1 on both standard and harder benchmarks while using fewer API calls than recent agent baselines. On Qwen2.5-Coder-32B, CollabCoder reached 82.50 average Pass@1 versus 80.22 for CodeSIM, with 4.12 API calls versus 4.87. On LiveCodeBench and xCodeEval with GPT-4o mini, it reported 44.56 average Pass@1 and lower call counts than CodeSIM and MapCoder. A practical first version does not need three full agents. A single agent can emit a failure label, keep a short repair log, and switch prompts between plan revision and code revision. The cheap check is whether repeated failing runs stop revisiting the same weak fix and whether average retries fall on tasks with hidden tests.

### Evidence
- [CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation](../Inbox/2026-04-15--collabcoder-plan-code-co-evolution-via-collaborative-decision-making-for-efficient-code-generation.md): Summarizes the plan-versus-code revision decision and reports benchmark gains with fewer API calls.
- [CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation](../Inbox/2026-04-15--collabcoder-plan-code-co-evolution-via-collaborative-decision-making-for-efficient-code-generation.md): Shows the core mechanism: revising the plan during execution based on intermediate outcomes.

## Mutation-score gating for generated tests on proprietary code
Enterprise test-generation workflows need a harder acceptance gate than coverage and compilation. The SAP HANA study shows why. On LevelDB whole-suite generation, all four tested models reached 100.00% mutation score in the source-only setting, but on proprietary SAP HANA the best source-only mutation score was 10.25%, rising to 25.14% with dependency and header context and still below a reduced human baseline of 30.41%. The same paper says compiler-feedback repair can raise compilation success to very high levels while many fixes weaken tests by removing assertions or leaving empty bodies. That supports a specific adoption change for teams evaluating generated tests: require mutation score, assertion-density checks, and context-controlled comparisons on code the model has not likely seen, with dependency context tracked as a separate condition. If a vendor demo only shows public repositories and coverage gains, this evidence says the workflow is still missing the main safeguard.

### Evidence
- [LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB](../Inbox/2026-04-15--llms-taking-shortcuts-in-test-generation-a-study-with-sap-hana-and-leveldb.md): Provides the LevelDB versus SAP HANA gap, the mutation-score results, and the effect of adding dependency context.
- [LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB](../Inbox/2026-04-15--llms-taking-shortcuts-in-test-generation-a-study-with-sap-hana-and-leveldb.md): Confirms the proprietary-code setting and the paper's concern about shortcut behavior on public benchmarks.
