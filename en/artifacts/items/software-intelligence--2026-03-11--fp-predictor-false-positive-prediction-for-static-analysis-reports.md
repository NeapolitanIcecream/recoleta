---
source: arxiv
url: http://arxiv.org/abs/2603.10558v1
published_at: '2026-03-11T09:05:39'
authors:
- Tom Ohlmer
- Michael Schlichtig
- Eric Bodden
topics:
- static-analysis
- false-positive-prediction
- graph-neural-network
- code-property-graph
- software-security
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# FP-Predictor - False Positive Prediction for Static Analysis Reports

## Summary
This paper proposes **FP-Predictor**, which uses a graph convolutional network to predict whether static application security testing (SAST) reports are **true positives or false positives** at the report level, in order to reduce the cost for developers of handling false alarms. The core idea is to convert the reported code fragment into a code property graph, then let the model learn code structure and semantics to judge whether the alert is trustworthy.

## Problem
- Although SAST tools can automatically discover potential vulnerabilities, they produce **many false positives**, which wastes developers’ investigation time, slows down the remediation of real vulnerabilities, and weakens trust in automated security analysis.
- Traditional rule-based/pattern-matching methods struggle to capture the complex code structure, control flow, and data dependencies that determine **whether a report is truly dangerous**.
- The paper focuses on the scenario of **Java cryptographic API misuse**, especially how to post-process and filter existing static analysis alerts, rather than directly detecting vulnerabilities from code.

## Approach
- The method constructs the code of the method corresponding to each SAST alert into a **Code Property Graph (CPG)**, integrating three program views: **AST, CFG, and PDG**, to represent syntax, control flow, and data dependency relationships.
- It uses a **GCN** to perform graph learning on the CPG and outputs a score in the range \[0,1\]; the paper uses a **0.8 threshold**, where scores above the threshold are classified as false positives, and otherwise as true positives.
- Each graph node contains three types of features: a **Word2Vec vector of the Jimple statement**, a **one-hot encoding of the node type**, and a marker indicating whether it is a **violation node**.
- The model is trained and tested on **CamBenchCAP** (with an 80/20 split), then transferred to **CryptoAPI-Bench** to evaluate generalization; input alerts come from **CogniCrypt 5.0.2**.
- Mechanistically, this can be simply understood as turning the “code context around an alert” into a graph, allowing the model to learn whether “this kind of structure is usually a real vulnerability or a false positive.”

## Results
- On **CamBenchCAP**, using an **80/20 train-test split**, the model reports **100% accuracy** on the test set; the authors also acknowledge that the dataset contains only **431** labeled samples and is relatively structured/synthetic, which may overestimate generalization ability.
- On **CryptoAPI-Bench**, under automatic evaluation: among **91** alerts for real vulnerabilities, it correctly identified **89/91** as true positives, for a true-positive-side accuracy of about **97.8%**; among **27** false alerts triggered by safe examples, it identified only **1/27** as false positives, for a false-positive-side accuracy of about **3.7%**.
- After manual review, the authors argue that **22/26** of the initial “misclassifications” actually contain real security issues or poor cryptographic practices, so the “effective accuracy” on the false-positive side could increase from **1/27 (3.7%)** to **23/27 (85.2%)**.
- Based on the above manual re-evaluation, the paper claims overall accuracy can reach **96.6%**; if the ground truth is not adjusted for **3** “disputed but unlabeled-changed” bad-practice cases, then the overall accuracy is **94.1%**.
- The paper also reports training cost: on a PC with **Intel i7-11700K + RTX 4090 + 64GB RAM**, model training takes about **5 minutes**.
- The main limitation is that the current CPG **lacks interprocedural/interclass connections**, making scenarios with complex control flow such as `if` statements or cross-method dependencies harder to handle; the authors plan to add a **call graph** and graph explainability methods.

## Link
- [http://arxiv.org/abs/2603.10558v1](http://arxiv.org/abs/2603.10558v1)
