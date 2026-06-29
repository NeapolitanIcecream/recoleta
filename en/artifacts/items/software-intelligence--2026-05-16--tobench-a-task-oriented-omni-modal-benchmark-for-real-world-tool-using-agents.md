---
source: arxiv
url: https://arxiv.org/abs/2605.16909v1
published_at: '2026-05-16T09:49:25'
authors:
- Zhiqiang Liu
- Wenhui Dong
- Yilang Tan
- Yuwen Qu
- Haochen Yin
- Chenyang Si
topics:
- tool-using-agents
- multimodal-benchmark
- mcp-tools
- agent-evaluation
- closed-loop-verification
- computer-use-agents
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents

## Summary
TOBench is a benchmark and execution harness for agents that must use tools, handle multimodal inputs, inspect generated artifacts, and fix mistakes before final submission. The paper claims current models remain far below humans on these workflows.

## Problem
- Existing tool-use and multimodal benchmarks often test API calls, GUI use, perception, or final answers as separate skills.
- Real work tasks can require reading images, documents, audio, or video, editing files, using MCP tools, rendering outputs, and checking whether the result meets task rules.
- This matters because agents can appear competent on isolated tests while failing when tool execution, multimodal reasoning, and self-checking must work together.

## Approach
- TOBench contains 100 executable tasks across 2 task families: Customer Service with 67 tasks and Intelligent Creation with 33 tasks.
- The benchmark covers 20 subcategory slices and connects agents to 27 MCP servers with 324 tools.
- Each task gives the agent a user request, role, domain rules, input assets, available tools, workspace state, and a task-specific verifier.
- The core mechanism is closed-loop multimodal verification: the agent uses tools, looks at the artifact or tool output, decides whether it satisfies the task, and revises when needed.
- Evaluation uses task-specific grounded checkers that combine format checks, code checks, tool-log checks, live or time-sensitive tool checks, and VLM-based inspection.

## Results
- On all 100 tasks, the best reported model is Qwen3.5-Plus with 41.0% task success, compared with a 94.0% human benchmark.
- The best closed-source results are Claude-Opus-4.6 and Gemini-3-Pro at 32.0% average task success.
- Hard tasks remain mostly unsolved: the best score is 20.00% on Customer Service-Hard and 15.38% on Intelligent Creation-Hard.
- GPT-5 scores 26.80% average success, GPT-5.2 scores 22.00%, and GPT-4o scores 6.12%.
- Qwen3.5-Plus averages 25.0 tool calls, 559.1k tokens, and $0.17 per task, while Gemini-3.1-Pro averages 21.5 tool calls, 1506.6k tokens, and $3.03 per task.
- The paper reports common failure modes in tool calls, tool parameters, multimodal reasoning, and missing self-verification before stopping.

## Link
- [https://arxiv.org/abs/2605.16909v1](https://arxiv.org/abs/2605.16909v1)
