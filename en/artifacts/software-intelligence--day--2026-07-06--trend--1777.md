---
kind: trend
trend_doc_id: 1777
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
topics:
- coding agents
- software engineering
- agent evaluation
- open-source software
- agent security
run_id: materialize-outputs
aliases:
- recoleta-trend-1777
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/open-source-software
- topic/agent-security
language_code: en
pass_output_id: 308
pass_kind: trend_synthesis
---

# Coding agents are being measured as repository co-workers, not code generators

## Overview
The day’s strongest evidence treats coding agents as repository actors that train, act, and fail inside real workflows. KAT-Coder-V2.5, EvoAgentBench, and EdgeBench put weight on executable environments, long runs, and reusable procedures; GitHub studies add maintainer-facing costs.

## Findings

### Executable repository training and long-run evaluation
Repository-level coding agents need rebuildable projects, real tests, and long trajectories. KAT-Coder-V2.5 reports that AutoBuilder raised executable environment construction success from 16.5% to 57.2% and produced more than 100,000 verifiable environments across 12 languages. Its training pipeline also filters trajectories by exploration, localization, patch quality, verification, recovery, and honesty.

Long-run evaluation follows the same emphasis. EdgeBench measures agents over 134 real-world tasks, including 36 systems and software engineering tasks, with about 38,000 hours of interaction. It reports that 12-hour learning curves fit a log-sigmoid form with mean R² = 0.998. EvoAgentBench adds a procedure-transfer test: every test task shares at least one verified Ability with a training task, yet automatic memory methods still show mixed gains and some large negative-transfer cases.

### Open-source evidence exposes integration costs
The GitHub-facing studies add measurements that matter to maintainers. One study links 13,360 AI chat sessions to repository histories across 1,240 open-source repositories. Code Writing accounts for 34.7% of sessions, and the paper reports no broad deterioration in observable code-quality signals or pull-request merge rates after AI adoption. Survey responses still flag a social cost: developers see other people’s AI-generated code as harder to maintain than their own.

Concurrent agent pull requests create a clearer operational burden. In AIDev-pop, exact temporal overlap appears in 40.2% of repositories with agent-authored pull requests, covering 79.4% of agent PRs. Merge replay finds textual conflicts in 19.8% of same-agent pairs and 41.7% of cross-agent pairs. A related mutation-taxonomy paper shows that performance-labeled agent PRs are rare, under 1% of AIDev-pop, but their diff patterns vary by agent and optimization target.

### Agent internals and team design become measurable variables
Several papers treat agent behavior as something that can be probed or configured, not just scored at the end. Latent Programming Horizons collects 22,714 repair trajectories and 22.4 million hidden-state vectors. Linear probes decode current correctness and partial correctness above chance, with best AUC around 0.83–0.84 on Qwen3.6-35B-A3B. Future-label signals stay above chance for about 25 steps.

Team structure also gets measured. The pm4aa prototype mines GitHub event logs to derive project-specific roles and constraints, then generates a LangGraph application. On Commitizen, it assigns 589 users to 8 roles and builds a 5-agent proof of concept. A separate study of personality and emotion prompts finds that profile choice changes code-generation pass@1 by 7.1 to 11.3 percentage points across models, while fear and high-conscientiousness prompts increase revision activity and token use without consistent performance gains.

### Tool-connected agents need stricter data boundaries
Security evidence focuses on trust boundaries inside tool responses. The agent data injection paper shows that attackers can place delimiters, JSON-like structure, tags, or spoofed metadata inside untrusted content so a large language model reads it as trusted agent data. The attack applies to web agents through fake UI identifiers and to coding agents through spoofed GitHub issue comments or fake tool responses.

The reported success rates are high enough to affect deployment decisions. Probabilistic delimiter injection reaches 31.3%–43.3% attack success on JSON data across 6 models, and DOM-style data reaches 33.3%–100.0%. Against cited defenses, instruction injection reaches only 0.0%–0.7%, while agent data injection reaches up to 50.0%. The authors report arbitrary click attacks on Claude in Chrome, Antigravity, and Nanobrowser, plus remote code execution and supply-chain paths on Claude Code, Codex, and Gemini CLI.
