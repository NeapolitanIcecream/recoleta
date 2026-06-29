---
source: arxiv
url: https://arxiv.org/abs/2606.06923v1
published_at: '2026-06-05T05:38:51'
authors:
- M. Danish Lim
- I. Danial Bin Sharudin
- Wen Han Chen
- Cedric Lim
- Laura Wynter
topics:
- ai-agent-skills
- tool-use
- agent-orchestration
- retrieval-augmented-agents
- customer-service-agents
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Declarative Skills for AI Agents in Knowledge-Grounded Tool-Use Workflows

## Summary
The paper tests whether natural-language skill files are a better control layer than a coded state machine for tool-using customer-service agents. Its main claim is that skill files help when retrieval is good, while poor retrieval hurts every agent type.

## Problem
- Customer-service agents must combine conversation, policy lookup, identity checks, tool discovery, and ordered state-changing actions.
- In the $\tau$-Knowledge banking benchmark, agents work over 698 documents, about 195K tokens, 71 topics, 14 permanent tools, 51 discoverable tools, and 97 tasks.
- This matters because wrong retrieval or wrong tool order can cause failed tasks, missed user requests, or unauthorized writes.

## Approach
- The paper compares three agents on the same tools, user simulator, and tasks: an unscaffolded baseline, a DeclarativeAgent, and an ImperativeAgent.
- The DeclarativeAgent appends three Markdown skill files to the system prompt: banking procedures, customer interaction, and knowledge discovery.
- The ImperativeAgent uses a coded finite-state machine with phases for greeting, triage, verification, planning, execution, confirmation, completion, advisory, and escalation.
- The ImperativeAgent restricts allowed actions by phase, enforces a verification gate before writes, keeps a task queue, sorts tasks with simple dependency rules, and escalates after retry limits.
- The paper formalizes the agents as policy classes in a Dec-POMDP and tests them across five language models and two retrieval regimes.

## Results
- The excerpt does not provide the main pass^1 numbers for DeclarativeAgent or ImperativeAgent, so the claimed gains cannot be checked numerically from the supplied text.
- The paper claims that under high-quality retrieval, declarative skill files improve procedural-task accuracy and reduce orchestration errors compared with the unscaffolded baseline.
- The paper claims the imperative state machine does not reliably improve task success or compliance, and can be brittle despite deterministic gates.
- Retrieval quality is the strongest measured bottleneck in the reproduced $\tau$-Knowledge baseline: Claude-4.5-Opus high reasoning drops from 39.69% pass^1 with gold documents to 18.30% with text-emb-3-large, 19.59% with Qwen3-emb-8B, 17.78% with BM25, and 24.74% with terminal use.
- GPT-5.2 high reasoning drops from 32.73% pass^1 with gold documents to 23.45% with text-emb-3-large, 24.74% with Qwen3-emb-8B, 24.48% with BM25, and 25.52% with terminal use.
- The strongest non-gold reproduced baseline is GPT-5.2 high reasoning with terminal use at 25.52% pass^1; the strongest gold reproduced baseline is Claude-4.5-Opus high reasoning at 39.69% pass^1.

## Link
- [https://arxiv.org/abs/2606.06923v1](https://arxiv.org/abs/2606.06923v1)
