---
source: hn
url: https://github.com/anma-labs/anma
published_at: '2026-06-21T23:41:02'
authors:
- nxy
topics:
- code-intelligence
- ai-coding-agents
- software-architecture
- ci-governance
- human-ai-interaction
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Show HN: ANMA, boundary contracts for cheaper AI coding agents

## Summary
ANMA turns YAML module contracts into Claude Code guidance, edit-blocking hooks, and CI checks so cheaper coding agents stay inside declared architecture boundaries. The strongest evidence is on boundary violations in Python and TypeScript, with weaker but positive Go evidence.

## Problem
- Cheaper or faster coding agents can make edits that cross module boundaries, such as adding disallowed imports.
- Architecture docs can drift from CI rules, which gives agents and humans different instructions than the checks enforce.
- This matters for teams that use agents in bulk coding workflows and need module boundaries to hold without manual review of every edit.

## Approach
- Developers write plain YAML contracts for each module, including its public interface, allowed dependencies, owners, and source roots.
- `anma sync` generates `CLAUDE.md`, per-module guidance, `.claude/rules`, a `PreToolUse` hook, backend configs, CI workflow files, and optional `CODEOWNERS` entries.
- The generated guidance tells Claude Code which modules and imports are allowed before it edits code.
- The generated hook blocks a proposed boundary-breaking edit with exit code 2; the same boundary check can run in pre-commit and CI.
- Python supports module dependency and public interface enforcement; Go and TypeScript currently enforce module-to-module dependencies.

## Results
- In a controlled Python benchmark with Claude Haiku 4.5, the plain repo had boundary violations in 13 of 19 runs; ANMA had 0 violations in 20 runs, Fisher's exact p < 0.0001.
- The reported Python control violation rate was 68%, reduced to 0% with ANMA guidance.
- In a pre-registered TypeScript follow-up, the control condition had 18 violations in 20 runs; ANMA had 0 in 20 runs, Fisher's exact p < 0.00001.
- In Go, control had 10 violations in 30 runs and ANMA had 0 in 30 runs, p = 0.0004; the authors call this suggestive because the control rate was below the pre-registered 0.40 floor.
- Claude Opus 4.8 respected the Python boundary without ANMA in the reported study, so the claimed gain is strongest for cheaper agents and for CI governance rather than for improving a frontier model.
- The tool is described as about 800 lines, with no runtime component, one required dependency, and optional backends: tach for Python, go-arch-lint for Go, and dependency-cruiser for TypeScript.

## Link
- [https://github.com/anma-labs/anma](https://github.com/anma-labs/anma)
