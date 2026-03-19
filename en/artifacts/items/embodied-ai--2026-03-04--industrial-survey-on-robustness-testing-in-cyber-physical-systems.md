---
source: arxiv
url: http://arxiv.org/abs/2603.04587v1
published_at: '2026-03-04T20:30:39'
authors:
- Christophe Ponsard
- Abiola Paterne Chokki
- "Jean-Fran\xE7ois Daune"
topics:
- cyber-physical-systems
- robustness-testing
- industrial-survey
- failure-analysis
- chaos-engineering
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Industrial Survey on Robustness Testing In Cyber Physical Systems

## Summary
This is a survey of the current state of CPS robustness testing in industry in Wallonia, Belgium, focusing on how companies define, design, test, and operate robustness. The value of the paper lies in summarizing real pain points in SME-dominated settings and providing a basis of requirements for subsequently transferring methods such as Chaos Engineering to CPS.

## Problem
- The paper addresses the following questions: how industry currently practices CPS robustness testing, what key gaps exist, and how these practices differ from academic or advanced methods.
- This is important because CPS are widely used in high-risk domains such as manufacturing, energy, transportation, and healthcare, and insufficient robustness can lead to safety, operational, and economic losses.
- Especially for SMEs, robustness work is often carried out **ad hoc**; test environments are expensive and complex, problems are hard to reproduce, and they must also face cybersecurity threats at the same time.

## Approach
- The authors conducted an industrial survey using **semi-structured interviews + pre-filled online questionnaires** to investigate **10 companies**; each interview lasted about **1.5 hours**, and the questionnaire was designed to take about **30 minutes** to complete.
- The survey structure covers the full CPS lifecycle: robustness definition, sources of requirements, design practices, test execution, failure classification and root cause analysis, toolchains, and missing capabilities.
- The questionnaire structure was intentionally aligned with a **2016 Swedish industrial survey** to enable cross-study comparison and assess whether the findings have broader representativeness.
- The sample was mainly SMEs (**only 1 large company out of 10**), covering multiple industries such as transportation/logistics and manufacturing/Industry 4.0, and involving full software lifecycle activities from specification to testing.
- Rather than proposing a new algorithm, the paper systematically synthesizes company feedback to distill practice patterns, common challenges, and future tool/method needs, such as automated testing, fault injection, unified log analysis, and Chaos Engineering adaptation.

## Results
- The survey covered **10 companies**, on the same order of magnitude as the **13 companies** in the comparative study; among them, **only 1 was a large company**, with the rest mainly SMEs, indicating that the results better reflect the real constraints of small and medium-sized enterprises.
- In terms of robustness understanding, **all companies** recognized the IEEE definition of robustness; at the same time, **all companies spontaneously mentioned cybersecurity** as one of the core concerns of robustness, showing that robustness and security are already highly coupled in industry.
- Regarding sources of requirements, robustness requirements mainly came from **customers and internal practice**, while standards/specifications were cited less directly; the paper also provides a few explicit examples, such as **2 companies** that explicitly raised requirements for a “degraded mode.”
- For failure types, companies reported **all types** in the CRASH classification, but **only 1 case of catastrophic failure** was reported; by contrast, more common and more difficult issues were **Silent** and **Hindering** problems that are hard to diagnose and reproduce.
- In testing practice, most companies place robustness testing in the later stages of development, and test environments are usually **hybrid environments of simulated components + target hardware**; the paper does not provide unified percentage statistics, but clearly notes that real field testing is minimized because of high cost.
- The paper does not report traditional quantitative metrics such as algorithm performance or benchmark dataset accuracy; the strongest concrete conclusion is that industry generally lacks dedicated robustness tools and relies on general-purpose testing tools, logs, and self-developed scripts, with the most urgent needs concentrated in **scenario combination generation, continuous automated testing, unified monitoring/log fusion, load testing, and AI assistance**.

## Link
- [http://arxiv.org/abs/2603.04587v1](http://arxiv.org/abs/2603.04587v1)
