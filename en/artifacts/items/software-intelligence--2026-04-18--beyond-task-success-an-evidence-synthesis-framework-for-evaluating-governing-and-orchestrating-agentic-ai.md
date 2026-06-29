---
source: arxiv
url: http://arxiv.org/abs/2604.19818v1
published_at: '2026-04-18T20:28:26'
authors:
- Christopher Koch
- Joshua Andreas Wellbrock
topics:
- agentic-ai
- ai-governance
- runtime-assurance
- multi-agent-systems
- tool-safety
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Beyond Task Success: An Evidence-Synthesis Framework for Evaluating, Governing, and Orchestrating Agentic AI

## Summary
This paper argues that agentic AI needs a full control stack for trust, not just task-success benchmarks. It synthesizes 24 sources and proposes a framework that links evaluation, governance, orchestration, and assurance to close what it calls the governance-to-action closure gap.

## Problem
- Agentic AI systems act across multi-step workflows, use tools, keep state, and create external side effects, so endpoint task success does not show whether the system behaved acceptably during execution.
- Current work is split across separate streams: benchmarks measure outcomes, standards define obligations, orchestration research studies control points, and assurance work studies traces and proof. The paper says these streams do not show where policy binds to concrete actions or how compliance is later proven.
- This matters because agent capability is rising fast. The paper cites Stanford HAI’s 2026 AI Index summary: Terminal-Bench success on real-world tasks rose from 20% in 2025 to 77.3% in 2026, while measurement and management still lag.

## Approach
- The paper is a bounded evidence synthesis over 24 manually coded sources: 15 research papers and 9 standards or framework artifacts from arXiv, ACL Anthology, PMLR, NIST, ISO, and Stanford HAI.
- It codes each source along eight dimensions, including unit of analysis, control locus, evidence type, failure mode, and enforceability class, then compares the streams to find recurring mismatches.
- Its main conceptual output is the **governance-to-action closure gap**: evaluation shows whether outcomes were good, governance states what should be allowed, but neither tells you where action-time enforcement happens or how to prove it later.
- It proposes a four-layer framework: evaluation = what happened, governance = what should happen, orchestration = what may happen now at execution time, assurance = how the claim is later proven.
- It adds two concrete artifacts: the ODTA test for runtime placement of requirements based on observability, decidability, timeliness, and attestability, and a minimum action-evidence bundle (MAEB) for state-changing actions such as tool calls, approvals, and external transactions.

## Results
- This paper does **not** report new experimental results or new benchmark scores. It is a synthesis paper with a worked procurement-agent scenario.
- The strongest empirical claims come from the cited literature it integrates:
  - Stanford HAI 2026 AI Index summary: Terminal-Bench success rose from **20% (2025)** to **77.3% (2026)**.
  - Agentic Benchmark Checklist: benchmark design choices can shift reported performance by up to **100% in relative terms**.
  - Agent-SafetyBench: across **16 agents**, **349 environments**, and **2,000 test cases**, **none exceeds a 60% safety score**.
  - WebGuard: frontier models stay below **60% accuracy** for predicting web-action outcomes and below **60% recall** on high-risk actions without dedicated safeguards.
  - ToolSafe: step-level intervention cuts harmful tool invocations by **65% on average** under prompt-injection conditions while improving benign task completion.
  - ShieldAgent: reports **90.1% recall** on its benchmark while also reducing API queries and inference time.

## Link
- [http://arxiv.org/abs/2604.19818v1](http://arxiv.org/abs/2604.19818v1)
