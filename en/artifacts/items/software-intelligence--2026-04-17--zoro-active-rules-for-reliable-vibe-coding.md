---
source: arxiv
url: http://arxiv.org/abs/2604.15625v1
published_at: '2026-04-17T02:06:55'
authors:
- Jenny Ma
- Sitong Wang
- Joshua H. Kung
- Lydia B. Chilton
topics:
- code-intelligence
- human-ai-interaction
- software-foundation-model
- automated-software-production
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ZORO: Active Rules for Reliable Vibe Coding

## Summary
Zoro turns rules files such as `AGENTS.md` from passive text into active controls during AI-assisted coding. It ties rules to plan steps, blocks progress until required rules are proven, and lets users revise rules from concrete failures.

## Problem
- In vibe coding, rules files are common, but agents often stop following them as a session goes on because rules are only loaded as static context.
- Developers cannot easily see which rules were applied, whether they were followed, or how to improve weak or outdated rules.
- This matters because teams use these rules to enforce architecture, workflow, UI, and safety constraints; if the agent skips them, developers must manually inspect, correct, and repeat instructions.

## Approach
- Zoro adds an **Enrich-Enforce-Evolve** workflow on top of existing coding agents such as Codex, Claude Code, Cline, and Cursor.
- **Enrich:** after the agent creates an initial plan, Zoro matches rules to specific plan steps and can split or rewrite steps so the rules are attached where they matter.
- **Enforce:** during execution, the agent must call Zoro CLI commands to mark step progress and submit proof that each required rule was followed; for testable rules, it must also provide unit tests before moving on.
- **Evolve:** users review the rule evidence in the UI, add in-situ notes when a rule was applied poorly, and Zoro aggregates those notes to refine the ruleset with LLM help.
- The system is agent-agnostic through a `ZORO.md` instruction file and a shared `.zoro` directory that stores the enriched plan, rule metadata, evidence, and user notes.

## Results
- The paper reports a **57% increase in rule following** with Zoro compared with standard vibe coding.
- The technical evaluation covers **36 vibe coding sessions** and says Zoro improves rule adherence while **maintaining feature-completion ability** relative to a standard coding agent.
- The user study includes **12 participants** and reports a shift in how people control agents: users moved from prompt engineering toward rule engineering.
- The formative design work included **10 programmer interviews** plus observation of **3 programmers** in sessions lasting **2-3 hours** each.
- The excerpt does not provide a metric definition, dataset name, variance, or exact baseline score beyond the 57% relative improvement claim.

## Link
- [http://arxiv.org/abs/2604.15625v1](http://arxiv.org/abs/2604.15625v1)
