---
source: arxiv
url: http://arxiv.org/abs/2603.03875v1
published_at: '2026-03-04T09:27:46'
authors:
- Tab
- Zhang
- Bjorn De Sutter
- Christian Collberg
- Bart Coppens
- Waleed Mebane
topics:
- reverse-engineering
- software-protection
- empirical-study
- user-study
- student-participants
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Empirical Studies on Adversarial Reverse Engineering with Students

## Summary
This paper studies how to conduct **human-subject experiments in adversarial reverse engineering** using students rather than professional reverse engineers, and summarizes how to design studies, provide training, collect data, and handle ethical issues so that results are more rigorous and reproducible. Combining a systematic literature review with the authors’ own course-based experimental experience, it offers practical recommendations for future research.

## Problem
- The paper addresses the question of whether **students can serve as a viable substitute for professional participants in empirical reverse engineering research** when professional reverse engineers are difficult to recruit and expensive, and how to reduce the resulting risks to external validity.
- This matters because evaluating software protection and reverse engineering requires **real human attack and analysis behavior**; theoretical analysis or automated evaluation alone is often insufficient.
- Human-subject studies in this area are still rare, and existing work often has methodological problems in participant selection, training, measurement, and ethics, which affect the credibility and reproducibility of results.

## Approach
- The authors first conducted a **systematic literature review**: starting from 19 relevant papers identified in prior reviews as seeds, they combined Web of Science searches with forward citation tracking in Google Scholar, ultimately including **36 papers** involving human-subject experiments, user studies, or practitioner surveys related to reverse engineering or malware analysis.
- Study selection followed a two-round process: titles and abstracts were first screened to exclude non-empirical studies and non-peer-reviewed work, followed by full-text screening that retained only studies with **human participants** focused on RE tasks, tools, software protection strength, or analysis workflows.
- Data extraction used **independent coding by multiple researchers, consolidation by a senior author, and discussion to resolve disagreements**, improving review reliability; each paper was independently coded by at least **3 authors**.
- Beyond the review, the authors also summarize their experience running student experiments in a **master-level software hacking and protection course**, focusing on how to embed experiments into a course, train students, deal with heterogeneity in student ability, collect fine-grained data, and ensure privacy, motivation, and genuinely voluntary consent.
- The final output is a set of **methodological recommendations**. The core contribution is not a new algorithm, but a more actionable research design framework for RE human-subject experiments, helping balance cost, feasibility, and validity under real-world constraints.

## Results
- One key finding from the literature review is that, in an earlier survey covering **571 papers** on software protection, only **21 papers** reported human-subject experiments; after further aggregation, this paper identifies **36 relevant papers**, with **31 unique papers** used for statistical presentation after deduplication, indicating that the human-evidence base in this research area remains limited.
- The specific numbers in the search process are: **19 papers** in the RE-related seed set; a Web of Science query returned **81** records, from which **9 papers** were added after screening; forward citation tracking then added **8 papers**; this produced a final set of **36 papers** included in the analysis.
- The authors’ claimed main contribution is not improved performance, but **four methodological contributions**: a systematic review, a discussion of related work across SE/RE, a summary of their own course-based experimental experience, and a list of recommendations for future experiments.
- The paper explicitly states that its own course experiments show that **successfully conducting this type of student-based experiment remains difficult**; this is one of the strongest empirical conclusions in the paper, but the excerpt **does not provide comparable quantitative effect metrics** such as accuracy, time reduction, or significance-test results.
- In terms of review coverage, the paper shows that student participation in RE experiments is widespread: the table includes many studies using students, with participant counts ranging from single digits to several dozen, and one ambiguously described study reporting **425** participants; however, the excerpt does not provide unified aggregate statistics or meta-analytic effect sizes.
- Therefore, the paper’s “results” are better understood as a **methodological and evidentiary synthesis** rather than an algorithmic breakthrough: it argues that through better training, task design, data collection, and ethical procedures, RE experiments using students can become more rigorous, reproducible, and closer to professional practice.

## Link
- [http://arxiv.org/abs/2603.03875v1](http://arxiv.org/abs/2603.03875v1)
