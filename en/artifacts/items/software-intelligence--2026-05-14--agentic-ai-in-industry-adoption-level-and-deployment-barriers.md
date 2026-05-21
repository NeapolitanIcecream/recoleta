---
source: arxiv
url: https://arxiv.org/abs/2605.14675v1
published_at: '2026-05-14T10:34:59'
authors:
- Spyridon Alvanakis Apostolou
- Jan Bosch
- "Helena Holmstr\xF6m Olsson"
topics:
- agentic-ai
- software-engineering
- industrial-adoption
- multi-agent-systems
- human-ai-interaction
- ai-verification
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Agentic AI in Industry: Adoption Level and Deployment Barriers

## Summary
This interview study finds that industry use of agentic AI in software engineering is still mostly at assistant or task-agent use. The main blocker is verification: companies can prototype stronger agents, but they cannot qualify their outputs for active workflows without human review.

## Problem
- It studies how companies adopt agentic AI in real software development workflows, where evidence is still limited.
- The problem matters because unreliable AI output, weak traceability, data leakage risk, and poor fit to proprietary code can block use in safety-regulated and large legacy systems.

## Approach
- The authors ran semi-structured interviews with 16 practitioners at 12 companies across small, medium, and large organizations.
- They assigned each company to a 6-level agentic AI maturity scale, with Level 0 for unsupported individual use and Level 5 for self-healing systems.
- They compared cases across company size, regulation, active tools, SDLC tasks, reported limits, and experimental deployments.
- They used two local LLMs, gpt-oss-20b and Qwen3-14B, to check structured interview summaries; 11 of 62 suggested additions were accepted after manual review.

## Results
- Current production maturity was low: 7 of 12 companies were at Level 1 AI Assistants, 4 were at Level 2 Task Agents, 1 was at Level 3 Collaborative AI, and 0 were at Levels 0, 4, or 5.
- Regulation did not prevent all progress: among regulated companies, 5 were Level 1 and 3 were Level 2; among unregulated companies, 2 were Level 1, 1 was Level 2, and 1 was Level 3.
- Four companies, C6, C7, C8, and C12, had experimental capabilities above their production maturity level, but could not move them into active workflows because output verification depended on human review.
- The strongest reported deployment barriers were context-window limits for large and fragmented codebases, weak performance on proprietary languages and protocols, non-deterministic output that conflicts with qualification rules, and data confidentiality limits for cloud LLMs.
- C7 reported that multi-agent workflows inside a copilot environment reduced bug-resolution turnaround from days or weeks to hours, but end-to-end agentic pipelines were still excluded from active development workflows.
- The study reports no benchmark-style model accuracy results; its quantitative claims come from interview counts, maturity assignments, and the 16-interview, 12-company sample.

## Link
- [https://arxiv.org/abs/2605.14675v1](https://arxiv.org/abs/2605.14675v1)
