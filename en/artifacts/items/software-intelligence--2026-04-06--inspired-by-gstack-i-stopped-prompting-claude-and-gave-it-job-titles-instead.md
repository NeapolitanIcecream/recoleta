---
source: hn
url: https://github.com/tonone-ai/tonone
published_at: '2026-04-06T23:25:26'
authors:
- thisisfatih
topics:
- multi-agent-software-engineering
- code-intelligence
- automated-software-production
- developer-tooling
- agent-orchestration
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Inspired by gstack: I stopped prompting Claude and gave it job titles instead

## Summary
Tonone is an open-source plugin and agent pack that turns one coding session into a coordinated set of role-based AI specialists for engineering, product, design, research, security, and operations. Its main claim is better end-to-end work flow than using one general assistant per person and passing outputs around by hand.

## Problem
- Teams often use separate AI assistants for separate roles, then move outputs across people and tools manually. The project says this loses context at each handoff.
- A single general-purpose assistant does not keep stable domain ownership across product planning, coding, infrastructure, security, testing, and deployment.
- This matters for software production because planning, implementation, review, and release usually span many specialties, and fragmented context can slow work or reduce output quality.

## Approach
- Tonone defines 23 named specialists, each tied to a domain such as backend, infrastructure, security, observability, product, research, UX, analytics, testing, or marketing.
- It uses lead agents such as Apex for engineering and Helm for product to route work to the right specialists and combine their outputs into a single workflow.
- The system is delivered as Claude Code plugin commands and as markdown-based agent and skill files for Codex CLI. Skills live in `skills/<name>/SKILL.md`, and agents can be invoked by reading those workflow documents.
- The package supports parallel reconnaissance for existing codebases. In the `/apex-takeover` flow, agents inspect architecture, infrastructure, CI/CD, security, observability, backend, database, and frontend, then produce a system map, risk assessment, quick wins, and roadmap.
- Engineering tasks are scoped into S/M/L execution levels with token and cost estimates. One example gives ~30K tokens and ~$0.05 for a small auth task, ~120K tokens and ~$0.20 for a medium version, and ~250K tokens and ~$0.45 for a larger build-out.

## Results
- The excerpt gives no benchmark study, no controlled evaluation, and no measured quality metrics against other agent systems or prompting baselines.
- The concrete scale claim is 23 specialists and 125 skills covering engineering, product, design, research, analytics, marketing, mobile, firmware, ML, infrastructure, and security.
- The project claims setup in 2 install commands for Claude Code: `claude plugin marketplace add tonone-ai/tonone` and `claude plugin install tonone@tonone-ai`.
- The main quantitative example is task sizing for "Build user authentication for our SaaS": S uses Spine + Warden at ~30K tokens and ~$0.05, M uses Spine + Warden + Flux + Relay at ~120K tokens and ~$0.20, and L adds Vigil + Atlas at ~250K tokens and ~$0.45.
- It claims parallel takeover analysis across multiple specialists with a final report containing a system map, risk assessment, quick wins, and roadmap, but the excerpt does not provide accuracy, speed, or user study numbers.
- The package is MIT licensed and presented as usable through Claude Code v1.0+ and Codex CLI with agent and skill markdown files read directly by the tool.

## Link
- [https://github.com/tonone-ai/tonone](https://github.com/tonone-ai/tonone)
