---
kind: ideas
granularity: day
period_start: '2026-04-21T00:00:00'
period_end: '2026-04-22T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- code-llm-evaluation
- program-repair
- test-generation
- gui-code
- agent-governance
tags:
- recoleta/ideas
- topic/code-llm-evaluation
- topic/program-repair
- topic/test-generation
- topic/gui-code
- topic/agent-governance
language_code: en
pass_output_id: 101
pass_kind: trend_ideas
upstream_pass_output_id: 100
upstream_pass_kind: trend_synthesis
---

# Executable behavior gates

## Summary
Behavioral checks are getting specific enough to change coding workflows. The clearest near-term moves are adding runtime-trace collection to automated repair, adding interaction playtests to GUI code generation, and screening API documentation drift with executable tests before filing a report.

## Runtime-trace collection inside automated program repair
Bug-fixing agents can add a debugging pass before patch generation. The useful change is simple: when a failing test and stack trace do not explain the fault, instrument the suspect function, run the reduced failing test, and feed the runtime state back into the repair loop. DebugRepair reports 295 correct fixes on Defects4J with DeepSeek-V3 and a 51.3% average gain over each backbone model’s vanilla setting across five additional models. The paper also includes two guardrails that matter for production use: it strips the failing test down to the minimal failure-triggering context, and it checks that inserted debug statements do not change the original logic, with an AST-based fallback when LLM-written instrumentation breaks compilation.

This is a concrete build for teams already running automated patch suggestions in CI or issue triage. A cheap first check is to take bugs that your current repair flow marks as unresolved after one or two attempts, then compare plain retrying against a trace-collection step that captures key variable values and branch states before asking for the next patch. The practical payoff is fewer patches that only suppress the visible failure and more patches that address the actual runtime condition behind it.

### Evidence
- [DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging](../Inbox/2026-04-21--debugrepair-enhancing-llm-based-automated-program-repair-via-self-directed-debugging.md): Reports runtime-trace-guided repair approach, safety checks for instrumentation, and benchmark gains including 295 correct fixes on Defects4J and 51.3% average improvement.

## Interaction playtesting for generated GUI code
GUI code generation needs an interaction test gate before merge. Compile success and unit tests miss event-order bugs, stale state, and logic errors that only appear during real use. PlayCoder puts a concrete metric around that gap with Play@k, which asks whether at least one generated candidate is actually playable end to end. In the reported Python results, Claude-Sonnet-4 drops from 18.6% Exec@3 to 9.9% Play@3, and GPT-5 drops from 17.5% Exec@3 to 6.9% Play@3. The paper’s PlayTester agent drives the UI through task-oriented playthroughs and checks for behavioral violations, then a repair loop uses those traces to revise the code.

The immediate workflow change is for teams generating small internal tools, dashboard front ends, or simple games with code models. Add a replayable interaction script and a playability check alongside compile and unit-test checks. Start with one user-critical path such as create, edit, save, or complete-level flow, and fail the run when the interface reaches a wrong state even if tests pass. This is a narrower build than full browser automation infrastructure, but it matches the failure mode the paper surfaces: executable GUI code that still breaks during use.

### Evidence
- [PlayCoder: Making LLM-Generated GUI Code Playable](../Inbox/2026-04-21--playcoder-making-llm-generated-gui-code-playable.md): Defines Play@k, describes automated GUI playtesting, and quantifies the drop from executable code to playable behavior for GPT-5 and Claude-Sonnet-4.

## Executable documentation checks for changed API methods
API documentation review can move from text diffing to executable checks. Cascade turns method documentation into tests, runs those tests against current code, then asks a second question before opening a report: would code regenerated from the same documentation pass the failing tests without breaking the ones that already pass? That two-step screen is aimed at the main adoption blocker for doc-code inconsistency tools, which is wasted review time from noisy alerts. In extra Java, C#, and Rust repositories, Cascade found 13 unknown inconsistencies and 10 were later fixed by developers.

A practical use case is release review for SDKs and internal libraries where method comments and examples drift as behavior changes. The build is concrete: generate tests from API docs for touched methods, require fail-on-current and pass-on-regenerated behavior before flagging a mismatch, and send only those cases to maintainers. A cheap validation pass is to run it on a recent set of doc-related commits and measure how many alerts correspond to changes that developers already corrected later. This gives documentation owners a narrower queue built around executable disagreement, not wording differences.

### Evidence
- [CASCADE: Detecting Inconsistencies between Code and Documentation with Automatic Test Generation](../Inbox/2026-04-21--cascade-detecting-inconsistencies-between-code-and-documentation-with-automatic-test-generation.md): Explains the fail-on-original, pass-on-regenerated execution check and reports 13 new inconsistencies found across repositories, with 10 later fixed.
