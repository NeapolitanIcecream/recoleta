---
source: arxiv
url: https://arxiv.org/abs/2604.27882v1
published_at: '2026-04-30T14:01:06'
authors:
- Giuseppe Arbore
- Andrea Sillano
- Luigi De Russis
topics:
- multi-agent-systems
- persona-agents
- agent-orchestration
- personalization
- human-ai-interaction
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Building Persona-Based Agents On Demand: Tailoring Multi-Agent Workflows to User Needs

## Summary
The paper proposes a runtime pipeline that creates persona-based agents for each user query, using the user profile, task needs, and session context. It targets personalized multi-agent workflows, but the excerpt reports no implementation, benchmark, or user study.

## Problem
- Multi-agent systems often use preset roles, communication paths, and execution order, which makes them hard to adapt to user expertise, task context, and preferred interaction style.
- This matters because users may need different explanations, task splits, and agent behaviors for the same high-level request.
- Fixed agent setups require prompt or orchestration changes when the user or task changes.

## Approach
- A central orchestrator receives an open-ended query and runs ProfileEncode to infer user traits, intent, domain familiarity, and communication preferences.
- TaskDecompose splits the query into subtasks and records dependencies so some tasks can run in parallel while others wait for required outputs.
- PersonaCraft creates a persona for each subtask, with role, domain skills, communication style, and capabilities drawn from the query and user profile.
- AgentFactory instantiates an LLM-backed agent from each persona, then the orchestrator assigns tasks, routes intermediate outputs, and aggregates the final answer.
- The system keeps generated personas and agents within a session and can add new ones on later queries.

## Results
- The excerpt gives 0 quantitative evaluation results: no accuracy, task-completion, latency, cost, or user-satisfaction numbers are reported.
- The claimed system flow has 4 stages: Query Analysis, Agent Generation and Instantiation, Agent Assigning and Execution, and Answers Aggregation and Displaying.
- The algorithm lists 18 steps for on-demand persona-based agent generation, starting with a user query and ending with an aggregated response.
- The strongest concrete claim is architectural: agent roles, styles, and coordination behavior are generated at runtime from the user profile, task plan, and session context.
- The paper claims the session model improves coherence across multiple queries by retaining prior agents and personas, but it provides no measured comparison against fixed-role multi-agent systems.

## Link
- [https://arxiv.org/abs/2604.27882v1](https://arxiv.org/abs/2604.27882v1)
