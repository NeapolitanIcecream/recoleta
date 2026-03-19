---
source: arxiv
url: http://arxiv.org/abs/2603.14375v1
published_at: '2026-03-15T13:29:31'
authors:
- Xiangbo Gao
- Mingyang Wu
- Siyuan Yang
- Jiongze Yu
- Pardis Taghavi
- Fangzhou Lin
- Zhengzhong Tu
topics:
- video-generation
- world-model
- temporal-grounding
- benchmarking
- physical-simulation
relevance_score: 0.54
run_id: materialize-outputs
language_code: en
---

# The Pulse of Motion: Measuring Physical Frame Rate from Visual Dynamics

## Summary
This paper proposes **Visual Chronometer**, a method for estimating the true physical frame rate (PhyFPS) solely from the appearance of motion in a video, in order to measure and correct “time-scale hallucinations” in generated videos. The authors also construct two benchmarks showing that current mainstream video generation models generally suffer from inconsistencies between physical motion speed and nominal frame rate.

## Problem
- The paper aims to solve the following issue: although video generation models produce visuals and motion that appear smooth, they **lack a stable pulse corresponding to real-world time**, leading to ambiguous, drifting, and uncontrollable motion speeds, which the authors call **chronometric hallucination**.
- This matters because if video models are treated as **world models**, they must not only generate frames that “look like they are moving,” but also ensure that motion speeds align with real physical time; otherwise, they cannot reliably simulate real-world dynamics.
- Existing training pipelines usually treat slow motion, time-lapse, and normal videos uniformly at standardized frame rates, so models fail to learn “how much real time each frame actually corresponds to.”

## Approach
- The core method is **Visual Chronometer**: given a video clip, it directly predicts the underlying true physical frame rate **PhyFPS** from the visual dynamics, rather than relying on unreliable metadata FPS.
- The training procedure is straightforward: starting from a set of high-confidence videos where “metadata FPS = true FPS,” the videos are first upsampled to **240 FPS**, then different physical frame-rate versions are synthesized through **controlled temporal resampling**, allowing the model to learn what motion looks like at 12/24/60/... FPS.
- To better approximate real capture mechanisms, the authors synthesize three types of temporal sampling: **sharp capture** (fast shutter, no blur), **motion blur** (motion blur with different exposure durations), and **rolling shutter** (rolling-shutter distortion).
- In terms of architecture, the method uses **VideoVAE+** as the video encoder, followed by an **attention pooling regression head** that outputs `log(PhyFPS)`, and is trained with **MSE** in log space to handle a wide frame-rate range more stably.
- The paper also introduces two benchmarks: **PhyFPS-Bench-Real** for validating prediction accuracy on real videos, and **PhyFPS-Bench-Gen** for auditing generation models on three aspects: meta FPS alignment, within-video stability, and across-video stability.

## Results
- The training data covers **18 target PhyFPS** values, yielding a final total of **465,535** video clips, all standardized to **128 frames**; training uses windows of up to **32 frames**, runs for **125,000** iterations, on 4 **RTX A6000** GPUs, with a global batch size of **32**.
- On **PhyFPS-Bench-Gen**, the authors evaluate multiple open- and closed-source video generation models and find widespread **mismatch between Meta FPS and PhyFPS**. For example, **LTX-Video** has a meta FPS of **24** but a predicted PhyFPS of **46.52**, with an average error of **23.67 FPS** and a percentage error of **99%**; **InfinityStar (10s)** shows **16 → 36.15**, with an average error of **20.19 FPS** and a percentage error of **126%**.
- A relatively strong open-source model is **Wan2.1-T2V-1.3B**: meta FPS **24**, PhyFPS **26.28**, average error **7.54 FPS**, percentage error **31%**. A relatively strong closed-source model is **Sora-2**: meta FPS **30**, PhyFPS **36.21**, average error **8.40 FPS**, percentage error **28%**.
- In terms of temporal stability, different models show **Intra CV** of about **0.10–0.17** and **Inter CV** of about **0.25–0.52**, indicating that not only is the overall speed often inaccurate, but time-scale jitter also exists across different videos from the same model and even across different segments within the same video.
- The user study collected **1,490** pairwise comparisons from more than **15** participants. The original generated videos received a temporal naturalness preference of only **19.0%**; **Pred**, which applies global correction based on the predicted average PhyFPS, reaches **44.2%**, while **Pred Dyn**, which applies dynamic correction to local segments, achieves **36.9%**, showing that PhyFPS-based post-processing can significantly improve perceived naturalness.
- The abstract and main text also claim that strong vision-language models are “**highly unreliable**” as PhyFPS judges, but the provided excerpt does not include the corresponding quantitative values. The specific accuracy numbers for PhyFPS-Bench-Real are also not expanded in the excerpt.

## Link
- [http://arxiv.org/abs/2603.14375v1](http://arxiv.org/abs/2603.14375v1)
