---
source: arxiv
url: http://arxiv.org/abs/2603.14191v1
published_at: '2026-03-15T03:01:13'
authors:
- Dectot--Le Monnier de Gouville Esteban
- Mohammad Hamdaqa
- Moataz Chouchen
topics:
- yara
- threat-intelligence
- malware-detection
- software-ecosystem
- repository-mining
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Mining the YARA Ecosystem: From Ad-Hoc Sharing to Data-Driven Threat Intelligence

## Summary
This paper presents the first large-scale empirical characterization of the open-source YARA ecosystem, showing that its sharing model is highly centralized, updates are slow, and real-world detection performance is unstable. The authors argue that current public rule repositories are more like “raw data dumps” than directly trustworthy, high-quality threat intelligence sources.

## Problem
- The paper addresses the following problem: although the open-source YARA rule ecosystem is widely used for malware detection, its structure, maintenance status, propagation speed, and real detection reliability have long lacked systematic evidence.
- This matters because security teams and DevSecOps workflows directly reuse these public rules; if the rules are outdated, noisy, or imbalanced in coverage, defenders pay the scanning performance cost without receiving effective detection benefits.
- Existing methods mostly focus on the syntax of individual rules or automatic generation, but lack a global evaluation of whether the entire sharing ecosystem is trustworthy, timely, and covers modern threats.

## Approach
- The authors built a mixed-method pipeline to mine and analyze **8.4 million** YARA rules from **1,853** GitHub repositories at scale.
- They used repository mining and commit history to analyze ecosystem structure and propagation: identifying “source repositories” and “mirror repositories,” and measuring rule reuse, author influence, and technical lag.
- They used fuzzy hashing **ssdeep** to cluster near-duplicate rules, compressing massive textual rules into **94.4k** clusters of “unique rule logic”; under an adversarial benchmark, they selected a **65%** similarity threshold and obtained **F1=0.77**.
- They used the static analysis tool **yaraQA** to assess syntactic/structural quality, and dynamically benchmarked rules on **4,026** malware samples and **2,000** benign samples to compare the gap between “looking well written” and “actually detecting effectively” in practice.
- They used semi-automated threat classification to analyze rule coverage across different malware families, checking whether the ecosystem is biased toward older threats while neglecting today’s more critical initial access vectors.

## Results
- In terms of scale, the paper analyzed **1,853** GitHub repositories and **8.4 million** rules, and clustered them into **94.4k** unique rule logic groups, making this the first large-scale ecosystem study of its kind.
- The ecosystem is highly centralized: just **10** authors drive **80%** of rule adoption, indicating that rule influence is concentrated in the hands of a very small number of core contributors.
- Ecosystem updates are extremely slow: repositories have a **median inactivity period of 782 days**, and rule propagation shows a **median technical lag of 4.2 years**, indicating that many repositories resemble static archives rather than continuously updated intelligence sources.
- Static quality appears high on the surface: the **average yaraQA score is 99.4/100**; however, the authors argue that this does not align with real-world effectiveness, and many “syntactically perfect” rules still produce substantial false positives and low recall at runtime.
- The dynamic evaluation used **4,026** malware samples and **2,000** benign samples; the provided abstract/excerpt **does not give finer-grained false positive rates, recall values, or specific numerical comparisons against baselines**, but the core conclusion is that there is “significant noise (false positives) and low recall.”
- Threat coverage shows a systemic bias: rules are clearly skewed toward traditional high-profile threats such as **Ransomware**, while coverage of modern initial access vectors such as **Loaders** and **Stealers** is severely insufficient. The authors summarize this as a “**double penalty**” for defenders—high scanning overhead for decayed intelligence.

## Link
- [http://arxiv.org/abs/2603.14191v1](http://arxiv.org/abs/2603.14191v1)
