---
source: arxiv
url: http://arxiv.org/abs/2603.01520v1
published_at: '2026-03-02T06:50:28'
authors:
- Jukka Ruohonen
- Esmot Ara Tuli
- Hiraku Morita
topics:
- compliance-as-code
- linux-distributions
- cybersecurity-compliance
- security-controls
- cra-mapping
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Compliance as Code: A Study of Linux Distributions and Beyond

## Summary
This paper conducts a large-scale empirical analysis of a real-world open source “compliance as code” project, examining compliance rule coverage in Linux distributions, similarity, control sources, and mapping to EU CRA requirements. Its importance lies in providing rare empirical data for automated, continuous cybersecurity compliance and evaluating its scalability for CRA enforcement in 2027.

## Problem
- The paper addresses the problem that existing research on “compliance as code” is scarce, and there is a lack of systematic empirical analysis of real compliance rule repositories themselves. It is unclear how rule coverage differs across Linux distributions, how similar the rules are to one another, which security controls they cover, and whether these rules can support new regulations such as the CRA.
- This matters because manual compliance checks and system hardening are difficult to scale and prone to errors, while regulatory requirements—especially the EU Cyber Resilience Act—are increasing, creating a need for automated, continuous compliance verification.
- It specifically focuses on four questions: whether rule coverage differs across five Linux distribution vendors; whether rule text/code is similar; which external security controls the rules cover; and whether the rules can be mapped to the CRA’s essential cybersecurity requirements.

## Approach
- The authors selected archived data from the ComplianceAsCode project as of 2025-11-20 and built a dataset covering **5** vendors, **14** Linux distribution releases, **102** guides, and **1,504** unique rules.
- They used descriptive statistics and the Kruskal-Wallis test to compare differences in the number of guides, number of rules, number of rules with warnings, and severity distributions across different vendors/versions.
- To analyze rule similarity, they extracted each rule’s short rationale and code snippet, tokenized them, and applied **cosine similarity** using both **TF** and **TF-IDF** weighting. The core idea is simple: to see whether rule descriptions and scripts are essentially approximate templates with only a few words/parameters changed.
- To assess regulatory relevance, the authors manually mapped rules to **12** groups of CRA essential requirements defined in prior research, using one-to-one mapping; they also performed blind inter-rater validation on **500** randomly selected rules by three authors, using Cohen/Fleiss kappa to examine subjectivity.
- They also counted the external security control sources referenced by the rules and analyzed their coverage across organizations and standards.

## Results
- In terms of data scale, the authors report **102** guides, **1,504** unique rules, covering **14** releases and **5** vendors; each release has on average about **12** guides, **740** rules, and **179** rules with warnings.
- There are significant differences in release coverage: for example, **RHEL 10** has **1,000** rules, accounting for about **66%** of all unique rules; by contrast, **Debian 11** has only **51**, and **Ubuntu 24.04** has **635**. Kruskal-Wallis tests across vendors show statistically significant differences for guides, rules, and rules-with-warnings (**p=0.036, 0.031, 0.031**, respectively).
- In terms of rule severity, most rules are **medium**; across vendors, only the frequency differences in the medium category reach conventional significance levels (**p=0.031**), while low/high/others are **p=0.087/0.054/0.209**, indicating that severity structure is generally more similar, while coverage scale differs more.
- The similarity analysis shows that **code snippets are more similar than natural-language rationales**, and TF shows more similarity than TF-IDF. The authors do not provide specific average similarity values in the given excerpt, but they clearly claim that there is some template-like reuse at the code level, while no statistical similarity exists among the rationales.
- In terms of external control coverage, the rules map to **24** control categories from **10+** organizations. The most covered include **os-srg: 835** rules, **nist: 808**, **stigid: 734**, **stigref: 723**, and **cis: 703**; several of these controls span **14** products and **5** vendors.
- Regarding the CRA, the authors argue that these rules **can** be mapped to the CRA’s essential cybersecurity requirements, meaning the existing project could potentially support future regulatory compliance by adding new checks; however, agreement among the three authors on individual rule mappings is only **modest**. The excerpt does not provide specific kappa values, so more precise quantitative agreement results cannot be reported.

## Link
- [http://arxiv.org/abs/2603.01520v1](http://arxiv.org/abs/2603.01520v1)
