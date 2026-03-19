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
- llm-for-code
- ide-plugin
- library-migration
- python
- human-in-the-loop
- developer-tools
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# MigMate: A VS Code Extension for LLM-based Library Migration of Python Projects

## Summary
MigMate is an open-source VS Code plugin that embeds LLM-based Python library migration capabilities into the development environment and reduces the risk of automated migration through human-confirmed previews. The paper focuses on tool design and a preliminary usability evaluation, rather than proposing a fundamentally new underlying migration algorithm.

## Problem
- Python projects often need to migrate from one third-party library to another with similar functionality, but manual migration is time-consuming because developers must understand both the old and new library APIs and modify code across the entire codebase.
- Existing recommendation or API mapping tools usually only help with “finding replacement libraries” or “finding corresponding APIs,” while leaving much of the actual code modification work to developers.
- Pure command-line automation tools can disrupt the development workflow; and LLM-generated changes may also include irrelevant modifications, so an in-IDE human-in-the-loop mechanism for review and rejection is needed to build trust.

## Approach
- The core method is straightforward: MigMate calls its existing backend, MigrateLib, from within VS Code, lets the LLM automatically generate library migration changes, and then presents those changes as interactive diff previews for developers to approve item by item, file by file, or all at once before applying them.
- The plugin triggers migration from dependency files (such as `requirements.txt` and `pyproject.toml`), allows users to select the source and target libraries, and launches a MigrateLib subprocess in the background to perform the migration.
- The backend workflow includes: running tests before migration to establish a baseline; calling the LLM to generate migrated code; if post-migration test results differ, executing several post-processing repair steps; and running tests again to check whether correctness has been restored.
- The plugin provides two key interface types: a migration preview (Refactor Preview or Webview) for explicit confirmation of code changes; and a test results view for comparing pre- and post-migration tests and inspecting failure messages and logs.
- The design emphasis is not on completely replacing developers, but on combining automation with human oversight to reduce context switching and improve usability and controllability.

## Results
- The preliminary user study included **8** participants who completed the experiment (9 were originally recruited, and 1 dropped out), using a within-subject design to compare manual migration with plugin-assisted migration.
- On the **requests → httpx** task, average time decreased from **25:23** manually to **10:42** with plugin assistance; on the **tablib → pandas** task, it decreased from **27:51** to **10:48**.
- The paper claims that MigMate saves about **60%** of migration time on average; however, the study measured only time and usability, and **did not evaluate migration correctness**.
- In terms of usability, MigMate achieved an average **SUS = 80.9/100**, placing it around the **90th percentile** and corresponding to an **A-grade**.
- Telemetry shows that the most commonly used migration trigger was **Hover Trigger 62.5%**, followed by **Context Menu 33.3%**; the Command Palette was used only **once**.
- The paper also cites its prior work as background: GPT-4o achieved **94%** migration results that were “at least partially correct” and **57%** that were “fully correct” on a PyMigBench subset; the CLI tool MigrateLib made **32%** of migrations fully correct, and the remaining migrations required manual fixes for only an average of **14%** of migration-related changes. These numbers mainly demonstrate the backend’s foundational capability, rather than new experimental results for the MigMate plugin itself.

## Link
- [http://arxiv.org/abs/2603.01596v1](http://arxiv.org/abs/2603.01596v1)
