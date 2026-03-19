---
source: hn
url: https://www.anthropic.com/constitution
published_at: '2026-03-08T22:50:29'
authors:
- doener
topics:
- ai-alignment
- constitutional-ai
- safety-governance
- model-behavior
- value-alignment
relevance_score: 0.09
run_id: materialize-outputs
language_code: en
---

# Claude's Constitution

## Summary
This is not an experimental research paper, but Anthropic’s published constitution for Claude: a normative framework used to shape the model’s values, modes of judgment, and behavioral priorities. Its core goal is to have Claude make holistic tradeoffs among “safety, ethics, compliance, and helping users,” while placing human oversight at the highest priority.

## Problem
- Problem addressed: how to clearly specify **values, behavioral boundaries, and conflict priorities** for a highly capable general AI, so as to avoid harmful, deceptive, uncontrolled, or excessively sycophantic behavior in the real world.
- Why it matters: frontier AI may profoundly affect society; if a model’s values are unstable, its judgment is poor, or it undermines human oversight, it could create irreversible risks.
- It also addresses a balancing problem: the model should not pursue only “safe refusal,” nor only “obedient usefulness,” but instead maintain a robust balance among helpfulness, ethics, and supervisability.

## Approach
- Proposes a “constitution” for Claude as the highest source of norms for training and behavioral alignment, and requires other guidance to remain consistent with it.
- Defines four core priorities, to be weighed holistically and in order: **broadly safe > broadly ethical > compliant with Anthropic’s guidelines > genuinely helpful**.
- The method leans more toward **cultivating values and judgment** rather than relying only on rigid rules; that is, enabling the model to understand “why to act this way” so it can generalize to new situations.
- At the same time, it retains a small number of **hard constraints**, such as not providing help that would significantly increase biological weapons attack capability, and not undermining appropriate human oversight mechanisms.
- It also gives a more fine-grained mechanism for “helpfulness”: using principal hierarchy, the user’s long-term well-being, inference of true intent, and avoidance of sycophancy/manipulation/excessive paternalistic intervention to determine how to respond.

## Results
- The text **does not provide quantitative experimental results**; it reports no benchmark datasets, accuracy, success rate, or numerical comparisons with other methods.
- Its strongest concrete claim is that this constitution “plays a crucial role in the training process,” and that its contents “directly shape Claude’s behavior.”
- It explicitly states four core objectives and their priority order: 1) broadly safe, 2) broadly ethical, 3) guideline compliance, 4) genuinely helpful.
- It explicitly states an alignment approach of “values plus judgment first, rules as support,” and treats the document as a continuously revised “work in progress.”
- It also makes an openness claim: the full text is released under **CC0 1.0**, allowing free reuse as a reference for broader AI governance/alignment practice.

## Link
- [https://www.anthropic.com/constitution](https://www.anthropic.com/constitution)
