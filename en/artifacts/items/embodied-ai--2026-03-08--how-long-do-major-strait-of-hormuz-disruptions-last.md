---
source: hn
url: https://statwonk.com/hormuz-duration-model.html
published_at: '2026-03-08T22:45:46'
authors:
- RA_Fisher
topics:
- survival-analysis
- duration-modeling
- geopolitical-risk
- mixture-model
- shipping-disruption
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# How Long Do Major Strait of Hormuz Disruptions Last?

## Summary
This analysis uses a duration model with an extremely small sample to predict how much longer the 2026 Strait of Hormuz disruption may last, and further incorporates “rapid policy reversal” and “shipping recovery lag” into a layered forecast. The core conclusion is: if we look only at the historical baseline, the disruption could last a very long time; if we consider a rapid de-escalation scenario, the median time to political easing shrinks substantially, but the time to restoring meaningfully usable transit remains clearly slower.

## Problem
- The paper aims to answer: **how much longer the current disruption to commercial shipping in the Strait of Hormuz will last, and when “meaningful transit” can resume**.
- This matters because Hormuz is a critical global energy and shipping chokepoint; duration directly affects oil transport, insurance, risk premia, supply chains, and policy judgment.
- The difficulty is that the sample is extremely small and the events are highly heterogeneous: historically there have been only **5 major disruptions**, of which only **4 have ended**, while the current **2026** event is still a right-censored sample.

## Approach
- First, a duration model is fit to the historical **5 Hormuz disruptions**, comparing **exponential / Weibull / generalized gamma**; because the Weibull shape parameter is close to **1.0** and the generalized gamma is numerically unstable, the final baseline model uses a **single-parameter exponential distribution**.
- The baseline model treats the current event as **right-censored**, using total exposure time of **3,971 days** and the number of resolved events **d=4** to estimate the hazard rate; the key mechanism of the exponential distribution is **memorylessness**: having already lasted 8 days does not change the distribution of the “remaining duration.”
- To reflect the possibility of a “rapid policy reversal,” the author adds a **two-component mixture model**: one branch is the historical Hormuz baseline hazard **λH = 0.001007/day**, and the other is a rapid de-escalation branch calibrated from **11 tariff-escalation decisions in 2025–2026**, with **λD ≈ 0.1791/day** and rapid de-escalation probability **p = 6/11 ≈ 0.545**.
- Because political de-escalation does not mean shipping immediately resumes, the author then adds a **two-stage model**: total time = political/military off-ramp time + shipping reopening lag time. The latter is not fit parametrically, but instead constructed as a discrete distribution based on maritime analog scenarios, with an expected reopening lag of about **38 days**.
- Finally, **200,000 Monte Carlo** draws are used to add the mixture-model political duration and the reopening lag, producing a full predictive distribution for the restoration of “meaningful transit.”

## Results
- The baseline exponential model implies an average Hormuz disruption duration of about **993 days**, with a **median of 688 days (about 1.9 years)**; the author also notes a **10% probability** that it lasts more than **6.3 years**. The hazard rate **95% CI = (0.000274, 0.002577)/day**, corresponding to an average duration of about **388–3650 days**, indicating very large uncertainty.
- Under the baseline model, the fact that the current 2026 event has already lasted **8 days** does not change the forecast for remaining time, because the exponential distribution is **memoryless**.
- After introducing the rapid de-escalation branch in the mixture model, the **median remaining time to political easing drops sharply from 688 days to 13 days**; however, the **mean is still 454 days**, because the long-conflict branch preserves a very long right tail.
- Key calibration values for the mixture model include: among **11** tariff-sample events, **8** saw reversal, and **6** of those occurred within **30 days**; the mean of the rapid de-escalation branch is derived from the **6 within-30-day reversal samples** (**2, 3, 0.5, 7, 2, 19 days**), hence **λD ≈ 1/5.58 = 0.1791/day**.
- After adding the “reopening lag,” the **median time to restoration of meaningful transit rises from 13 days to 88 days**, about **6×**; the **mean rises from 454 days to 489 days**, and the **90th percentile rises from 1504 days to 1531 days**. This suggests that short- to medium-term outcomes are mainly affected by reopening frictions, while the long tail is still dominated by conflict duration.
- Under the full two-stage model, the author claims that the **probability of restoring meaningful transit within 30 days is about 21%**, while the **probability that transit remains materially disrupted after 60 days is about 56%**. The analysis also emphasizes that these results are based on an extremely small sample, cross-domain calibration, and scenario assumptions, and therefore constitute a **descriptive framework rather than a causal forecast**.

## Link
- [https://statwonk.com/hormuz-duration-model.html](https://statwonk.com/hormuz-duration-model.html)
