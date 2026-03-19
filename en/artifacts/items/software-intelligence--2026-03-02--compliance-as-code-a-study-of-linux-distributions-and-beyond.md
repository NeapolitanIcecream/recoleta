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
- security-controls
- automated-compliance
- cyber-resilience-act
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Compliance as Code: A Study of Linux Distributions and Beyond

## Summary
This paper conducts a large-scale empirical analysis of a real-world open-source “compliance as code” project, examining compliance rule coverage in Linux distributions, rule similarity, coverage of external control frameworks, and mappings to EU CRA requirements. Its importance lies in showing that compliance checks can be programmatically encoded, and in providing early evidence for automated compliance under the Cyber Resilience Act, which will take effect starting in 2027.

## Problem
- The paper addresses the following problem: there is very little existing research on “compliance as code,” and there is a lack of empirical analysis of real compliance rule repositories, making it unclear how rule coverage, reuse patterns, and regulatory adaptability differ across Linux distributions.
- This matters because manual compliance checking is hard to scale and prone to errors, while operating systems in network-connected products will soon be subject to regulations such as the CRA, making automated and continuous compliance increasingly important.
- The authors also specifically ask whether these existing rules can support future regulatory updates, especially the CRA’s essential cybersecurity requirements.

## Approach
- Using the ComplianceAsCode project as a case study, the authors collected **102** guides, covering **14** Linux distribution versions and **1,504** unique rules from **5** vendors/communities.
- Through descriptive statistics and the **Kruskal-Wallis** test, they compared differences in the distributions of guides, rules, warnings, and severities across vendors/releases.
- They performed **cosine similarity** analysis separately on the rules’ short rationales and code snippets, using **TF** and **TF-IDF** weighting, to assess similarity at the textual explanation and implementation levels.
- They counted the external security controls referenced by the rules, finding coverage of **24** control categories from **10+** organizations, including NIST, DISA, CIS, ISO, ANSSI, BSI, PCI SSC, and others.
- They manually mapped the rules to **12** groups of CRA essential requirements, and used blinded three-author evaluation on **500** randomly sampled rules plus kappa agreement checks to assess subjectivity; the authors note that agreement for some individual mappings was only “moderate.”

## Results
- In terms of scale, the paper analyzed **1,504** unique rules and **102** guides; each release had on average about **740** rules, **12** guides, and **179** rules with warnings. Coverage differences were clear: **RHEL 10** had **1,000** rules, about **66%** of all unique rules; by contrast, **Debian 11** had only **51** rules, and **Ubuntu 24.04** had **635**.
- Statistical tests showed significant cross-vendor differences in coverage: Kruskal-Wallis **p=0.036** for guides, **p=0.031** for rules, and **p=0.031** for rules with warnings; for severity, only the **medium** category was significant (**p=0.031**), while low/high/others were not significant (respectively **p=0.087/0.054/0.209**).
- On average, slightly less than **1/4** of the rules had warnings; in the severity distribution, most rules were labeled **medium**, and the overall pattern was similar across distributions.
- The similarity analysis showed that the rules’ **code snippets** were **more similar** than their natural-language rationales, and the two kinds of similarity were **uncorrelated** with each other; the authors did not provide a unified threshold or a complete numeric table, but explicitly noted that TF detected more similarities than TF-IDF, and that code reuse/template-like patterns were evident.
- In terms of control coverage, the rules could be mapped to **24** control categories across **10+** organizations; highly covered controls included **os-srg: 835** rules, **nist: 808**, **stigid: 734**, **stigref: 723**, and **cis: 703**, indicating that the project is already connected to multiple mainstream security baselines and standards.
- Regarding regulatory fit, the authors claim that these rules **can be mapped to the CRA’s essential cybersecurity requirements**, suggesting that the project could be extended in the future to support new automated compliance checks; however, in the manual validation of the **500**-rule sample, agreement among the three authors on individual rule mappings was only **moderate/limited**, indicating that this part still involves substantial interpretation.

## Link
- [http://arxiv.org/abs/2603.01520v1](http://arxiv.org/abs/2603.01520v1)
