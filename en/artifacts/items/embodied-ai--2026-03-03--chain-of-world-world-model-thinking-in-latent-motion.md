---
source: arxiv
url: http://arxiv.org/abs/2603.03195v1
published_at: '2026-03-03T12:52:06'
authors:
- Fuxiang Yang
- Donglin Di
- Lulu Tang
- Xuancheng Zhang
- Lei Fan
- Hao Li
- Chen Wei
- Tonghua Su
- Baorui Ma
topics:
- vision-language-action
- world-model
- latent-action
- robot-manipulation
- video-vae
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Chain of World: World Model Thinking in Latent Motion

## Summary
This paper proposes CoWVLA, which combines the temporal reasoning of world models with the compact motion representation of latent actions, allowing a robot to “think” about future dynamics in latent motion space. The core goal is to improve VLA dynamic understanding, action learning efficiency, and control performance without reconstructing redundant video backgrounds for an entire segment.

## Problem
- Existing world-model VLAs learn environment dynamics by predicting future frames, but they must reconstruct large amounts of static background pixels, leading to long sequences and inefficient training, and easily wasting capacity on “copying the image” rather than modeling key motions.
- Existing latent-action methods are compact, but usually encode only changes between two frames, lacking continuous-time modeling and learning less world knowledge such as “what is moving, where it is moving, and how the scene will change next.”
- This matters because robot manipulation requires long-horizon temporal reasoning and generalizable understanding of environment dynamics, rather than just short-horizon action mapping.

## Approach
- A pretrained video VAE is used as a latent motion extractor to explicitly decompose a video segment into a structure latent and motion latents, yielding a more compact and interpretable continuous motion representation instead of directly predicting full-frame pixels.
- During pretraining, the model takes a language instruction and an initial frame as input, and uses a learnable motion query `Q` to predict the latent motion of the entire video segment while also predicting the terminal frame, thereby learning a latent dynamic chain “from the current state to the future state.”
- To avoid peeking into the future, `Q` uses a causal mask, so it can only see the instruction and the initial frame, and cannot directly access the terminal frame or future observations.
- During co-fine-tuning, sparse keyframes and discrete action tokens are jointly modeled in the same autoregressive decoder; the same `Q` summarizes latent dynamics over the whole temporal span and aligns them with multi-step action prediction.
- The mechanism is essentially: first learn to describe how the world changes using compressed “motion codes,” then connect this dynamic prior to real action generation.

## Results
- On **LIBERO**, CoWVLA achieves an average success rate of **0.956**, higher than **TLA 0.952**, **UniVLA 0.950**, **pi_0 0.942**, **villa-X 0.901**, and **FlowVLA 0.881**. By subcategory: SPATIAL **0.972**, OBJECT **0.978**, GOAL **0.946**, LONG **0.928**.
- On **LIBERO-LONG**, CoWVLA reaches **0.928**, surpassing **TLA 0.920**, **UniVLA 0.914**, and **GR00T N1 0.906**, indicating stronger performance on long-horizon tasks.
- On **SimplerEnv-WidowX**, CoWVLA averages **0.760**, outperforming **FlowVLA 0.740**, **UniVLA 0.687**, **villa-X 0.625**, **LAPA 0.573**, and **CogACT 0.513**. Task-wise results are: Stack Block **0.625**, Put Carrot **0.667**, Put Spoon **0.792**, Put Eggplant **0.958**.
- Compared with the pre-co-fine-tuning version, performance on **SimplerEnv-WidowX** improves from **0.729** to **0.760**; among these, Stack Block rises from **0.458** to **0.625**, and Put Eggplant from **0.917** to **0.958**, showing that co-fine-tuning can translate the latent dynamic prior into stronger control performance.
- Video VAE reconstruction metrics show that its latent representation has good fidelity: before/after fine-tuning, **PSNR 32.7/33.4**, **SSIM 0.923/0.934**, **LPIPS 0.122/0.123**.
- The paper also makes a qualitative efficiency claim: compared with future-frame-reconstruction world models, CoWVLA avoids reconstructing redundant intermediate frames and therefore has “moderate computational efficiency,” but the excerpt does not provide more detailed numerical comparisons of training or inference cost.

## Link
- [http://arxiv.org/abs/2603.03195v1](http://arxiv.org/abs/2603.03195v1)
