---
source: hn
url: https://zipcodefirst.com
published_at: '2026-03-07T23:26:26'
authors:
- dsalzman
topics:
- form-ux
- postal-code-autofill
- address-entry
- web-development
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Put the zip code first

## Summary
This article argues that ZIP/postal code should come first in address forms, and that city, state, and country should be auto-filled based on it, in order to reduce user input and improve the address entry experience. The core idea is not a new algorithm, but a direct, practical proposal to improve existing address form interaction design.

## Problem
- Traditional address forms usually require users to manually enter street, city, and state, then select country, and only enter ZIP at the end, resulting in a large amount of repetitive input that could be avoided.
- Once the ZIP is known, the system can usually already infer **city/state/country**, but many products do not make use of this information, creating an inefficient, error-prone, and frustrating form flow.
- This matters because address entry is a high-frequency scenario; poor interaction design wastes a large amount of user time, increases error rates, and hurts downstream delivery, payments, and data quality.

## Approach
- Move ZIP/postal code to the front of the address form, letting users enter this strongest structured signal first.
- Use a free ZIP lookup API or lookup table to reverse-map **1 input field** into **3 auto-filled fields: city, state, country**.
- After obtaining the ZIP, constrain street address autocomplete to the corresponding area, shrinking the search space from nationwide to local, thereby improving autocomplete speed and accuracy.
- Complement this with `inputmode="numeric"`, proper `autocomplete` attributes, and when necessary an internationalized variant of “country first, postal code second”; the principle is “do not make users re-enter information the system already knows.”

## Results
- The article gives a clear mapping: a **5-character US ZIP code** can infer **3 fields** (city, state, country), i.e. “1 input auto-fills 3 fields.”
- The article gives the example that entering **90210** directly yields **Beverly Hills, California, United States**.
- The author claims that street address autocomplete can be narrowed from about **160 million** addresses to “**a few thousand**” candidates, making it “faster and more accurate,” but provides no benchmarks, dataset details, or quantitative error metrics.
- Implementation complexity is described as extremely low: a free API can be used, and the example code takes about **4–5 lines** to complete ZIP-to-city/state/country autofill.
- There are no formal experiments, A/B tests, or academic metrics; the strongest concrete claim is that it significantly reduces input, avoids scrolling through state/country dropdowns, and improves form completion experience and data quality.

## Link
- [https://zipcodefirst.com](https://zipcodefirst.com)
