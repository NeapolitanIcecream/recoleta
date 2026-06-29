---
kind: ideas
granularity: day
period_start: '2026-03-30T00:00:00'
period_end: '2026-03-31T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- code-repair
- context-compression
- agent-security
- program-analysis
- code-generation
tags:
- recoleta/ideas
- topic/code-repair
- topic/context-compression
- topic/agent-security
- topic/program-analysis
- topic/code-generation
language_code: en
pass_output_id: 5
pass_kind: trend_ideas
upstream_pass_output_id: 4
upstream_pass_kind: trend_synthesis
---

# LLM Coding Control Surfaces

## Summary
Concrete work is forming around three control points in LLM coding systems: shrinking repository context before repair, restoring taint and slicing across LLM call boundaries, and limiting what coding agents can touch on a developer machine. The evidence is strongest where the papers report measurable effects on repair accuracy, analysis quality, or operator workflow, and weaker where security tooling is still early but already specific enough to test in practice.

## Structured code-context compression before patch generation
A code-repair stack can add a dedicated context-compression stage between retrieval and patch generation now. The evidence points to a practical target: keep repository structure, score code at units such as files, functions, class headers, and statement blocks, and fit the final prompt to a fixed token budget. SWEzze reports about 6x compression, a 51.8% to 71.3% token cut, and a 5.0% to 9.2% lift on SWE-bench Verified across GPT-5.2, DeepSeek-V3.2, and Qwen3-Coder-Next. The training signal is also concrete enough to copy in a smaller internal experiment: derive minimal sufficient contexts from passing repairs, then train a reranker against those distilled segments.

The adoption case is straightforward for teams already running issue-resolution or repository-level repair flows and paying for large prompts. A cheap validation check is to replay a small solved set, compare uncompressed prompts against a structured compressor, and track three things together: patch pass rate, completion rate, and total prompt tokens. The caution from the adjacent repair study is useful here. Better localization helps, but it does not remove the downstream bottleneck. Systems given oracle file and line spans still stayed below 50% success in their native pipelines, and the best fixed added-context probe solved only six extra cases beyond the three-system Solved@10 union. That argues for treating context compression as an operational component that improves cost and focus, while keeping separate measurement on prompt construction and patch synthesis quality.

### Evidence
- [Compressing Code Context for LLM-based Issue Resolution](../Inbox/2026-03-30--compressing-code-context-for-llm-based-issue-resolution.md): Reports the structured compression method, 6x compression, large token cuts, and repair gains on SWE-bench Verified.
- [Beyond Localization: Recoverable Headroom and Residual Frontier in Repository-Level RAG-APR](../Inbox/2026-03-30--beyond-localization-recoverable-headroom-and-residual-frontier-in-repository-level-rag-apr.md): Shows that even with much stronger localization, repair success remains capped, so context handling and synthesis still need separate work.

## NL/PL boundary taint analysis for LLM callsites
Security review teams can add an NL/PL boundary pass to static analysis for code that builds prompts and consumes model outputs as SQL, JSON, shell commands, file paths, or generated code. The new paper gives a concrete analysis shape for that pass: label each placeholder at each LLM callsite by how much of its information survives into the output, use those labels to decide taint propagation across the call, and trim backward slices when placeholders are blocked. On the reported benchmark, that two-stage pipeline reached F1 0.923 for taint propagation and reduced slice size by a mean of 15% in files with non-propagating placeholders.

This fits a real operational problem. Existing taint analysis breaks at the model call, even though the risky pattern is often simple: untrusted input enters a prompt and the program later executes the returned artifact. The paper ties this to real prompt-injection and sandbox-escape cases. A practical first build is a checker for Python or TypeScript services that flags model outputs flowing into sinks and records the placeholder-to-output label alongside each finding. Teams can test it on a narrow slice of code first, such as LLM-backed SQL generation or agent tool calls, and compare alert count and review time against a boundary-blind taint rule.

### Evidence
- [Crossing the NL/PL Divide: Information Flow Analysis Across the NL/PL Boundary in LLM-Integrated Code](../Inbox/2026-03-30--crossing-the-nl-pl-divide-information-flow-analysis-across-the-nl-pl-boundary-in-llm-integrated-code.md): Defines the NL/PL boundary taxonomy and reports F1 0.923 for taint propagation plus 15% smaller backward slices.

## Least-privilege local sandbox for coding agents
Coding agents need a least-privilege wrapper that sits outside the model and outside the IDE. The immediate build is a local sandbox layer that starts from deny-by-default filesystem, network, and syscall permissions, then grants only the paths and operations a task actually needs. greywall is an example of that shape: a single-binary sandbox with built-in agent profiles, shell-aware command blocking, and a learning mode that traces file access and turns it into a reusable profile.

The workflow evidence from secure code review points in the same direction. Claude Code was useful when the human reviewer kept tasks narrow, verified claims, and corrected factual mistakes in the running context. That is a workable review pattern, but it still assumes the tool can be trusted with broad local access. A sandbox closes that gap for routine use on real developer machines. The first deployment target is teams using Claude Code, Cursor, Codex, or Aider on sensitive repositories without container isolation. A cheap check is to run one normal editing and test cycle under a learned profile, log blocked actions, and count how many blocks are harmless overreach versus real access the task needs.

### Evidence
- [The Blackwall Between Your AI Agent and Your Filesystem](../Inbox/2026-03-30--the-blackwall-between-your-ai-agent-and-your-filesystem.md): Describes a deny-by-default sandbox for coding agents with filesystem, network, and syscall controls plus learned least-privilege profiles.
- [Leveling Up Secure Code Reviews with Claude Code](../Inbox/2026-03-30--leveling-up-secure-code-reviews-with-claude-code.md): Shows a human-verified coding workflow where the model was useful but made at least one factual error, supporting containment around agent use.
