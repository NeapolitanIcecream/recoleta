---
source: arxiv
url: http://arxiv.org/abs/2603.08372v1
published_at: '2026-03-09T13:34:40'
authors:
- Fabian Stiehle
- Markus Funke
- Patricia Lago
- Ingo Weber
topics:
- digital-markets-act
- platform-architecture
- value-sensitive-design
- regulatory-compliance
- interoperability
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Designing Value-Based Platforms: Architectural Strategies Derived from the Digital Markets Act

## Summary
This paper interprets the EU Digital Markets Act (DMA) from a technical and software architecture perspective, proposing a set of actionable platform design strategies to translate abstract values such as "fairness," "contestability," and "user choice" into architectural decisions. Based on compliance reports from large platforms, the authors also summarize real-world implementation tactics and the ecosystem opportunities that arise from them.

## Problem
- The paper addresses the question: **how to systematically translate the abstract regulatory values and obligations in the DMA into platform architecture design strategies**; this matters because the lock-in effects, data advantages, and self-preferencing of very large platforms can undermine fair competition, innovation, and user choice.
- Existing software architecture research focuses more on modularity, evolution, and integration, while paying insufficient attention to the social harms of platforms and to "value-based architectural design"; in particular, there is a lack of work that directly derives technical design methods from regulations such as the DMA.
- Platform compliance is not just a legal issue; it directly affects core technical design choices such as interface openness, interoperability, default settings, data flows, and distribution mechanisms, so a systematic "compliance-by-design" approach is needed.

## Approach
- The authors use **qualitative coding + thematic analysis** to analyze the DMA's **109 recitals**, extracting three types of information: the problems to be solved, the intent of the rules (do's / don'ts), and the underlying values.
- Based on these coding results, the authors synthesize scattered obligations into **8 high-level design strategies** that express the fundamental architectural directions for achieving goals such as "fair practice," "user choice," and "contestability."
- To validate completeness, the authors map all obligations in DMA **Art. 5-7** to these strategies; the paper explicitly states that **no obligation was found that could not be covered by the strategies**.
- To connect theory and practice, the authors further analyze the annual compliance reports of **Alphabet, Amazon, Apple, Booking, Meta**, covering about **650 pages** of documents, and extract **15 gatekeeper tactics** from them.
- The core mechanism can be summarized in the simplest terms as: **first identify from the regulation why systems should be designed in a certain way, then organize that into a small number of general design strategies, and finally derive actionable tactics from real platform compliance practices.**

## Results
- The paper's main outputs are **8 high-level design strategies** and **15 implementation tactics**, claimed to be among the **first systematic architectural strategies from a technical DMA perspective**, aimed at incorporating abstract human values into platform architecture design.
- The data and analytical scope includes: **109 DMA recitals**, **all obligations in Art. 5-7**, **5 gatekeepers (Alphabet, Amazon, Apple, Booking, Meta)**, and about **650 pages** of compliance documents.
- Method validation result: the authors state that when mapping all obligations in **Art. 5-7** to the proposed strategies, **they found no obligation requiring additional strategies for coverage**, which supports the completeness of the strategy set.
- Practical result: **15 tactics** are distilled from the compliance reports, such as alternative app distribution, open interfaces and protocols, default service management, data portability tools, direct third-party data transfer, end-to-end encrypted interoperability, and two-sided advertising transparency.
- The paper **does not provide experimental quantitative metrics such as performance improvement, accuracy, AUC, or win rate**, nor does it benchmark against existing technical methods; its "breakthrough" lies mainly in **methodology and design knowledge production**, rather than conventional machine-learning-style numerical SOTA.
- The strongest concrete claim is that although the DMA challenges existing platform architectures, it also creates new ecosystem opportunities; the proposed strategies/tactics can be used not only for gatekeeper compliance, but also to help third-party services identify new opportunities in interfaces, distribution, interoperability, and data access.

## Link
- [http://arxiv.org/abs/2603.08372v1](http://arxiv.org/abs/2603.08372v1)
