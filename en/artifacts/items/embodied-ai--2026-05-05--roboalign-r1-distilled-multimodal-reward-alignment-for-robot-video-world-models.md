---
source: arxiv
url: https://arxiv.org/abs/2605.03821v1
published_at: '2026-05-05T14:49:00'
authors:
- Hao Wu
- Yuqi Li
- Yuan Gao
- Fan Xu
- Fan Zhang
- Kun Wang
- Penghao Zhao
- Qiufeng Wang
- Yizhou Zhao
- Weiyan Wang
- Yingli Tian
- Xian Wu
- Xiaomeng Huang
topics:
- robot-world-models
- reward-alignment
- video-generation
- multimodal-judge
- long-horizon-prediction
- robot-data-scaling
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models

## Summary
RoboAlign-R1 improves robot video world models by training them with a distilled multimodal reward and by refreshing long-horizon rollouts during inference. The paper reports better task alignment, physical realism, and pixel metrics on RobotWorldBench, RT-1, and BridgeData V2.

## Problem
- Robot video world models are often trained with reconstruction, MSE, LPIPS, or SSIM losses, which can miss instruction following, manipulation success, contact quality, and physical consistency.
- Long autoregressive rollouts accumulate token-level errors, so video predictions can drift over time and become less useful for planning.
- Multimodal judges can score high-level robot behavior, but an 8B judge is too slow and costly to use directly as an online RL reward.

## Approach
- The authors build RobotWorldBench with 10,000 annotated video-instruction pairs from RT-1, BridgeData V2, CALVIN, and LIBERO.
- They fine-tune Qwen3-VL-8B-Thinking into RoboAlign-Judge, which scores generated robot videos on six dimensions: instruction following, manipulation success, action-outcome consistency, temporal consistency, contact realism, and physics adherence.
- They distill the 8B judge into a 98M student reward model that scores about 50 videos per second and supplies rewards for GRPO post-training.
- The robot video model uses a tokenized action-conditioned video sequence: context tokens, dynamics tokens, and discretized action tokens are modeled by a 12-layer LLaMA decoder.
- Sliding Window Re-encoding decodes the last predicted frame every W steps, re-encodes it as fresh context, and continues generation with a shorter active history.

## Results
- On RobotWorldBench, RoboAlign-R1 scores 8.52±0.15 total versus iVideoGPT at 7.74±0.62, a reported +10.1% gain over the best baseline and lower score variance.
- It leads all six judge dimensions: instruction following 2.72±0.06, manipulation 1.72±0.07, action-outcome 0.72±0.05, temporal 0.78±0.05, contact 1.00±0.04, and physics 1.58±0.07.
- The abstract reports gains over the strongest baseline of +7.5% on Manipulation Accuracy and +4.6% on Instruction Following under the in-domain evaluation protocol.
- On pixel metrics, the paper reports a 4.9% LPIPS reduction on RT-1 and an 8.7% MSE reduction on BridgeData V2 against the respective runners-up.
- Sliding Window Re-encoding gives +2.8% SSIM, +0.62 dB PSNR, -9.8% LPIPS, -12.2% ROI-LPIPS, and about +1% latency.
- Reward distillation reduces online reward cost by more than 10x compared with using the 8B teacher judge directly, while the main ranking is also checked with an external VLM and a blinded human study.

## Link
- [https://arxiv.org/abs/2605.03821v1](https://arxiv.org/abs/2605.03821v1)
