---
source: hn
url: https://statwonk.com/hormuz-duration-model.html
published_at: '2026-03-08T22:45:46'
authors:
- RA_Fisher
topics:
- survival-analysis
- duration-modeling
- mixture-model
- maritime-disruption
- risk-forecasting
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# How Long Do Major Strait of Hormuz Disruptions Last?

## Summary
This analysis uses a duration model with an extremely small sample to forecast how much longer the major 2026 Strait of Hormuz disruption may last, and further distinguishes between two stages: "political de-escalation" and "actual restoration of shipping." Its value lies in combining historical episodes, rapid policy-reversal scenarios, and operational delays in shipping resumption into a quantifiable uncertainty framework.

## Problem
- The question it aims to answer is: given that commercial shipping in the Strait of Hormuz has already been disrupted in 2026, how much longer will this disruption last, and when might "restored navigation" occur?
- This matters because Hormuz is a critical energy and shipping chokepoint, so the duration directly affects oil transport, insurance, shipowner decisions, supply chains, and policy judgments.
- The difficulty is that the sample is extremely small and highly heterogeneous: only 5 major episodes have been identified since 1981, and the current episode has only been observed for 8 days and is right-censored.

## Approach
- First, a duration model is fit to 5 historical Strait of Hormuz disruption episodes, comparing the exponential, Weibull, and generalized Gamma; because the Weibull shape parameter is close to 1 and the generalized Gamma is unstable in a small sample, the **exponential distribution** is ultimately chosen as the baseline model.
- The baseline model treats episode duration as a random variable with a constant hazard rate, and estimates the parameter using right-censored MLE: 4 completed events and 3,971 total exposure days, yielding a baseline Hormuz hazard rate of about **λH = 0.001007/day**.
- To reflect the possibility of a "rapid policy rollback," the author then adds a **two-component mixture model**: one branch is the historical long-conflict Hormuz branch, while the other is a rapid de-escalation branch calibrated from rapid rollback behavior in 11 tariff-escalation decisions during 2025–2026; in the main specification, the probability of rapid de-escalation is **p = 6/11 ≈ 0.545**, and the rapid-branch hazard rate is **λD ≈ 0.1791/day**.
- Finally, the model separates "political/military de-escalation" from "commercial shipping recovery" into two stages: it first simulates the time to de-escalation, then adds a **shipping-resumption lag distribution** constructed from shipping analog cases and current operating conditions, with an expected additional lag of about **38 days**, and uses **200,000 Monte Carlo draws** to generate the total forecast.

## Results
- The baseline Hormuz exponential model gives an average duration of about **993 days** and a median of about **688 days**; because the exponential distribution is memoryless, this also applies to forecasting the remaining duration of the current episode. The author also reports that there is a **50%** probability the disruption ends within about **1.9 years**, but a **10%** probability it lasts more than **6.3 years**.
- Uncertainty around the baseline parameter is substantial: the hazard rate **95% CI = (0.000274, 0.002577)/day**, corresponding to an average duration of roughly **388–3650 days**, because there are only **4** completed observations.
- The mixture model substantially lowers the median for "political de-escalation": from the baseline **688 days** to **13 days**, because the model assigns roughly **55%** probability to the rapid de-escalation branch; however, the mean remains as high as **454 days**, indicating that a long tail still exists.
- In the two-stage model, after adding the operational lag for shipping resumption, the median forecast for "meaningful restoration of navigation" rises from **13 days** to **88 days**, an increase of about **6x**; the mean rises from **454 days** to **489 days**, and the **90th percentile** rises from **1504 days** to **1531 days**.
- On key interval probabilities, the author states that the probability of restoring meaningful navigation within **30 days** is about **21%**, while the probability that traffic remains materially impaired after **60 days** is about **56%**.
- The article explicitly acknowledges that it does not deliver a strongly robust structural causal conclusion: all results rest on an ultra-small sample, cross-domain calibration, and assumed scenario distributions, so the strongest claim is that it "provides a ranged, layered probabilistic framework," rather than a precise point forecast.

## Link
- [https://statwonk.com/hormuz-duration-model.html](https://statwonk.com/hormuz-duration-model.html)
