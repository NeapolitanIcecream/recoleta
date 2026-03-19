---
source: arxiv
url: http://arxiv.org/abs/2603.01596v1
published_at: '2026-03-02T08:26:31'
authors:
- Matthias Kebede
- May Mahmoud
- Mohayeminul Islam
- Sarah Nadi
topics:
- llm-software-engineering
- library-migration
- vscode-extension
- developer-tools
- human-in-the-loop
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# MigMate: A VS Code Extension for LLM-based Library Migration of Python Projects

## Summary
MigMate is a plugin that embeds LLM-based Python library migration capabilities into VS Code, semi-automating what is otherwise a tedious third-party library replacement process. It emphasizes completing migrations with human confirmation in the loop, reducing workflow switching and increasing developers’ trust in AI-generated changes.

## Problem
- The paper addresses the problem that **third-party library migration in Python projects is time-consuming, tedious, and error-prone**; developers must not only understand the APIs of both the old and new libraries, but also make consistent changes across the entire codebase, resulting in high maintenance costs.
- Existing tools often only recommend replacement libraries or map APIs, **still leaving a large amount of code rewriting work to developers**; meanwhile, pure CLI tools interrupt normal development workflows inside the IDE.
- This matters because libraries can become outdated, unsuitable, or in need of replacement; if migration costs are too high, project maintenance, upgrades, and technology stack evolution will all be slowed down.

## Approach
- The core idea is simple: **package the authors’ existing LLM migration tool MigrateLib into the VS Code plugin MigMate**, so developers can initiate migrations directly from dependency files instead of leaving the IDE to use the command line.
- On the backend, MigrateLib first runs the original tests to establish a baseline, then has the LLM generate migrated code, and runs the tests again; if the test results are inconsistent, it performs several post-processing fixes before comparing test results to determine migration status.
- On the frontend, MigMate adds an **interactive preview and human confirmation mechanism**: developers can inspect and approve code changes one by one, file by file, or in batch, preventing the LLM from introducing unrelated edits.
- The plugin also provides a **test results view**, displaying pre- and post-migration test summaries, error messages, and logs directly in a Webview to help identify the causes of failures.
- The design also includes lazy-load activation, dependency-file hover/right-click triggers, Quick Pick selection of source and target libraries, configurable models and preview modes, and more, to minimize usage friction.

## Results
- The preliminary user study included **8 valid participants** (9 were originally recruited, 1 dropped out), comparing completion time for manual migration versus plugin-assisted migration.
- For the **requests → httpx** task, average completion time dropped from **25:23** (manual) to **10:42** (plugin).
- For the **tablib → pandas** task, average completion time dropped from **27:51** (manual) to **10:48** (plugin).
- The paper claims the plugin saves about **60%** of migration time on average.
- In terms of usability, MigMate achieved an average **SUS score of 80.9/100**, approximately in the **90th percentile**, corresponding to an **A-grade** usability rating.
- Telemetry data shows the most common trigger method was **Hover Trigger 62.5%**, followed by **Context Menu 33.3%**; however, the paper **does not report quantitative results on migration correctness**, and explicitly states that this user study did not measure correctness. In prior backend-related work, the authors cite that MigrateLib can achieve **32% fully correct migrations**, and in the remaining cases only **14% of migration-related edits** on average still need to be manually fixed by developers; in an earlier LLM benchmark, GPT-4o achieved **94% at least partially correct and 57% fully correct**.

## Link
- [http://arxiv.org/abs/2603.01596v1](http://arxiv.org/abs/2603.01596v1)
