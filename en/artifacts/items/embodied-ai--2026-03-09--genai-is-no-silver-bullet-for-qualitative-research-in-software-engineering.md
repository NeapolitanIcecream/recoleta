---
source: arxiv
url: http://arxiv.org/abs/2603.08951v1
published_at: '2026-03-09T21:35:36'
authors:
- Neil A. Ernst
- Christoph Treude
topics:
- software-engineering
- qualitative-research
- generative-ai
- llm-assisted-analysis
- research-methodology
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# GenAI Is No Silver Bullet for Qualitative Research in Software Engineering

## Summary
This is a position/review paper aimed at qualitative research in software engineering. Its core argument is that GenAI is helpful for some narrow, low-context qualitative tasks, but is far from capable of replacing human researchers. The authors emphasize that whether GenAI is appropriate depends on the research method, epistemological stance, and data type; localized successes cannot be generalized into “automated qualitative research.”

## Problem
- The paper addresses the question: **What exactly can GenAI help with in qualitative research in software engineering, and in which scenarios does it fail?** This matters because there is currently overly optimistic discourse in industry and academia claiming that **LLMs can automatically perform qualitative analysis**.
- This is important because qualitative research in software engineering deals with **a socio-technical system in which people and technology are intertwined**, often involving heterogeneous materials such as interviews, observations, code repositories, chat logs, tickets, and documents. Misusing GenAI could undermine **validity, reliability, reflexivity, and ethical compliance**.
- The authors also point out that different qualitative research strategies—such as deductive coding, thematic analysis, grounded theory, and ethnography—differ greatly in **context requirements, depth of interpretation, and the role of the researcher**. Therefore, a single successful AI case cannot represent the entire spectrum of qualitative research.

## Approach
- This is not a technical paper proposing a new model; its core method is **conceptual synthesis + literature evidence review + a small-scale paper scan**, used to systematically discuss the different dimensions of qualitative research in software engineering and the applicability of GenAI across those dimensions.
- The authors first break down the qualitative research spectrum by research strategies and methods, such as respondent/field/lab/data strategies, inductive/deductive/mixed coding, and constructivism versus post-positivism, using these dimensions to explain why GenAI can only fit some tasks.
- They then review existing empirical evidence, focusing on how **LLMs perform as additional coders, summarization/translation tools, and candidate-theme suggesters**, and compare their performance in low-context deductive labeling tasks versus tasks with a high interpretive burden.
- The paper also conducts a **preliminary review of conference paper usage in 2025**: it screens papers from ICSE, CHASE, and CSCW that use qualitative coding, and counts the share that report tool use or GenAI involvement in coding, in order to observe real-world adoption.
- Finally, put simply, the authors’ mechanistic conclusion is: **LLMs are more like “accelerators/assistant annotators” than “qualitative researchers capable of meaning-making.”** They are suitable for applying labels according to an existing codebook, but are not good at truly understanding complex situations, co-constructing meaning, or developing theory.

## Results
- The paper’s most direct empirical results come from its conference paper review: it examined **258 ICSE 2025 papers, 37 CHASE 2025 papers, and 312 CSCW 2025 papers**; among them, the numbers identified as containing qualitative coding were **25, 16, and 209**, respectively.
- Among these papers, the numbers reporting “tool use for coding” were **5 ICSE papers (1.9% of all papers), 2 CHASE papers (5.4%), and 20 CSCW papers (6.4%)**; only **CSCW had papers explicitly reporting the use of GenAI for coding: 7 papers (2.7% of all CSCW papers, 3.3% of its qualitative-coding papers), while ICSE/CHASE were both 0**.
- Based on this, the authors argue that **actual adoption of GenAI in qualitative research in software engineering is still very limited, and is concentrated mainly in newer CSCW papers and in more deductive/positivist tasks**, rather than having broadly entered inductive thematic analysis or grounded theory.
- External evidence reviewed in the paper shows that, in deductive labeling for requirements engineering, LLMs and human analysts can reach **Cohen's kappa > 0.7**, indicating “high agreement,” but **zero-shot performance is poor**, showing continued reliance on human-designed codebooks and prompts.
- Another cited study, covering **6 SOTA LLMs, 10 annotation tasks, and 5 datasets**, finds that for low-context tasks with clear labels, models can reach performance close to human inter-annotator agreement; but for high-context tasks requiring causal inference or explanation of static-analysis warnings, performance drops substantially.
- For more interpretive thematic analysis, the paper does not present a single strong quantitative advantage. Instead, its strongest claims are that **GenAI can improve efficiency and help with transcription, summarization, translation, and deductive coding, but is clearly inadequate for latent themes, contextual understanding, reflexivity, and constructivist methods, and cannot replace human researchers.**

## Link
- [http://arxiv.org/abs/2603.08951v1](http://arxiv.org/abs/2603.08951v1)
