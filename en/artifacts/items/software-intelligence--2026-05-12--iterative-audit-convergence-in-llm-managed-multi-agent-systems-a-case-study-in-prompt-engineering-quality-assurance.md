---
source: arxiv
url: https://arxiv.org/abs/2605.12280v1
published_at: '2026-05-12T15:39:04'
authors:
- Elias Calboreanu
topics:
- multi-agent-systems
- prompt-quality-assurance
- llm-auditing
- cross-document-validation
- agentic-software-engineering
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Iterative Audit Convergence in LLM-Managed Multi-Agent Systems: A Case Study in Prompt Engineering Quality Assurance

## Summary
The paper reports a single production case study where Claude sub-agents audited 8 prompt-specification files for AEGIS, a 7-lane LLM orchestration pipeline. Nine audit rounds found 51 prompt-specification consistency defects and ended with one clean full-scope pass.

## Problem
- Multi-agent LLM systems often keep behavior rules, data contracts, tool permissions, and integration logic in prompt files. A wrong field name, stale Jira rule, or missing lane reference can break agent handoffs or corrupt downstream work.
- Informal prompt review can miss cross-file defects because each file may look valid on its own while disagreeing with another file.
- The study asks which defect classes appeared only after later expanded-scope rounds and how convergence behaved across about 7150 lines of prompt specifications.

## Approach
- The audit covered 8 files: 7 lane-level `PROMPT.md` files with 6907 lines and a shared 245-line `TICKET_CONTRACT.md`.
- Claude sub-agents used a checklist adapted from Weinberg and Freedman-style walkthroughs. The checklist covered version consistency, cross-lane schemas, Jira permissions, labels, lane-count references, cadence, and internal contradictions.
- Early rounds reviewed one file at a time. Later rounds loaded producer and consumer files together, then all 8 files, so the agents could compare schemas and contracts across documents.
- Findings included exact line citations. Fixes were applied between rounds and checked with targeted greps where possible.
- The study stopped after round 9, when a full-scope audit across all 8 files and all 7 checklist dimensions returned 0 findings.

## Results
- The audit found 51 prompt-specification defects across about 7150 lines, or about 7.1 defects per thousand specification lines.
- Per-round defect counts were 15, 8, 12, 2, 8, 1, 4, 1, and 0. The curve rose again in rounds 3 and 5 after the audit scope expanded.
- The defect taxonomy was: stale Jira references 12 (23.5%), version drift 9 (17.6%), semantic misleading text 8 (15.7%), missing Lane 7 coverage 7 (13.7%), label or contract gaps 6 (11.8%), cross-lane schema mismatch 5 (9.8%), and formula or timing drift 4 (7.8%).
- Severity coding found 5 high-severity defects (9.8%), 32 medium-severity defects (62.7%), and 14 low-severity defects (27.5%). All high-severity defects were cross-lane schema mismatches.
- Cross-lane schema mismatches appeared only in rounds 4-8 after multi-file comparison became standard. The strongest example was a `priority_score` versus `fix_priority` field-name mismatch between Lane 3 and Lane 4, which could have caused silent runtime failure.
- The study did not run a single-pass full-scope control, used the same LLM family for authoring and auditing, and used one author for defect coding, so the results support a bounded case-study claim rather than a general performance estimate.

## Link
- [https://arxiv.org/abs/2605.12280v1](https://arxiv.org/abs/2605.12280v1)
