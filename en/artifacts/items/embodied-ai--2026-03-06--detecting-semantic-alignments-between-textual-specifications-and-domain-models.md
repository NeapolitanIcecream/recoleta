---
source: arxiv
url: http://arxiv.org/abs/2603.06037v1
published_at: '2026-03-06T08:46:57'
authors:
- Shwetali Shimangaud
- "Lola Burgue\xF1o"
- Rijul Saini
- "J\xF6rg Kienzle"
topics:
- requirements-engineering
- domain-modeling
- semantic-alignment
- llm-based-validation
- traceability
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Detecting Semantic Alignments between Textual Specifications and Domain Models

## Summary
This paper proposes a method for detecting semantic alignment/misalignment between **textual requirement specifications** and **domain models**, aiming to help modelers verify whether model elements are correctly supported by the requirements. The method combines rule-based NLP, model slicing, template-based sentence generation, and LLM-based judgment, and provides traceable evidence sentences.

## Problem
- The problem addressed: determining whether elements in a complete or partially completed domain model are **semantically consistent** with the original natural-language requirements, **semantically conflicting**, or have **insufficient evidence**.
- This is important because creating correct domain models from text is inherently difficult, especially for novice modelers; incorrect models can affect requirements analysis, traceability, and subsequent model-driven development.
- Existing automatic generation/linking methods still require manual validation, while the fact that “the same requirement can correspond to multiple correct models” makes validation itself difficult to automate.

## Approach
- First, use **rule-based NLP preprocessing** on the requirements text to extract textual concepts, relationships, and their corresponding sets of original sentences.
- For each element in the domain model (attributes, associations, compositions, inheritance, enumerations, etc.), extract a **minimal model slice** that preserves the minimum context needed to understand that element.
- Use a heuristic **semantic matcher** to map model elements to relevant sentences in the requirements, determining “which sentences are talking about this element.”
- Then use rules to convert each model slice into an **artificial natural-language sentence**, for example rewriting attributes/associations into simple English sentences.
- Finally, use an LLM to make a three-way judgment between the “generated sentence” and the “matched original sentences”: **equivalent**, **contradictory**, or **contains**; for each type of question, use multiple semantically equivalent prompt variants and apply **relative majority voting**, classifying each element as aligned / misaligned / unclassified and outputting evidence sentences.

## Results
- The approach was evaluated on multiple example domains from the literature, where the data consisted of **textual specifications + reference domain models**, and additionally used **mutation** to systematically construct erroneous models from correct models.
- The paper claims it can identify alignments and misalignments with **precision close to 1.0**, indicating that it almost never misclassifies model elements.
- **Recall is about 78%**, meaning it can classify more than **3/4** of model elements, while the rest remain unclassified due to insufficient evidence.
- Inference time ranges from **18 seconds to 1 minute per model element**.
- The clearest comparative conclusion in the paper is not a comprehensive tabular comparison against specific SOTA numerical baselines, but rather the emphasis that the algorithm “almost never misclassifies” and can cover most elements, making it suitable for integration into modeling tools for immediate feedback, warnings, or offline quality assessment.

## Link
- [http://arxiv.org/abs/2603.06037v1](http://arxiv.org/abs/2603.06037v1)
