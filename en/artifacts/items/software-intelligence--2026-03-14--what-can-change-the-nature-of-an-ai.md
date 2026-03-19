---
source: hn
url: https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/
published_at: '2026-03-14T22:52:48'
authors:
- onatm
topics:
- prompt-engineering
- ai-agents
- model-alignment
- anthropomorphism
- code-intelligence
relevance_score: 0.7
run_id: materialize-outputs
language_code: en
---

# What can change the nature of an AI?

## Summary
This article argues that context configurations such as prompts, `AGENTS.md`, and `PERSONALITY.md` cannot truly change an AI’s “nature”; they can only temporarily alter its surface behavior and speaking style. The author emphasizes that a model’s substantive capabilities and tendencies can mainly change only during training, post-training, or fine-tuning.

## Problem
- The article criticizes a common misunderstanding: people treat “role setting” in prompt engineering as if it changes the model itself.
- This misunderstanding matters because it exaggerates AI’s autonomy, personhood, and moral agency, leading to misjudgments about its risks, capabilities, and appropriate boundaries of use.
- In software agent scenarios, mistaking “speaking like a senior engineer” for “actually having a senior engineer’s judgment and sense of responsibility” can lead to misplaced trust.

## Approach
- The core view is very direct: `AGENTS.md`, `PERSONALITY.md`, skill descriptions, and similar files are essentially just additional context, not modifications to the model’s parameters or internal mechanisms.
- The author limits real “change” to three categories: training, post-training, and fine-tuning.
- By contrasting “role-playing/tone change” with “change in nature,” the article argues that the former is only imitation at the level of script, voice, and costume, not the formation of cognition or conscience.
- The author further points out that the “personality” a model displays in conversation is merely a behavior pattern temporarily induced by context during a single inference session, and it disappears when the session ends.

## Results
- This is not an experimental paper; **the excerpt provides no quantitative results, datasets, baselines, or evaluation metrics**.
- The strongest concrete claim is that prompt files can only change **surface behavior**, not the model’s “nature”; real change can occur only at **3** stages: training, post-training, and fine-tuning.
- The author claims that a coding agent’s so-called “personality” appears only briefly within a single session, on a particular inference instance, and belongs to “context” rather than being a persistent property.
- The article also makes a strong but non-quantitative judgment: treating imitation as conscience (or selfhood) is a serious mistake, and models therefore should not be anthropomorphized as agents that can “feel remorse” or “be responsible.”

## Link
- [https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/](https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/)
