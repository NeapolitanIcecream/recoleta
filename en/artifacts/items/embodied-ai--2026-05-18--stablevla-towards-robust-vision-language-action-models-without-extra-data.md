---
source: arxiv
url: https://arxiv.org/abs/2605.18287v1
published_at: '2026-05-18T12:15:16'
authors:
- Yiyang Fu
- Chubin Zhang
- Shukai Gong
- Yufan Deng
- Kaiwei Sun
- Qiyang Min
- Qibin Hou
- Yansong Tang
- Jianan Wang
- Daquan Zhou
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-robustness
- sim2real
- adapter-tuning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# StableVLA: Towards Robust Vision-Language-Action Models without Extra Data

## Summary
StableVLA improves VLA policy tolerance to unseen visual corruptions by replacing the usual visual projector with an Information Bottleneck Adapter. It reports large gains without extra robot data or corruption-specific augmentation.

## Problem
- VLA models can fail when camera inputs contain blur, noise, weather effects, or digital artifacts that were absent during training.
- The paper reports that VLA-Adapter drops from 96% clean success to much lower success under corruptions, reaching 0% in some severe blur cases.
- This matters because real robots often work with imperfect images, and collecting data for every possible disturbance is impractical.

## Approach
- StableVLA keeps the VLA-Adapter setup and replaces the MLP projector between the vision encoder and LLM policy with a Fused IB-Adapter.
- IB-Adapter computes channel-wise covariance across visual features, then applies sigmoid gates to suppress channels that look like independent noise.
- A parallel MLP path preserves spatial detail needed for precise manipulation, while the IB path adds denoised semantic features.
- The model uses the same training setting as VLA-Adapter, with no extra robot data and no corruption-specific training augmentation.

## Results
- The abstract claims an average improvement of 30% over baseline with fewer than 10M added parameters.
- Replacing the original adapter with IB-Adapter gives a 35.2% average improvement across synthetic visual corruptions in simulation.
- On LIBERO severity-5 corruptions, StableVLA improves over VLA-Adapter by 40.2% to 139.6% across four task suites.
- Table 1 reports LIBERO severity-5 success gains over VLA-Adapter: Spatial 82.0% vs 58.5%, Object 70.2% vs 29.3%, Goal 71.9% vs 47.3%, Long 45.3% vs 26.2%.
- On CALVIN, StableVLA completes more tasks than VLA-Adapter at every reported setting: clean 4.17 vs 4.14, severity 3 2.77 vs 2.56, severity 4 2.11 vs 1.89, severity 5 1.51 vs 1.44.
- In a real Pack Doll task under visual corruptions, StableVLA-0.5B reaches 50% success, compared with VLA-Adapter-0.5B at 20% and OpenPi-0.5-3B at 40%; the paper also reports a 31.7 percentage-point real-robot pick-and-place gain.

## Link
- [https://arxiv.org/abs/2605.18287v1](https://arxiv.org/abs/2605.18287v1)
