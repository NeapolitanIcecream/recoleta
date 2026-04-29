---
source: hn
url: https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files
published_at: '2026-04-22T23:23:56'
authors:
- knes
topics:
- agents-md
- code-generation
- developer-documentation
- software-engineering-agents
- evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all

## Summary
This article reports an internal study of how `AGENTS.md` files change coding-agent performance on real software tasks. Good files improved output by an amount the authors compare to moving from Haiku to Opus, while bad files reduced quality below having no `AGENTS.md`.

## Problem
- Coding agents often read local documentation, but teams do not know which `AGENTS.md` patterns help task completion and which patterns send the agent into irrelevant docs, extra checks, and incomplete code.
- A single document can help one task and hurt another. In the same module, one file improved `best_practices` by 25% on a bug fix and reduced `completeness` by 30% on a feature task.
- This matters because `AGENTS.md` is one of the few documentation locations with near-guaranteed discovery by agent harnesses, so bad guidance can directly lower code quality and speed.

## Approach
- The authors used AuggieBench, an internal eval suite built from real landed PRs in a large monorepo. For each task, the agent was asked to reproduce the work, and its output was scored against the reviewed “golden PR.”
- They filtered to single-module or single-app PRs where an `AGENTS.md` could plausibly help, then ran each task twice: with and without the file.
- They traced which docs agents actually discovered during hundreds of sessions, including `AGENTS.md`, referenced docs, directory `README.md`, nested `README`s, and orphan docs.
- They compared document patterns such as concise main files, procedural workflows, decision tables, code examples, domain rules, and warning-heavy or architecture-heavy docs.

## Results
- Top-performing `AGENTS.md` files were about 100–150 lines plus a few focused references. In mid-size modules of about 100 core files, they produced 10–15% gains across metrics.
- A six-step workflow for adding a new integration reduced PRs with missing wiring files from 40% to 10%, increased `correctness` by 25%, and increased `completeness` by 20%.
- A decision table for choosing between similar patterns increased `best_practices` by 25% in the cited state-management example.
- Small real-code examples improved `code_reuse` by 20% when the file included templates such as `createSlice`, `createAsyncThunk`, and typed selector usage.
- Failure modes were large: architecture-heavy docs caused one task to load about 80K irrelevant tokens, read 12 docs, and lose 25% `completeness`; a file with 30+ warning-only rules made PRs take 2x as long and cut `completeness` by 20%.
- Discovery rates were uneven: `AGENTS.md` was auto-discovered in 100% of cases, referenced docs were read in 90%+ of sessions when needed, directory `README.md` in 80%+, nested `README`s in about 40%, and orphan `_docs/` content in under 10% of sessions.

## Link
- [https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files)
