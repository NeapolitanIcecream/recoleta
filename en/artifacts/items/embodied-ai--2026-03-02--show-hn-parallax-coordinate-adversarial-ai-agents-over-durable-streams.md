---
source: hn
url: https://github.com/s2-streamstore/parallax
published_at: '2026-03-02T23:04:19'
authors:
- infiniteregrets
topics:
- multi-agent-systems
- durable-streams
- agent-orchestration
- adversarial-reasoning
- persistent-memory
relevance_score: 0.11
run_id: materialize-outputs
language_code: en
---

# Show HN: Parallax – Coordinate adversarial AI agents over durable streams

## Summary
Parallax is a proof-of-concept system for coordinating multiple isolated groups of AI agents to conduct "adversarial/parallel" research, built around S2 durable streams to persist state and support crash recovery. It aims to improve on the single-model, single-context research pattern by letting different agent cohorts reason independently before synthesizing their results.

## Problem
- Many existing AI research tools typically rely on **one model in one context** to role-play multiple perspectives, which can easily lead to perspective coupling, cross-contamination, and groupthink.
- Without **persistent, recoverable, dynamically orchestrated** communication infrastructure, multi-agent collaboration becomes fragile for long-running tasks, multi-user/multi-machine participation, and staged reasoning.
- This matters because more reliable multi-perspective analysis, auditing, forecasting, and decision support may be better suited than single-agent workflows for complex business, technical, and security problems.

## Approach
- The system first uses a **planner** to generate a strategy JSON that defines the topology (such as groups, rounds, hierarchical, custom), agent modes, and aggregation method.
- The **executor** then creates independent agent sessions for different groups on S2 streams; during the generation phase, groups are **isolated from one another and cannot read other groups' content**.
- An **autonomous moderator** reads the streams from all groups, decides whether to pivot, split into new streams, move to the next phase, or terminate, and then performs the final synthesis.
- All state is stored in **S2 durable streams**, so agent sessions are persistent, support "resume from tail," and allow any credentialed machine or human to join the same swarm.
- The system supports assigning different backends to different groups, such as using Claude for threat modeling and Codex for code review, and can constrain dynamic stream count, phase transition count, and total timeout through hyperparameters.

## Results
- The text **does not provide formal experiments, benchmark data, or quantitative metrics**, nor does it include paper-style evaluation results, so the magnitude of any performance improvement cannot be confirmed.
- The strongest specific claim given is that it can run research sessions with **3 independent groups × 2 agents per group**, for example `--groups 3 --agents-per-group 2 --max-messages 15`.
- It also shows a usage example with **5 independent panelists and 3 rounds of Delphi forecasting**, claiming the moderator feeds aggregated results back and lets estimates "converge," but **does not provide convergence error, variance, or baseline comparisons**.
- The system claims to support dynamically creating streams, with long-running workflows constrained by parameters such as `--max-dynamic-streams 4`, `--max-phase-transitions 3`, and `--timeout 15`.
- On reliability, it explicitly claims "**all state lives in S2 - crash and resume from the tail**," meaning state is persisted and crash recovery is supported, but **it provides no figures for recovery success rate, latency, or throughput**.
- The author explicitly describes it as a **"vibecoded proof of concept"**, so at present it is better understood as an engineering prototype and design signal rather than a rigorously validated research breakthrough.

## Link
- [https://github.com/s2-streamstore/parallax](https://github.com/s2-streamstore/parallax)
