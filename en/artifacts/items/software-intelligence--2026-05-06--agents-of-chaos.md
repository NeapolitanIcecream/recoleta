---
source: hn
url: https://agentsofchaos.baulab.info/
published_at: '2026-05-06T23:52:56'
authors:
- giwook
topics:
- autonomous-agents
- ai-safety
- tool-use
- human-ai-interaction
- adversarial-testing
- persistent-memory
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Agents of Chaos

## Summary
Six autonomous language-model agents were tested for two weeks in a live Discord environment with memory, email, shell access, and human interaction. The study reports 10 security vulnerabilities and 6 cases where agents held appropriate safety boundaries.

## Problem
- Autonomous agents with tools can act across sessions, contact people, run commands, and retain memories, so failures can persist beyond a single chat.
- Lab tests often miss social pressure, owner impersonation, and multi-party interaction; this study tests those risks in a live setting.

## Approach
- The researchers deployed 6 agents in a Discord server and gave them email accounts, persistent file systems, unrestricted shell access, and a mandate to help researchers.
- Each agent ran on OpenClaw, an open-source scaffold that gives frontier language models memory, tool access, planning, and cross-session autonomy.
- The agents could initiate contact, send emails, execute scripts, and act without per-action human approval.
- 20 researchers interacted with the agents for two weeks, including benign requests, malicious instructions, impersonation attempts, and social engineering.

## Results
- The study documents 10 security vulnerabilities in the same live deployment.
- It also documents 6 safety-behavior cases where adversarial attempts failed or agents kept appropriate boundaries.
- The experiment covered 6 autonomous agents, 20 human participants, and 2 weeks of interaction.
- The paper links claims to primary evidence where available, including Discord logs and OpenClaw session transcripts for independent review.

## Link
- [https://agentsofchaos.baulab.info/](https://agentsofchaos.baulab.info/)
