---
kind: ideas
granularity: day
period_start: '2026-04-23T00:00:00'
period_end: '2026-04-24T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- coding-agents
- test-generation
- static-analysis
- runtime-verification
- human-oversight
tags:
- recoleta/ideas
- topic/coding-agents
- topic/test-generation
- topic/static-analysis
- topic/runtime-verification
- topic/human-oversight
language_code: en
pass_output_id: 105
pass_kind: trend_ideas
upstream_pass_output_id: 104
upstream_pass_kind: trend_synthesis
---

# Postgeneration Verification Controls

## Summary
The clearest near-term builds add hard structure around what the model is allowed to produce and keep verification active after generation. The most concrete cases here are a typed intermediate for static-analysis chat, runtime semantic checkers synthesized from existing tests, and repository test bots that expand one trusted test into scenario variants with repair and validation.

## Typed JSON translation layer for natural-language static analysis
Static-analysis chat should stop asking the model to write Joern CPGQL directly. The better build is a two-step translator: the model fills a small typed JSON form for query intent, then deterministic code maps that form into the final query and runs validation before execution. The evidence is unusually concrete. In a 20-task benchmark over Apache Commons Lang and OWASP WebGoat, the schema-bound JSON design beat direct query generation for every tested model, with gains of 15.0 points for Qwen 72B and 25.0 points for Llama 70B. It also beat an agentic tool loop that used about 8 times more tokens per task and still produced worse results.

The operational pain is familiar to teams building natural-language access for static analysis: generated queries often execute but answer the wrong question, while free-form agent loops add latency and failure modes without solving DSL correctness. A typed intermediate gives product teams a place to enforce allowed query types, required fields, and schema checks before anything touches the analysis engine.

A cheap validation path is straightforward. Take a backlog of real English analysis requests from security or AppSec users, define a narrow JSON schema for the top query families, and compare result-match rate, execution success, and token cost against direct query generation. If the tool already logs failed or misleading CPGQL generations, those requests are the right starting set.

### Evidence
- [Less Is More: Measuring How LLM Involvement affects Chatbot Accuracy in Static Analysis](../Inbox/2026-04-23--less-is-more-measuring-how-llm-involvement-affects-chatbot-accuracy-in-static-analysis.md): Reports that a schema-bound JSON intermediate outperformed direct CPGQL generation and an agentic tool loop across all tested models, with concrete accuracy and token-cost differences.
- [Less Is More: Measuring How LLM Involvement affects Chatbot Accuracy in Static Analysis](../Inbox/2026-04-23--less-is-more-measuring-how-llm-involvement-affects-chatbot-accuracy-in-static-analysis.md): Explains why CPGQL usability is a practical adoption blocker for developers who lack DSL and schema knowledge.

## Runtime checker generation from existing integration tests
Teams with decent test suites can add runtime semantic checking by compiling selected tests into always-on checkers for production and staging. FlyCatcher points to a concrete way to do this: use existing tests as the source of intended behavior, infer a checker with static analysis plus LLM synthesis, track the needed abstract state in shadow state, and validate the generated checker on held-out tests before deployment.

This fits a real gap in coding-agent workflows. Generated code may pass the local test suite and still violate semantics later under different workloads. Runtime checkers cover that gap for failures that do not crash the program or trip ordinary assertions. On 400 tests from four Java systems, FlyCatcher inferred 334 checkers, with 300 judged correct through cross-validation. It produced 2.6 times more correct checkers than T2C and detected 5.2 times more mutants.

The first users are teams running stateful Java services where silent failures are expensive: messaging, replication, session handling, inventory logic, or any code with invariants that matter after deployment. The cheap check is to pick one subsystem with high-value integration tests, generate checkers for a small batch of tests, and measure three things in staging: validation pass rate for the generated checker, extra mutant detection, and runtime overhead. The paper’s overhead range, 2.7% to 40.3%, makes that measurement necessary before broad rollout.

### Evidence
- [FlyCatcher: Neural Inference of Runtime Checkers from Tests](../Inbox/2026-04-23--flycatcher-neural-inference-of-runtime-checkers-from-tests.md): Provides the full method and headline results for inferring runtime checkers from tests, including checker counts, correctness, mutant detection, cost, and overhead.
- [FlyCatcher: Neural Inference of Runtime Checkers from Tests](../Inbox/2026-04-23--flycatcher-neural-inference-of-runtime-checkers-from-tests.md): Gives concrete examples of silent semantic failures and explains why semantic runtime checkers are useful in production systems.

## Scenario expansion for repository test bots from a single seed test
A useful next step for repository test bots is to start from one developer-written test and expand it into a family of scenario variants, then repair those tests until they compile and pass. TestGeneralizer gives a concrete recipe for this workflow. It infers the scenario behind the seed test, writes a scenario template with variation points, instantiates those variants, and uses project facts from program analysis to keep the generated tests valid.

The user pressure is clear in mature repositories: the first test often captures one happy path, while the rest of the scenario coverage arrives later through bug reports and patch releases. This paper targets that gap directly. Across 12 Java projects, 506 focal methods, and 1,637 test scenarios, TestGeneralizer improved mutation-based scenario coverage by 57.67% over EvoSuite, 37.44% over gpt-o4-mini, and 31.66% over ChatTester. The most persuasive adoption signal is the field study: 16 of 27 generated tests were accepted and merged by maintainers.

This is a buildable workflow for CI or for pull-request review on changed methods that already have at least one trusted test. A low-cost trial is to run it only on files with new or modified tests, limit output to two or three candidate variants per seed test, and track merge acceptance, flaky-test rate, and distinct bug findings. That setup keeps reviewer load bounded while showing whether scenario expansion is adding useful coverage or only more test volume.

### Evidence
- [Generalizing Test Cases for Comprehensive Test Scenario Coverage](../Inbox/2026-04-23--generalizing-test-cases-for-comprehensive-test-scenario-coverage.md): Describes the three-stage scenario-generalization pipeline and reports benchmark gains plus merged-test results from the field study.
- [Generalizing Test Cases for Comprehensive Test Scenario Coverage](../Inbox/2026-04-23--generalizing-test-cases-for-comprehensive-test-scenario-coverage.md): States the practical testing problem clearly: important tests often arrive late after bugs, because the initial test captures only part of the intended scenario space.
