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
- platform-architecture
- digital-regulation
- value-sensitive-design
- software-ecosystems
- interoperability
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Designing Value-Based Platforms: Architectural Strategies Derived from the Digital Markets Act

## Summary
This paper interprets the Digital Markets Act (DMA) from the perspective of technology and software architecture, and proposes a method for translating abstract values such as "fairness, contestability, and user choice" into platform design principles. Using qualitative coding and thematic analysis, the authors distill high-level strategies and implementation tactics that can be used to redesign large digital platforms.

## Problem
- The paper addresses the question of **how regulatory requirements like the DMA can be translated into executable software architecture strategies**; this matters because platform monopoly, lock-in, self-preferencing, and data misuse can all harm fair competition, innovation, and user choice.
- Existing software architecture research focuses more on modularity, evolution, and integration, and **rarely deals systematically with human values and social impacts in platform ecosystems**, especially lacking a bridge from regulation to architecture.
- Abstract values (such as fairness and contestability) are difficult to directly operationalize in design decisions; if they cannot be translated early into architectural constraints and capabilities, platforms often end up complying only reactively after the fact.

## Approach
- The authors treat the DMA as a "source of values and design constraints" and conduct systematic qualitative coding of its **109 recitals**, extracting three types of information: platform problems, regulatory intent (do's / don'ts), and underlying values.
- They then use thematic analysis to synthesize these discrete requirements into **8 high-level design strategies**, and validate them by mapping them to the obligations in DMA Articles 5-7; the authors claim that **all obligations are covered by these strategies**, with no need for additional strategies.
- To further operationalize the high-level strategies, the authors analyze the annual compliance reports of **Alphabet, Amazon, Apple, Booking, Meta**, deriving **15 gatekeeper tactics** from about **650 pages** of documentation.
- In the simplest terms, the core mechanism is: **first extract from the regulation what platforms should avoid and support, then organize these requirements into a set of architectural strategies, and finally summarize concrete implementation tactics from real compliance practices**.
- Tactic examples given in the paper include: consent management, allowing default app uninstallation, default service management, open interfaces and protocols, optional interoperability, alternative app distribution, data portability tools, direct transfer of data to third parties, and two-sided ad transparency.

## Results
- The paper's main output is a **design knowledge framework** consisting of **8 high-level architectural strategies** and **15 concrete tactics** for translating the values emphasized by the DMA into platform design practice.
- Quantitatively, the authors report that their analysis covers **109 DMA recitals**, **5 gatekeepers (Alphabet, Amazon, Apple, Booking, Meta)**, and about **650 pages of compliance documentation**.
- The validation result is that the authors map all obligations in DMA **Art. 5-7** to the proposed strategies and claim that **no uncovered obligations were found**; this suggests that the strategy set is "complete" within the scope of this regulation.
- The paper lists **15 tactics**, such as **T8 Alternative App Distribution**, **T11 Portability Tool**, and **T15 Two-Sided (Ad) Transparency**, and explains their architectural implications as well as the opportunities they create for third-party services.
- The paper **does not provide traditional experimental performance metrics** such as accuracy, F1, or latency, nor numerical comparisons with baseline methods; its strongest concrete claim is that the method is the first systematic study of the DMA from a technical architecture perspective, producing a reusable strategy-tactic mapping and an open replication package.

## Link
- [http://arxiv.org/abs/2603.08372v1](http://arxiv.org/abs/2603.08372v1)
