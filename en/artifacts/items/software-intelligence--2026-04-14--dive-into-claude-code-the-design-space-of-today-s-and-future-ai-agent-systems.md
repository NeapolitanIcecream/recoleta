---
source: arxiv
url: http://arxiv.org/abs/2604.14228v1
published_at: '2026-04-14T17:59:37'
authors:
- Jiacheng Liu
- Xiaohan Zhao
- Xinyi Shang
- Zhiqiang Shen
topics:
- ai-agents
- coding-agents
- agent-architecture
- code-intelligence
- multi-agent-systems
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems

## Summary
This paper is a source-code analysis of Claude Code, framed as a study of how modern coding agents are built. It argues that the main agent logic is simple, while most of the system complexity sits in permissions, context management, extensibility, delegation, and persistence.

## Problem
- The paper studies how a production coding agent should handle autonomous actions such as running shell commands, editing files, and using external services without losing user control or safety.
- This matters because agentic coding tools face design problems that autocomplete tools do not: permission control, long-horizon reliability, context-window limits, extensibility, and multi-step execution.
- Anthropic documents Claude Code at the product level, but detailed architectural descriptions are limited, so the paper tries to recover those design choices from the public TypeScript source.

## Approach
- The authors analyze publicly available Claude Code source code (version v2.1.88) and map the system into major components and subsystem layers.
- The core mechanism is a simple loop: assemble context, call the model, read any tool-use requests, check permissions, run approved tools, feed results back, and repeat until the task ends.
- Around that loop, the paper identifies concrete surrounding systems: a permission system with 7 modes and an ML-based auto-mode classifier, a 5-layer context compaction pipeline, 4 extensibility mechanisms (MCP, plugins, skills, hooks), subagent delegation, and append-oriented session storage.
- The paper also compares Claude Code with OpenClaw across several design dimensions to show how deployment context changes architectural choices such as per-action checks versus perimeter access control.
- It organizes the analysis through 5 stated design values and 13 design principles derived from source inspection and cited Anthropic documents.

## Results
- The paper claims the main agent loop is structurally simple: a single `queryLoop()` while-loop handles model calls, tool dispatch, and repeated execution across CLI, SDK, and IDE-facing surfaces.
- It reports that only about **1.6%** of the codebase is AI decision logic and about **98.4%** is operational infrastructure, based on cited community analysis of the extracted source.
- It identifies **7** high-level system components, **5** architectural layers, **13** design principles, **7** permission modes, **5** context-compaction stages, **4** extensibility mechanisms, up to **54** built-in tools (**19** unconditional and **35** conditional), and **27** hook event types (**5** safety-related, **22** lifecycle/orchestration).
- For context limits, the paper states Claude Code is designed around model windows of **200K** tokens for older models and **1M** tokens for Claude 4.6 models, with five compaction stages applied before each model call.
- The paper cites Anthropic usage data rather than presenting its own benchmark: about **27%** of Claude Code-assisted tasks in an internal survey of **132** engineers and researchers were tasks users would not have attempted without the tool.
- The excerpt provides no new experimental benchmark table or head-to-head quantitative evaluation against baselines such as SWE-bench, OpenHands, or OpenClaw; its strongest claims are architectural and descriptive rather than benchmark-driven.

## Link
- [http://arxiv.org/abs/2604.14228v1](http://arxiv.org/abs/2604.14228v1)
