---
source: arxiv
url: http://arxiv.org/abs/2603.14191v1
published_at: '2026-03-15T03:01:13'
authors:
- Dectot--Le Monnier de Gouville Esteban
- Mohammad Hamdaqa
- Moataz Chouchen
topics:
- yara-rules
- threat-intelligence
- ecosystem-mining
- malware-detection
- detection-as-code
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Mining the YARA Ecosystem: From Ad-Hoc Sharing to Data-Driven Threat Intelligence

## Summary
This paper provides the first large-scale, data-driven systematic characterization of the open-source YARA ecosystem, showing that although it is widely used for “Detection as Code,” it overall resembles an outdated, copy-propagated rule warehouse rather than a high-quality intelligence source. Combining repository mining, static analysis, and dynamic benchmarking, the study reveals systemic problems such as centralization, lag, and insufficient detection effectiveness.

## Problem
- The paper addresses the problem that the open-source YARA rule ecosystem has long relied on ad-hoc sharing, but lacks systematic evidence about its structure, maintenance status, propagation mechanisms, and actual detection performance.
- This matters because YARA has become the de facto standard for malware detection and software supply chain defense; if shared rules are outdated, noisy, or coverage-skewed, defenders incur additional performance costs in CI/CD and security operations without receiving effective protection.
- Existing work mostly focuses on individual rule quality, syntax checking, or automatic generation, rather than validating at the ecosystem level whether “public rule repositories are actually reliable and usable.”

## Approach
- The authors conducted a mixed-method study of **8.4 million rules** across **1,853 GitHub repositories**, building an eight-stage pipeline to analyze rule discovery, extraction, deduplication, propagation, author influence, quality, and threat coverage.
- They first performed repository mining: discovering YARA projects on GitHub, extracting rules, and cross-validating on a **10% random subset (about 840,000 rules)** with Plyara, reporting **100% agreement** with their regex-based extraction results.
- To identify rules that are “logically identical but textually slightly different,” the paper used **ssdeep fuzzy hashing** and hierarchical clustering, aggregating near-duplicate rules at a **65% similarity threshold** and yielding **94,400 unique rule logics**.
- To analyze ecosystem propagation, they distinguished “source repositories” from “mirror repositories” based on first-seen time, first-publisher ratio, and technical lag, measuring the delay from rule creation to adoption by other repositories.
- To assess real-world reliability, they compared static quality scores (yaraQA) with dynamic detection performance, and tested false positives, recall, and coverage bias on **4,026 malicious samples** and **2,000 benign samples**.

## Results
- In terms of scale, the paper analyzed **1,853 repositories and 8.4 million rules**, ultimately aggregating them into **94,400 unique rule logics**, indicating large-scale copying and redundancy in the ecosystem.
- Author influence is highly concentrated: **the top 10 authors drive 80% of rule adoption**, showing that the ecosystem is not a distributed collaboration network but a centralized supply chain dominated by a small number of key nodes.
- Ecosystem updates are clearly stagnant: repositories have a **median inactivity of 782 days** and a **median technical lag of 4.2 years**, suggesting that public repositories function more like static archives than continuously updated intelligence feeds.
- Static quality appears high on the surface: rules have an **average static quality score of 99.4/100**; however, dynamic benchmarking shows a disconnect from real-world performance, and the authors explicitly state that there are **significant false positives** and **low recall**.
- The coverage distribution is clearly biased: rules are more focused on traditional high-exposure threats such as **Ransomware**, while coverage of modern initial access vectors such as **Loaders** and **Stealers** is **severely insufficient**.
- In method validation, near-duplicate detection after ssdeep threshold tuning achieved **F1 = 0.77** on an adversarial benchmark; rule extraction reached **100% agreement** with a formal parser on the **10% subset**. The paper does not provide, in the given excerpt, more detailed false-positive rates, recall values, or complete dataset-stratified comparisons.

## Link
- [http://arxiv.org/abs/2603.14191v1](http://arxiv.org/abs/2603.14191v1)
