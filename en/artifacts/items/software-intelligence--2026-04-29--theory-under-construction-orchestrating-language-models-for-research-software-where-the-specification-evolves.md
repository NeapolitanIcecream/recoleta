---
source: arxiv
url: https://arxiv.org/abs/2604.27209v2
published_at: '2026-04-29T21:28:17'
authors:
- Halley Young
- "Nikolaj Bj\xF6rner"
topics:
- llm-orchestration
- code-intelligence
- research-software
- software-agents
- multi-agent-engineering
- automated-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves

## Summary
Comet-H is a controller for using language models to build research software when the theory, code, benchmarks, and paper all change during the run. The paper’s strongest claim is that explicit grounding and audit steps can keep long LM development runs from accumulating unsupported claims.

## Problem
- It targets research-software projects where the specification is still being formed, so the mathematical thesis, executable code, benchmark surface, and public claims can drift apart.
- This matters because an LM can copy its own unsupported claims into later prompts, papers, READMEs, code changes, and benchmark choices.
- The paper names two failure modes: hallucination accumulation and desynchronization between theory, code, evidence, claims, and the model’s stale view of the repository.

## Approach
- Comet-H treats a project workspace as six tracked parts: theory, repositories, public claims, evidence, utility hypothesis, and open obligations.
- A controller rereads the on-disk workspace, scores 17 prompt families against current deficits, and picks the next prompt with a hand-set linear score.
- New claims create follow-up obligations that decay over time, so recent unchecked work receives priority while old unresolved items fade.
- Any paper or README change forces a grounding step and then a skeptical audit, so public claims must point back to code, commands, benchmark outputs, or ledgers.
- Theory changes are allowed only through adjacent moves that preserve existing capability and improve at least one test, benchmark, or grounding record.

## Results
- The system produced 46 research-software repositories across about two dozen domains; the introduction also states 12+ domains.
- A standard run generates batches of 10 repositories, and Table 1 lists Comet-H runs as lasting 24–48 hours with mutable metrics and multi-session operation.
- The in-depth a3 repository reached F1 = 0.768 on a 90-case Python static-analysis benchmark, compared with the next-best baseline at F1 = 0.364.
- The authors report monotone ablation gains from adding theory/practice coupling layers, but the excerpt does not provide the ablation table values.
- The paper reports observations across about 400 commits of orchestrated development and says audit-and-contraction passes dominate the later phases of successful runs.

## Link
- [https://arxiv.org/abs/2604.27209v2](https://arxiv.org/abs/2604.27209v2)
