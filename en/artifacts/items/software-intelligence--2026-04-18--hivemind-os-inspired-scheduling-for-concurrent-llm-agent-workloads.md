---
source: arxiv
url: http://arxiv.org/abs/2604.17111v1
published_at: '2026-04-18T18:59:33'
authors:
- Justice Owusu Agyemang
- Jerry John Kponyo
- Obed Kwasi Somuah
- Elliot Amponsah
- Godfred Manu Addo Boakye
- Kwame Opuni-Boachie Obour Agyekum
topics:
- llm-agents
- multi-agent-systems
- api-scheduling
- coding-agents
- resource-management
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# HiveMind: OS-Inspired Scheduling for Concurrent LLM Agent Workloads

## Summary
HiveMind is a transparent HTTP proxy that schedules concurrent LLM agent traffic the way an operating system schedules competing processes. It targets a common failure case in coding-agent workloads: many agents share one rate-limited API, collide, and die even when total capacity is enough.

## Problem
- The paper addresses failures in parallel LLM coding agents that share one API key or endpoint. Without coordination, agents hit rate limits, connection caps, latency spikes, and transient server errors such as HTTP 502 and `ECONNRESET`.
- This matters because coding agents are long-running, stateful sessions. A mid-run API failure can waste 50k-500k tokens, lose context, and force a restart after file edits and tool calls have already happened.
- The motivating incident had 11 concurrent Claude Code agents on one Anthropic key; 3 died, a 27% failure rate, wasting about 135k tokens and about 15 minutes. The paper argues the issue was coordination, not total API capacity, since staggering starts by 5 seconds would have let all 11 finish.

## Approach
- HiveMind puts a local proxy between agents and the upstream model API, so existing agents need no code changes. Agents keep making normal HTTP requests, and the proxy decides when and how to forward them.
- The core mechanism is a set of five OS-style scheduling controls plus transparent retry: admission control limits in-flight requests, rate-limit tracking watches RPM/TPM and provider headers, AIMD backpressure lowers concurrency when latency or errors rise, token budgets cap runaway agents, and priority queues order work by priority and estimated cost.
- A circuit breaker fast-fails new requests when recent error rate is too high, then probes for recovery after a cooldown. Retryable errors such as 429, 502, 503, 529, and connection resets are retried with exponential backoff and jitter, hidden from the agent.
- The system auto-detects provider profiles for Anthropic, OpenAI, Azure OpenAI, Google AI, Ollama, and generic OpenAI-compatible endpoints. It also supports SSE streaming and extracts token counts from stream events or response bodies.
- An implementation detail the paper stresses is dynamic concurrency control through an `asyncio.Condition` instead of mutating a semaphore, which made resizing safe under load.

## Results
- Across 7 scenarios with 5-50 concurrent agents, uncoordinated execution had 72%-100% failure rates under contention, while HiveMind reduced failures to 0%-18% according to the abstract.
- In Table 5, direct vs HiveMind failure rates were: `micro-10` 100% -> 10%, `micro-20` 100% -> 10%, `micro-50` 100% -> 0%, `replay-11` 73% -> 18%, `stress` 100% -> 10%, and `lat.-spike` 100% -> 0%. `micro-5` was 0% in both modes because contention was absent.
- Wasted compute from dead agents fell by 48%-100% across the evaluated scenarios. Table 5 reports token waste reduction of 48% in `replay-11`, 94% in `micro-20`, and 100% in `micro-10`, `micro-50`, `stress`, and `lat.-spike`.
- The ablation study on `replay-11` says full HiveMind achieved 11 alive, 0 dead, 0.0% failure. Disabling retry dropped performance to 4 alive, 7 dead, 63.6% failure, making retry the most important single primitive. Admission-only gave 2 alive, 9 dead, 81.8% failure, so simple concurrency caps were not enough.
- Removing backpressure caused 1 death out of 11 agents, or 9.1% failure. Removing admission control or rate-limit tracking still gave 0.0% failure in that scenario, which the authors interpret as compensation from the remaining controls.
- Real-world validation against Ollama reports under 3 ms proxy overhead per request in the abstract. The provided excerpt does not include the full Table 7 values beyond that overhead claim.

## Link
- [http://arxiv.org/abs/2604.17111v1](http://arxiv.org/abs/2604.17111v1)
