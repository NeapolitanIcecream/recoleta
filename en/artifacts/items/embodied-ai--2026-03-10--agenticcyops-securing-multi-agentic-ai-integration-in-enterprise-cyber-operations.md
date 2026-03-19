---
source: arxiv
url: http://arxiv.org/abs/2603.09134v1
published_at: '2026-03-10T03:15:36'
authors:
- Shaswata Mitra
- Raj Patel
- Sudip Mittal
- Md Rayhanur Rahman
- Shahram Rahimi
topics:
- multi-agent-security
- llm-agents
- cyber-operations
- tool-orchestration
- memory-security
- mcp
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# AgenticCyOps: Securing Multi-Agentic AI Integration in Enterprise Cyber Operations

## Summary
This paper proposes AgenticCyOps, a security framework for multi-agent AI integration in enterprise cybersecurity operations. Its core argument is that most known attacks ultimately converge on two key integration surfaces: **tool orchestration** and **memory management**, and it designs layered defenses accordingly.

## Problem
- When multi-agent LLM systems are granted tool invocation, shared memory, and autonomous communication capabilities, they expose new attack surfaces not present in traditional deterministic pipelines.
- Existing research mostly focuses on prompt injection or single-point vulnerabilities, lacking a unified architectural security model suitable for enterprise deployment.
- This matters because in SOC/CyberOps scenarios, once an agent is manipulated, it may do more than simply “make mistakes” — it may help attackers evade detection; meanwhile, in practice, attackers can move laterally in under 30 minutes, while organizations take an average of 181 days to detect an intrusion and 60 days to contain it.

## Approach
- The paper first decomposes the attack surface of multi-agent systems into three layers: **component layer, coordination layer, and protocol layer**, and finds that most attacks converge on two primary trust boundaries: **tool orchestration** and **memory management**.
- Based on these two boundaries, it proposes five defensive principles: **authorized interfaces**, **capability scoping**, **verified execution**, **memory integrity & synchronization**, and **access-controlled data isolation**.
- On the tool side, in simple terms: first verify that what you are connecting to is legitimate, then reduce permissions to the minimum necessary, and finally validate every high-risk action before execution.
- On the memory side, in simple terms: filter and validate before writes, perform consistency/consensus checks during reads, and isolate memory across organizations or tasks to prevent contamination and unauthorized propagation.
- The paper applies this framework to an **MCP**-based SOC workflow, using **phase-scoped agents**, **consensus validation loops**, and **per-organization memory boundaries** to implement defense in depth.

## Results
- The paper claims that its design, validated through **coverage analysis, attack path tracing, and trust boundary assessment**, can cover attack vectors documented in the literature and provide at least two complementary layers of defense for each class of vector.
- Across 4 representative attack chains, the system can **intercept 3 within the first two steps**, meaning **75% (3/4)** of representative attack chains can be blocked early.
- Compared with a flat multi-agent architecture, the paper reports a **minimum 72% reduction in exploitable trust boundaries**.
- The paper also provides several background figures to illustrate the urgency of the setting: attackers can move laterally across networks in under **30 minutes**; SOCs take an average of **181 days** to detect intrusions and an additional **60 days** to contain them.
- This paper mainly offers an **architecture-level security framework and case-based evaluation**, rather than standard machine learning benchmark experiments; accordingly, its results focus on coverage, attack-path interruption, and trust-boundary reduction rather than model metrics like Accuracy or F1.

## Link
- [http://arxiv.org/abs/2603.09134v1](http://arxiv.org/abs/2603.09134v1)
