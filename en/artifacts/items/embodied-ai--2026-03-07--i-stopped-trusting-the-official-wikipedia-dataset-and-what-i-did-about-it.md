---
source: hn
url: https://omarkamali.com/blog/wikipedia-monthly-pipeline
published_at: '2026-03-07T22:52:41'
authors:
- omneity
topics:
- wikipedia-dataset
- data-pipeline
- multilingual-corpus
- data-cleaning
- low-resource-languages
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# I stopped trusting the official Wikipedia dataset, and what I did about it

## Summary
This article argues that the official HuggingFace Wikipedia dataset has gone unupdated for a long time, causing severe data gaps for many languages, especially low-resource ones. The author built a Wikipedia cleaning and publishing pipeline that updates monthly and covers 340+ language editions, providing more complete and cleaner text corpora.

## Problem
- The official Wikipedia dataset snapshots are too old; for example, the author found in 2025 that Moroccan Arabic was still using a 2023 snapshot, with only **8,000** articles in the dataset while **11,000+** already existed online, meaning about **30%** of the content was missing.
- The MediaWiki markup language and template system are extremely complex, so direct cleaning easily produces erroneous text; namespace labels are also localized across languages, and if they are not recognized, irrelevant labels can be mixed into the training corpus.
- When scaling the process across all languages, engineering issues arise such as fragile API access, insufficient disk space, memory bottlenecks, and instability in large-scale uploads, all of which hinder researchers from obtaining fresh, high-quality Wikipedia corpora.

## Approach
- The author adopted a compromise approach: first use **mwparserfromhell** for structural parsing, then handle templates, conditional logic, and language-specific labels through **deterministic rules**, with the goal of extracting clean plain text from raw dumps.
- MediaWiki namespace labels for each Wikipedia language edition are collected automatically and published as a separate dataset, **wikipedia-labels**, to identify and strip localized labels such as Category/تصنيف/Catégorie.
- The single-language prototype was generalized into a parameterized pipeline for all language editions, regularly downloading, parsing, cleaning, and publishing datasets from Wikimedia monthly dumps.
- To address resource bottlenecks, the author added resumable processing, memory-monitoring-based scheduling, and more dynamic parallelism control to avoid memory explosions and swap/disk crashes during complex template handling stages.
- The release also includes **10k / 5k / 1k** article subsets, lowering storage and memory barriers for users downloading and processing the corpora.

## Results
- The final dataset, **omarkamali/wikipedia-monthly**, achieves **monthly updates** and covers **340+** Wikipedia language editions.
- Compared with the previous process, processing time was reduced from **12–14 days** to **3 days** on the author's laptop, and can be done in **<24 hours** on a server.
- The latest version is based on a **2026** snapshot, making it **3 years newer** than the official HuggingFace Wikipedia dataset most researchers use by default.
- In terms of data growth: Moroccan Arabic increased from **8,000** articles to **11,000+**; English is missing about **700,000** articles compared with the official version; Arabic is missing about **100,000** articles.
- Overall, corpus size shows a **median growth of 6.8%** relative to the official version, with some languages growing more; another **31** languages were only added to Wikipedia after 2023, meaning the previous official corpus had **no text data at all** for them.
- The article also provides concrete signals of adoption and impact: for example, **Nous Research** used it to train **Hermes 4**, and it has already been cited in papers from **INRIA HAL lab** and others; however, it does not provide model accuracy comparisons on standard NLP benchmarks.

## Link
- [https://omarkamali.com/blog/wikipedia-monthly-pipeline](https://omarkamali.com/blog/wikipedia-monthly-pipeline)
