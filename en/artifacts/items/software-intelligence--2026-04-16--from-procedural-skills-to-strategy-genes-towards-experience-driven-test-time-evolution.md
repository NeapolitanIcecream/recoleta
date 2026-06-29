---
source: arxiv
url: http://arxiv.org/abs/2604.15097v1
published_at: '2026-04-16T14:55:49'
authors:
- Junjie Wang
- Yiming Ren
- Haoyang Zhang
topics:
- test-time-adaptation
- llm-agents
- code-generation
- experience-reuse
- prompt-representation
- scientific-programming
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# From Procedural Skills to Strategy Genes: Towards Experience-Driven Test-Time Evolution

## Summary
This paper argues that reusable experience for LLM agents works better as a compact control object than as a long skill document. In 4,590 trials on 45 scientific code-solving scenarios, the proposed **strategy gene** format beats documentation-heavy skill packages and supports iterative experience updates more effectively.

## Problem
- The paper studies how to reuse past experience at test time so an LLM agent changes its behavior without changing model weights.
- Many prior systems store experience as long skills, reflections, or memory documents, but those formats may help humans read and review them more than they help the model act on them during inference.
- This matters for code and scientific task solving because token budget and attention are limited; extra documentation can dilute the useful guidance and lower pass rates.

## Approach
- The authors compare two experience formats built from the same underlying task knowledge: **Skill**, a documentation-heavy package of about 2,500 tokens, and **Gene**, a compact control-oriented object of about 230 tokens.
- A Gene contains a small fixed structure: task-matching signals, a short summary, a few strategic steps, and failure-aware **AVOID** cues, with optional constraints and validation hooks.
- They add a **Gene Evolution Protocol (GEP)** to canonicalize genes into structured objects that can be edited, compared, accumulated, and reused across tasks.
- The evaluation uses 4,590 retained trials across 45 scientific code-generation scenarios, scored by checkpoint-based pass rate, with two Gemini models: Gemini 3.1 Pro Preview and Gemini 3.1 Flash Lite Preview.
- The paper runs three probes: a Skill probe to locate useful signal inside long skills, a Gene probe to test whether Gene is better than a short prompt, and an Evolution probe to test how experience should accumulate over time.

## Results
- In the main comparison, **Gene** reaches **54.0%** average pass rate, versus **51.0%** for **no guidance** and **49.9%** for **Skill**. Relative to no guidance, Gene gains **+3.0 percentage points**, while Skill drops **-1.1 points**.
- By model, Skill changes **Gemini Pro** from **60.1%** to **50.7%** and **Flash** from **41.8%** to **49.0%**. Gene keeps **Pro** near baseline at **59.9%** and improves **Flash** to **48.2%**.
- In Gene construction ablations, **keywords only** scores **53.5%** average (**+2.5 pp**), **keywords + summary** scores **51.0%** (**+0.0 pp**), and **keywords + summary + strategy** scores **54.0%** (**+3.0 pp**). The gain comes from adding explicit strategy, not from adding more text.
- Figure 1 reports a representative comparison where a compact Gene gives **+3.0 pp** over baseline while a full Skill package gives **-1.1 pp**.
- For iterative evolution on **CritPt**, gene-evolved systems improve over paired base models from **9.1% to 18.57%** and from **17.7% to 27.14%**.
- The excerpt does not include full numeric tables for every probe, but it states these concrete findings: useful control signal inside Skill is sparse, matched-budget Skill fragments improve over full Skill yet still trail Gene, structural perturbations hurt Gene less, and compact distilled failure warnings work better than appending raw failure history.

## Link
- [http://arxiv.org/abs/2604.15097v1](http://arxiv.org/abs/2604.15097v1)
