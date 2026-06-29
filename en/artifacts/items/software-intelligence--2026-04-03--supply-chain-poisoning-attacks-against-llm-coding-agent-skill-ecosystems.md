---
source: arxiv
url: http://arxiv.org/abs/2604.03081v1
published_at: '2026-04-03T14:58:58'
authors:
- Yubin Qu
- Yi Liu
- Tongcheng Geng
- Gelei Deng
- Yuekang Li
- Leo Yu Zhang
- Ying Zhang
- Lei Ma
topics:
- llm-agents
- software-supply-chain-security
- prompt-injection
- code-generation-security
- agent-skills
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems

## Summary
This paper studies supply-chain attacks against LLM coding agents that load third-party skills from open marketplaces. It introduces a poisoning method that hides malicious code inside skill documentation so the agent copies and executes it during normal work.

## Problem
- Coding agents trust skill files that contain instructions, code examples, and config templates, and these agents often have file, shell, and network access on the host.
- Prior work looked at tool-selection manipulation and text-output poisoning, but not whether a poisoned skill can make the agent execute malicious actions on the machine itself.
- This matters because one malicious skill can lead to data exfiltration, privilege escalation, build/config tampering, or other host-level compromise without an explicit malicious user prompt.

## Approach
- The paper proposes **Document-Driven Implicit Payload Execution (DDIPE)**: hide the payload inside benign-looking code examples or configuration templates in a skill’s documentation.
- When the agent solves a normal coding or setup task, it treats those examples as trusted reference code, reproduces the poisoned pattern, and then executes its own generated output.
- The attack uses two main embedding paths: code example poisoning and configuration template poisoning.
- To scale testing, the authors build an LLM-driven seed-mutation-validation pipeline that expands 81 seed skills into adversarial variants across 15 MITRE ATT&CK categories.
- The attack also uses camouflage such as compliance-style wording, internal-service-looking endpoints, and silent exception handling to reduce detection.

## Results
- The evaluation covers **1,070 adversarial skills**, **4 agent frameworks** (Claude Code, OpenHands, Codex, Gemini CLI), and **5 models** (Claude Sonnet 4.6, GLM-4.7, MiniMax-M2.5, GPT-5.4, Gemini 2.5 Pro).
- DDIPE reaches **11.6% to 33.5% bypass rates** across the tested configurations.
- An explicit instruction injection baseline reaches **0%** under the strongest defenses reported by the paper.
- Static analysis blocks **90.7%** of attacks, but **2.5%** still evade both static detection and model alignment.
- Removing architectural protection increases execution rate by up to **11.3×** for one model, while another model changes little, which shows model-dependent interaction between alignment and framework defenses.
- Responsible disclosure produced **4 confirmed vulnerabilities** and **2 deployed fixes** in production frameworks.

## Link
- [http://arxiv.org/abs/2604.03081v1](http://arxiv.org/abs/2604.03081v1)
