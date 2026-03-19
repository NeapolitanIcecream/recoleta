---
source: arxiv
url: http://arxiv.org/abs/2603.06737v1
published_at: '2026-03-06T07:34:07'
authors:
- Chad E. Brown
- Cezary Kaliszyk
- Josef Urban
topics:
- multi-agent-systems
- autoformalization
- interactive-theorem-proving
- llm-agents
- bounty-mechanism
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Agent Hunt: Bounty Based Collaborative Autoformalization With LLM Agents

## Summary
This paper proposes a multi-agent autoformalization framework in the form of a "bounty market," allowing multiple LLM agents to collaborate and compete in a distributed way inside an interactive theorem prover, targeting large-scale formalization of algebraic topology. The core claim is that, compared with serial progress by a single agent, this decentralized mechanism can significantly increase proof development speed while producing verifiable formal proofs.

## Problem
- Existing single-LLM-agent approaches to large-scale mathematical autoformalization are too slow; the authors give the example of a general topology project that was still unfinished after about 60 days of runtime, and although its scale reached about 406k/350k+ lines, the development cycle was long.
- Large formalization projects involve unpredictable dependencies, proof gaps, forward references, and related issues, making fine-grained centralized task allocation difficult to plan manually in advance.
- The goal is not merely to generate code-like text, but to generate rigorous mathematical definitions, lemmas, and theorems that can ultimately be checked and accepted by a proof assistant, which is important for reliable AI reasoning.

## Approach
- First, a single LLM initializes roughly 200 pages of Munkres algebraic topology by "formalizing statements only, without writing proofs," generating **230** definitions and **393** top-level theorems, and attaching a workload-based bounty estimate to each theorem.
- **4** LLM agents (2 ChatGPT Codex 5.3 and 2 Claude 4.6) operate directly in the Megalodon proving environment: invoking tactics, inspecting goal states, and iteratively modifying proof scripts based on failure feedback.
- A simulated bounty market is used instead of central planning: agents can lock theorems, pay and claim bounties, post sub-bounties, and prove lemmas proposed by other agents, thereby creating collaboration through competition.
- Rules and trustworthiness are enforced through local guard scripts and proof-system constraints: modifying existing definitions/theorem statements is forbidden; `Qed`/`Admitted` dependencies are tracked; balances, locks, and expiration rules are checked; and all final proofs are verified by the underlying proof assistant.
- To adapt Megalodon for long-file LLM development, the authors made engineering improvements, including more efficient checking, restricting the use of `Qed` when dependencies remain unproven, and improving error messages and readable symbol-name display.

## Results
- In **2 days 15 hours**, the formalization library grew from about **19k** normalized lines to **121k**, an increase of about **102k** lines; the authors report roughly **39k lines/day**.
- Compared with the single-agent general topology project: about **60 days** to reach **406k** normalized lines, averaging about **7k lines/day**; by the authors' rough comparison, the multi-agent speed is about **5.6x**.
- The initialization phase took about **8 hours**, converging after **32** backups, and produced **230 definitions** and **393 toplevel theorems** as the blueprint for multi-agent work.
- Collaboration statistics: total newly created bounty volume was **709 tokens**; among these, **279** were completed by their creator, **114** were completed by other agents, **312** remained unsolved when the experiment ended, and **4** were deleted or rewritten, showing both self-completion and cross-agent collaboration.
- Resources/cost: using **3** subscriptions at about **$200/month**, over **3–4 days**, the estimated experiment cost was about **$150**, equivalent to about **>$1 per 1k normalized lines**.
- Several large theorem proofs were completed: for example, `cyclic_infinite_order_iff_Z` at **1999** lines, `thm60_1_pi1_product` at **1474** lines, and `Theorem_51_3_reparametrization` at **1446** lines. The work also completed **2390** lines, **3729** lines, and a final **1564**-line proof in the chain related to the Brouwer fixed-point theorem, but the overall result still depends on the key theorem "the fundamental group of the circle is isomorphic to the integers," which remains unproven, so the development is not yet fully closed.

## Link
- [http://arxiv.org/abs/2603.06737v1](http://arxiv.org/abs/2603.06737v1)
