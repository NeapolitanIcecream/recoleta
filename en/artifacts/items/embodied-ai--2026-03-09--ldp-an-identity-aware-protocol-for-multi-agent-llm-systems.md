---
source: arxiv
url: http://arxiv.org/abs/2603.08852v1
published_at: '2026-03-09T19:13:17'
authors:
- Sunil Prakash
topics:
- multi-agent-llm
- agent-protocols
- llm-routing
- structured-communication
- provenance
- ai-governance
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# LDP: An Identity-Aware Protocol for Multi-Agent LLM Systems

## Summary
LDP proposes an “identity-aware” communication protocol for multi-agent LLM systems, making model identity, quality/cost signals, session governance, provenance, and trust domains first-class citizens at the protocol layer. The paper provides a JamJet plugin implementation and uses preliminary experiments against A2A/random baselines to show that this kind of AI-native protocol mainly brings efficiency and governance advantages, rather than consistently improving overall quality in a small delegate pool.

## Problem
- Existing multi-agent protocols such as A2A and MCP mainly expose surface-level information like names, descriptions, and skills, but do not treat **model identity, reasoning style, quality calibration, and cost characteristics** as protocol primitives, leaving routing and delegation decisions insufficiently informed.
- This matters because the effectiveness of multi-agent LLM systems depends not only on **who to assign a task to**, but also on **how to communicate, how to preserve context, how to track provenance, and how to enforce security boundaries**; lacking these increases latency, token cost, and governance risk.
- The authors aim to solve the following: how to design a more “AI-native” inter-agent protocol so that delegation is more efficient, more governable, and better able than existing protocols to support complex multi-round collaboration.

## Approach
- The core method is to propose **LDP (LLM Delegate Protocol)**: give each agent a richer “identity card” that explicitly carries information such as model family, quality hints, reasoning profile, context window, latency/cost hints, and trust domain, so that the router can choose agents more appropriately.
- It designs **progressive payload modes**: from plain text (Mode 0) to structured semantic frames (Mode 1), while supporting more advanced but not yet fully validated modes; the two communicating parties first negotiate the richest shared mode, and automatically fall back to a more conservative mode if needed.
- It introduces **governed sessions**, i.e., persistent multi-round sessions: capabilities, budget, privacy, and audit requirements are negotiated first, and then tasks are exchanged continuously within the session, avoiding repeated transmission of context in every round.
- It attaches **structured provenance** to each result (who generated it, confidence, whether it was verified, etc.), and applies signatures, replay protection, policy checks, and cross-domain restrictions at the protocol layer through **trust domains**.
- In implementation, LDP is integrated as a **JamJet external plugin adapter**; evaluation uses local Ollama models as agents and Gemini 2.5 Flash as the LLM judge, compared against A2A and random routing.

## Results
- **Routing quality (RQ1)**: In overall quality, LDP scores **6.80±3.62**, A2A **7.43±3.54**, and random **6.95±3.21** (n=30); **there is no significant difference between LDP and A2A** (p=0.56). The authors explicitly acknowledge that in a small pool of only **3 agents**, identity-aware routing **did not improve overall quality**.
- **Latency gains (RQ1)**: On easy tasks, LDP routes tasks to lightweight models, achieving latency of **2.9s vs 34.8s**, or about **12× faster**; this is one of the clearest empirical advantages in the paper.
- **Payload efficiency (RQ2)**: Semantic frames (Mode 1) reduce tokens from **1215±751** to **765±510**, a **37%** reduction relative to text; relative to A2A JSON (**1128±804**), the reduction is **32%**. This token decrease is **significant** (p=0.031, d=-0.7).
- **Payload latency/quality (RQ2)**: Semantic frames have latency of **14.0s** versus **24.1s** for text, making them **42%** faster; quality is **5.70±2.93 vs 5.54±4.05**, with **no observed quality loss** (p=0.96).
- **Provenance (RQ3)**: Decision quality with accurate provenance is close to that with no provenance (**7.65±1.21 vs 7.85±1.84**, p=0.47); but **noisy provenance** lowers quality to **6.85±2.66** and increases variance, indicating that **unverified confidence metadata may be worse than having no metadata at all**.
- **Sessions and simulation analysis**: The abstract claims that governed sessions eliminate **39% token overhead** over **10 conversation rounds**; in trust-domain simulations, attack detection is **96% vs 6%**, and in fallback-chain simulations, task completion is **100% vs 35%**. But the authors also emphasize that these security/recovery results mainly reflect **protocol design properties and simulation analysis**, not empirical validation in real attack scenarios.

## Link
- [http://arxiv.org/abs/2603.08852v1](http://arxiv.org/abs/2603.08852v1)
