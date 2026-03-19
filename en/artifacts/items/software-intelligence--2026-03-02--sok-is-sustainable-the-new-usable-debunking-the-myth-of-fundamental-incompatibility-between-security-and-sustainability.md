---
source: arxiv
url: http://arxiv.org/abs/2603.01958v1
published_at: '2026-03-02T15:08:13'
authors:
- Maxwell Keleher
- David Barrera
- Sonia Chiasson
topics:
- cybersecurity
- sustainability
- usable-security
- systematic-literature-review
- hci
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# SoK: Is Sustainable the New Usable? Debunking The Myth of Fundamental Incompatibility Between Security and Sustainability

## Summary
This paper systematically reviews digital sustainability design guidelines and compares them with cybersecurity design principles, arguing that there is little evidence for the claim that “security and sustainability are inherently in conflict.” The authors contend that most goals of the two are actually aligned, and that the few conflicts mostly stem from one-sided or excessive application of security principles.

## Problem
- Many devices that still function properly are forced into retirement because vendors stop supporting them, update cycles are too short, or security is used as the justification, producing large amounts of e-waste; a 2024 UN report says e-waste is being generated at about **5 times** the rate of collection and recycling efforts.
- Industry and some research implicitly assume that “more secure means less environmentally friendly” or “more sustainable means less secure,” which allows vendors to use security as a justification for shortening product lifespans.
- The key question is whether **security, durability, and reusability** really cannot be achieved at the same time; this affects device lifespan, user costs, environmental impact, and who should bear responsibility.

## Approach
- The authors conducted a systematic literature review using a **citation chasing** method, starting from seed papers and tracing forward/backward citations, ultimately including **29 papers**.
- From these papers, they extracted **155** design/development guidelines related to digital sustainability, then compressed them through inductive thematic analysis into **12 sustainability themes**, covering three stages: design and development, use, and disposal/end of life.
- They then compared these **12 themes** one by one with the **22 security design principles** proposed by van Oorschot to determine where they align and where tensions exist.
- The authors further use real-world cases (such as Chromecast certificate expiration, Windows 11 hardware requirements, and Android’s short update cycles) to show that many supposed conflicts actually result from security design failing to account for long-term maintenance, openness, repairability, and the allocation of system responsibility.

## Results
- In terms of literature review scale, the authors claim their analysis covers a fairly broad range of digital sustainability guidance: Round 1 produced **1119** candidate papers, Round 2 produced **1980** candidate papers, and **29** papers were ultimately included.
- The thematic analysis produced **12 themes** from **155 guidelines**; **123** were assigned to these 12 themes, while **32** were categorized as miscellaneous.
- The 12 themes are distributed across the lifecycle, including **6 themes** for the design and development stage, **3 themes** for the use stage, and **3 themes** for the disposal/end-of-life stage; for example, “Compatibility and Openness” contains **16** guidelines, “Context and Stakeholders” contains **19** guidelines, and “Repair and Maintain” contains **13** guidelines.
- The central conclusion is that there is **almost no evidence** supporting a “fundamental tension” between security and sustainability; the authors argue that the few points of tension usually arise from **incomplete, incorrect, or overzealous application of security principles**, rather than any essential contradiction between the two.
- The paper **does not provide performance metrics or experimental scores on standard benchmark datasets** (such as accuracy/F1/win rate); its main contribution is systematic evidence and a conceptual framework, rather than quantifiable improvements in model performance.
- The strongest specific claims include: security and sustainability **overlap** in many design goals; both are troubled by the narrative that “users are the weakest link”; and the usable security community is well positioned to incorporate sustainability into its agenda, because both fields require shifting responsibility from individuals to system design.

## Link
- [http://arxiv.org/abs/2603.01958v1](http://arxiv.org/abs/2603.01958v1)
