---
source: arxiv
url: https://arxiv.org/abs/2605.10787v1
published_at: '2026-05-11T16:20:51'
authors:
- Yuanyang Li
- Xue Yang
- Longyue Wang
- Weihua Luo
- Hongyang Chen
topics:
- llm-agents
- tool-use
- mcp
- software-automation
- agent-benchmarking
- stateful-sandboxes
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox

## Summary
ComplexMCP is an MCP-based benchmark for LLM agents that must use many dependent tools inside changing software sandboxes. The main finding is that strong commercial models still fail many real software-automation tasks: the best reported model reaches 55.31% success versus 93.61% for humans.

## Problem
- It tests the gap between simple API calling and commercial software automation, where tools share state, depend on earlier calls, and can fail during execution.
- The problem matters because agents that skip checks, choose the wrong prerequisite tool, or give up after an error can change the wrong software state or leave a task unfinished.
- Prior benchmarks often use isolated tools, fixed environments, AST matching, or small sandboxes, so they miss failures caused by state, dependencies, and noisy execution.

## Approach
- ComplexMCP uses the Model Context Protocol to expose over 300 tools: more than 150 interdependent tools across 7 stateful sandboxes plus more than 150 stateless APIs.
- The 7 stateful sandboxes are LightOS, LightTalk, LightShop, LightWeather, LightFlight, LightStock, and LightNews. They keep session state such as chat history, trade history, carts, permissions, and other nested data.
- A seed sets the initial environment data and execution-time perturbations such as API failures. The same seed gives repeatable runs while different seeds change entities, permissions, and failures.
- The benchmark has 47 manually curated tasks. Some gold trajectories require more than 30 unique tools and more than 60 total tool calls.
- Evaluation is rule-based: it compares the agent’s final nested environment state with the ground-truth state, reports completion rate and misbehaving rate, and counts a task as correct only when completion is 100% and misbehavior is 0%.

## Results
- In full-context ReAct evaluation over 47 tasks, Gemini-3-Flash has the highest model success rate at 55.31% ± 0.00, with 85.79% ± 0.50 completion rate and 4.39% ± 0.19 misbehaving rate.
- Human users reach 93.61% ± 1.74 success, 97.73% ± 1.18 completion rate, and 0.81% ± 0.27 misbehaving rate using the same MCP interface and evaluator.
- Other reported success rates include Gemini-3-Pro at 44.67% ± 1.74, GLM-4.7 at 42.55% ± 0.00, Claude-Opus-4 at 41.84% ± 2.01, Claude-Sonnet-4.5 at 39.71% ± 1.00, and Qwen-3-Max at 31.20% ± 1.00.
- GPT-5.1 reaches 19.14% ± 1.74 success, 24.63% ± 1.87 completion rate, and 1.42% ± 0.47 misbehaving rate; the authors report that it often fails to recover after token or tool errors.
- The full-context setting uses about 29,964 prompt tokens for tool descriptions. With an average of 11 tool-calling rounds, the repeated prompt volume is about 360,000 tokens per task before counting generation and tool feedback.
- The authors identify three failure modes: tool retrieval saturation as the action space grows, skipped environment checks caused by overconfident planning, and failure rationalization instead of recovery after errors.

## Link
- [https://arxiv.org/abs/2605.10787v1](https://arxiv.org/abs/2605.10787v1)
