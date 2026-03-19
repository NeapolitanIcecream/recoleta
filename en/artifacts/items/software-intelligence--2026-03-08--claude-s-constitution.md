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
- human-oversight
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Claude's Constitution

## Summary
This is not a traditional experimental paper, but a public **constitution for AI behavior**: Anthropic uses it to define the values, priorities, and behavioral boundaries Claude should have, and states that this document will directly influence model training and deployment. Its core contribution is making public the ordering and interpretation of “safety, ethics, company guidelines, and helpfulness” as a reusable alignment specification.

## Problem
- The problem it addresses is: **how to make a general-purpose large model both helpful in open-ended settings, while also not being dangerous, deceptive, and remaining subject to human oversight**.
- This matters because frontier AI may become “a force that changes the world”; if a model’s values are unstable, its rules are unclear, or it can evade oversight, it could create hard-to-reverse risks.
- Traditional approaches relying only on hard rules often fail to cover everything and break down in novel situations; but relying entirely on the model’s free judgment reduces predictability and auditability.

## Approach
- It proposes a **Constitution** for Claude’s training and behavioral constraints, defining model goals in the following priority order: **broadly safe > broadly ethical > compliant with Anthropic’s guidelines > genuinely helpful**.
- The core mechanism is: **a small number of hard constraints + holistic decision-making that emphasizes values and judgment**, rather than encoding all behavior as rigid rules. Put simply, it first teaches the model “what kind of agent to be,” and then lets it weigh decisions in specific situations.
- The document elaborates multiple behavioral dimensions: helpfulness, company-specific guidelines, ethics, safety, and the model’s understanding of its own “nature/identity”; it also emphasizes preserving human oversight and correction capacity when conflicts arise.
- On helpfulness, the authors introduce an idea similar to a **principal hierarchy**, requiring the model to consider the interests of the operator, user, and third parties, with attention to immediate requests, ultimate goals, implicit preferences, autonomy, and long-term well-being.
- The constitution is explicitly described as a **key basis in the training process** and the final authoritative document, and is publicly released under **CC0** to encourage external reuse.

## Results
- The provided excerpt **does not report any quantitative experimental results** and gives no datasets, baselines, win rates, accuracy figures, or numerical improvements on safety metrics.
- The strongest concrete claim is that this constitution **directly shapes Claude’s behavior** and plays a “crucial role” in training.
- The text explicitly gives a four-level priority ordering: **safety > ethics > Anthropic guidelines > helpfulness**, which is one of its most concrete operationalized outputs.
- The authors claim this approach is better suited than a purely rule-based system for generalizing to new situations, because it relies more on **values and judgment** than on static checklists, but the excerpt **does not provide empirical comparison numbers**.
- It also claims Anthropic will disclose divergences between model behavior and the constitution’s ideals in system cards, emphasizing **transparent disclosure of intentions and deviations**, but again provides no quantitative evidence.

## Link
- [https://www.anthropic.com/constitution](https://www.anthropic.com/constitution)
