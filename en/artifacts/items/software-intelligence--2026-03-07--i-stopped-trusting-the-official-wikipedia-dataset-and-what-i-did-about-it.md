---
source: hn
url: https://omarkamali.com/blog/wikipedia-monthly-pipeline
published_at: '2026-03-07T22:52:41'
authors:
- omneity
topics:
- dataset-pipeline
- wikipedia-corpus
- data-engineering
- multilingual-nlp
- low-resource-languages
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# I stopped trusting the official Wikipedia dataset, and what I did about it

## Summary
This article proposes and implements a monthly updated multilingual Wikipedia corpus construction pipeline to replace the long-stagnant official HuggingFace Wikipedia dataset. Its core value lies in filling in the large number of articles missing from outdated snapshots, especially improving the availability of training data for low-resource languages and newly established language editions.

## Problem
- The official HuggingFace Wikipedia dataset has gone a long time without updates. The author found that in 2025 they were still using a 2023 snapshot, leading to obvious data gaps; for example, the Moroccan Arabic dataset had about **8,000** articles, while the website already had **11,000+**, meaning about **30%** of the knowledge was missing.
- Directly using raw Wikimedia dumps is not easy: MediaWiki markup, nested templates, conditional logic, and localized namespace names can cause naïve cleaning to produce erroneous text, contaminating the training corpus.
- At the scale of 340+ languages, there are also engineering issues such as unstable APIs, disk/memory bottlenecks, and failures when uploading at scale, making continuously updated data production very difficult.

## Approach
- The core method takes a “pragmatic compromise” approach: first use **mwparserfromhell** to parse structure, then use **deterministic rules** to handle templates, conditionals, and cleaning details, rather than running the full MediaWiki engine.
- To solve the problem of localized namespace names across languages, the author automatically collected and then manually cleaned MediaWiki namespace labels for all language editions, publishing them as a separate dataset, **omarkamali/wikipedia-labels**, used to correctly strip labels such as Category/تصنيف/Catégorie across languages.
- The single-language cleaning workflow was parameterized and expanded into a general monthly pipeline covering **340+ Wikipedia editions**, with **10k / 5k / 1k** subsets provided to lower storage and memory barriers for downstream users.
- To address resource bottlenecks, the author identified complex nested templates as the main memory hotspot, then replaced simple mutex locking with **memory-monitored scheduling**: new tasks are scheduled only when memory is below a threshold, dynamically controlling parallelism.

## Results
- Processing efficiency improved significantly: total multilingual processing time dropped from **12–14 days** to **3 days** on the author's laptop, and **<24 hours** on a server.
- Data coverage is clearly better than the official version: the latest build is based on a **2026 snapshot**, making it **3 years newer** than the official HuggingFace Wikipedia dataset most researchers use by default.
- The increase in article scale is concrete and substantial: Moroccan Arabic increased from **8,000** to **11,000+**; English has **about 700,000 more articles** than the official version; Arabic has **about 100,000 more articles**.
- In terms of overall data growth, the author claims the **median increase** in total corpus size is **6.8%**, with some languages showing “explosive growth.”
- For newly covered languages, **31 languages** were added to Wikipedia only after 2023, so before the author's release they had **never had usable text corpora**.
- In terms of impact, the author claims the dataset has been used by **Nous Research to train Hermes 4** and cited by papers from **INRIA HAL lab** and others; however, the article does not provide more standard benchmark scores or model performance comparisons.

## Link
- [https://omarkamali.com/blog/wikipedia-monthly-pipeline](https://omarkamali.com/blog/wikipedia-monthly-pipeline)
