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
- multimodal-benchmark
- geo-temporal-reasoning
- visual-localization
- temporal-inference
relevance_score: 0.37
run_id: materialize-outputs
language_code: en
---

# TimeSpot: Benchmarking Geo-Temporal Understanding in Vision-Language Models in Real-World Settings

## Summary
TimeSpot is a real-world geo-temporal understanding benchmark for vision-language models, requiring models to determine both “where” and “when” from images alone. The paper shows that even the strongest current VLMs, despite having decent coarse-grained geographic recognition ability, remain clearly insufficient in temporal inference and geo-temporal consistency.

## Problem
- Existing image geolocation benchmarks mostly evaluate only “place,” and rarely require models to explicitly predict “time” (season, month, local time, daylight phase) or check whether the two are physically consistent.
- This matters because disaster response, traffic planning, navigation, environmental monitoring, and world modeling all depend on correctly understanding both place and time; being able to guess the country but not infer the season/time can lead to unreliable or even unsafe decisions.
- Existing evaluations also often favor landmarks, text, or retrieval-style metrics, making it hard to tell whether models are truly using subtle signals such as shadows, vegetation, climate, and architecture for physically grounded reasoning.

## Approach
- Introduces **TimeSpot**: containing **1,455** real ground-level images covering **80** countries, emphasizing non-landmark, low-text scenes that depend on subtle physical cues.
- The task requires outputting a **9-field structured schema**: 4 temporal attributes (season, month, local time, daylight phase) + 5 geographic attributes (continent, country, climate zone, environment type, latitude/longitude).
- Annotations use “programmatic generation + manual verification”: month, season, daylight phase, and local time are computed from timestamps, time zones, and solar ephemeris; country, climate zone, and coordinates are mapped from geographic metadata, then manually checked for visual consistency and anomalous samples.
- Evaluation looks not only at classification accuracy, but also **time accuracy within a 1-hour window, time MAE, coordinate error, and geodesic great-circle distance**, and checks cross-field physical consistency, such as whether month-season-hemisphere align and whether time is compatible with daylight phase.
- The authors also conduct supervised fine-tuning (SFT) as a diagnostic intervention to test whether explicit supervision can improve geo-temporal understanding, but the abstract states that improvements remain insufficient.

## Results
- Dataset scale and coverage: **1,455** images, **80** countries; latitude range **-54.80 to 71.96**, longitude range **-173.24 to 170.31**, with global distribution.
- Core conclusion of the paper: even for the strongest model, **country accuracy peaks at only 77.59%** (Gemini-2.5-Flash-Thinking), yet **median geodesic error still reaches 892.54 km**, showing that correct coarse-grained localization does not imply reliable true spatial reasoning.
- Temporal understanding is weaker: **time-of-day accuracy peaks at only 33.74%** (GLM-4.1V-9B-Thinking, under a **±1 hour window**), with the best corresponding **time MAE of about 3:58**; this indicates that models struggle to stably infer specific time from visual cues.
- Other representative results: **season accuracy peaks at 65.81%** (o4-mini), **month accuracy peaks at 48.20%** (o4-mini), **daylight-phase accuracy peaks at 64.09%** (Qwen-VL2.5-7B-Instruct).
- On geographic fields, **continent accuracy peaks at 90.51%** (Gemini-2.5-Flash), **country accuracy peaks at 77.59%** (Gemini-2.5-Flash-Thinking), but the best **mean distance** is still close to **892.54 km**, showing that fine-grained localization remains poor.
- The abstract does not provide specific gain numbers for SFT; the strongest concrete claim is: **although supervised fine-tuning brings improvements, the overall results are still insufficient to support robust, physically grounded geo-temporal understanding**.

## Link
- [http://arxiv.org/abs/2603.06687v1](http://arxiv.org/abs/2603.06687v1)
