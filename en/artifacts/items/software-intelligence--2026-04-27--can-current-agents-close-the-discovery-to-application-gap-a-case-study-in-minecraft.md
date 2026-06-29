---
source: arxiv
url: https://arxiv.org/abs/2604.24697v1
published_at: '2026-04-27T16:58:04'
authors:
- Zhou Ziheng
- Huacong Tang
- Jinyuan Zhang
- Haowei Lin
- Bangcheng Yang
- Qian Long
- Fang Sun
- Yizhou Sun
- Yitao Liang
- Ying Nian Wu
- Demetri Terzopoulos
- Xiaofeng Gao
topics:
- ai-agents
- minecraft-benchmark
- scientific-discovery
- multi-agent-systems
- causal-reasoning
- redstone-circuits
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Can Current Agents Close the Discovery-to-Application Gap? A Case Study in Minecraft

## Summary
SciCrafter tests whether LLM agents can discover missing Minecraft redstone rules and use them to build working circuits. Current frontier agents reach only about 26% success without help, and the paper finds large gaps in identifying what to investigate and in applying discovered rules.

## Problem
- Current agent benchmarks rarely test the full discovery-to-application loop: find an unknown causal rule, record it, and use it to build a working system.
- Minecraft redstone gives controllable circuit tasks where agents cannot always rely on memorized facts, especially when task parameters scale.
- This matters for automated engineering agents because real tasks often require asking the right experimental question before construction can succeed.

## Approach
- SciCrafter defines 5 redstone task families with 5 difficulty levels each, for 25 tasks total: simultaneous ignition, T-junction routing, sequential activation, distance-equalized ignition, and pulse extension.
- Agents build circuits that ignite lamps in specified spatial or temporal patterns; an automated checker presses a button and verifies per-tick lamp states.
- Difficulty increases through parameters such as lamp count, delay sequence, and pulse duration, which force agents to learn mechanics such as signal decay, repeater direction, repeater delay, and unintended side connections.
- The evaluation runs GPT-5.2, Gemini-3-Pro, Claude-Opus-4.5, Grok-4, GLM-4.7, Qwen3-235B, Qwen2.5-72B, and Qwen3-32B under Claude Code, with 50 verification trials per task and 8 runs.
- The diagnosis adds interventions in sequence: oracle hints for what to investigate, a scientist sub-agent for controlled experiments, and a structured knowledge book with Claim, Evidence Proof, Constraints, and Example fields.

## Results
- The best baseline is Gemini-3-Pro at 26.0% success across 25 tasks; GPT-5.2 reaches 25.5%, Claude-Opus-4.5 reaches 21.0%, and Qwen3-32B reaches 10.5%.
- Oracle hints roughly double success for strong models: Gemini-3-Pro rises from 26.0% to 52.5%, GPT-5.2 from 25.5% to 51.0%, and Claude-Opus-4.5 from 21.0% to 46.0%.
- Adding the scientist sub-agent gives another 7.5 to 14.0 percentage points across models; Gemini-3-Pro reaches 64.0%, GPT-5.2 reaches 60.0%, and Claude-Opus-4.5 reaches 59.0%.
- The remaining application gap is still large: 36.0 percentage points for Gemini-3-Pro, 40.0 for GPT-5.2, 41.0 for Claude-Opus-4.5, and 57.0 for Qwen2.5-72B.
- Structured consolidation beats free-form summaries in the reported ablation: the Claim-Proof-Constraints-Example format reaches 64.0% versus 58.0% for free-form summaries.
- The paper claims the main bottleneck for frontier models is shifting toward knowledge gap identification, while residual application skill remains the largest absolute gap overall.

## Link
- [https://arxiv.org/abs/2604.24697v1](https://arxiv.org/abs/2604.24697v1)
