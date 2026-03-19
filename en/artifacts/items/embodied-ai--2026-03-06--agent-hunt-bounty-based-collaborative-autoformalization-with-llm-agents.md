---
source: arxiv
url: http://arxiv.org/abs/2603.06737v1
published_at: '2026-03-06T07:34:07'
authors:
- Chad E. Brown
- Cezary Kaliszyk
- Josef Urban
topics:
- autoformalization
- interactive-theorem-proving
- llm-agents
- multi-agent-collaboration
- bounty-mechanism
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Agent Hunt: Bounty Based Collaborative Autoformalization With LLM Agents

## Summary
This paper studies how to enable multiple large language model agents to collaboratively complete large-scale mathematical autoformalization in an interactive theorem proving environment using a “bounty market” model. The core contribution is a decentralized task-allocation mechanism that supports both competition and collaboration, significantly improving formalization speed and producing a set of algebraic topology proofs verified by a proof assistant.

## Problem
- Existing single-agent autoformalization progresses too slowly on large, textbook-scale projects; the authors note as an example that a general topology project ran for about **60 days** and was still unfinished, despite already exceeding **350k/406k lines**.
- Large formalization projects involve unpredictable dependencies, proof gaps, forward references, and similar issues, making **static centralized planning** difficult to decompose efficiently.
- A multi-agent collaboration mechanism is needed that can scale in parallel while still ensuring the final results are **strictly verified** by a proof assistant.

## Approach
- First, a single LLM was used to initialize about **200 pages** of the algebraic topology portion of Munkres by “formalizing statements only, without writing proofs,” yielding **230 definitions** and **393 top-level theorems**, with a difficulty/cost estimate attached to each theorem as the initial bounty task pool.
- **4 LLM agents** were used (two variants of ChatGPT Codex 5.3, Claude Opus 4.6, and Claude Sonnet 4.6), interacting directly in the Megalodon proving environment: invoking tactic, inspecting proof state, and iteratively revising proof scripts based on failure feedback.
- A **bounty market mechanism** was designed: agents can lock theorems, claim bounties, issue sub-bounties for sub-lemmas, and compete or collaborate with each other; modifying existing definitions/theorem statements is disallowed to prevent “bounty farming.”
- A local guard script was used to enforce rules for balances, locks, bounties, `Qed/Admitted`, and so on, and the Megalodon kernel and error messages were improved to increase efficiency and safety for long files and untrusted-agent scenarios.
- In addition to completing proofs, agents could propose new intermediate lemmas and a small number of new definitions to organize proof structure; all accepted proofs were ultimately checked by the underlying proof assistant.

## Results
- The formalization scale grew from about **19k normalized lines** to **121k** within **2 days 15 hours**; the 4 agents together achieved about **39k lines/day**, compared with a single-agent general topology project at about **406k lines / 60 days ≈ 7k lines/day**, for a speedup of about **5.6×** (rough comparison).
- The initial task pool contained **230 definitions** and **393 top-level theorems**; the total bounty amount was **45k simulated USD tokens**. During the experiment, the agents issued **709 tokens** in new sub-bounties, of which **279** were completed by the issuer, **114** by other agents, **312** remained unsolved at the end of the experiment, and **4** were removed or rewritten, showing both self-completion and cross-agent collaboration.
- In terms of resource cost, the authors used **3 $200/month** subscriptions for about **3–4 days**, estimating a total cost of about **$150**, which works out to **over $1 per 1k normalized lines**.
- The paper lists several completed large proofs, such as `cyclic_infinite_order_iff_Z` at **1999 lines**, `thm60_1_pi1_product` at **1474 lines**, `Theorem_51_3_reparametrization` at **1446 lines**, and `thm53_3_product_covering` at **1339 lines**.
- Regarding case-study results, the Brouwer fixed-point theorem was completed as a **1564-line** proof, but it depends on a key theorem that is **not yet proved**: “the fundamental group of the circle is isomorphic to the integers”; related upstream proofs also include “circle embedded in the plane is non-null-homotopic” at **2390 lines** and a vector-field property proof at **3729 lines**.
- Several very long proofs with unresolved dependencies also remain incomplete, such as `lemma59_1_open_cover_generates_pi1_core` at **6132 lines**, `lemma68_1_extension_condition_free_product` at **5546 lines**, and `lemma54_1_path_lifting` at **2431 lines**; this indicates that the system can already advance complex proofs, but is still hindered by the quality of key definitions and deep dependency chains.

## Link
- [http://arxiv.org/abs/2603.06737v1](http://arxiv.org/abs/2603.06737v1)
