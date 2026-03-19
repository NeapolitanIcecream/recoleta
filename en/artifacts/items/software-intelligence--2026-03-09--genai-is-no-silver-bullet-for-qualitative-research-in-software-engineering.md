---
source: arxiv
url: http://arxiv.org/abs/2603.08951v1
published_at: '2026-03-09T21:35:36'
authors:
- Neil A. Ernst
- Christoph Treude
topics:
- generative-ai
- qualitative-research
- software-engineering
- llm-evaluation
- research-methodology
relevance_score: 0.55
run_id: materialize-outputs
language_code: en
---

# GenAI Is No Silver Bullet for Qualitative Research in Software Engineering

## Summary
This is a position/review paper on qualitative research in software engineering. Its core argument is that GenAI can help with some narrowly defined tasks, but it is far from a “silver bullet” for qualitative research. The authors systematically review different types of qualitative research in software engineering, the current evidence, potential benefits and risks, and argue for cautious, context-sensitive use with full disclosure.

## Problem
- The paper addresses the question: **where exactly can GenAI help in qualitative software engineering research, and where does it fail**, because the community currently tends to overgeneralize a small number of success cases to the entire qualitative research workflow.
- This matters because qualitative software engineering research deals with **a socio-technical system in which people and technology are intertwined**, involving heterogeneous data, strong contextual dependence, and high interpretive demands. If GenAI is mistakenly treated as an automated replacement, it may undermine **validity, reliability, reflexivity, and ethics**.
- The authors especially note that most existing evidence comes from **low-context, deductive coding** tasks, which cannot represent more interpretive research methods such as theme generation, grounded theory, or ethnography.

## Approach
- This is not a paper proposing a new model, but rather **conceptual framing + a preliminary literature review + evidence synthesis**. It first defines the spectrum and key dimensions of qualitative research in software engineering, such as epistemological stance, coding strategy, data granularity, iteration style, and the role of the researcher.
- Put simply, its core mechanism is: **break “qualitative research” into different tasks and methods, then assess one by one whether GenAI is appropriate**, rather than treating all qualitative research as the same kind of automatable work.
- The paper also conducts a **preliminary survey of usage in some 2025 conference papers**, checking which papers in ICSE, CHASE, and CSCW reported using GenAI/LLM in coding, and which only reported the use of conventional QDA tools.
- On this basis, the authors conclude that GenAI has already been used for three types of work: **deductive coding/labeling, summarization and translation, and conceptual support/candidate code suggestions**. They also analyze its epistemological mismatch with constructivist and reflexive forms of analysis.
- Finally, the paper revisits quality criteria from the perspectives of **reliability, validity, ethics, and governance**, arguing that GenAI should be treated as a supervised assistive tool rather than an autonomous qualitative researcher.

## Results
- The paper’s main “results” are evidence synthesis and an empirical scan, rather than a new benchmark. The authors’ preliminary review of 2025 conference papers finds that **CSCW 2025 had 7 papers that substantively used GenAI for qualitative analysis; ICSE 2025 and CHASE 2025 had 0 each**.
- In their screening data, the total numbers of papers at the three conferences were **ICSE 258, CHASE 37, CSCW 312**; among these, the numbers identified as qualitative coding papers were **25, 16, 209**; the numbers reporting “use of coding tools” were **5, 2, 20**; and the numbers reporting “GenAI used for coding” were **0, 0, 7**.
- Based on this, the authors report usage rates: **in CSCW, the prevalence of GenAI used for coding was 7/209 = 3.3%**. They also report tool-use proportions of **CSCW 6.4%, ICSE 1.9%, CHASE 5.4%**, while the reported proportions for GenAI coding were **CSCW 2.7%, ICSE 0%, CHASE 0%**.
- Their synthesis of prior external empirical work shows that in deductive labeling tasks in requirements engineering, LLMs acting as a second annotator can achieve **Cohen's kappa > 0.7**, but **zero-shot performance is poor**, indicating that success depends on human-prepared codebooks and prompt design.
- Another cited study found, across **6 frontier LLMs, 10 labeling tasks, and 5 datasets**, that models can approach human agreement on **low-context deductive tasks**, but perform significantly worse on tasks requiring causal inference and contextual understanding.
- The paper’s strongest overall conclusion is not a new performance record, but rather this: **the most credible current value of GenAI lies in transcription, narrow deductive coding, summarization/translation, and assisted candidate code generation; for highly interpretive work such as theme development, theory building, and ethnography, there is insufficient evidence, and significant risks remain, including bias, hallucinations, prompt sensitivity, reproducibility issues, and epistemological mismatch.**

## Link
- [http://arxiv.org/abs/2603.08951v1](http://arxiv.org/abs/2603.08951v1)
