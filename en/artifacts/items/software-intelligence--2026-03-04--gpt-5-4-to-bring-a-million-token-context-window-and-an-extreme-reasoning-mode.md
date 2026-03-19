---
source: hn
url: https://the-decoder.com/gpt-5-4-reportedly-brings-a-million-token-context-window-and-an-extreme-reasoning-mode/
published_at: '2026-03-04T22:52:08'
authors:
- jwilliams
topics:
- large-language-models
- long-context
- reasoning-mode
- coding-agents
- model-release-rumor
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# GPT-5.4 to bring a million-token context window and an extreme reasoning mode

## Summary
This is a media report about OpenAI GPT-5.4, not an official paper or technical report. The core highlights are that the context window may expand to 1 million tokens and that it may add an “extreme reasoning” mode for highly difficult tasks.

## Problem
- Existing models still tend to make errors on ultra-long-context tasks, especially complex tasks that last for several hours, such as programming agents and long-chain reasoning.
- For researchers and advanced users, the standard reasoning budget may be insufficient to handle the most difficult problems.
- OpenAI needs to narrow or eliminate the gap in context-window capability in competition with Google and Anthropic.

## Approach
- The report says GPT-5.4 will increase the context window to **1,000,000 tokens** to support longer inputs, longer task trajectories, and retention of more historical information.
- It introduces an **“extreme” thinking mode**, which allocates more compute resources to difficult problems in exchange for stronger reasoning ability rather than faster responses.
- One goal is to improve reliability on long tasks and reduce error accumulation during multi-hour execution.
- This capability is considered especially beneficial for programming agents like **Codex**, because they often need to run across files, across steps, and over long periods.

## Results
- The report claims GPT-5.4’s context window will reach **1,000,000 tokens**, more than **2 times** the current GPT-5.2’s **400,000 tokens** (about **2.5×**).
- It says this spec would put OpenAI at the same level as **Google** and **Anthropic** in context length, but **it does not provide benchmarks, datasets, or precise comparison figures**.
- The report further claims the new model will be **more reliable and make fewer errors** on “long tasks that can run for several hours,” but **it provides no quantitative metrics**.
- The “extreme” reasoning mode is described as a high-compute option aimed at researchers, but **no public data is provided on its latency, cost, or accuracy gains**.
- Therefore, the strongest concrete conclusion at present is only that a **1 million token context** and a **reasoning mode with a higher compute budget** are the main reported breakthroughs, rather than experimentally validated results officially confirmed by OpenAI.

## Link
- [https://the-decoder.com/gpt-5-4-reportedly-brings-a-million-token-context-window-and-an-extreme-reasoning-mode/](https://the-decoder.com/gpt-5-4-reportedly-brings-a-million-token-context-window-and-an-extreme-reasoning-mode/)
