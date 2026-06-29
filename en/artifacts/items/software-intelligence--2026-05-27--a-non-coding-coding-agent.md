---
source: hn
url: https://zserge.com/posts/socreates/
published_at: '2026-05-27T23:41:26'
authors:
- croottree
topics:
- coding-agents
- code-review
- llm-tool-use
- agent-loop
- context-management
- human-ai-interaction
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# A non-coding coding agent

## Summary
Socreates is a small coding-agent prototype that reviews a workspace through tool calls while leaving all code edits to the developer. The article explains the agent loop, tool interface, prompt, context trimming, and session memory, with no benchmarked performance results.

## Problem
- Coding agents can write large amounts of code, add unsafe changes, and create maintenance work that the developer must debug.
- Developers may want LLM assistance for review, error checking, and design pressure without giving the model write access.
- Agent implementations also need context control, safe tool execution, and persistent session state to work across turns.

## Approach
- The agent runs a simple loop: add the user message, send system prompt plus history to an LLM, execute requested tool calls, feed tool results back, and stop when the model returns a final answer.
- It uses a model-agnostic LLM interface with chat messages, tool schemas, tool calls, and token usage, with adapters for Ollama and OpenAI-compatible APIs.
- The system prompt forbids code, snippets, and pseudocode; it asks the model to cite file lines, ask critical questions, and respond within a small number of tool rounds.
- The tool set has 4 actions: list_files, read_file, search, and run_command; run_command requires user confirmation unless auto-approval is enabled.
- Context control trims long tool outputs to 400 characters, drops old turns when history exceeds 16,000 estimated tokens, and stores full session transcripts in .socreates/session.json.

## Results
- The article reports no quantitative benchmark, accuracy score, user study, or baseline comparison.
- The prototype uses 1 control loop, 4 tools, and no dependencies.
- The loop stops after 10 iterations; the prompt asks the model to respond within 2-3 tool rounds and to read a file in 1-2 calls when possible.
- History is capped at 16,000 estimated tokens; each tool output is capped at 16K characters, about 4K tokens.
- Search returns up to 30 matches, and read_file returns continuation hints for long files.
- The author tested qwen, llama, gemma, and the DeepSeek API with mixed results, and gives one sample review that points to a possible history-pollution bug after llm.Chat returns an error.

## Link
- [https://zserge.com/posts/socreates/](https://zserge.com/posts/socreates/)
