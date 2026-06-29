---
source: arxiv
url: http://arxiv.org/abs/2604.13100v1
published_at: '2026-04-10T09:30:08'
authors:
- Yi Lin
- Lujin Zhao
- Yijie Shi
topics:
- repo-level-code-generation
- multi-agent-software-engineering
- code-intelligence
- symbolic-contracts
- parallel-agent-orchestration
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm

## Summary
Contract-Coding is a repo-level code generation method that turns vague user intent into a structured contract, then uses that contract to coordinate parallel code generation and verification. The paper claims this reduces cross-file confusion and improves success on multi-file software tasks.

## Problem
- Repo-level generation from vague intent often fails because agents generate files in sequence and must carry growing amounts of raw code context.
- Early design mistakes spread through later files, and long code histories push important architectural details out of the model's effective attention.
- This matters for autonomous software production because multi-file projects need consistent APIs, file structure, and cross-module behavior, not just locally valid code.

## Approach
- The system first converts a loose user request into a **Language Contract**, a structured artifact that records requirements, APIs, module-to-file mapping, type signatures, and state definitions.
- Code generation is then factorized as: infer the contract from intent, then generate each file conditioned on the contract rather than on previously generated raw code.
- A **Hierarchical Execution Graph (HEG)** schedules tasks from the contract so multiple module implementations can run in parallel when their interfaces are already defined.
- A verifier and contract auditor check whether generated code matches the contract, whether required files and symbols exist, and whether code changes require contract updates.
- The contract is built and revised through constrained add/update operations, with checks for issues such as invalid graph structure or inconsistent signatures.

## Results
- On the Greenfield-5 benchmark, the full method reports **100%** success on **Gomoku** in **136s**, **100%** on **Plane Battle** in **117s**, **87%** on **City Sim** in **257s**, **80%** on **Snake++** in **198s**, and **47%** on **Roguelike** in **232s**.
- Against academic multi-agent baselines on **Roguelike**, Contract-Coding reports **47%** success versus **30%** for **OpenHands**, **10%** for **MetaGPT**, **10%** for **ChatDev**, and **0%** for **FLOW**.
- Against commercial tools on **Roguelike**, it matches **Trae** at **47%**, beats **CodeBuddy** at **40%**, beats **Lingma** at **33%**, and trails **Gemini Studio** at **63%**.
- The HEG ablation shows the same success rate but lower speed: on **Roguelike**, **Ours w/o HEG** gets **47%** in **510s**, while **Ours (Full)** gets **47%** in **232s**; on **Snake++**, **78%** in **465s** improves to **80%** in **198s**.
- The paper claims a sub-linear context effect: for the **Roguelike** task, a repository of **8,857 tokens** is reduced to a contract of about **1,900 tokens**, or about **4.6x** compression.
- The abstract also claims **47% functional success** with **near-perfect structural integrity** on Greenfield-5, but the excerpt does not provide a direct numeric structural-integrity metric.

## Link
- [http://arxiv.org/abs/2604.13100v1](http://arxiv.org/abs/2604.13100v1)
