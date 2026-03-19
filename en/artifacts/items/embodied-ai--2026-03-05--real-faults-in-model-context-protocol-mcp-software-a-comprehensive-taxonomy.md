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
- github-mining
relevance_score: 0.07
run_id: materialize-outputs
language_code: en
---

# Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy

## Summary
This paper systematically studies real faults in MCP servers and proposes the first fault taxonomy based on empirical data. Through large-scale GitHub issue analysis and a practitioner survey, it helps explain the most common and most critical sources of problems in MCP software.

## Problem
- The paper aims to answer: **what real faults actually occur in MCP (Model Context Protocol) software, and how these faults differ from ordinary software faults**.
- This matters because MCP is becoming a standard interface for interaction between LLMs and external tools/resources, and such systems directly affect **reliability, security, robustness, and testability**.
- Existing research has discussed general defects in LLM software, but **there has previously been no systematic fault taxonomy study specifically targeting MCP systems, especially MCP servers**.

## Approach
- The authors collected MCP Python SDK-related repositories at scale from GitHub: they initially found **13,555** repositories and, after filtering, retained **385** MCP server repositories.
- From these repositories, they extracted **30,795** closed issues; after filtering out non-English ones, **26,821** remained. They then used an LLM to identify bug-related issues, obtaining **3,591** bugs; after removing stale/duplicate/non-reproducible cases, **3,282** valid bugs remained.
- To focus on MCP-related faults, the authors first used an LLM to summarize issues (title, body, comments), then applied **BERTopic + embedding + UMAP + KMeans** to cluster the **3,282** bugs, producing **101** clusters.
- The authors then manually inspected the clustering results, identified **407 MCP-related issues**, and from these induced **5 high-level fault categories**, forming the paper's MCP fault taxonomy.
- To validate the completeness and generalizability of the taxonomy, the authors also conducted a survey of MCP practitioners, confirming that these categories all occur in practice and analyzing the distinguishing characteristics of MCP faults versus non-MCP faults.

## Results
- The paper's core contribution is the proposal of the **first large-scale taxonomy of real faults in MCP servers**, containing **5 high-level fault categories**; the excerpt does not provide the name or proportion of each category.
- In terms of data scale, the study is based on **385** repositories, **26,821** English closed issues, **3,282** refined bug issues, and ultimately identifies **407 MCP-related issues**.
- For issue classification model selection, the authors compared multiple LLMs; **GPT-4o-mini** performed best on 40 labeled samples, achieving **Accuracy 0.77 / Macro-F1 0.77**, slightly higher than **GPT-4.1 with Accuracy 0.74 / Macro-F1 0.75**, and also substantially higher than models such as **Gemma3:4.3b with Macro-F1 0.50**.
- For issue summarization model selection, **GPT-4.1-mini** was rated best in **10/15** samples, outperforming **GPT-4.1 with 3/15**, and was therefore used for full-scale summary generation.
- The practitioner survey indicates that **all identified high-level fault categories appear in real development practice**, and that MCP faults have characteristics distinct from non-MCP faults; however, the excerpt **does not provide more detailed quantitative survey results**.
- Compared with prior work that only studied general LLM software defects, the claimed breakthrough of this paper is that it **is the first to conduct a large-scale empirical taxonomy specifically for MCP servers and to provide a fault profile with direct implications for testing, robustness, and security engineering**.

## Link
- [http://arxiv.org/abs/2603.05637v1](http://arxiv.org/abs/2603.05637v1)
