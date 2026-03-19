---
source: arxiv
url: http://arxiv.org/abs/2603.05637v1
published_at: '2026-03-05T19:47:26'
authors:
- Mina Taraghi
- Mohammad Mehdi Morovati
- Foutse Khomh
topics:
- model-context-protocol
- software-testing
- bug-taxonomy
- llm-software
- empirical-software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy

## Summary
This paper proposes the first large-scale, empirically grounded taxonomy of real faults in MCP (Model Context Protocol) servers. Its significance lies in helping build more reliable and secure software for LLM tool use and integration with external resources.

## Problem
- Existing research has discussed general LLM software defects, but there is a **lack of systematic understanding of real faults in MCP software**.
- MCP is becoming a standard interface between LLMs and tools, resources, and host applications, so its faults directly affect **reliability, security, robustness, and interoperability**.
- Without understanding MCP-specific fault types, it is difficult to design targeted testing, debugging, and engineering practices, especially in safety-critical scenarios where the impact is greater.

## Approach
- The authors systematically collected repositories related to the MCP Python SDK from GitHub: they first identified **13,555** candidate repositories, then filtered them down to **385** real MCP server repositories.
- From these repositories, they extracted **30,795** closed issues; after filtering out non-English issues, **26,821** remained. They then used an LLM to classify **3,591** bug-related issues, and after removing stale, duplicate, and unreproducible cases, obtained **3,282** valid bug issues.
- To focus on MCP-related defects, the authors first used an LLM to summarize issue titles, bodies, and comments, then applied **BERTopic + embedding + UMAP + KMeans** clustering to divide the **3,282** bug issues into **101** clusters.
- On this basis, they manually examined and identified **407** MCP-related issues, from which they derived **5 high-level fault categories**, and then validated through a survey of MCP practitioners whether these categories were complete and actually occurred in practice.
- In short, the core mechanism is: **first collect real issues at scale, then use LLMs and clustering to narrow the scope, and finally derive the taxonomy manually and validate it through a practitioner survey**.

## Results
- The paper claims to present the **first** large-scale taxonomy of real faults for MCP servers, ultimately producing **5 high-level fault categories**.
- In terms of scale: **13,555** candidate repositories were narrowed to **385** MCP server repositories; **30,795** closed issues were reduced to **26,821** English issues, then to **3,282** refined bug issues; among these, **407** MCP-related issues were identified.
- In the comparison of issue classification models, the authors evaluated multiple LLMs using **40** manually labeled samples: **GPT-4o-mini** performed best, achieving **Accuracy 0.77 / Precision-macro 0.78 / Recall-macro 0.82 / F1-macro 0.77**; compared with **GPT-4.1** at **0.74 / 0.76 / 0.81 / 0.75**, and **Llama3.1:8b** at **0.77 / 0.81 / 0.82 / 0.76**.
- For summary model selection, the authors randomly sampled **15** bug issues to compare summary quality, and **GPT-4.1-mini** was rated best on **10/15** samples, outperforming **GPT-4.1** at **3/15**, so it was chosen as the summarization model for the full dataset.
- In the clustering stage, the authors embedded issue summaries into **3,072-dimensional** vectors, reduced them to **5 dimensions** with UMAP, and partitioned them into **101** clusters to support subsequent manual identification of MCP-related faults.
- Regarding final outcomes, the provided excerpt **does not provide more detailed quantitative results** (for example, the share of each of the 5 fault categories, survey sample size, statistics on severity differences, or significance comparisons with non-MCP faults). The strongest specific conclusion is that **all identified fault categories occur in practice, and MCP-specific faults have distinguishing characteristics compared with non-MCP faults**.

## Link
- [http://arxiv.org/abs/2603.05637v1](http://arxiv.org/abs/2603.05637v1)
