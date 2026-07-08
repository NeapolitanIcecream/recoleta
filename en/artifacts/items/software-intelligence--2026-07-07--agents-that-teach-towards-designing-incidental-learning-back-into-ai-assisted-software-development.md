---
source: arxiv
url: https://arxiv.org/abs/2607.06101v1
published_at: '2026-07-07T10:14:44'
authors:
- Rohit Mehra
- Samdyuti Suri
- Prithviraj K Tagadinamani
- Kapil Singi
- Vikrant Kaulgud
- Adam P. Burden
topics:
- ai-coding-agents
- software-engineering-education
- developer-tools
- human-ai-interaction
- multi-agent-systems
- knowledge-debt
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Agents That Teach: Towards Designing Incidental Learning Back into AI-Assisted Software Development

## Summary
The paper argues that AI coding agents can reduce developers' incidental learning and create Knowledge Debt when agents make code changes the developer cannot explain. It proposes SHIELD, a VSCode-based multi-agent prototype that turns an agent's reasoning trace into selective learning prompts and short lessons.

## Problem
- AI coding agents solve more coding work for developers, which can remove the code reading, debugging, and design reasoning that used to teach developers during normal work.
- The paper names the resulting gap Knowledge Debt: agent-made changes accumulate without matching developer understanding, which can hurt later debugging, adaptation, and maintenance.
- The motivation includes reported AI-code adoption of 42% of committed code today, projected to reach 65% by 2027, and a cited controlled study where AI-assisted developers scored 17% lower on a later comprehension test.

## Approach
- The paper proposes 6 design principles for adding incidental learning to developer-agent work: contextual, grounded, ambient, selective, adaptive, and closed-loop.
- SHIELD observes the coding agent's telemetry: code changes, rationale, alternatives considered, and confidence.
- A Teachability Triage Agent compares candidate concepts against a per-developer Concept Map and signals such as complexity, novelty, and transferability.
- A Probe Generator asks asynchronous questions in the IDE to check whether the developer already understands the concept.
- If a gap exists, a Microlearning Generator creates a short lesson tied to the actual code change, then a Knowledge Assessor checks comprehension and updates the Concept Map.

## Results
- The paper reports no empirical evaluation results, no user-study metrics, and no benchmark scores; it states that evaluation is future work.
- SHIELD is implemented as a VSCode extension using CrewAI, Azure backend services, Neo4j for the Concept Map, GPT-5.1 for agent roles, and Claude Code instrumentation.
- The prototype includes 5 named agent roles or components: Telemetry Observer Agent, Learning Orchestrator, Teachability Triage Agent, Probe Generator Agent, Microlearning Generator Agent, plus Knowledge Assessor Agent.
- The walkthrough shows 1 concrete task: a payment API webhook retry issue where Claude Code changes fixed retry logic to exponential backoff with jitter, and SHIELD turns that change into a probe, microlearning item, and comprehension check.
- The paper claims early stakeholder demonstrations produced positive feedback, but gives no counts, study design, or effect sizes.

## Link
- [https://arxiv.org/abs/2607.06101v1](https://arxiv.org/abs/2607.06101v1)
