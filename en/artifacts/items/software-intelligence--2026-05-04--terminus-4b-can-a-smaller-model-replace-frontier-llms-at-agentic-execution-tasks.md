---
source: arxiv
url: https://arxiv.org/abs/2605.03195v1
published_at: '2026-05-04T22:24:24'
authors:
- Spandan Garg
- Vikram Nitin
- Yufan Huang
topics:
- code-agents
- software-foundation-models
- terminal-execution
- small-language-models
- multi-agent-software-engineering
- context-management
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?

## Summary
Terminus-4B is a Qwen3-4B model trained to act as a terminal-execution subagent inside coding agents. The paper claims it can replace frontier LLMs for this narrow subtask while cutting main-agent token use by up to about 30%.

## Problem
- Coding agents often run builds, tests, installs, and diagnostics inside the main agent context, which can add tens of thousands of terminal-output tokens per command.
- This matters because verbose logs crowd out code, plans, and prior edits, raising cost and shortening the useful problem-solving trajectory.
- Existing subagent setups usually use frontier models for terminal work, even though the task is narrow: run commands, read output, and return a concise, accurate summary.

## Approach
- The paper adds an Execution Subagent tool to a coding agent. The main agent sends a natural-language query, and the subagent runs terminal commands in its own context.
- The subagent has one tool, Terminal. It runs one synchronous command per turn, uses explicit timeouts, has a default 10-turn limit, and returns a structured `<final_answer>` with per-command summaries.
- Terminus-4B starts from Qwen3-4B and is post-trained for this task with supervised finetuning on expert subagent trajectories, then GRPO reinforcement learning.
- RL rollouts are isolated from the main agent: a lightweight Qwen3-4B Instruct model forwards a fixed query to the subagent, so training focuses on the terminal-execution behavior.
- Rewards use an LLM judge with rubrics that compare candidate rollouts to reference trajectories across quality and failure dimensions.

## Results
- The abstract claims up to about 30% lower main-agent token use versus a No Subagent baseline, with no reported performance loss on SWE-Bench Pro and an internal SWE-Bench C# benchmark.
- The paper claims Terminus-4B closes the gap to Claude Sonnet, Claude Opus, and GPT-5.3-Codex as an Execution Subagent, and often beats them, but the excerpt does not include the full benchmark tables or exact resolve-rate numbers.
- In the Serilog example, the baseline used 2.46M main-agent tokens, 40 turns, and 18 direct terminal calls. With Terminus-4B as the subagent, the run used 740k main-agent tokens and 32 turns, while the subagent ran 9 commands internally.
- In that same example, the subagent returned about a 200-token summary instead of raw logs, including `dotnet build` success with 9 warnings and 0 errors, 769 passing unit tests, and 1 failing approval test with the likely fix.
- The training corpus starts from about 10k buildable instances across 2,144 repositories and 5 languages, producing 3,009 unique Execution Subagent invocations across 730 repositories.
- Task labels in the collected set include 2,692 test-execution tasks, 2,166 error-diagnosis tasks, 969 build/compile tasks, and 106 dependency tasks.

## Link
- [https://arxiv.org/abs/2605.03195v1](https://arxiv.org/abs/2605.03195v1)
