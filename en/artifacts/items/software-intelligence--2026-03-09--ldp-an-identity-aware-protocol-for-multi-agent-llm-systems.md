---
source: arxiv
url: http://arxiv.org/abs/2603.08852v1
published_at: '2026-03-09T19:13:17'
authors:
- Sunil Prakash
topics:
- multi-agent-systems
- agent-protocols
- llm-routing
- payload-negotiation
- provenance-tracking
- trust-domains
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# LDP: An Identity-Aware Protocol for Multi-Agent LLM Systems

## Summary
LDP proposes an "identity-aware" communication protocol for multi-agent LLM systems, turning model identity, reasoning style, cost, provenance, and security boundaries directly into protocol primitives. The paper provides a JamJet plugin implementation, and preliminary experiments against A2A/random baselines suggest that its main value lies in efficiency, governance, and recoverability rather than improvements in overall quality.

## Problem
- Existing multi-agent protocols such as A2A and MCP mainly expose names, descriptions, and skills, but do not treat **model-level attributes** (model family, quality/latency/cost, reasoning style) as first-class citizens, making it harder for routing and delegation to make better decisions.
- This matters because in multi-agent systems, the real bottleneck is not just **whether a call can be made**, but also **which model to choose, what communication format to use, how to preserve context across turns, and how to track provenance and define trust boundaries**.
- If the protocol layer lacks these capabilities, it leads to higher latency/Token overhead, weaker governance, and more fragile security and failure-recovery mechanisms.

## Approach
- Proposes **LDP (LLM Delegate Protocol)**, with the core idea that agents should explicitly expose actionable identity information at the protocol layer—such as “how strong this model is, how expensive it is, what it is good at, and which trust domain it belongs to”—thereby enabling smarter delegation.
- Designs five key mechanisms: **rich delegate identity cards** (20+ field identity cards), **progressive payload modes** (multi-level payload modes with automatic negotiation/fallback), **governed sessions** (persistent multi-turn sessions), **structured provenance** (structured provenance tracking for confidence and verification status), and **trust domains** (protocol-level security boundaries).
- For communication, LDP allows progressive negotiation across different payload modes, from plain text to semantic frames; if a higher-level mode fails, it automatically falls back to a simpler mode, guaranteeing at least Mode 0 text availability.
- In implementation, the authors build LDP as an **external plugin adapter for the JamJet runtime**, requiring no modification to the host system; experiments use local Ollama models as delegates and Gemini 2.5 Flash as the LLM judge.

## Results
- **Routing quality (RQ1)**: In overall quality, LDP scores **6.80±3.62**, A2A **7.43±3.54**, and random **6.95±3.21** (each **n=30**); **LDP vs. A2A shows no significant difference** (**p=0.56**). That is, in this small pool of only 3 delegates, identity-aware routing **does not improve overall quality**.
- **Routing latency (RQ1)**: On easy tasks, LDP achieves **about 12× lower latency** by assigning tasks to lightweight models: **2.9s vs. 34.8s (A2A)**. This is one of the paper’s clearest empirical gains, suggesting that identity metadata improves **efficiency** more than final quality.
- **Payload efficiency (RQ2)**: Semantic Frame (Mode 1) reduces Tokens from **1215±751 to 765±510** relative to raw text, a **37% reduction**; relative to A2A JSON (**1128±804**), it reduces Tokens by **32%**. This Token reduction is **significant** (**p=0.031, d=-0.7**), and latency drops from **24.1s to 14.0s (-42%)**, while quality remains essentially unchanged (**5.70 vs. 5.54, p=0.96**).
- **Provenance information (RQ3)**: Decision quality with accurate provenance is close to that with no provenance: **7.65±1.21 vs. 7.85±1.84** (**p=0.47**, not significant); but **noisy provenance** lowers quality to **6.85±2.66**, and calibration drops from **9.33±0.72/9.13±0.83** to **7.87±2.90**. The conclusion is: **unverified confidence metadata may be worse than having no provenance information at all**.
- **Session efficiency (abstract)**: governed sessions can eliminate **39% token overhead** at **10 conversation rounds**, reducing context transmission cost relative to stateless repeated invocation.
- **Simulated protocol analysis (not real attack experiments)**: trust domains achieve **96% vs. 6%** in attack detection, and fallback chains achieve **100% vs. 35% completion** in failure recovery. The authors explicitly note that these reflect **protocol architectural properties** more than strict empirical results under real attack scenarios.

## Link
- [http://arxiv.org/abs/2603.08852v1](http://arxiv.org/abs/2603.08852v1)
