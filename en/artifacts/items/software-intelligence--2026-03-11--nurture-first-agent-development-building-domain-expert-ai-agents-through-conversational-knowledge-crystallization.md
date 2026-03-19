---
source: arxiv
url: http://arxiv.org/abs/2603.10808v1
published_at: '2026-03-11T14:14:53'
authors:
- Linghao Zhang
topics:
- agent-development
- human-ai-interaction
- memory-augmented-agents
- knowledge-crystallization
- domain-expert-agents
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Nurture-First Agent Development: Building Domain-Expert AI Agents Through Conversational Knowledge Crystallization

## Summary
This paper proposes a "nurture first, crystallize later" agent development paradigm: instead of writing expert knowledge into code or prompts all at once, the agent is gradually cultivated through real conversations, and fragmented experience is periodically distilled into structured knowledge. Its core contribution is merging "development" and "use" into a continuous co-evolution process, aimed at domain knowledge that is highly tacit, personalized, and constantly changing.

## Problem
- The paper addresses the problem of **how domain expert knowledge can be effectively encoded into AI agents**, especially tacit knowledge, contextual judgment, and personalized experience that are difficult to formalize in advance.
- Traditional **code-first** approaches rely on engineers to encode knowledge as rules/processes: reliable, but poor at capturing expert judgment and costly to update; **prompt-first** approaches rely on static prompts: easy to start with, but limited by context windows and prone to static obsolescence.
- This matters because the general capabilities of current foundation models are no longer the main bottleneck; what truly limits high-value industry agents is the **configuration gap** between "being able to do tasks" and "producing outputs that experts trust."

## Approach
- It proposes **Nurture-First Development (NFD)**: agents begin with minimal scaffolding and are continuously "nurtured" by domain experts through real work conversations, rather than being fully developed before deployment.
- The core mechanism is the **Knowledge Crystallization Cycle**: fragmented experience is first acquired through everyday conversations, then periodically refined into reusable structured knowledge assets.
- It designs a **Three-Layer Cognitive Architecture** that divides knowledge into three layers: **Constitutional** (long-term principles/identity), **Skill** (task-oriented skills and reference knowledge), and **Experiential** (rapidly growing interaction experience).
- It also introduces the **Dual-Workspace Pattern** and **Spiral Development Model**: one workspace is used for everyday "nurturing" interactions, while the other is used for "surgical" knowledge crystallization and organization, with overall improvement proceeding in an ongoing spiral cycle.
- The paper also provides formal definitions, including knowledge states, crystallization operations, efficiency metrics, and algorithmic descriptions, and illustrates the method's applicability with a U.S. stock research agent case study.

## Results
- The paper **does not provide quantitative experimental results on standard benchmark datasets**, nor does it report accuracy, F1, win rate, or numerical comparisons with existing frameworks.
- Its explicit qualitative claim is that, compared with code-first / prompt-first, NFD changes the development-deployment relationship from a "sequential" one to a "concurrently interwoven" one, and shifts the primary developer from engineers/prompt engineers to the **domain practitioner themself**.
- The non-experimental comparison in Table 1 claims that NFD can achieve **time to first value** in **minutes (scaffold)**, whereas code-first takes **weeks–months** and prompt-first takes **hours–days**.
- At the architectural level, the paper makes a concrete capacity claim: because the **Constitutional Layer** is loaded in every session, it usually occupies **10–15%** of available context, so it should store only principles and indexes, rather than long blocks of detailed knowledge.
- Regarding scalability, the paper argues that the upper bounds of the three paradigms differ: code-first is constrained by **engineering capacity**, prompt-first by the **context window**, and NFD primarily by **memory retrieval quality**.
- The empirical portion is only a **financial research agent (U.S. equity analysis) case illustration**, intended to show how the framework can be applied rather than to prove breakthrough numerical gains on public benchmarks.

## Link
- [http://arxiv.org/abs/2603.10808v1](http://arxiv.org/abs/2603.10808v1)
