---
source: hn
url: https://hjr265.me/blog/building-gittop-with-agentic-coding/
published_at: '2026-03-15T23:28:27'
authors:
- birdculture
topics:
- agentic-coding
- developer-tools
- git-analytics
- terminal-ui
- llm-assisted-programming
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# My First Agentic Coding Project: GitTop

## Summary
This article introduces a terminal monitoring tool for Git repositories called GitTop, and the author's experience of using "fully agentic coding" for the first time to complete the project in a single weekend. Its core value lies not in algorithmic innovation, but in demonstrating that an LLM agent can complete a medium-sized, well-structured software project with relatively little code written manually.

## Problem
- The problem to solve is: how to intuitively analyze the development activity patterns of a repository from Git commit timestamps, such as when during the day the author most often commits code.
- Existing one-off scripts or static HTML Git statistics tools can answer part of the question, but they lack an interactive terminal experience and explorability similar to `htop`.
- More broadly, the article also explores whether an LLM agent can take on most of the coding work from requirements to implementation, and what that means for software "authorship/ownership."

## Approach
- A TUI application called GitTop was built: developed in Go, using Bubble Tea for the terminal UI, Lip Gloss for styling, and go-git to read repository data directly without invoking git from the shell.
- The development method was "fully agentic coding with Claude Code": the author described requirements step by step and guided by feature, while the model generated nearly all of the implementation, ultimately finishing after **26 commits**.
- The query system is not a simple string search, but is designed as a DSL supporting structured syntax such as `author:"alice"`, `path:*.go`, and `branch:main and not path:vendor`, compiling queries into AST filter nodes, each implementing `Match(*CommitInfo) bool`.
- For visualization, it uses Unicode braille characters to implement high-resolution charts; in an **80-column terminal**, it can achieve an effective horizontal resolution of **160 columns**, while other bar charts use fractional-width block elements for finer-grained rendering.
- Branch filtering does not stuff a `branch` field into each commit object; instead, it first traverses commits reachable from matching branches and builds a hash set, then filters by commit-hash membership to keep the data model clean.

## Results
- The project was completed in a weekend experiment; the author says it took **26 commits**, ultimately producing about **4,800 lines of Go code** and a **7-page dashboard**-style TUI tool.
- GitTop successfully answered the author's original question: on the Toph project, commits are mainly concentrated between **10:00–16:00**, with a peak around **noon**.
- For chart rendering, the article gives specific implementation gains: a braille chart provides **80 terminal columns ≈ 160 columns of effective resolution**; bar charts can represent fractional lengths such as **3.5 units wide**, rather than only rounding to 3 or 4.
- It does not provide standard academic benchmarks, public datasets, or quantitative comparisons with other methods, so there is no SOTA metric in the traditional sense.
- The strongest concrete claim is that the LLM agent not only completed the implementation, but also made better engineering choices at several design points, such as AST query compilation, branch hash-set filtering, and higher-resolution Unicode chart rendering.

## Link
- [https://hjr265.me/blog/building-gittop-with-agentic-coding/](https://hjr265.me/blog/building-gittop-with-agentic-coding/)
