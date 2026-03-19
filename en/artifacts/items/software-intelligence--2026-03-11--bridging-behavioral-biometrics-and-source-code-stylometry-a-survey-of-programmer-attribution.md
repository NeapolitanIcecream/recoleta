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
- source-code-stylometry
- behavioral-biometrics
- systematic-survey
- software-forensics
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Bridging Behavioral Biometrics and Source Code Stylometry: A Survey of Programmer Attribution

## Summary
This paper is a systematic mapping review of programmer attribution, organizing research from 2012–2025 on identifying authors based on source code style and behavioral features. Its main contribution is providing a unified taxonomy and pointing out clear gaps in the current field regarding behavioral signals, authorship verification, and reproducibility.

## Problem
- The paper addresses the problem of how to systematically organize the research landscape on “identifying the author of source code through source code and related behavioral features,” and clarify the relationships among different features, models, datasets, and evaluation methods.
- This is important because programmer attribution can be used in software forensics, plagiarism detection, educational analytics, developer profiling, and recruitment, yet existing research is scattered across software engineering, security, and digital forensics, with inconsistent methods and terminology.
- The authors specifically point out that most existing work focuses only on static code style, with relatively little study of programming behavioral signals, leaving the full picture of the field and its methodological gaps unclear.

## Approach
- The core method is a **systematic mapping study**: rather than proposing a new attribution model, the paper retrieves, screens, codes, and compares existing studies according to a predefined process.
- The authors start from **135** candidate publications and, through structured screening, ultimately include **47** studies published between **2012-2025**.
- The analysis dimensions include: authorship tasks (attribution / verification), feature types (stylometric, behavioral, hybrid), learning models, dataset sources, preprocessing pipelines, and evaluation methods.
- At the simplest level, what this paper does is organize prior research into a unified taxonomy based on “what signals were used, what models were paired with them, what data they were tested on, and how they were evaluated,” while also summarizing trends and gaps.
- The study also incorporates content-level thematic analysis to identify the main research clusters in the field, and provides reproducibility resources for the extracted attributes and statistical scripts (with a Zenodo link provided).

## Results
- In terms of literature coverage: **47** empirical studies were selected from **135** candidate publications, covering the period **2012-2025**.
- One of the paper’s core findings is that existing research is **strongly biased toward closed-world authorship attribution**, rather than the more difficult and more realistic authorship verification/open-world settings.
- In terms of feature usage: the review states that the field **mainly concentrates on stylometric features** (lexical, syntactic, structural, and other static code style features), while research on **behavioral signals** is clearly insufficient.
- Regarding data and evaluation: the authors note that the literature **relies heavily on a small number of benchmark datasets**, and that **reproducibility remains weak**; this means comparisons between methods may be significantly influenced by dataset and protocol choices.
- In terms of contribution: the paper claims to propose a unified taxonomy linking **stylometric/behavioral features** with **common machine learning techniques**, and provides a descriptive review of publication trends, benchmark datasets, and programming language distributions.
- As for quantitative performance results: the provided abstract and excerpt **do not report specific task performance numbers** (such as accuracy/F1 improvements or percentage gains over a baseline); the strongest quantifiable conclusions are mainly the literature scale and screening outcome (**135→47, 2012-2025**).

## Link
- [http://arxiv.org/abs/2603.11150v1](http://arxiv.org/abs/2603.11150v1)
