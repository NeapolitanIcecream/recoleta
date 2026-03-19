---
source: hn
url: https://github.com/191341025/Self-Evolving-Skill
published_at: '2026-03-06T23:50:56'
authors:
- tiansenxu
topics:
- self-evolving-agents
- context-memory
- prompt-governance
- skill-design-pattern
- knowledge-base
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Show HN: A governance pattern for self-evolving AI skills

## Summary
This work proposes a “self-evolving skill” governance pattern for Claude Code Skills, enabling skills to gradually accumulate reusable knowledge through real-world use while avoiding context bloat and knowledge degradation through strict gating. Its core contribution is moving self-evolution down from the model/agent layer to the prompt injection and external knowledge base layer, achieving controllable evolution without modifying model weights.

## Problem
- Traditional Skills are static: the author writes them once, users invoke them repeatedly, but domain knowledge discovered across sessions is not retained, causing every session to effectively “start from zero.”
- In scenarios such as database troubleshooting, codebase analysis, and business system integration, AI continuously discovers stable and reusable knowledge; if it is not preserved, reasoning cost and context window are wasted.
- Directly stuffing all historical knowledge into the prompt creates noise, redundancy, and context bloat, and may also introduce accumulated errors, so a memory growth mechanism with governance constraints is needed.

## Approach
- The core mechanism is a **Five-Gate governance protocol**: only knowledge that is reusable, consistent with existing knowledge, non-redundant, tagged for freshness, and placed in the correct location is allowed to be written, and the common outcome is “do not write.”
- Knowledge is maintained as a **living knowledge base** under `references/`, rather than by changing model parameters; typical files include `_index.md`, `schema_map.md`, `query_patterns.md`, `business_rules.md`, and `investigation_flows.md`.
- It uses **route-based selective loading**: first read `_index.md`, then load only the 1–2 topic files relevant to the current task rather than injecting everything, thereby controlling context overhead and preventing the knowledge base from becoming heavier as it grows longer.
- The design emphasizes **demand-driven, selective growth, and convergence toward stability after maturation**: no autonomous exploration, no script self-modification, and no pursuit of permanent growth; instead, knowledge naturally converges before business changes occur.
- This pattern is decoupled from the tool layer: it can use Python scripts or be replaced with MCP; what truly matters is the governance protocol, knowledge organization, and selective injection mechanism.

## Results
- The text **does not provide standardized quantitative metrics** (such as accuracy, success rate, token savings percentage, or numerical comparisons with baselines); the author explicitly states that “KPI-style metrics” are unnecessary and relies mainly on qualitative maturity signals for evaluation.
- It provides clear **context control thresholds**: when the knowledge base grows to **5 topic files, each 50–80 lines**, loading everything would waste about **250–400 lines** of context; therefore `_index.md` is required to stay within **40 lines**, a single topic file should be split if it exceeds **~80 lines**, and opportunities for consolidation should be reviewed when the total number of topic files exceeds **8**.
- It claims a “complete evolution experiment” has already been conducted on a **real database**, and that **full evolution logs, Five-Gate decision records, quality audits, and round-by-round knowledge snapshots** were retained, allowing comparison of any two rounds to observe how knowledge grew, but the excerpt does not report a specific experimental set, round statistics, or performance numbers.
- The strongest concrete claim is that this pattern confines self-evolution to the **context layer**, so even if the knowledge base is wrong, the worst case is only “an incorrect reference fact,” rather than an **irreversible behavioral change** at the model layer, thus offering higher safety than parameter-level self-evolution.
- Another concrete claim is that when domain knowledge covers **90%+ of routine scenarios**, the skill should enter a “mature/stable” phase and resume growth only when the business changes (such as new tables, new rules, or new workflows); this is its practical principle for handling the stability–plasticity tradeoff, not a quantitatively validated result.

## Link
- [https://github.com/191341025/Self-Evolving-Skill](https://github.com/191341025/Self-Evolving-Skill)
