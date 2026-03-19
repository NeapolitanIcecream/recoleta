---
source: arxiv
url: http://arxiv.org/abs/2603.09868v1
published_at: '2026-03-10T16:33:28'
authors:
- Aleksei Rozanov
- Arvind Renganathan
- Yimeng Zhang
- Vipin Kumar
topics:
- climate-ml
- benchmark
- zero-shot-transfer
- domain-generalization
- time-series-regression
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# CarbonBench: A Global Benchmark for Upscaling of Carbon Fluxes Using Zero-Shot Learning

## Summary
CarbonBench proposes a global zero-shot spatial transfer benchmark for terrestrial carbon flux upscaling, aiming to standardize evaluation of models' generalization ability to entirely unobserved new locations. It explicitly formulates carbon flux upscaling as a time-series regression/domain generalization problem affected by distribution shift in climate and vegetation.

## Problem
- This work addresses the question of how to reliably upscale point-based carbon flux observations into globally continuous space, and generalize to **unseen locations, climate zones, and vegetation types**, when eddy covariance tower observations are extremely sparse and severely uneven in geographic distribution.
- This matters because global carbon sink assessment, climate policy, carbon accounting, and Earth system model calibration all depend on spatially continuous carbon flux estimates, yet the number of publicly available flux towers is fewer than about 700, covering less than **0.015%** of Earth's land surface.
- Existing methods and benchmarks mainly lack standardized protocols for **zero-shot spatial transfer**, metrics and stratified evaluation suited to regression tasks, and unified feature/site/split settings, making fair comparison and reproduction across papers difficult.

## Approach
- The core mechanism is simple: treat each flux tower site as a "domain," use remote sensing features, meteorological drivers, and site metadata (such as IGBP vegetation type and Köppen climate class) to predict carbon fluxes, and then specifically test model performance on **previously unseen sites**.
- CarbonBench builds a unified dataset by aggregating **567** global flux tower sites, covering **2000–2024**, with more than **1.3 million** daily observations, and provides **3** target fluxes (GPP, RECO, NEE) along with quality flags.
- Input features are standardized into **150** ERA5-Land meteorological drivers, **12** MODIS remote sensing features, plus climate/vegetation categories and spatiotemporal information; for temporal models, a **30-day window** with a **15-day stride** is recommended.
- To rigorously evaluate spatial generalization rather than temporal autocorrelation, the benchmark uses zero-shot testing split by site, and provides two stratified split schemes: by **IGBP vegetation type (16 classes)** and by **Köppen climate type (5 broad classes)**.
- Evaluation uses metrics better suited to regression and distribution shift: **R², RMSE, nMAE**. Statistics are computed by site and reported with quantiles; testing is conducted only on high-quality samples (QC=1), while training can use quality-weighted losses to leverage all samples.

## Results
- The clearest result is the benchmark's scale and coverage: **1,304,309** timestamps, **567** sites, and a time span of **2000–2024**, of which **553,467** are highest-quality observations (QC=1).
- In terms of data modalities, the benchmark includes **3** target variables (GPP, RECO, NEE), **150** meteorological features, **12** remote sensing features, as well as climate/vegetation categories and spatiotemporal metadata.
- Regarding evaluation protocol, the example IGBP-stratified split gives **448** training sites and **115** test sites; common categories use an approximately **0.8/0.2** split, while rare vegetation classes (with site count ≤ **10**) use **0.5/0.5** to ensure evaluability.
- The paper claims this is the **first** standardized benchmark for **zero-shot spatial transfer in time-series regression** aimed at carbon flux upscaling, and it covers tree models, recurrent networks, Transformers, meta-learning, and domain generalization models as baseline directions.
- In the provided excerpt, **no specific model performance numbers are given** (for example, how much a model outperforms a baseline on R²/RMSE/nMAE under a given split), so no quantitative SOTA comparison can be reported; the strongest verifiable claims are its data scale, dual stratified protocols, and standardized evaluation design.

## Link
- [http://arxiv.org/abs/2603.09868v1](http://arxiv.org/abs/2603.09868v1)
