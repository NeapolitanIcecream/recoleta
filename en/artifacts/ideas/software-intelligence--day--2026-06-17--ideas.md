---
kind: ideas
granularity: day
period_start: '2026-06-17T00:00:00'
period_end: '2026-06-18T00:00:00'
run_id: c249ae6b-d0f1-46c3-ad74-5372d12de0c4
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- security agents
- agent harnesses
- LLM infrastructure
- software architecture
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/security-agents
- topic/agent-harnesses
- topic/llm-infrastructure
- topic/software-architecture
language_code: en
pass_output_id: 265
pass_kind: trend_ideas
upstream_pass_output_id: 264
upstream_pass_kind: trend_synthesis
---

# Provenance-Aware Coding Agent Evaluation

## Summary
Coding-agent work is moving toward checks that preserve task provenance, separate visible correctness from hidden security behavior, and turn agent reasoning into executable evidence. The practical changes are small enough to test inside existing evaluation and security workflows: run the same model through more than one harness, require security-specific hidden tests, ask audit agents to write falsifiable assertions, and build future-looking tasks from repository evidence available before a cutoff date.

## Model-and-harness security regression runs for vulnerability-fixing agents
Security teams evaluating coding agents should score the model and the agent harness as a pair. Endor Labs reran Claude Fable 5 on the same 200 vulnerability-fixing tasks through Cursor and compared it with an earlier Claude Code run. Cursor + Fable 5 reached 72.6% FuncPass and 29.0% SecPass after anti-cheating and strict-test adjustments, while Claude Code + Fable 5 reached 59.8% FuncPass and 19.0% SecPass.

The workflow change is concrete: keep a fixed set of real vulnerability-fix tasks, run the same model through each candidate IDE or CLI harness, and report FuncPass, SecPass, timeouts, empty patches, and confirmed cheating separately. The SecPass split matters because a patch can pass visible functional tests and still leave the vulnerability open. In the Endor Labs comparison, 13 of 25 Cursor-only security wins were cases where the Claude Code run passed functional tests but failed hidden security tests.

A cheap adoption check is a 20-task slice from the organization’s own past vulnerability fixes. If the same model produces different SecPass results across Cursor, Claude Code, and any internal harness, procurement and AppSec teams get a more useful buying signal than a model-only leaderboard score.

### Sources
- [Claude Fable 5: The harness matters more than the model](../Inbox/2026-06-17--claude-fable-5-the-harness-matters-more-than-the-model.md): Reports the Cursor versus Claude Code comparison for the same Claude Fable 5 model, including FuncPass, SecPass, cheating, and the security gap among functionally passing patches.
- [Claude Fable 5: The harness matters more than the model](../Inbox/2026-06-17--claude-fable-5-the-harness-matters-more-than-the-model.md): Describes the benchmark setup with real projects, one patch per task, Docker isolation, FuncPass, and SecPass.

## Assertion-backed fuzzing for LLM security audit findings
LLM security audit agents should write their safety assumptions as executable assertions at the code site they are judging. Code-Augur follows this pattern: the agent builds a threat model, records local invariants as in-source assertions when it thinks code is safe, and sends the instrumented program to a guided grey-box fuzzer. A failed assertion becomes either a vulnerability report or a bad specification that the agent must refine.

This gives security engineers a direct artifact to inspect after an agent says a file is safe. The surviving assertions can also be kept with the audit record, so later reviews can retest the same assumptions when nearby code changes. The paper reports that Code-Augur found 22 new vulnerabilities in open-source projects, with 16 fixed or confirmed by developers at the time of writing.

A first implementation can target parsers, image codecs, protocol handlers, and other input-heavy code. Ask the agent to emit assertions only for attacker-controlled input boundaries and state conversions, run existing fuzz targets or a short fuzzing budget, and triage assertion failures before filing bugs.

### Sources
- [Code-Augur: Agentic Vulnerability Detection via Specification Inference](../Inbox/2026-06-17--code-augur-agentic-vulnerability-detection-via-specification-inference.md): Summarizes Code-Augur’s method: threat model, in-source assertions, guided grey-box fuzzing, triage, and reported open-source vulnerability results.
- [Code-Augur: Agentic Vulnerability Detection via Specification Inference](../Inbox/2026-06-17--code-augur-agentic-vulnerability-detection-via-specification-inference.md): States that Code-Augur commits local invariants as assertions and uses a fuzzer to falsify those assumptions, with 22 new vulnerabilities and 16 fixed or confirmed.

## Forecast-conditioned repository tasks for coding-agent benchmarks
Benchmark maintainers can reduce direct replay of public pull requests by generating tasks from repository signals available before a cutoff date. SWE-Future builds evidence bundles from pre-snapshot issues, pull requests, labels, titles, and short text, forecasts task families, freezes those forecasts, and then validates them against later pull-request metadata. The later patches are used for validation, not as task prompts or gold solutions.

The reported dataset shows enough detail for a small internal trial. In an 80-repository retrospective study, SWE-Future produced 260 task families across 76 repositories. The final release contains 200 executable tasks across 61 repositories, with hidden tests, gold patches, validation labels, provenance, and execution logs. Bugfix forecasts had the clearest signal, with 89 of 139 bugfix families matching later work as strong or related.

An evaluation owner could pilot this on 10 active repositories: freeze a snapshot, generate bugfix and enhancement families from earlier issue and PR text, wait for a validation window, then synthesize executable tasks only from families that match later project work. The resulting benchmark carries a provenance trail and a time boundary that are easier to audit than copied public issue-and-PR pairs.

### Sources
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): Describes SWE-Future’s pre-snapshot evidence bundles, forecast validation, hidden tests, gold patches, provenance, execution logs, and the main retrospective results.
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): Explains the contamination problem with replayed public GitHub issues and pull requests, and introduces forecast-conditioned task synthesis.
