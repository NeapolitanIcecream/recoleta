---
source: arxiv
url: http://arxiv.org/abs/2603.14646v1
published_at: '2026-03-15T22:54:03'
authors:
- Thuy Ngoc Nguyen
- Duy Nhat Phan
- Cleotilde Gonzalez
topics:
- theory-of-mind
- temporal-memory
- llm-evaluation
- human-ai-interaction
- belief-tracking
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Dynamic Theory of Mind as a Temporal Memory Problem: Evidence from Large Language Models

## Summary
This paper reconceptualizes dynamic Theory of Mind (ToM) as a problem of **temporal memory and retrieval**, rather than merely a static judgment of belief at a single moment. The authors introduce the DToM-Track benchmark and find that large language models are generally better at judging **current beliefs** but struggle to recall **prior beliefs before an update**.

## Problem
- Existing ToM evaluations mostly focus on the static question of “what does someone believe right now,” overlooking the fact that in real interactions, beliefs must be maintained, updated, and recalled over time.
- This matters because in long-term human–AI interaction, a system must not only understand what a user currently thinks, but also track what they thought before, when it changed, and why it changed.
- The core challenge the authors study is whether LLMs can represent and retrieve **belief trajectories**, rather than merely inferring the current state from the latest context.

## Approach
- They propose **DToM-Track**: an evaluation framework for temporal belief reasoning in multi-turn dialogue, specifically testing three dynamic abilities: **pre-update** (recall of beliefs before an update), **post-update** (inference of current beliefs after an update), and **update-detection** (identifying when a belief changed).
- They use controlled **LLM-LLM dialogue generation**: before each turn, agents have hidden inner speech (internal representations), creating information asymmetry and simulating ToM / false-belief scenarios.
- Belief updates are explicitly injected at predetermined turns, and a belief tracker records belief type, source turn, whether it was overwritten, and pre-update content, in order to construct time-sensitive questions.
- A multi-stage LLM-based filtering and validation process checks whether planned belief updates were actually realized in the dialogue and whether the QA items are answerable and have acceptable option quality, producing the final dataset.
- Zero-shot multiple-choice evaluation is conducted on 6 models, covering 3B–70B, both open- and closed-source models.

## Results
- The final **DToM-Track** dataset contains **5,794** questions, covering **6** question types and **5** types of mental states; specifically temporal **1,807 (31.2%)**, false belief **1,761 (30.4%)**, second-order **768 (13.3%)**, update detection **591 (10.2%)**, post-update **527 (9.1%)**, and pre-update **340 (5.9%)**.
- Overall accuracy ranges from **35.7%–63.3%**, all above the four-choice random baseline of **25%**; the best model is **LLaMA 3.3-70B: 63.3%**, the lowest is **LLaMA 3.2-3B: 35.7%**, and GPT-4o-mini achieves **55.1%**.
- Average performance by question type shows **update-detection 67.5%** as the highest, followed by **post-update 63.9%**, while **pre-update 27.7%** is significantly the lowest, indicating that models can capture “what is believed now” but struggle to recall “what was believed before.”
- Compared with standard ToM tasks, dynamic recall is harder: **pre-update 27.7%** is clearly lower than **false belief 44.7%**, suggesting that “tracking belief evolution” is a distinct challenge from classical false-belief reasoning.
- A clear “recency bias” also appears at the individual model level: for example, **GPT-4o-mini** scores **68.5% / 27.6%** on post-update / pre-update, **LLaMA 3.3-70B** scores **71.3% / 40.9%**, and **LLaMA 3.1-8B** scores **57.9% / 12.1%**.
- The authors’ strongest claim is that this asymmetry—“strong on current beliefs, weak on prior beliefs”—appears across model families and scales, consistent with explanations based on **recency bias** and **interference** in cognitive science, suggesting that dynamic ToM is constrained by temporal representation and memory retrieval, not just model parameter scale.

## Link
- [http://arxiv.org/abs/2603.14646v1](http://arxiv.org/abs/2603.14646v1)
