---
source: hn
url: https://github.com/ahmedbutt2015/spine
published_at: '2026-05-02T23:38:07'
authors:
- ahmedthefayyaz
topics:
- codebase-onboarding
- code-intelligence
- static-analysis
- claude-code
- repository-mapping
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Spine – verified codebase onboarding for Claude Code

## Summary
Spine is a CLI and Claude Code skill that builds a verified onboarding guide for an unfamiliar codebase. It uses static source relationships to create a small architecture map, reading order, and repo context file for later Claude sessions.

## Problem
- Developers and coding agents often lose time finding entry points, subsystems, and the files to read first in a new repository.
- Existing onboarding docs can be stale, broad, or based on guesses, which can mislead humans and Claude Code sessions.
- The tool matters because repo context affects code review, bug fixing, feature work, and agent prompting.

## Approach
- Spine detects likely entry points, then extracts a small “spine” from source relationships it can verify through static analysis.
- It creates a Mermaid architecture diagram only from proven edges; if Mermaid validation fails twice, the diagram is omitted.
- The `/map` path gives a deterministic map-only preview with no synthesis step and no `ONBOARDING.md`.
- The `/onboard` path writes a full guide with a verified map, reading order, mental model, subsystem summaries, gotchas, and estimated read time.
- With `--write-context-file`, it can refresh `.claude/REPO_CONTEXT.md` so later Claude Code sessions start with a compact repo snapshot.

## Results
- The excerpt reports no controlled evaluation, benchmark score, dataset result, or baseline comparison.
- A sample run detects `1` JavaScript library entry point, writes `ONBOARDING.md`, and covers `7` spine files and `4` subsystems.
- The sample cost estimate is about `$0.008` input plus `$0.010` output, or about `$0.018` total.
- The sample claims about `3.5` hours of manual exploration saved for about `$0.02` of LLM cost.
- Current verified spine coverage lists `6` language families: TypeScript/JavaScript, Python, Go, Rust, and PHP, with TypeScript and JavaScript grouped together.
- The launch benchmark recommendation is `axios`; follow-up demo repos named in the excerpt are `glow`, `poetry`, and `log`.

## Link
- [https://github.com/ahmedbutt2015/spine](https://github.com/ahmedbutt2015/spine)
