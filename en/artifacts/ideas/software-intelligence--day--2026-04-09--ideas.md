---
kind: ideas
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
run_id: ead7a913-d224-4dbe-aa9c-41958ae9d654
status: succeeded
topics:
- code-generation
- testing
- agent-infrastructure
- security-analysis
- bug-localization
tags:
- recoleta/ideas
- topic/code-generation
- topic/testing
- topic/agent-infrastructure
- topic/security-analysis
- topic/bug-localization
language_code: en
pass_output_id: 45
pass_kind: trend_ideas
upstream_pass_output_id: 44
upstream_pass_kind: trend_synthesis
---

# Verifiable code generation workflows

## Summary
The most usable changes in this set are a code-training loop built around executable tests, a test-reviewed workflow for small internal software, and runtime coverage inspection for coding-agent audits. Each one ties model output to something a team can check: pass/fail matrices, reviewed tests, or line-level read coverage.

## Label-free code model tuning with self-generated tests
A code-generation training loop that co-evolves tests with solutions is now concrete enough to try in internal fine-tuning and eval pipelines. ZeroCoder shows that execution feedback from self-generated code and self-generated tests can improve both sides without human-written tests or reference solutions. On Qwen2.5-Coder-7B-Instruct, the label-free setup improved code generation by 14.5%, and DyB^4 raised that to 21.6%; across three model families and six benchmarks, average gains reached 18.8% for code generation and 62.7% for test generation. The practical build is a small runner that samples multiple candidate programs and tests for each task, executes the full pass/fail matrix, drops low-information tasks, and tracks whether discriminative tests improve mutation scores before they are trusted as rewards. This fits teams that already have code tasks but do not have large stores of curated unit tests. A cheap check is to run it on one narrow internal task family and compare Pass@1 and mutation score against a standard execution-only baseline.

### Evidence
- [ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?](../Inbox/2026-04-09--zerocoder-can-llms-improve-code-generation-without-ground-truth-supervision.md): Quantified gains for label-free co-evolution of code and tests, plus the DyB^4 calibration detail and benchmark coverage.

## Developer review centered on generated tests for small internal tools
A test-first coding workflow where developers review generated tests and avoid direct edits to production code now has a small but usable prototype behind it. Test-Oriented Programming and the Onion tool use natural-language specifications to generate test files first, then generate implementation until those tests pass. In the reported BibTeX CLI task, all 10 runs succeeded across GPT-4o-mini and Gemini 2.5-Flash, and none required direct production-code edits. The operational value is narrow and clear: teams with repetitive internal tools or small greenfield services can move review effort into acceptance tests and class tests, where intent is easier to inspect than raw implementation. The limit is also clear. The evidence covers one small application and does not report benchmark-style cost or time metrics. A sensible trial is a single low-risk internal utility, with review time, retry count, and test-edit frequency logged from the start.

### Evidence
- [Test-Oriented Programming: rethinking coding for the GenAI era](../Inbox/2026-04-09--test-oriented-programming-rethinking-coding-for-the-genai-era.md): Describes the workflow, the Onion prototype, and the 10-run result with no direct production-code edits.

## Coverage dashboards for post-run review of coding-agent security audits
Post-run coverage maps for coding agents look ready for security audit teams that need to inspect what an agent actually examined before trusting the result. The coverage viewer described here reconstructs file and line reads from Claude Code and codex-cli session logs, links them to sub-tasks, and shows the result in a web UI. The reported OpenSSH audit runs show why this matters: GPT-5.4 settings covered about 8.3k to 17.7k median uniquely covered lines as reasoning budget increased, while Opus 4.6 runs reached about 30.3k to 31.8k median lines and touched many more files. A workflow change follows from that visibility. Teams can treat coverage gaps as a review artifact, compare prompt and model settings on explored attack surface, and schedule follow-up runs against untouched code regions. The cheap check is straightforward: instrument one recurring audit target, then see whether coverage-guided reruns find issues or hypotheses that the first pass missed.

### Evidence
- [Understanding Agents: Code Coverage for Coding Agents](../Inbox/2026-04-09--understanding-agents-code-coverage-for-coding-agents.md): Provides the tool design and the OpenSSH coverage differences across models and reasoning budgets.
