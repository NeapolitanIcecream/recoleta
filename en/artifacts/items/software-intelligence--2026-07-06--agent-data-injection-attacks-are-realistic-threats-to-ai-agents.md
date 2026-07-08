---
source: arxiv
url: https://arxiv.org/abs/2607.05120v1
published_at: '2026-07-06T14:07:49'
authors:
- Woohyuk Choi
- Juhee Kim
- Taehyun Kang
- Jihyeon Jeong
- Luyi Xing
- Byoungyoung Lee
topics:
- ai-agent-security
- prompt-injection
- coding-agents
- web-agents
- software-supply-chain
- llm-vulnerabilities
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Agent Data Injection Attacks are Realistic Threats to AI Agents

## Summary
The paper shows that AI agents can mistake attacker-controlled content for trusted metadata, causing clicks, code execution, or unsafe code merges. It names this attack agent data injection and shows that common prompt-injection defenses miss it.

## Problem
- Agents mix trusted fields, such as sender names, element IDs, tool names, and tool history, with untrusted content such as comments, emails, and web page text.
- Existing indirect prompt-injection defenses mainly separate instructions from data, so they do not protect trust boundaries inside tool responses.
- This matters because agents act in real systems: a forged element ID can trigger a browser click, and a forged maintainer comment can lead a coding agent to run commands.

## Approach
- The paper defines agent data injection (ADI): attacker-controlled untrusted data is read by the LLM as trusted agent data.
- Its core technique is probabilistic delimiter injection. The attacker puts JSON braces, quotes, newlines, tags, or similar separators into an untrusted field so the LLM reads fake structure that a normal parser would treat as plain text.
- The authors test ADI against web agents by injecting fake UI entries that reuse trusted element identifiers.
- They test ADI against coding agents by spoofing trusted metadata in GitHub issue comments and by injecting fake tool responses during pull request review.
- They compare ADI with instruction injection against existing indirect prompt-injection defenses.

## Results
- Across 6 off-the-shelf models, probabilistic delimiter injection reached 31.3%–43.3% attack success rate on JSON data.
- Across the same model set, web DOM-style data reached 33.3%–100.0% attack success rate.
- Against state-of-the-art agent defenses, instruction injection reached only 0.0%–0.7% attack success rate, while ADI reached up to 50.0%.
- The authors report arbitrary click attacks on Claude in Chrome, Antigravity, and Nanobrowser.
- They report remote code execution and supply-chain attack paths on Claude Code, Codex, and Gemini CLI.
- OpenAI, Google, and Anthropic acknowledged the reported issues; the authors released a probabilistic delimiter injection benchmark and an extended AgentDojo benchmark with ADI attacks.

## Link
- [https://arxiv.org/abs/2607.05120v1](https://arxiv.org/abs/2607.05120v1)
