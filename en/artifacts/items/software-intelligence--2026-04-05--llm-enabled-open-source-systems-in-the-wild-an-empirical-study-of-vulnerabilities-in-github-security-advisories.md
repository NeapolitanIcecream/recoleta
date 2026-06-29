---
source: arxiv
url: http://arxiv.org/abs/2604.04288v1
published_at: '2026-04-05T22:07:31'
authors:
- Fariha Tanjim Shifat
- Hariswar Baburaj
- Ce Zhou
- Jaydeb Sarker
- Mia Mohammad Imran
topics:
- llm-security
- open-source-security
- software-vulnerabilities
- github-advisories
- supply-chain-security
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# LLM-Enabled Open-Source Systems in the Wild: An Empirical Study of Vulnerabilities in GitHub Security Advisories

## Summary
This paper studies how vulnerabilities show up in open-source software that uses LLM components, using GitHub Security Advisories from Jan 2025 to Jan 2026. It finds that the code-level bugs are mostly familiar software weaknesses, while LLM-specific risk appears more clearly at the system-design level through OWASP LLM categories.

## Problem
- The paper asks whether standard advisory fields such as CWE are enough to describe vulnerabilities in LLM-enabled open-source systems.
- This matters because LLM software connects prompts, model output, tools, file systems, APIs, and agents, so the path from input to harm can pass through model behavior that normal package metadata does not describe.
- If advisory schemas miss that layer, security teams can see the bug class but miss how LLM use, prompt flow, or tool authority makes exploitation possible.

## Approach
- The authors collected **295 GitHub Security Advisories** published between **January 2025 and January 2026** that referenced LLM-related terms.
- They manually reviewed **133 unique affected packages** and grouped them into **LLM-associated (84 packages, 226 advisories)**, **Possible LLM-associated (16 packages, 34 advisories)**, and **Non-LLM-associated (33 packages, 35 advisories)**.
- They then randomly sampled **100 advisories** from the first two groups and manually labeled them with the **OWASP Top 10 for LLM Applications 2025** to capture model-mediated exposure patterns.
- The core mechanism is simple: use **CWE** to describe the implementation bug, and use **OWASP LLM categories** to describe how LLM-specific system behavior exposes or amplifies that bug.
- Annotation reliability was reported as **Cohen's kappa = 0.76** and **Gwet's AC1 = 0.95**.

## Results
- Across the full **295-advisory** set, the authors found **99 distinct CWE IDs**. The most common were **CWE-94 code injection (24)**, **CWE-502 unsafe deserialization (22)**, **CWE-77 command injection (22)**, **CWE-78 OS command injection (19)**, **CWE-79 XSS (19)**, and **CWE-22 path traversal (18)**.
- In the **100-advisory** OWASP-annotated sample, the top LLM risk categories were **Supply Chain / LLM03 (44%)**, **Excessive Agency / LLM06 (20%)**, **Prompt Injection / LLM01 (18%)**, **Sensitive Information Disclosure / LLM02 (17%)**, **Unbounded Consumption / LLM10 (17%)**, **Improper Output Handling / LLM05 (12%)**, **Data and Model Poisoning / LLM04 (7%)**, and **Vector and Embedding Weaknesses / LLM08 (1%)**.
- **37%** of annotated advisories had multiple OWASP labels, which shows that many issues combine several stages such as prompt manipulation, unsafe output use, and privileged tool execution.
- The most common OWASP label combinations were **LLM03+LLM06 (12 cases)**, **LLM01+LLM05 (10)**, **LLM01+LLM06 (10)**, and **LLM01+LLM05+LLM06 (7)**.
- Advisory metadata covered package ecosystem and severity, but it did **not** include a structured field for LLM involvement. By ecosystem, the 295 advisories included **PyPI 162**, **npm 96**, **Go 22**, **Packagist 10**, **crates.io 3**, and **Maven 3**.
- The main claim is that the study found **no new LLM-specific implementation weakness classes**. The gap is in reporting: CWE captures the code defect, while OWASP LLM categories capture the model-mediated exposure path that GHSA metadata often misses.

## Link
- [http://arxiv.org/abs/2604.04288v1](http://arxiv.org/abs/2604.04288v1)
