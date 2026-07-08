---
source: arxiv
url: https://arxiv.org/abs/2607.05202v1
published_at: '2026-07-06T15:17:09'
authors:
- Xingze Gao
- Chuanrui Hu
- Hongda Chen
- Pengfei Yao
- Zhao Wang
- Yi Bai
- Zhengwei Wu
- Yunyun Han
- Xiaofeng Cong
- Jie Gui
- Yafeng Deng
- Teng Li
topics:
- agent-self-evolution
- llm-agents
- code-intelligence
- software-engineering
- benchmarking
- procedural-transfer
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# EvoAgentBench: Benchmarking Agent Self-Evolution via Ability Transfer

## Summary
EvoAgentBench is a benchmark for testing whether LLM agents can turn past task traces into reusable procedures for later tasks. It covers web research, algorithmic reasoning, software engineering, and knowledge work, with an Ability Graph that guarantees every test task has related training-side procedural support.

## Problem
- Existing agent benchmarks mostly test single-task success, so they do not show whether an agent reused a procedure learned from earlier work.
- Memory benchmarks focus on stored facts, retrieval, or personalization, while this paper targets reusable procedures such as search plans, debugging steps, and validation workflows.
- The gap matters for long-horizon agents because higher reliability depends on carrying useful procedures across tasks without memorizing answers or relying on near-duplicate examples.

## Approach
- The benchmark collects no-skill agent traces across four domains using three construction backbones: Kimi-K2.5, GLM-5.1, and DeepSeek-V3.2.
- It extracts raw Ability cards from traces. Each card records a trigger condition, reusable procedure, supporting evidence, applicability boundary, and role: Method, Guard, or Workflow.
- It canonicalizes Ability cards through embedding-based candidate blocking, three LLM adjudicators, and expert review, then keeps only operationally equivalent units.
- It builds domain-specific Ability Graphs where tasks are connected when they share an edge-eligible Ability.
- It creates a train/test split where every test task shares at least one verified Ability with a training task in the same Ability community.

## Results
- EvoAgentBench uses a 528 train / 267 test split across four domains: BrowseComp-Plus, SWE-Bench Verified, LiveCodeBench, and GDPVal.
- Construction starts from 2,605 source tasks, extracts 7,326 raw Ability cards from 2,516 tasks, canonicalizes them into 170 Ability units, and retains a 1,108-task Ability Graph; the final test split has 0 unsupported test tasks.
- The diagnostic Anchor Skill condition improves every reported scaffold-domain-backbone cell. Average accuracy rises from 37.5% to 45.0% on Qwen3.5-27B (+7.5), from 49.2% to 59.7% on Qwen3.5-397B (+10.5), and from 36.7% to 42.5% on Gemma-4-31B (+5.8).
- Automatic methods show mixed transfer. Average gains over Vanilla are Memento: -2.4, +1.5, -0.7; ReasoningBank: +3.6, +2.4, +0.4; GEPA: +1.2, +3.5, +5.7 across Qwen3.5-27B, Qwen3.5-397B, and Gemma-4-31B respectively.
- Negative transfer is large in some cells: Memento drops Qwen3.5-27B Nanobot SWE by 36.3 points, GEPA drops Qwen3.5-27B OpenClaw knowledge work by 12.3 points, and ReasoningBank drops Gemma-4-31B OpenClaw algorithmic reasoning by 10.9 points.
- The paper claims curated Ability content transfers across model families, while current automatic self-evolution methods fail to keep positive gains across all domains, scaffolds, and backbones.

## Link
- [https://arxiv.org/abs/2607.05202v1](https://arxiv.org/abs/2607.05202v1)
