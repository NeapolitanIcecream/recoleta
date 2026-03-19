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
- ai-agents
- execution-model
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Show HN: AEF – Agents State Machine

## Summary
AEF (Agent Execution Framework) proposes using a finite-state machine to organize the execution flow of an AI agent, making states, events, actions, and transitions explicit. It can be viewed as a lightweight specification for an "agent operating system." It is primarily a design and implementation framework rather than a research paper with experimental validation.

## Problem
- It addresses the lack of **clear execution control** for AI agents in scenarios involving multi-step interactions, external events, timeouts, interruptions, and failures.
- This matters because without explicit states and transitions, agents can easily end up with chaotic flows, be hard to debug, hard to recover, and behave unpredictably.
- For multi-agent or complex workflow systems, a unified way is needed to describe "what is happening now, why a switch occurs, and what happens next."

## Approach
- The core method is to model the agent as a **finite-state machine**: the agent is in a given state, receives an event, performs an action, and transitions to the next state.
- Each state explicitly defines `Entry / Actions / Status / Exit / Default`, corresponding respectively to initialization on entry, behavior within the state, the current state indicator, exit conditions, and the default fallback state.
- Transitions are expressed in the form `$STATE_A --[event]--> $STATE_B`, and it is recommended that each state define the events that can trigger exit, guard conditions, and actions during transition.
- The framework emphasizes designing for exceptions and edge cases, such as failures, user silence, unexpected input, external API calls, and interruption recovery.
- Through examples such as a to-do assistant, a multi-step task handler, and an assistant with contextual memory, the text shows how to build an agent workflow starting from 3–5 main states.

## Results
- The text **does not provide quantitative experimental results** and does not report datasets, accuracy, success rate, latency, or numerical comparisons with baseline methods.
- The strongest concrete claim is that the Execution Framework can clearly answer three questions: where the agent is (state), what triggered the movement (event), and what happened during the transition (action).
- The specification provides at least **5 state fields** (Entry, Actions, Status, Exit, Default) and **3 core runtime elements** (state, event, action/transition) for structuring agent behavior definitions.
- The text recommends starting practical design with **3–5 main states** and covering scenarios such as failure, silence, and abnormal input to improve maintainability and predictability.

## Link
- [https://github.com/mikemasam/aef-spec](https://github.com/mikemasam/aef-spec)
