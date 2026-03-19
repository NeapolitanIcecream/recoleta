---
source: arxiv
url: http://arxiv.org/abs/2603.07670v1
published_at: '2026-03-08T15:08:01'
authors:
- Pengfei Du
topics:
- llm-agent-memory
- retrieval-augmented-agents
- agent-benchmarks
- reflective-memory
- hierarchical-memory
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers

## Summary
This is a survey paper on the “memory” mechanisms of autonomous LLM agents, systematically organizing the landscape of memory design, evaluation, and applications from 2022 to early 2026. Its core contribution is not to propose a single new model, but to provide a unified write-manage-read framework, mechanism taxonomy, and evaluation perspective.

## Problem
- The paper addresses the question: **How can LLM agents continuously remember, organize, and invoke past experience during long-term interactions that exceed a single context window**? Otherwise, agents will repeatedly make the same mistakes, redundantly explore, and fail to adapt in a personalized way.
- This matters because truly autonomous agents need to learn user preferences across sessions, retain task experience, and avoid repeatedly incurring costly failures; without memory, an LLM is more like a one-off text generator than an actor capable of sustained improvement.
- The paper also points out that memory is not simply database retrieval, but a problem of maintaining a “sufficient historical state” under constraints of compute, latency, storage, accuracy, and privacy.

## Approach
- The core method is to formalize agent memory as a minimal **write-manage-read loop**: the agent first reads from memory the content relevant to the current task, then decides on an action, and subsequently writes back new observations, results, and feedback while performing summarization, deduplication, prioritization, contradiction handling, or forgetting.
- The paper proposes a **three-dimensional taxonomy** to unify different memory systems: by temporal scope into working/episodic/semantic/procedural memory; by storage substrate into contextual text, vector databases, structured databases, and executable skill libraries; by control method into heuristics, LLM self-control, and reinforcement-learning-style learned control.
- It further summarizes five major mechanism families: **in-context compression**, **retrieval-augmented storage**, **reflective self-improvement**, **hierarchical virtual context**, and **policy-learned memory management**, and analyzes their respective costs, fragilities, and suitable scenarios.
- On the evaluation side, the paper summarizes the shift from static recall tests to **multi-turn, multi-session, decision-coupled agentic benchmarks**, and emphasizes that evaluation should not only consider “whether it can remember,” but also whether memory actually improves downstream task completion.

## Results
- This is a survey rather than a single experimental paper, so there is **no single new experimental metric**; its “results” are mainly the synthesis, comparison, and summarization of prior work.
- Representative evidence cited in the paper includes: after **Voyager** removes its skill library, the speed of progressing through tech-tree milestones drops by **15.3×**; with the skill library, it can obtain **3.3×** more unique items, indicating that procedural memory directly determines performance.
- In **MemoryArena (2026)**, when an active-memory agent is replaced with a long-context baseline, the completion rate on cross-session dependency tasks drops from **80%+** to about **45%**, showing that long context alone is insufficient to support long-term tasks.
- **Reflexion (2023)**, by storing verbalized self-reflection, reaches **91% pass@1** on **HumanEval**, compared with **GPT-4 baseline’s 80%**, showing that reflective memory can significantly improve performance on coding tasks.
- **ReAct (2022)** reports a **34% absolute gain** on **ALFWorld**; **RETRO (2022)** uses a **7.5B** parameter model with a **2-trillion-token** retrieval corpus and matches **175B Jurassic-1** on **10 of 16 benchmarks**.
- The paper’s strongest claim is that across multiple existing systems, **the performance gap created by “whether effective memory exists” is often larger than the gap created by changing the LLM backbone model itself**.

## Link
- [http://arxiv.org/abs/2603.07670v1](http://arxiv.org/abs/2603.07670v1)
