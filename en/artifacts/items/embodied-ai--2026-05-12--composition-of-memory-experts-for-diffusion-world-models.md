---
source: arxiv
url: https://arxiv.org/abs/2605.18813v1
published_at: '2026-05-12T09:43:10'
authors:
- Sebastian Stapf
- Pablo Acuaviva Huertos
- Aram Davtyan
- Paolo Favaro
topics:
- diffusion-world-models
- long-term-memory
- product-of-experts
- video-prediction
- navigation-planning
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Composition of Memory Experts for Diffusion World Models

## Summary
CoME is a diffusion world model method that combines short-term, long-term, and spatial memory experts so generated futures stay consistent with past observations.

## Problem
- World models need long histories for planning and navigation, because an agent may revisit a place and should predict the same objects and layout it saw before.
- Transformer context is costly because attention grows quadratically, while recurrent and state-space models compress history and lose details.
- Long-context video prediction also needs spatial consistency, since similar-looking locations can cause wrong recall.

## Approach
- The method composes several diffusion experts at sampling time with a Product of Contrastive Experts rule.
- A short-term memory expert attends to recent context, described as about 10-100 images, to keep local motion and visual details stable.
- A long-term memory expert stores episodic history in LoRA adapter weights through test-time finetuning on about 100-1000 images.
- A spatial long-term memory expert conditions generation on pose, maps, or other spatial signals so predictions match location as well as appearance.
- The contrastive rule compares each conditional expert with its unconditional version to reduce spurious modes without narrowing each local mode in the KDE analysis.

## Results
- On Memory Maze, the Base model reports LPIPS 0.209, SSIM 0.771, and PSNR 19.16.
- Adding STM improves Memory Maze results to LPIPS 0.156, SSIM 0.820, and PSNR 21.29.
- The visible table shows STM improves LPIPS by 0.053, SSIM by 0.049, and PSNR by 2.13 over Base on Memory Maze.
- The excerpt says LTM, SLTM, and especially STM+LTM further improve temporal consistency and beat the listed baselines, but the rows with their exact numbers are truncated.
- The experiments use Memory Maze with 30k trajectories of 1k frames, RECON with over 5k real outdoor trajectories, and RE10K indoor scenes with camera poses.
- Baselines are trained for 150k steps; the DiT baseline uses 3 context frames to predict 17 frames, while the STM expert uses 33 conditioning frames to predict 17 frames.

## Link
- [https://arxiv.org/abs/2605.18813v1](https://arxiv.org/abs/2605.18813v1)
