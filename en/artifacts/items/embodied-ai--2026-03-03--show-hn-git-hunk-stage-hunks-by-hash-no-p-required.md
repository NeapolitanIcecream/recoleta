---
source: hn
url: https://git-hunk.paulie.app/
published_at: '2026-03-03T23:32:04'
authors:
- shhac
topics:
- git-tooling
- developer-tools
- automation
- ci-cd
- llm-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Git-hunk – Stage hunks by hash, no "-p" required

## Summary
This is a non-interactive Git hunk staging tool that replaces the interactive prompts of `git add -p` with stable hashes, allowing scripts, CI/CD, and LLM agents to deterministically select and stage code hunks.
Its core value is turning “partial staging that can only be done manually” into a workflow that is machine-readable, automatable, and reproducible.

## Problem
- It addresses the problem that Git’s built-in partial staging mainly relies on the interactive prompt of `git add -p`, so **automation systems, CI/CD, scripts, and LLM agents cannot use it reliably**.
- Interactive hunk selection also introduces problems such as **requiring a human to be present, blocking pipelines, and unstable hunk ordering**, which hurts reproducibility and programmatic control.
- This matters because modern development increasingly depends on agentic programming, automated commits, and pipelines; if code fragments cannot be staged precisely in a non-interactive way, many automated development scenarios get stuck.

## Approach
- The core method is simple: **first assign each diff hunk a stable content hash, then inspect and stage that hunk by hash**, rather than selecting hunks one by one through `y/n/q/...` prompts.
- The workflow is split into three non-interactive commands: `list` to enumerate hunks, `diff` to inspect by hash, and `add` to stage by hash; therefore the whole process can be scripted and orchestrated.
- The hashing mechanism uses `SHA1(file_path + '\0' + stable_line + '\0' + diff_lines)`, where `stable_line` comes from the line-number anchor on the “immutable side,” to avoid changing the identifiers of other hunks after staging one hunk.
- The key mechanism is that **the hashes of the remaining hunks stay unchanged during multi-step staging**; this makes stepwise automated selection a reliable process, instead of later identifiers being changed by earlier operations.
- The tool also provides interfaces such as `--porcelain`, `count`, `--exclusive`, and `--oneline`, strengthening machine-readability and determinism in scripting, CI, and human-machine collaboration scenarios.

## Results
- The article **does not provide standard paper-style quantitative experimental results**; there are no dataset, accuracy, throughput, latency, or baseline comparison numbers.
- The strongest concrete claim is that, compared with `git add -p`, the tool achieves **3 explicit steps** (Enumerate / Select / Stage) and **0 interactive prompts**, turning partial staging into a fully non-interactive workflow.
- It claims that hunk identifiers use **SHA-1** stable content hashes, and the example shows that after staging `a3f7c21`, the hashes of the remaining hunks such as `b82e0f4` and `c91d3a8` **remain unchanged**.
- Compared with the built-in interactive approach, the author explicitly claims advantages including **fully non-interactive, deterministic across runs, machine-readable output, stable content hashes**, and the intended beneficiaries include **LLM Agents, Scripts & CI, Humans**.
- The available commands include at least **4 categories**: `list`, `diff`, `add`, and `count`; it also supports hash prefixes and range views (such as `a3f7` and `a3f7:3-5`), reflecting an interface design oriented toward programmatic workflows.

## Link
- [https://git-hunk.paulie.app/](https://git-hunk.paulie.app/)
