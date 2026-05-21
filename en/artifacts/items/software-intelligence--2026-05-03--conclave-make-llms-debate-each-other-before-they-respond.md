---
source: hn
url: https://adndvlp.github.io/conclave/
published_at: '2026-05-03T23:45:45'
authors:
- andngd
topics:
- multi-agent-software-engineering
- llm-debate
- code-agents
- automated-software-production
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Conclave – make LLMs debate each other before they respond

## Summary
Conclave adds a structured multi-LLM debate engine to OpenCode so several models can discuss a software task before one response or implementation is chosen. It targets code work where a single model may miss architecture flaws, edge cases, or security issues.

## Problem
- Single-model coding agents can miss design flaws, edge cases, and security risks before code is written.
- Teams that already pay for Claude Code, Gemini CLI, Codex, or local models may lack direct API access for multi-model workflows.
- Multi-model debate adds latency and cost, so the tool is aimed at complex tasks rather than simple prompts.

## Approach
- Conclave modifies OpenCode with a team debate engine; the page says about 12 files were changed while OpenCode keeps providers, agents, git support, tools, and the TUI.
- Models debate in structured rounds using LEAD, SUPPORT, ALIGN, BUILD, and CHALLENGE signals.
- A winner is selected by endorsement score after the debate.
- Users can mix CLI-authenticated and API models, including Claude Code, Gemini CLI, Codex, OpenAI, Anthropic, DeepSeek, Google, NVIDIA, Groq, and Ollama.
- Each model gets a debate thread sized to its context limit; large-context models can see more context, while smaller models get signal summaries.

## Results
- The excerpt reports no benchmark, dataset, or human-evaluation results showing output-quality gains over a single LLM.
- Implementation scope: about 12 OpenCode files modified to add the debate engine.
- Cost and latency scale with team size and rounds: 3 models debating for 3 rounds make 9 API calls per user message.
- Cost example: each team member makes an independent call, so a 3-model team costs about 3x a single-model call unless free CLI or local models are used.
- Context claim: the tool can pair a 1M-token DeepSeek model with a 128K-token Gemini Flash model by truncating or summarizing the debate thread per model.
- Maturity claim: the project is weeks old; debate, team persistence, and provider connections work, while context optimization, live streaming, and Breaking Teams are roadmap items.

## Link
- [https://adndvlp.github.io/conclave/](https://adndvlp.github.io/conclave/)
