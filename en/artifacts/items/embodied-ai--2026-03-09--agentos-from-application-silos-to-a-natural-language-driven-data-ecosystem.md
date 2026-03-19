---
source: arxiv
url: http://arxiv.org/abs/2603.08938v2
published_at: '2026-03-09T21:13:52'
authors:
- Rui Liu
- Tao Zhe
- Dongjie Wang
- Zijun Yao
- Kunpeng Liu
- Yanjie Fu
- Huan Liu
- Jian Pei
topics:
- agent-operating-system
- natural-language-interface
- multi-agent-orchestration
- intent-mining
- personal-knowledge-graph
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# AgentOS: From Application Silos to a Natural Language-Driven Data Ecosystem

## Summary
This paper proposes **AgentOS**: reimagining the traditional GUI/application-centered operating system as a "personal agent operating system" centered on a natural-language entry point and an agent kernel. The core argument is that the key challenge of such a system is fundamentally not traditional systems engineering, but an ongoing knowledge discovery and data mining problem.

## Problem
- The paper aims to solve the following problem: existing LLM agents still run as "ordinary applications" on traditional operating systems designed for GUIs/CLIs, leading to **missing semantics, fragmented context, and uncontrolled permission management**, making it difficult for them to safely and reliably act on behalf of users over the long term.
- This matters because local autonomous agents are spreading rapidly; if the underlying OS remains stuck in the "screen as interface" and application-silo model, agents can only rely on fragile visual scraping and mouse/keyboard simulation, making reliability and security major bottlenecks.
- The paper summarizes this risk as **Shadow AI**: the system cannot understand and constrain agent behavior semantically, so once high privileges are granted, problems such as malicious prompt injection, data leakage, and unintended operations are amplified.

## Approach
- The core method is to propose a new OS architecture: replacing the desktop and multi-application switching with a unified natural-language/voice entry point, **Single Port**, so that users primarily express goals in natural language rather than manually operating individual apps.
- The system core becomes the **Agent Kernel**: upward, it parses ambiguous human intent into structured tasks; downward, it decomposes tasks into subtasks and invokes multiple agents and underlying capabilities (files, network, hardware, APIs) to execute them.
- Traditional applications are replaced by composable **Skills-as-Modules**. Put simply, "software functionality" is broken into reusable micro-skills, and users can even define rules and automation workflows directly in natural language.
- To make the system truly usable, the paper reframes implementation as a KDD pipeline: using **personal knowledge graphs** for context and intent inference, **two-tower recommendation** for skill retrieval, and **sequential pattern mining** to discover common workflows from interaction traces and optimize them automatically.
- For security and reliability, the paper advocates adding a **Semantic Firewall** for semantics-based input inspection/data leakage prevention, combined with sandboxing and **state rollback** mechanisms to limit damage caused by hallucinations or erroneous actions.

## Results
- This article is primarily a **vision/architecture paper**, and in the provided content it **does not report experimental data, benchmark scores, or quantitative improvements**, so there are no verifiable SOTA numerical results.
- The most specific external observation given in the paper is that OpenClaw gained **100,000+ GitHub stars** within a few weeks, used as motivational evidence for the "explosion of local autonomous agents," rather than as an experimental result for AgentOS itself.
- The paper proposes that the evaluation dimensions for AgentOS differ from those of traditional OSes: shifting from **CPU load / memory faults / disk I/O** to metrics such as **Intent Alignment, task completion rate, tool invocation accuracy, hallucination rate, context drift**, but it does not provide measured values for these metrics.
- The claimed "breakthrough" is mainly conceptual: redefining the OS as a **real-time intent mining and knowledge discovery engine**, and systematically proposing a research agenda composed of PKG, recommender systems, sequential pattern mining, semantic firewalls, state rollback, and related components.

## Link
- [http://arxiv.org/abs/2603.08938v2](http://arxiv.org/abs/2603.08938v2)
