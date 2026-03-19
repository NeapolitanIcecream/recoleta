---
source: arxiv
url: http://arxiv.org/abs/2603.11150v1
published_at: '2026-03-11T17:45:06'
authors:
- Marek Horvath
- Emilia Pietrikova
- Diomidis Spinellis
topics:
- programmer-attribution
- code-stylometry
- behavioral-biometrics
- systematic-survey
- software-forensics
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Bridging Behavioral Biometrics and Source Code Stylometry: A Survey of Programmer Attribution

## Summary
This is a systematic mapping survey on programmer attribution, reviewing research from 2012 to 2025 on identifying authors based on source code style and behavioral features. The paper’s core contribution is not to propose a new model, but to provide a unified organization of tasks, features, models, datasets, and evaluation practices, while pointing out the main gaps in the field.

## Problem
- The problem addressed is: how to identify or verify a programmer’s identity based on **stylistic, structural, or behavioral characteristics** in source code artifacts, and what features, models, data, and evaluation methods existing studies have used.
- This matters because programmer attribution is relevant to **software forensics, plagiarism detection, educational analytics, developer profiling, and security contexts**, yet existing research is scattered across multiple communities with inconsistent methodological conventions.
- The paper points out a clear imbalance in the field: research is **overly concentrated on closed-world authorship attribution and static code stylometric features**, while **behavioral signals, authorship verification, and reproducibility** remain underexplored.

## Approach
- It uses a **systematic mapping study** approach to systematically screen and categorize the programmer attribution literature, rather than training a new attribution model.
- The search covers **2012–2025**, using combinations of three keyword groups: authorship tasks, source code objects, and analysis methods, with searches conducted in **IEEE Xplore, ACM DL, Scopus**, supplemented by snowballing via **Google Scholar**.
- From **135** candidate papers, a structured inclusion/exclusion process narrowed the set to **47** empirical studies for analysis.
- A unified classification framework is built along multiple dimensions: **authorship task (attribution/verification)**, **feature type (stylistic/behavioral/hybrid)**, **learning model**, **dataset source**, and **evaluation method**.
- The paper proposes a **taxonomy** that maps **stylistic and behavioral features** to common machine learning techniques, and adds descriptive analyses of publication trends, benchmark datasets, programming languages, and thematic clusters.

## Results
- The paper’s main “results” are survey findings rather than improvements in model performance; the key reported numbers are that **47** studies were selected from **135** candidate publications, covering **2012–2025**.
- The study finds that the field is **strongly biased toward closed-world authorship attribution**, meaning most work assumes a known set of candidate authors rather than more realistic open-world settings or verification tasks.
- At the feature level, the literature mainly relies on **stylometric features** (such as lexical, syntactic, and structural features); in contrast, research on **behavioral signals** is much more limited.
- At the data level, the paper notes that research **relies heavily on a small number of benchmark datasets**, implying that conclusions may be constrained by dataset distribution, with insufficient cross-dataset generalization and ecosystem coverage.
- At the methodological level, the authors explicitly note that **reproducibility remain less explored**, meaning many studies lack sufficient reproducibility in data, preprocessing, and evaluation protocols.
- The abstract and excerpt **do not provide specific cross-paper aggregate metrics such as accuracy/F1/Top-k**; the strongest concrete claim is that this survey offers a unified framework and taxonomy, and systematically identifies research gaps in behavioral features, authorship verification, and the standardization of data and evaluation.

## Link
- [http://arxiv.org/abs/2603.11150v1](http://arxiv.org/abs/2603.11150v1)
