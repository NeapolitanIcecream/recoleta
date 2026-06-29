---
kind: ideas
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
run_id: 9170a383-c720-44d1-803e-18c4c9822e57
status: succeeded
topics:
- AI coding agents
- code uncertainty
- software testing
- agent runtime control
- MCP
- bug localization
- structured output
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/code-uncertainty
- topic/software-testing
- topic/agent-runtime-control
- topic/mcp
- topic/bug-localization
- topic/structured-output
language_code: en
pass_output_id: 241
pass_kind: trend_ideas
upstream_pass_output_id: 240
upstream_pass_kind: trend_synthesis
---

# Coding agent assurance mechanisms

## Summary
Agentic software work has usable control points at three places: generated code can be scored before it moves to review or another agent, MCP agents can run with capped recent tool history plus short summaries, and AI-generated tests can carry candidate-level evidence through build, execution, coverage, mutation, and repair steps.

## Confidence scoring before generated code enters review or another agent step
Teams using coding agents can add a pre-review score for each generated patch or function. Code Is More Than Text gives a concrete recipe: combine Top-K token entropy, agreement across sampled pseudo-code plans, and the pass rate on self-generated tests. Across five code LLMs and four benchmarks, that ensemble raised average AUROC for predicting hidden-test success from 0.696 to 0.776.

FASE gives a cheaper companion check when tests are missing or expensive. It samples 10 code solutions, embeds them with a model such as Qwen3-Embedding-8B, clusters them with a minimum-spanning-tree rule, and computes entropy over the clusters. On HumanEval and BigCodeBench-hard, it reports a 25% average gain in Spearman correlation with Pass@1 at about 0.3% of the cost of LLM-based semantic entropy.

A practical adoption test is a CI or agent-router step that records these scores for generated code, then compares score bands with real review outcomes, unit-test failures, and rollback data. Low-score outputs can be sent to retry, extra tests, or human review before another agent builds on them.

### Evidence
- [Code Is More Than Text: Uncertainty Estimation for Code Generation](../Inbox/2026-06-08--code-is-more-than-text-uncertainty-estimation-for-code-generation.md): Shows the three code-specific uncertainty signals and benchmark gains for predicting generated-code correctness.
- [FASE: Fast Adaptive Semantic Entropy for Code Quality](../Inbox/2026-06-08--fase-fast-adaptive-semantic-entropy-for-code-quality.md): Shows a lower-cost semantic entropy method based on sample embeddings and MST clustering.

## Capped recent tool history with summaries for MCP agents in verbose enterprise workflows
Enterprise MCP agents should have an explicit context policy that keeps recent tool state intact and stores the full trace outside the model context. In the D365 Finance and Operations hotel-expense benchmark, full conversation history completed 71.0% of tasks while using 1,480,996 tokens. Keeping the last five complete tool call and response pairs raised completion to 79.0% and cut tokens to 535,274. Adding a short summary of the three most recent evicted interactions raised completion to 91.6% with 553,374 tokens.

The build is small enough for a middleware layer around an MCP client: persist every call, pass only the last five complete interactions plus a short rolling summary to the model, and attach trace IDs to each tool result. The trace IDs matter because enterprise MCP practitioners named fast fault localization as the main troubleshooting obstacle in all 20 interviews. The same runtime layer should also enforce controls outside model obedience, such as tool allowlists, state checks, and stop conditions, matching the agent-harness requirement for control mechanisms independent of the model.

### Evidence
- [Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents](../Inbox/2026-06-08--less-context-better-agents-efficient-context-engineering-for-long-horizon-tool-using-llm-agents.md): Reports the D365 F&O context-pruning experiment, completion rates, token counts, and the last-five-plus-summary policy.
- [Understanding How Enterprises Adopt the Model Context Protocol for LLM-Driven Software Engineering](../Inbox/2026-06-08--understanding-how-enterprises-adopt-the-model-context-protocol-for-llm-driven-software-engineering.md): Reports enterprise MCP adoption interviews and the universal complaint about fault localization.
- [What makes a harness a harness: necessary and sufficient conditions for an agent harness](../Inbox/2026-06-08--what-makes-a-harness-a-harness-necessary-and-sufficient-conditions-for-an-agent-harness.md): Defines agent-harness runtime requirements, including task-aware context management and controls independent of model obedience.

## Candidate-level evidence records for AI-generated unit tests
Teams accepting AI-generated tests need a record for each candidate test, including failed and repaired candidates. TestMap shows the shape of that record for C#/.NET: repository and commit metadata, Roslyn project information, build results, TRX execution results, Cobertura coverage, Stryker.NET mutation data, xNose test-smell checks, prompts, model settings, repair attempts, and final outcome labels.

This is a practical workflow change for test-generation pilots. Each generated test can enter review with its target method, baseline coverage, coverage change, mutation signal, build and execution logs, repair count, and smell checks attached. Reviewers can reject tests that only compile, prioritize tests with coverage or mutation evidence, and inspect recurring failure modes by model, prompt, context mode, or repair budget. The useful first check is whether this record reduces reviewer time and catches low-value passing tests in one real repository.

### Evidence
- [TestMap: Evidence Infrastructure for Foundation-Model-Assisted Test Generation](../Inbox/2026-06-08--testmap-evidence-infrastructure-for-foundation-model-assisted-test-generation.md): Describes TestMap’s evidence categories, .NET toolchain, outcome labels, and candidate-level traceability for generated tests.
