---
source: arxiv
url: http://arxiv.org/abs/2603.08604v1
published_at: '2026-03-09T16:52:27'
authors:
- Tianyi Li
- Satya Samhita Bonepalli
- Vikram Mohanty
topics:
- llm-sensemaking
- human-ai-collaboration
- hypothesis-generation
- fact-extraction
- prompting
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# What to Make Sense of in the Era of LLM? A Perspective from the Structure and Efforts in Sensemaking

## Summary
This paper explores how LLMs can collaborate with humans in complex sensemaking tasks, using the analysis of fictional terrorist attack clues as a case to compare GPT-4 with novice crowd analysts. Preliminary results show that LLMs are better at proposing hypotheses with broader coverage, while humans are stronger in the completeness of fact extraction.

## Problem
- The paper aims to address the question of how LLMs should help humans perform sensemaking when facing complex, ambiguous, multi-document information, and at which stages such assistance is most effective.
- This matters because complex analytical tasks require both extracting reliable facts from raw materials and forming reasonable hypotheses under incomplete information; although LLMs are strong at synthesis and inference, they are also prone to hallucinations and distortion.
- The authors are particularly concerned with how LLMs compare with humans in two aspects: "extracting facts" and "generating hypotheses consistent with the answer key."

## Approach
- The study uses a dataset containing 10 documents, with the task of proposing several reasonable hypotheses about fictional terrorist activity.
- It compares two ways of using GPT-4 against an existing novice crowdsourcing baseline: one is **holistic**, where the model directly generates alternative hypotheses as a whole; the other is **step-by-step**, where the model is required to produce intermediate analytical results according to predefined steps.
- The evaluation uses two core metrics: **Coverage** (how many relevant facts/hypotheses are covered) and **Comprehensiveness** (whether the covered content is complete and accurate in detail).
- The core mechanism can be understood most simply as comparing two collaboration modes: "letting the LLM analyze freely at a holistic level" versus "having the LLM follow the human analytical process step by step," to see which is better suited for complex sensemaking.

## Results
- For **fact extraction**, the crowd analysis covered **17 key facts**, and **all 17 were comprehensive**; this was the strongest human baseline result reported in the paper.
- Under the **holistic** approach, the LLM only implicitly covered **6 facts**, with **0 comprehensive**, indicating that it jumps directly to hypotheses while neglecting solid evidentiary listing.
- Under the **step-by-step** approach, the LLM improved fact extraction to **9 facts**, of which **5 were comprehensive**; this is better than holistic, but still clearly weaker than the human baseline of 17 comprehensive facts.
- For **hypothesis generation**, the crowd analysis covered **4 of 15 predefined hypotheses**, and **all 4 were comprehensive**.
- The **holistic** LLM performed best at the hypothesis level: it covered **10/15 hypotheses**, of which **6 were comprehensive**, significantly higher than the crowd's **4/15** coverage.
- The **step-by-step** LLM was instead weaker on hypotheses, with only **3 hypotheses comprehensively covered**; the paper does not provide a more complete total coverage count, but clearly states that its hypothesis performance was below holistic.

## Link
- [http://arxiv.org/abs/2603.08604v1](http://arxiv.org/abs/2603.08604v1)
