---
source: arxiv
url: http://arxiv.org/abs/2603.08520v1
published_at: '2026-03-09T15:54:18'
authors:
- Yi Chen
- Yun Bian
- Haiquan Wang
- Shihao Li
- Zhe Cui
topics:
- llm-code-security
- iterative-refinement
- multi-agent
- cegis
- semantic-constraints
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# SCAFFOLD-CEGIS: Preventing Latent Security Degradation in LLM-Driven Iterative Code Refinement

## Summary
This paper studies an often-overlooked problem in LLM-driven iterative code optimization: code functionality may keep improving, while security quietly declines over multiple iterations. The authors propose SCAFFOLD-CEGIS, which uses explicit semantic constraints and multi-agent gated verification to prevent this "latent security degradation."

## Problem
- The paper addresses **latent security degradation during multi-round LLM code refinement**: even when each round appears to improve functionality, performance, or maintainability, security defenses may be gradually removed, weakened, or bypassed.
- This matters because real-world AI coding tools have shifted from one-shot generation to multi-turn interaction; if security constraints exist only as “soft requirements” in prompts, models may drift away from the original security goals due to specification drift.
- Existing SAST gating is not sufficient. The authors point out that it has blind spots for “structural degradation,” and may even create a false sense of security: under the protected baseline, the latent security degradation rate rises from **12.5%** to **20.8%**.

## Approach
- The core method is **SCAFFOLD-CEGIS**: inspired by the CEGIS paradigm, it converts security requirements that were previously implicit in prompts into **verifiable hard constraints** that are forcibly checked whenever code is modified.
- The framework uses collaboration among four agents: SecurityArchitectAgent identifies security-critical elements and generates “semantic anchors”; ImplementerAgent produces candidate code under these constraints; GatekeeperAgent performs four-layer gating; AssimilatorAgent extracts lessons from failure cases and feeds them back into later iterations.
- The most critical mechanism is **semantic anchoring**: it fixes validation functions, sanitization logic, authorization checks, API signatures, and security invariants in place, preventing the model from accidentally deleting them during refactoring.
- The four-layer gated verification includes: test correctness checks, safety monotonicity checks (disallowing increases in new SAST risks), diff budget control (limiting the size of a single change), and anchor integrity checks (ensuring critical defense logic remains present).
- The failure assimilation mechanism summarizes error patterns from rejected candidates into natural-language rules, helping later generations avoid repeating the same mistakes.

## Results
- In observational experiments with GPT-4o, **43.7%** of iteration chains had more vulnerabilities than the initial baseline after **10 rounds**, showing that the phenomenon of “iterative optimization actually harming security” is real.
- Even with explicit security-hardening prompts, degradation still exists: the paper reports a degradation rate of **28.6%** under that setting.
- The authors built an experimental setup containing **24** programming task samples, covering **6** types of security scenarios, **2** languages (Python/Java), **3** models, and **4** iterative strategies, for a total of **288** iteration chains and **2,880** iteration steps.
- The analysis of SAST gating shows that it cannot effectively suppress latent security degradation; instead, it increases the latent security degradation rate from **12.5%** to **20.8%**, indicating that purely rule-based static analysis cannot cover structural issues such as “removing defensive logic / weakening exception handling.”
- Compared with **6** existing defense methods, the full SCAFFOLD-CEGIS reduces the latent security degradation rate to **2.1%**.
- Under the authors’ experimental setup, the framework achieves a **100% safety monotonicity rate**, meaning that each iteration step is no less secure than the previous one.

## Link
- [http://arxiv.org/abs/2603.08520v1](http://arxiv.org/abs/2603.08520v1)
