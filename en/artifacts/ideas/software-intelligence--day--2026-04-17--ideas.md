---
kind: ideas
granularity: day
period_start: '2026-04-17T00:00:00'
period_end: '2026-04-18T00:00:00'
run_id: 2c820f02-ea9f-4551-985d-436f1ebff98d
status: succeeded
topics:
- code-agents
- repository-reasoning
- requirement-alignment
- multimodal-retrieval
- formal-verification
tags:
- recoleta/ideas
- topic/code-agents
- topic/repository-reasoning
- topic/requirement-alignment
- topic/multimodal-retrieval
- topic/formal-verification
language_code: en
pass_output_id: 77
pass_kind: trend_ideas
upstream_pass_output_id: 76
upstream_pass_kind: trend_synthesis
---

# Intermediate Action Checks

## Summary
The clearest short-term builds are control layers that check understanding before an agent acts. The most concrete cases here are a structural repository locator for intent-only queries, a requirement-alignment gate around code generation, and a rule-enforcement wrapper for long coding sessions. Each one inserts a specific intermediate check with direct evidence of better localization, better task fit, or better rule adherence.

## Datalog-backed repository localization for name-free engineering requests
Repository agents need a structural code locator for requests that contain no useful names. LogicLoc is a concrete pattern for that layer: extract repository facts, let the model write Datalog over those facts, then gate the query with parser checks and a synthesize-check-refine loop before execution in Soufflé. The practical use case is issue triage and repo navigation when the request sounds like a property of the codebase, not a search string. The paper’s example query asks for non-`__init__` functions with more than 15 parameters and returns two exact matches in Astropy, which is the kind of answer a lexical retriever often misses. A cheap product test is simple: collect internal engineering questions that mention behavior, structure, or constraints but omit file and symbol names, then compare exact hit rate against your current repo search or agent retrieval stack.

### Evidence
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md): Summarizes the keyword-agnostic localization problem, LogicLoc architecture, and the concrete Astropy example with exact matches.
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md): Confirms the system translates natural-language queries into Datalog and executes them in a validated closed loop.

## Requirement checklist gating before and after code generation
Coding assistants can add a requirement-check step before code generation and another one after the first draft. REA-Coder gives a direct template: turn the prompt into a checklist of requirement questions, compare the model’s answers with reference answers, rewrite the requirement when gaps appear, generate code, then inspect failed outputs by masking key semantic spans in the requirement and asking the model to recover them from the code. This fits teams that already have tests but still see code that solves the wrong task. The reported gains are large enough to justify a narrow rollout on difficult prompt classes: average improvement over the best baseline reaches 30.25% on CodeContests-raw and 26.75% on CodeContests, and even the pre-generation alignment step alone improves first-pass code over zero-shot by 210.44% on APPS and 344.67% on xCodeEval. A practical first deployment is a pre-submit gate for coding agents working on tickets with long natural-language acceptance criteria.

### Evidence
- [Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation](../Inbox/2026-04-17--bridging-the-gap-between-user-intent-and-llm-a-requirement-alignment-approach-for-code-generation.md): Provides the full REA-Coder loop and benchmark gains across models and datasets, including pre-generation alignment gains.
- [Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation](../Inbox/2026-04-17--bridging-the-gap-between-user-intent-and-llm-a-requirement-alignment-approach-for-code-generation.md): Confirms the paper's claim that existing methods rarely verify whether the model actually understood the requirement.

## Step-level rule enforcement for AI coding sessions
Teams using `AGENTS.md` or similar rule files can move rule-following out of prompt memory and into an execution gate tied to plan steps. Zoro shows what that support layer looks like: attach rules to specific steps after planning, require proof for each applied rule during execution, and demand unit tests before advancing on testable rules. That addresses a common failure in long coding sessions, where the agent drifts away from architectural, workflow, or UI constraints and the developer has to keep repeating them. The reported result is a 57% increase in rule following across 36 sessions, and the system is designed to work with existing agents through a shared instruction file and evidence directory. The immediate build is a thin wrapper around your current coding agent that records which rule blocked progress, what proof was submitted, and which rules users keep editing after failures.

### Evidence
- [ZORO: Active Rules for Reliable Vibe Coding](../Inbox/2026-04-17--zoro-active-rules-for-reliable-vibe-coding.md): Describes the Enrich-Enforce-Evolve workflow and the 57% rule-following improvement across 36 sessions.
- [ZORO: Active Rules for Reliable Vibe Coding](../Inbox/2026-04-17--zoro-active-rules-for-reliable-vibe-coding.md): Shows the operational pain: agents ignore instructions over time and developers repeatedly reassert project rules.
