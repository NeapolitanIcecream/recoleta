---
source: hn
url: https://git-hunk.paulie.app/
published_at: '2026-03-03T23:32:04'
authors:
- shhac
topics:
- git-tooling
- code-automation
- developer-tools
- llm-agents
- ci-cd
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Show HN: Git-hunk – Stage hunks by hash, no "-p" required

## Summary
`git-hunk` is a tool that provides a non-interactive, scriptable interface for partial staging in Git, using stable hashes instead of the manual prompts of `git add -p`. It is mainly aimed at automation, CI/CD, and LLM/Agent workflows, making hunk selection and staging deterministic and programmable.

## Problem
- Git's built-in partial staging mainly relies on `git add -p`, which is an interactive prompt flow that automation programs, CI/CD, and LLM agents cannot use reliably.
- Interactive hunk selection requires a human to confirm step by step at the keyboard, blocking unattended software production workflows.
- Interactive workflows also suffer from unstable hunk ordering and insufficiently deterministic results, which is unfavorable for scripts, multi-step agent execution, and reproducible operations.

## Approach
- The core method is to generate a **stable content hash** for each diff hunk, and then use the hash to `list`, `diff`, and `add`, with no interactive prompts required.
- The hash mechanism is based on `SHA1(file_path + '\0' + stable_line + '\0' + diff_lines)`, using the line number from the “immutable side” as the anchor point to avoid one staged hunk affecting the identifiers of other hunks.
- The workflow is simplified into three steps: first enumerate all hunks and their hashes, then inspect the specific diff by hash, and finally stage by hash.
- The key design point is that after staging one hunk, the hashes of the remaining hunks stay unchanged, enabling reliable multi-step scripts and agent operations.
- The tool also provides machine-friendly interfaces such as `--porcelain`, `count`, and hash-prefix selection, making it easy to integrate with CI, scripts, and agents.

## Results
- The text **does not provide standard benchmark tests or experimental data** and does not report quantitative evaluation results such as accuracy, speed, or success rate.
- It explicitly claims that compared with `git add -p`, this method achieves a hunk staging workflow with **0 interactive prompts**: selection and staging are completed through the three commands `list`, `diff`, and `add`.
- The key paper-style claimed improvements include **deterministic across runs**, **machine-readable output**, and **fully non-interactive**, but no numerical comparison baseline is given.
- The strongest concrete mechanistic result given is that in the example, after staging `a3f7c21`, the hashes of the remaining hunks `b82e0f4` and `c91d3a8` remain unchanged, demonstrating identifier stability in multi-step staged operations.
- In terms of applicable scenarios, the author explicitly claims it can be used by **LLM agents, Scripts & CI, Humans**, but does not provide figures for task completion rate or productivity improvement.

## Link
- [https://git-hunk.paulie.app/](https://git-hunk.paulie.app/)
