---
source: hn
url: https://hjr265.me/blog/building-gittop-with-agentic-coding/
published_at: '2026-03-15T23:28:27'
authors:
- birdculture
topics:
- agentic-coding
- code-generation
- tui-application
- git-analytics
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# My First Agentic Coding Project: GitTop

## Summary
GitTop is a Git repository TUI dashboard rapidly built through fully agentic coding, which the author used to evaluate the capabilities and experience of using an LLM in real software implementation. The article’s core value is not an algorithmic breakthrough, but in showing how agentic programming can produce a usable, reasonably well-structured medium-sized tool within a single session, while raising the human-machine collaboration question of “authorship/ownership.”

## Problem
- The problem to solve is: how to present Git commit times and repository activity in an **interactive terminal interface** intuitively, instead of relying on one-off scripts or static HTML reports.
- The deeper question is: can **fully agentic coding** complete a real, non-toy software project with relatively little human-written code? This matters for automated software production and code intelligence.
- The article also raises a key human-computer collaboration question: when the human is responsible for goals, judgment, and iteration, while the agent handles the actual coding, does the developer still “own” the project?

## Approach
- The author used **Claude Code** for fully agentic development “one feature at a time”: the human provided requirements, direction, and feedback, while the agent wrote the implementation, ultimately producing GitTop.
- The tech stack is **Go + Bubble Tea + Lip Gloss + go-git**, and the target artifact is a Git repository TUI dashboard similar to htop, rather than shelling out to git commands.
- The filtering system uses a small **DSL** supporting structured queries such as `author:"alice"`, `path:*.go`, and `branch:main and not path:vendor`; the agent refactored the parsing logic into a **Participle**-based AST/node matching model, with each node implementing `Match(*CommitInfo) bool`.
- Chart rendering uses **Unicode braille** to achieve higher-resolution sparklines, and uses Unicode block elements in other bar charts to display fractional widths, improving terminal visualization precision.
- Branch filtering does not contaminate the main data model; instead, it precomputes a hash set of “commits reachable from matching branches,” then filters by commit hash membership, keeping the `CommitInfo` structure clean.

## Results
- The project was completed in **a single weekend** through **26 commits**, reaching a final size of about **4,800 lines of Go code** and producing a **7-page** terminal dashboard; this is the most direct productivity result in the article.
- GitTop successfully answered the author’s original analysis question: on the Toph project, commits are mostly concentrated between **10:00–16:00**, with a **clear peak around noon**.
- The terminal charts are claimed to achieve an effective **160-column resolution** in an **80-column terminal** via braille encoding (a 2×4 dot matrix per character), and to use fractional block elements to render bars such as **3.5 characters wide**, rather than only rounding to 3 or 4.
- The author emphasizes that several implementation details were **better engineering choices proactively proposed by the agent**, such as the Participle parser refactor, fractional-width bar charts, and the hash-set-based branch filtering architecture, but the article **does not provide standard benchmarks, control experiments, or systematic quantitative evaluation**.
- Therefore, the article’s strongest claim is not model-performance SOTA, but rather that with relatively little handwritten code, an agent can produce software that is “usable and not poorly structured” in the course of building a real project, while exposing new **human-AI authorship/ownership** experience questions.

## Link
- [https://hjr265.me/blog/building-gittop-with-agentic-coding/](https://hjr265.me/blog/building-gittop-with-agentic-coding/)
