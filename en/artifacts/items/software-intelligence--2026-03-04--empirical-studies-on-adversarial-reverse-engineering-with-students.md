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
- empirical-software-engineering
- human-subjects
- software-protection
- study-methodology
relevance_score: 0.27
run_id: materialize-outputs
language_code: en
---

# Empirical Studies on Adversarial Reverse Engineering with Students

## Summary
This paper discusses how to use students rather than professional reverse engineers to conduct empirical studies of adversarial reverse engineering, and summarizes how to design such studies so they are more rigorous, reproducible, and externally valid. Drawing on a systematic literature review and the authors' own teaching-experiment experience, it provides methodological recommendations rather than new reverse-engineering algorithms.

## Problem
- Adversarial reverse engineering and software protection require **human-subject experiments** to evaluate real-world protection effectiveness, but recruiting professional reverse engineers is difficult, expensive, and yields small samples.
- Using students makes experiments easier to run, but introduces **external validity** concerns: students' experience, skills, and motivation differ from those of professionals, which may distort conclusions.
- There are very few existing human experiments in this area, and they often have methodological issues; the authors cite a 2025 review stating that among **571** software-protection evaluation papers, only **21** reported human-subject studies.

## Approach
- The authors first conducted a systematic literature review on **human experiments and user studies** in adversarial reverse engineering / malware analysis.
- Literature search process: starting from an existing seed set of **19** RE-related human-experiment papers, they searched Web of Science and obtained **81** records; after deduplication and screening, **9** were retained. They then performed forward citation tracking on the merged set of **26** papers, added **8** more, and ultimately included **36** papers for analysis.
- Data extraction used multi-researcher coding: each paper was independently coded by at least **3** authors, then consolidated by senior authors and reconciled through discussion.
- After removing duplicate reports, the authors analyzed **31** independent studies, focusing on experimental motivation, participant types and counts, student training, task design, data collection, privacy, and ethics.
- In addition to the literature review, the authors also draw on their own experience running student experiments in a master's course, discussing how to train students, control for skill heterogeneity, protect privacy, and improve experimental rigor.

## Results
- The clearest quantitative finding comes from the literature's scale and scarcity: in a prior review covering **571** software-protection evaluation papers, only **21** included human-subject studies, showing that the empirical human-evidence base in this area is very weak.
- The paper's own systematic review ultimately included **36** papers; **5** of these were duplicate reports of other experiments, so the count of independent experiments/studies is **31**.
- Regarding participant composition, the review shows that many studies did use students, but also included professionals and practitioner surveys; the paper's central conclusion is that **students can serve as a practical substitute sample, but training, experimental design, and threat-mitigation measures are required to reduce external-validity risks**.
- Methodologically, the authors claim four categories of contributions: the systematic review, integration of related work across SE/RE, lessons from their own course experiments, and recommendations for future experiments. These are **advances at the methodology and research-design level**, not SOTA results in model or tool performance.
- The provided excerpt **does not report specific performance metrics** (such as task success rate, time savings, statistical significance, or numerical comparisons with baseline tools); the strongest concrete claim is that successfully running student-based RE experiments remains difficult, but under resource constraints, more meaningful and reproducible results can be obtained through more disciplined training, data collection, ethics, and experimental design.

## Link
- [http://arxiv.org/abs/2603.03875v1](http://arxiv.org/abs/2603.03875v1)
