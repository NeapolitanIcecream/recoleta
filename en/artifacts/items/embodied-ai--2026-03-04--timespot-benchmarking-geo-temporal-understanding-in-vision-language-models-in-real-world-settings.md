---
source: arxiv
url: http://arxiv.org/abs/2603.06687v1
published_at: '2026-03-04T07:27:35'
authors:
- Azmine Toushik Wasi
- Shahriyar Zaman Ridoy
- Koushik Ahamed Tonmoy
- Kinga Tshering
- S. M. Muhtasimul Hasan
- Wahid Faisal
- Tasnim Mohiuddin
- Md Rizwan Parvez
topics:
- vision-language-models
- geo-temporal-reasoning
- benchmarking
- image-geolocation
- temporal-inference
relevance_score: 0.46
run_id: materialize-outputs
language_code: en
---

# TimeSpot: Benchmarking Geo-Temporal Understanding in Vision-Language Models in Real-World Settings

## Summary
TimeSpot is a benchmark for evaluating real-world geo-temporal understanding in vision-language models, requiring models to predict both “where” and “when” from images alone. The paper shows that even today’s strongest VLMs, while appearing reasonably good at coarse-grained geolocation, still fall clearly short on temporal inference and cross-field physical consistency.

## Problem
- Existing visual geolocation benchmarks mostly evaluate only **location**, and rarely require models to explicitly predict temporal attributes such as **season, month, local time, and daylight phase**.
- This matters because applications such as disaster response, traffic planning, embodied navigation, and world modeling need to know not only “where” but also “when”; otherwise, they can produce physically implausible judgments.
- The paper also points out that retrieval-style localization metrics can mask the problem: a model may guess the country correctly while having large coordinate error, poor time estimation, and contradictions between geographic and temporal fields.

## Approach
- Introduces **TimeSpot**: a benchmark containing **1,455** ground-level images covering **80 countries**, emphasizing non-landmark scenes with little text and relying on subtle physical cues such as shadows, vegetation, architecture, and climate.
- Each image requires output in a **9-field structured format**: 4 temporal attributes (season, month, local time, daylight phase) and 5 geographic attributes (continent, country, climate zone, environment type, latitude, longitude).
- Annotations use **programmatic generation + manual verification**: month/season/daylight phase/local time are determined from timestamps, time zones, and solar astronomical information; country, continent, climate zone, and related fields are mapped from coordinates and geographic databases, then manually reviewed for boundary cases.
- Evaluation considers not only classification accuracy, but also **time accuracy within a 1-hour window, time MAE, latitude/longitude error, and great-circle distance error on Earth’s surface**, and adds **cross-field consistency** and confidence diagnostics.
- The paper also conducts **supervised fine-tuning (SFT)** as a diagnostic intervention to test whether explicit supervision can improve geo-temporal understanding.

## Results
- The benchmark contains **1,455** images covering **80** countries; the abstract says the data come from **80 countries**, while the statistical table lists **82 unique countries**, indicating a minor numerical inconsistency in the text.
- The strongest country classification result reaches **77.59% country accuracy** (**Gemini-2.5-Flash-Thinking**), but its **median / geographically emphasized distance error in the text** is still as high as **892.54 km**, showing that “guessing the country correctly” does not mean reliable precise localization.
- Temporal inference is clearly harder: the highest **time-of-day accuracy** is only **33.74%** (**GLM-4.1V-9B-Thinking**, under a ±1 hour window), corresponding to a time MAE of **3:58**; the abstract also explicitly states that temporal performance is overall low.
- On geographic fields, stronger models such as **Gemini-2.5-Flash-Thinking** achieve **90.31% continent accuracy, 77.59% country accuracy, 70.86% climate accuracy, 64.47% environment accuracy**, but on temporal fields only **51.13% season, 24.26% month, 22.19% time accuracy, 36.56% daylight-phase accuracy**.
- Some models are strong on coarse classification, but coordinate-level errors remain large. For example, **Gemini-2.5-Flash-Thinking** has latitude/longitude MAE of **3.04° / 9.85°** and a distance error of **892.54 km**; **GLM-4.5V-106B-MoE** has **69.68%** country accuracy, but still a distance error of **1280.87 km**.
- The paper’s core conclusion is that even after evaluation and supervised fine-tuning, current SOTA VLMs still lack robust, physically grounded joint geo-temporal understanding, especially in temporal grounding and geo-temporal consistency; the passage does not provide the full quantitative improvement numbers for SFT.

## Link
- [http://arxiv.org/abs/2603.06687v1](http://arxiv.org/abs/2603.06687v1)
