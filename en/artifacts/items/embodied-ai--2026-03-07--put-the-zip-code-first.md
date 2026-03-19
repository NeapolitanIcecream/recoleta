---
source: hn
url: https://zipcodefirst.com
published_at: '2026-03-07T23:26:26'
authors:
- dsalzman
topics:
- ux-design
- web-forms
- address-autofill
- postal-code
- human-computer-interaction
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Put the zip code first

## Summary
This article discusses the interaction design of web address forms, not an academic research paper. Its core argument is to place the ZIP code at the very beginning of address entry and use existing APIs to automatically fill in the city, state, and country, thereby reducing user input and form friction.

## Problem
- Existing address forms usually require users to manually enter the street, city, state, and country first, and only enter the ZIP code at the end, even though the ZIP alone is already sufficient to infer multiple fields.
- This creates unnecessary input burden, inefficient dropdown selection, more user errors, and a worse address autocomplete experience.
- The article emphasizes that this kind of inefficient design is extremely common in e-commerce and checkout flows, so it systematically wastes large amounts of user time and degrades the conversion experience.

## Approach
- Move the ZIP code to the beginning of the address form; in U.S. scenarios, after entering a 5-digit ZIP, automatically look it up or call a free API to fill city、state、country.
- Once the ZIP is known, use restricted-scope autocomplete for the street address, shrinking the search space from nationwide addresses to a small set of candidates near that ZIP.
- In internationalized scenarios, the author further explains that you can also determine the country first (for example, prefill it or have the user select it first), and then use the postal code to autocomplete the remaining fields.
- At the same time, pair this with basic form-engineering improvements: use `inputmode="numeric"` for numeric fields, correctly set the browser `autocomplete` attributes, and avoid resetting the form after navigation back.

## Results
- The article **does not provide formal experiments, datasets, or reproducible experimental metrics**, so there are no quantitative results in the academic sense.
- The most specific numerical claims include: a U.S. ZIP code has **5 characters** and can infer **3 fields** (city/state/country).
- The author claims that the search space for street autocomplete can be reduced from about **160 million** addresses to “**a few thousand**,” making it faster and more accurate, but provides no benchmarks or error rates.
- The implementation cost is described as extremely low: a **free API** can be used, and the example code takes about **4–5 lines** to complete ZIP-to-city/state/country autofill.
- The article’s strongest conclusion is that this is an “already solved problem”; the main obstacle is not technology, but product and organizational inertia.

## Link
- [https://zipcodefirst.com](https://zipcodefirst.com)
