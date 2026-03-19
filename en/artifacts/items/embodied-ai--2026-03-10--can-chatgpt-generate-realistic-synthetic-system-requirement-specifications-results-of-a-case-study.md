---
source: arxiv
url: http://arxiv.org/abs/2603.09335v1
published_at: '2026-03-10T08:10:56'
authors:
- Alex R. Mattukat
- Florian M. Braun
- Horst Lichter
topics:
- requirements-engineering
- synthetic-data
- large-language-models
- prompt-engineering
- quality-evaluation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Can ChatGPT Generate Realistic Synthetic System Requirement Specifications? Results of a Case Study

## Summary
This paper investigates whether ChatGPT can generate synthetic requirements documents that **look realistic** **without access to real system requirements specifications (SyRS) and without relying on domain experts during the generation process**. The conclusion is: **yes, to a certain extent**, but LLM-based automatic quality assessment is clearly unstable and **still cannot replace expert review**.

## Problem
- The paper addresses the problem that real **SyRS** are highly valuable for software engineering research, but are often unavailable due to **confidentiality, proprietary restrictions, and difficulty of access**, resulting in data scarcity.
- If sufficiently realistic **synthetic SyRS (SSyRS)** can be generated, they could support method development, tool evaluation, test generation, and benchmark construction in requirements engineering.
- The difficulty is that black-box LLMs (such as ChatGPT) are prone to **hallucinations** and **overconfidence**, especially in specialized-domain text generation, where they may produce requirements that appear plausible but are actually contradictory or incorrect.

## Approach
- The authors designed an **iterative generate–evaluate–prompt-rewrite** process, using ChatGPT-4o to generate SSyRS across **10 industries**, and after **10 iterations** ultimately obtained **300** documents.
- During generation, they used a simplified **ISO/IEC/IEEE 29148**-style template, combined with prompt patterns such as **zero-shot, template, persona, chain-of-thought**, to have the model write requirements documents in a uniform structure.
- They defined three quality attributes: **Completeness** (whether the template is complete), **Degree of Realism / DoR** (how realistically similar the documents are to real SyRS), and **Semantic Similarity** (the degree of semantic overlap among different documents in the same domain, to avoid exact duplication).
- Completeness and DoR were mainly evaluated through LLM prompting; **Semantic Similarity** was computed using **SBERT all-mpnet-base-v2** to reduce the impact of hallucinations.
- To test the reliability of automatic scoring, the authors also conducted **cross-model validation**, comparing DoR scoring differences among **GPT-4o, GPT-5.2 (instant / thinking), and Sonnet 4.5**, supplemented by an expert survey study.

## Results
- The final dataset contains **300 SSyRS** covering **10 industries**; the iteration-10 dataset contains **21,478 words** in total, with an average of **716 words** per document, a median of **719**, a minimum of **644**, and a maximum of **811**.
- The **Completeness** result was the strongest: the authors state that **all SSyRS passed the completeness check**, meaning all elements required by the template were included.
- Overall **Semantic Similarity** had a mean of **0.66**, a median of **0.67**, and a range of **0.50–0.82**; domain means ranged from **0.59 (government)** to **0.73 (healthcare)**, indicating that the documents were related to each other but not entirely redundant.
- The expert study received **n=87** submissions (the paper also mentions **n=83 experts**), of which **62% of experts** considered these synthetic requirements documents to be **realistically credible**.
- However, **automatic DoR scoring was highly unstable and strongly model-dependent**: by model average, **GPT-4o same-context = 0.90**, **GPT-4o new-context = 0.86**, **GPT-5.2 instant = 0.85**, **GPT-5.2 thinking = 0.73**, **Sonnet 4.5 = 0.64**. This indicates that model choice has a much greater impact on “realism scoring” than context differences.
- In repeated testing with Sonnet 4.5, the DoR for the same healthcare document ranged from **0.48 to 0.73**, a spread of **0.25**, with a mean of **0.59** and a standard deviation of **0.08**; based on this, the authors explicitly point out that **quantitative DoR evaluation is highly unreliable**. In addition, deeper inspection found **self-contradictions and content deficiencies** in the documents, so the paper’s core conclusion is not that “LLMs can already reliably replace real requirements documents,” but rather that “**they can partially generate realistic synthetic requirements, but automatic evaluation is insufficient to replace expert review**.”

## Link
- [http://arxiv.org/abs/2603.09335v1](http://arxiv.org/abs/2603.09335v1)
