---
source: hn
url: https://github.com/mikemasam/aef-spec
published_at: '2026-03-12T23:13:19'
authors:
- mikemasam
topics:
- agent-framework
- state-machine
- workflow-orchestration
- event-driven-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: AEF – Agents State Machine

## Summary
AEF (Agent Execution Framework) proposes using a **state machine** to organize the execution flow of AI agents, making explicit “what state it is currently in, what events it has received, and what actions it should take.” It is essentially a standardized framework for agent runtime behavior, emphasizing controllability, interpretability, and process design rather than a new model or learning algorithm.

## Problem
- The problem it addresses is that AI agent execution flows are often implicit and chaotic, lacking clear definitions of **states, events, actions, and transitions**, which makes behavior difficult to predict, debug, and maintain.
- This matters because when agents handle user input, timers, external APIs, exceptions, silent users, and similar situations, the absence of a unified execution framework can easily lead to infinite loops, lost context, or difficult error recovery.
- The article also implicitly targets multi-step tasks and context interruption issues: the agent needs to know “which step it is currently on, why it transitioned, and what it should do next.”

## Approach
- The core method is to design the agent as a **finite state machine**: each state defines what to do on entry (Entry), actions within the state (Actions), the current state indicator (Status), exit conditions and target state (Exit), and a default fallback state (Default).
- The agent receives various **events** (such as user input, timer triggers, and returned external data), and these events trigger transitions from one state to another, in a form like `$STATE_A --[event]--> $STATE_B`.
- The framework requires that each state clearly specify three things: which events can trigger leaving the current state, which conditions/guards must be satisfied, and which actions should be executed during the transition.
- It also emphasizes standardizing **entry actions** and **exit actions**, such as initializing variables, starting/stopping timers, sending an initial response, cleaning up resources, and logging state changes.
- In practice, it recommends first defining 3–5 main states and designing transition rules for edge cases such as failures, user silence, unexpected input, and interruption recovery; the article gives examples including a to-do assistant, multi-step task handling, and a context-aware assistant.

## Results
- What is provided is a **specification/framework description with examples**; the excerpt **does not report quantitative experimental results**, nor does it provide datasets, metrics, baselines, or percentage improvements.
- Its strongest concrete claim is that the Execution Framework can clearly answer three questions: **where the agent currently is (state)**, **what triggered the change (event)**, and **what happened during the transition (action)**.
- The article claims that this framework can be used to design agent workflows more clearly, including multi-step workflows, external API calls, memory management, and interruption handling, but it does not provide numerical validation.
- In terms of contribution type, it is more like an **engineering design specification/execution model** than a new algorithm achieving breakthroughs on agent benchmarks.

## Link
- [https://github.com/mikemasam/aef-spec](https://github.com/mikemasam/aef-spec)
