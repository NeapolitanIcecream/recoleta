---
source: hn
url: https://github.com/unloopedmido/contextlevy
published_at: '2026-05-24T23:31:25'
authors:
- nonlooped
topics:
- code-intelligence
- ai-agent-tooling
- pull-request-analysis
- repository-context
- developer-workflow
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Built a small PR guardrail for token bloat, worth maintaining?

## Summary
ContextLevy is a PR guardrail that estimates how much a change will bloat future AI coding-agent context. It targets generated files, logs, snapshots, lockfile churn, and similar repository noise before they become persistent agent overhead.

## Problem
- AI coding agents can become slower, costlier, and less useful when a repository gains high-volume or low-signal files.
- Pull requests can add generated clients, coverage output, build artifacts, vendored files, logs, snapshots, or agent instruction dumps without breaking application tests.
- Existing bundle-size checks do not measure repository context cost for AI-assisted development.

## Approach
- ContextLevy scans GitHub pull request diffs and estimates context weight from the changed files.
- It classifies risky files, including generated output, snapshots, logs, lockfile churn, vendored files, and agent instruction dumps.
- It posts a focused PR comment when configured thresholds are exceeded.
- It runs as a GitHub Action or npm CLI and uses pull request metadata plus diff patches available inside the workflow.
- It avoids external model analysis: no LLM calls, no code upload, no external analysis service, and no required telemetry.

## Results
- The excerpt reports no benchmark metrics, accuracy scores, latency numbers, or before-and-after cost reductions.
- It claims 2 delivery paths: a GitHub Action and an npm CLI.
- It claims 4 privacy and operations constraints: no LLM calls, no code upload, no external analysis service, and no telemetry required.
- GitHub Action setup uses 3 listed permissions: contents: read, pull-requests: write, and issues: write.
- Reported outputs are PR comments, JSON CLI output, configurable fail modes, threshold tuning, ignored paths, and pre-push hook usage.

## Link
- [https://github.com/unloopedmido/contextlevy](https://github.com/unloopedmido/contextlevy)
