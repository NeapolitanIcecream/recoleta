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
- software-testing
- chaos-engineering
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# Industrial Survey on Robustness Testing In Cyber Physical Systems

## Summary
This paper is a field study on how industry conducts robustness testing for Cyber-Physical Systems (CPS), with a focus on revealing common practices and pain points among SMEs in requirements, test environments, fault diagnosis, and toolchains. Its value lies in providing industrial evidence for subsequent work on automated robustness testing for CPS and the adaptation of Chaos Engineering.

## Problem
- The paper addresses the following question: how industry, especially SMEs, currently understands, designs, tests, and operates CPS robustness, and what gaps exist between these practices and academic/advanced methods.
- This is important because CPS are widely used in critical scenarios such as manufacturing, energy, transportation, and healthcare; once robustness is insufficient, it can lead to safety, operational, and economic losses.
- In practice, robustness is often handled in an “ad hoc, experience-driven” manner, and CPS involve coupling across hardware, software, and networks, open environments, and potential malicious attacks, making systematic testing more difficult.

## Approach
- The core method is an **industrial questionnaire + semi-structured interview survey**: the authors conducted a study with **10 companies** in Wallonia, Belgium, with each interview lasting about **1.5 hours** and the questionnaire pre-filled in about **30 minutes**.
- The survey framework follows the CPS lifecycle: robustness definition, requirement sources, design practices, test execution, fault types and root cause analysis, tool usage, and gaps.
- For comparability, the questionnaire structure referenced and reused the overall design of a **2016 Swedish industrial survey**, allowing horizontal comparison with existing literature.
- The analytical focus is not on proposing a new algorithm, but on summarizing industry consensus, common testing methods, failure modes (such as the CRASH classification), monitoring metrics, and companies’ real needs for automation and tool capabilities.
- In the simplest terms, the mechanism of this paper is to “systematically interview frontline industry practitioners, then organize their practices, problems, and needs into a panoramic view.”

## Results
- The survey covered **10 companies**, mostly **SMEs, with only 1 large enterprise**; the sample size is comparable to the **13 companies** in the comparison study, but the paper does not provide statistical significance analysis.
- All interviewed companies agreed with the IEEE definition of robustness; **all companies also spontaneously emphasized that cybersecurity/malicious attacks are a major robustness issue**, which is one of the paper’s strongest findings on industry consensus.
- Robustness requirements mainly come from **customer demands and internal practices**, with fewer coming from standards/specifications; only **2 more mature companies** explicitly mentioned “degraded mode” as a typical requirement.
- Typical performance/availability requirements include: the system should run continuously for **1 week without failure**; response times range from the **nanosecond level** in some medical scenarios to **about the hundred-millisecond level** in railway scenarios. These are among the few relatively specific quantitative examples in the paper.
- Robustness testing is usually carried out in the later stages of development, after sufficient functional validation; in agile processes, some companies add one robustness test every **2–3 sprints**, and conduct another at the end of the project.
- Regarding failure types, companies reported all categories in the CRASH classification, but **catastrophic failures were mentioned only once**; by contrast, more common pain points are **Silent** and **Hindering** faults, which are hard to reproduce and diagnose.
- Regarding test environments, the paper states that in **the vast majority of cases** a hybrid environment of “simulated components + target hardware” is used, but it does not provide an exact proportion; its main conclusion is that building high-fidelity, automatable, and low-cost test environments is the core bottleneck of robustness testing.
- The paper does not report algorithmic performance gains, benchmark SOTA, or A/B experimental metrics. Its strongest concrete claim is that industry generally lacks dedicated robustness tools; current practice relies heavily on general-purpose testing tools, self-built environments, and log analysis, while the most needed future capabilities are **scenario combination generation, continuous automated testing, unified monitoring/log correlation**, and CPS-oriented Chaos Engineering adaptation.

## Link
- [http://arxiv.org/abs/2603.04587v1](http://arxiv.org/abs/2603.04587v1)
