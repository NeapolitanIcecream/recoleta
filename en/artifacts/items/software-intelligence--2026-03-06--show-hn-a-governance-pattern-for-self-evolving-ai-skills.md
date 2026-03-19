---
source: hn
url: https://github.com/191341025/Self-Evolving-Skill
published_at: '2026-03-06T23:50:56'
authors:
- tiansenxu
topics:
- self-evolving-agents
- skill-governance
- context-memory
- code-intelligence
- database-investigation
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Show HN: A governance pattern for self-evolving AI skills

## Summary
This work proposes a governance pattern for "self-evolving skills" for Claude Code Skills, enabling skills to accumulate reusable knowledge during real use while avoiding context bloat and knowledge degradation through strict gating. Its core contribution is bringing the self-evolving agent paradigm down to the **Skill/prompt injection layer**, achieving controllable evolution without modifying model parameters.

## Problem
- Traditional Skills are static: authors write them once and users invoke them repeatedly, but in scenarios such as database investigation, codebase analysis, and business integration, the structural relationships, query patterns, and business rules discovered by AI during use cannot be retained, causing every session to "start from zero."
- If knowledge is simply appended continuously, the knowledge base quickly turns into noise, reducing accuracy and wasting the limited context window.
- A mechanism is needed that is **able to grow but also able to converge**: it must reuse experience across sessions while avoiding unbounded growth, accumulating conflicts, and uncontrolled evolution. This is important for code intelligence, software operations, and complex business system analysis.

## Approach
- The core mechanism is a Skill-oriented **living knowledge base**: reusable knowledge is maintained by topic in `references/`, such as schema mappings, query templates, business rules, and investigation flows, rather than fixing the Skill documentation in place.
- The **Five-Gate Governance Protocol** determines whether knowledge should be written: it checks whether the knowledge has reuse value, whether it conflicts with existing knowledge, whether it is redundant, whether it is time-sensitive, and which file it should go into; the most common outcome is "do not write," thereby suppressing noise growth.
- `_index.md` is used for **routing-based on-demand loading**: first read a small routing table, then load only the 1–2 topic files relevant to the current task, instead of injecting all knowledge into context, thereby controlling context overhead.
- It adopts an evolutionary philosophy of **demand-driven, selective growth, and stability after maturity**: only real user interactions can trigger updates; once knowledge covers routine scenarios, it should tend toward stability rather than continuing spontaneous exploration.
- Evolution is explicitly limited to the **context layer**: it does not modify model weights, perform architecture search, or allow tools to evolve autonomously. It only records tool-use experience and business knowledge, so the worst-case consequence of an error is just "one incorrect reference entry," rather than an irreversible change in model behavior.

## Results
- The article claims to have conducted a complete evolution experiment on a **real database**, and provides **full evolution logs, Five-Gate decision records, quality audits, and round-by-round knowledge snapshots**, allowing comparison between any two rounds to observe the process of knowledge growth.
- It provides a runnable reference implementation, `examples/db-investigator/`, for **MySQL database investigation**, and includes Python utility scripts (such as `db_query.py`, `fetch_structure.py`, and `fetch_index.py`); the tool layer can also be replaced with MCP.
- It gives explicit context control thresholds: `_index.md` should be **< 40 lines**; when the knowledge base grows to **5 topic files, each 50–80 lines**, loading everything would waste about **250–400 lines** of context; therefore only relevant files are loaded via routing. A single topic file exceeding **~80 lines** should be split, and if the total number of topic files exceeds **8**, merging should be considered.
- It gives a maturity target: when domain knowledge covers **90%+** of routine scenarios, the Skill should converge to a stable state and grow again only when the business changes.
- It does not provide quantitative metrics on standard benchmark datasets, nor direct numerical comparisons with other methods in terms of accuracy, success rate, or cost; its strongest empirical claim is that this pattern has been validated in real business database scenarios and can achieve controllable knowledge evolution through gating and routing mechanisms.

## Link
- [https://github.com/191341025/Self-Evolving-Skill](https://github.com/191341025/Self-Evolving-Skill)
