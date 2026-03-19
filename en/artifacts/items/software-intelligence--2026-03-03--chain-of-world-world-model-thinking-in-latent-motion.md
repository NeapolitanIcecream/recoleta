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
- latent-motion
- robot-learning
- embodied-ai
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Chain of World: World Model Thinking in Latent Motion

## Summary
CoWVLA proposes a VLA pretraining paradigm that combines the temporal reasoning of a “world model” with the compact representation of “latent actions,” learning robot dynamics through a latent motion chain rather than frame-by-frame reconstruction. It aims to learn vision-language-action control more efficiently while preserving an understanding of future states and changes in the world.

## Problem
- Existing world-model VLAs usually learn dynamics by predicting future image frames, but waste substantial capacity on reconstructing static backgrounds and redundant pixels, making training costly.
- Existing latent-action methods are more compact, but typically model only changes between adjacent frames, lacking continuous temporal reasoning and learning less world knowledge about “how a scene will evolve.”
- This matters because robot control must not only output actions, but also understand how actions continuously change the environment, which is especially important in long-horizon, multi-step manipulation.

## Approach
- A pretrained video VAE is used as a **latent motion extractor**, explicitly decomposing video segments into structure latents and motion latents; the motion component is further composed of motion representations from two directions and then concatenated into a unified latent motion vector.
- During pretraining, the model takes as input an “instruction + initial frame + a learnable motion query,” and learns to predict the continuous latent motion of the full video segment as well as the terminal frame, instead of reconstructing all intermediate frames.
- Through a causal mask, the motion query can only see the instruction and initial frame, and cannot peek at future frames, forcing the model to genuinely infer future dynamics.
- During co-fine-tuning, sparse keyframes and discrete action sequences are fed into a unified autoregressive decoder to jointly learn consistency among action tokens, keyframe tokens, and latent motion.
- The intuitive mechanism is: first teach the model to learn “what the core motion in this video segment is,” then align that motion understanding with actual action generation, thereby balancing compact representation, interpretability, and temporal world modeling.

## Results
- On **LIBERO**, CoWVLA achieves an average success rate of **0.956**, outperforming UniVLA’s **0.950**, TLA’s **0.952**, villa-X’s **0.901**, and FlowVLA’s **0.881**. By subset, it reaches: SPATIAL **0.972**, OBJECT **0.978**, GOAL **0.946**, LONG **0.928**.
- On **SimplerEnv-WidowX**, CoWVLA averages **0.760**, higher than FlowVLA’s **0.740**, UniVLA’s **0.687**, villa-X’s **0.625**, and LAPA’s **0.573**. The task-specific results are: Stack Block **0.625**, Put Carrot **0.667**, Put Spoon **0.792**, Put Eggplant **0.958**.
- The paper claims to outperform both existing **world-model** and **latent-action** methods; for example, compared with the best world-model baseline FlowVLA, it improves the SimplerEnv average by **+0.020** (0.760 vs 0.740); compared with the best latent-action baseline TLA, it improves the LIBERO average by **+0.004** (0.956 vs 0.952).
- Video VAE reconstruction quality on SimperEnv-related evaluations reaches: pretraining PSNR/SSIM/LPIPS of **32.7 / 0.923 / 0.122**, and after fine-tuning **33.4 / 0.934 / 0.123**, while downstream average success rate improves from **0.729** to **0.760**.
- In implementation, the latent motion extractor is adapted and trained on **237k** robot videos; the backbone uses Emu3 with **8.5B** parameters. This supports its “large-scale pretraining + downstream robot control” setting, but the paper mainly describes computational efficiency qualitatively as “moderate computational efficiency,” without providing more detailed throughput/cost comparison numbers.

## Link
- [http://arxiv.org/abs/2603.03195v1](http://arxiv.org/abs/2603.03195v1)
