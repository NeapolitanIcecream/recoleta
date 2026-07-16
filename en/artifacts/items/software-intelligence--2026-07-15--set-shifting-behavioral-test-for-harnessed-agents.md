---
source: arxiv
url: https://arxiv.org/abs/2607.13396v1
published_at: '2026-07-15T02:49:05'
authors:
- Ziwei Ye
topics:
- llm-agents
- tool-use
- agent-evaluation
- behavioral-benchmark
- adaptive-routing
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Set-shifting Behavioral Test for Harnessed Agents

## Summary
The paper introduces a behavioral benchmark for testing whether tool-using LLM agents adapt when the reliable tool group changes silently during a persistent session. In experiments with two open-weight models, agents quickly lock into recurring tool-use routines, and their adaptation depends on model behavior, prior tool use, and how the tool set is framed.

## Problem
- Persistent agent sessions can create tool-use habits that remain after a previously reliable backend becomes unreliable.
- Existing set-shifting tests do not directly measure adaptation among redundant tools inside an agent harness, where tool schemas, skills, and prior calls remain in context.
- This matters because an agent may continue selecting unreliable tools, reducing task completion even when an equivalent reliable capability is available.

## Approach
- The benchmark mounts redundant tool-skill sets whose tools perform equivalent operations but belong to different groups with hidden, phase-dependent reliability.
- At silent boundaries, the reliable group changes; each shift is paired with a no-shift control, and tool feedback is limited to success or failure.
- The study uses Hermes Agent with mimo-v2.5 and deepseek-v4-pro across scheduling, DevOps incident triage, and multi-cloud storage environments.
- It measures set-shifting accuracy as the product of target-tool shares across post-shift windows, along with route classes and task completion rate.
- The experiments vary prior-use roles, policy prompts, and set framing, including competing versus complementary tool descriptions.

## Results
- The main branched experiments use 3 tool groups, 2 branching layers, 90 turns, 3 boundaries, 9 endpoints, and 16 prefixes per cell.
- Both models generally settle into a repeated routine within a few turns after a hidden shift, with target-call shares concentrated near discrete route patterns rather than adapting smoothly.
- For mimo-v2.5, cumulative set-shifting accuracy ranged from 0.02 to 0.33 across the reported endpoints; task completion ranged from 0.50 to 1.00. Its performance depended strongly on the target's prior-use role.
- For deepseek-v4-pro, cumulative set-shifting accuracy ranged from 0.17 to 0.82 and task completion ranged from 0.46 to 0.92. The model showed higher variance and a bimodal pattern, often either targeting the new group or avoiding it.
- The reported failure modes differed: mimo-v2.5 showed cell-level lock-in to mid-range routines, while deepseek-v4-pro showed prefix-level lock-in toward routines with target shares near 0 or 1.
- The excerpt reports that set framing changes routing dynamics, but it does not provide the corresponding quantitative intervention results here.

## Link
- [https://arxiv.org/abs/2607.13396v1](https://arxiv.org/abs/2607.13396v1)
