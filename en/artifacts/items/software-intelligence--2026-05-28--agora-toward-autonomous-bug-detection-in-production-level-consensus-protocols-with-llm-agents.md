---
source: arxiv
url: https://arxiv.org/abs/2605.29910v1
published_at: '2026-05-28T13:27:47'
authors:
- Xiang Liu
- Sa Song
- Zhaowei Zhang
- Huiying Lan
- Jason Zeng
- Ming Wu
- Michael Heinrich
- Yong Sun
- Ceyao Zhang
topics:
- llm-agents
- code-intelligence
- bug-detection
- consensus-protocols
- multi-agent-testing
- software-verification
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Agora: Toward Autonomous Bug Detection in Production-Level Consensus Protocols with LLM Agents

## Summary
Agora is a three-agent LLM system for finding protocol-level logic bugs in consensus implementations. It reports 15 previously unknown safety bugs across Raft, EPaxos, HotStuff, and BullShark, while the tested ReAct-style LLM baselines found 0 protocol-level logic bugs.

## Problem
- Consensus code can lose safety through state-dependent bugs that span elections, recovery, message order, dependency tracking, signatures, or persistence.
- Standard LLM code agents tend to find local implementation bugs, such as memory or simple logic errors, and miss bugs that need protocol-level reasoning.
- This matters because consensus failures can corrupt data in distributed storage and databases or cause financial loss in blockchain systems.

## Approach
- Agora uses three LLM agents: an Orchestrator that tracks global state and prior findings, a Strategy agent that creates protocol-specific attack scenarios, and a TestGen agent that writes and runs unit tests.
- The method follows hypothesis-driven testing: each bug hypothesis includes trigger conditions, an action sequence, expected faulty behavior, and oracle checks.
- A small knowledge library gives the agents consensus bug patterns and constraints for CFT and BFT protocols, so the search avoids unrealistic scenarios such as Byzantine assumptions in CFT systems.
- The Strategy agent varies node behavior, crashes, recovery, joins, message ordering, and conflict relationships; the TestGen agent iterates on tests until they run and expose a violation or the retry limit is reached.

## Results
- Across four consensus implementations, Agora found 15 previously unknown protocol-level logic bugs: 1 in Raft, 9 in EPaxos, 4 in HotStuff, and 1 in BullShark.
- The ReAct-style baselines using GPT-5.2, Gemini 3.0 Pro Preview, Claude Sonnet 4.5, and Qwen3 Coder 480B A35B found 22 implementation bugs in total and 0 protocol-level logic bugs.
- With Agora, GPT-5.2 found 8 logic bugs, Gemini 3.0 Pro Preview found 11, Claude Sonnet 4.5 found 6, and Qwen3 Coder 480B A35B found 9; the combined unique total was 15.
- Ablation results in the excerpt show Agora found 11 bugs in that study setting; removing bug-exploitation cut this to 3, removing constraints-analyzer cut it to 1, and removing state-analyzer, scenario-generator, or reflection-loop cut it to 0.
- The paper reports that removing one component reduced effectiveness by 73% to 100%, based on the ablation table.

## Link
- [https://arxiv.org/abs/2605.29910v1](https://arxiv.org/abs/2605.29910v1)
