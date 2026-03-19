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
- personal-knowledge-graph
- skill-recommendation
- semantic-security
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# AgentOS: From Application Silos to a Natural Language-Driven Data Ecosystem

## Summary
This paper proposes **AgentOS**, arguing that operating systems should be restructured from a GUI/application-centered model into a personal agent operating system centered on a natural language entry point and multi-agent coordination. The core claim is that the key problem for future OSes is no longer just systems engineering, but a data mining problem of continuously performing intent mining and knowledge discovery.

## Problem
- Existing local agents still run as ordinary applications on traditional operating systems, creating a mismatch with legacy architectures designed for GUIs/CLIs, which leads to context fragmentation, fragmented interaction, and brittle automation.
- The “Screen-as-Interface” model makes agents rely on visual scraping, clicking, and keystroke simulation, making them prone to failure when interfaces change and causing loss of underlying semantic information.
- Traditional application-level permission-based security models are difficult to use to constrain autonomous agents, creating risks such as “Shadow AI,” prompt injection, data leakage, and erroneous operations; this matters because agents are rapidly becoming a new mainstream layer of human-computer interaction.

## Approach
- Proposes **Single Port**: replacing the desktop, windows, icons, and other GUI primary paradigms with a unified text/voice natural language entry point, generating visual interfaces dynamically only when necessary.
- Designs an **Agent Kernel**: upward, it handles intent parsing, context maintenance, and multimodal understanding; downward, it decomposes user goals into subtasks and coordinates multiple agents to interact with the file system, network, and devices through MCP.
- Refactors traditional applications into **Skills-as-Modules**, allowing users to define composable skills directly in natural language, with the system orchestrating them on demand into workflows.
- Frames implementing AgentOS as a KDD pipeline: using a **Personal Knowledge Graph (PKG)** for contextual reasoning, **two-tower recommendation** for skill retrieval, **Sequential Pattern Mining (SPM)** for workflow optimization, and new evaluation methods to measure **Intent Alignment**.
- Adds **Semantic Firewall**, taint-aware memory, data loss prevention, and system-level snapshot rollback for security and fault tolerance, to control prompt injection, hallucinations, and erroneous execution with high privileges.

## Results
- This is a **vision/architecture paper**; in the excerpt, it **does not provide experimental results, benchmark scores, or quantitative performance improvements**, nor does it report numerical gains over baselines on specific datasets.
- The only clearly quantified adoption signal in the paper is that OpenClaw gained **100,000+ GitHub stars** within a few weeks, used as background evidence for the rise of local autonomous agents rather than as an experimental result for AgentOS itself.
- The paper’s main breakthrough claim is that the core objective of an OS should shift from **CPU/memory/disk I/O** to a metric system centered on achieving user intent, such as **Intent Alignment, task completion rate, and tool invocation accuracy**.
- The paper also claims that AgentOS can shift system evolution from static patch-based upgrades to continuous learning-style optimization relying on methods such as **SPM, recommender systems, PKG, and MIRA**, but it does not provide quantitative validation.

## Link
- [http://arxiv.org/abs/2603.08938v2](http://arxiv.org/abs/2603.08938v2)
