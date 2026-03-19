---
source: arxiv
url: http://arxiv.org/abs/2603.02765v1
published_at: '2026-03-03T04:04:28'
authors:
- George Bredis
- Nikita Balagansky
- Daniil Gavrilov
- Ruslan Rakhimov
topics:
- model-based-rl
- world-models
- representation-learning
- temporal-transformer
- partial-observability
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Next Embedding Prediction Makes World Models Stronger

## Summary
This paper proposes NE-Dreamer, a world-model reinforcement learning method that does not perform pixel reconstruction and instead directly predicts the “next-step encoder embedding” to learn state representations better suited for long-term memory and partially observable environments. The authors claim it is clearly stronger than DreamerV3 and multiple decoder-free baselines on DMLab memory/navigation tasks, while not degrading performance on DMC.

## Problem
- Existing world-model-based MBRL in high-dimensional, partially observable environments needs to learn latent states that preserve information across time; otherwise, it cannot perform long-horizon prediction and control well.
- Traditional Dreamer-style methods rely on pixel reconstruction, which creates a heavy training burden and can waste capacity on visual details such as textures that are irrelevant to decision-making.
- Many decoder-free methods only enforce representation alignment at the “same timestep” and lack explicit temporal prediction constraints, so they are prone to representation drift or collapse on memory and navigation tasks.

## Approach
- NE-Dreamer keeps Dreamer’s RSSM world model and imagination-based actor-critic, and only replaces the representation learning objective from pixel reconstruction with “next-embedding prediction.”
- At timestep t, the model uses a **causal temporal Transformer** to read the history of latent/state/action sequences and predicts the next-step encoder embedding \(\hat e_{t+1}\) using only past information.
- The prediction is aligned with the stop-gradient target of the true next-step embedding \(e_{t+1}\); specifically, it uses the **Barlow Twins** redundancy-reduction loss, which both encourages predictive agreement and suppresses representation collapse.
- The total world-model loss consists of reward, continuation, KL regularization, and next-embedding loss, and does not require a pixel decoder, data augmentation, or additional auxiliary supervision.
- Through ablations, the authors emphasize that performance mainly comes from two factors: **sequence modeling with a causal Transformer** and **prediction training with the target shifted to the next step**, rather than minor tricks such as the projector.

## Results
- On **DMLab Rooms**, the authors report that under the **same compute budget and model scale** (**50M environment steps, 5 seeds, 12M parameters**), NE-Dreamer outperforms the strong decoder-based baseline **DreamerV3** and decoder-free baselines **R2-Dreamer** and **DreamerPro**; the extracted text does not provide an explicit score table, but repeatedly uses phrases like “substantial gains” and “dramatic improvement” to describe clear improvements on four tasks.
- The core claim of Figure 1 / Figure 3 is that on the four **memory/navigation-heavy** DMLab Rooms tasks, NE-Dreamer learns more stably and achieves higher final returns on all tasks; the largest gains appear on tasks that depend on long-term memory rather than short-term visual cues.
- Mechanistic ablations on **DMLab Rooms** show that removing the **causal temporal transformer** or removing the **next-step shift** causes performance to “drop sharply / almost lose the gains”; removing the projector mainly affects optimization speed and stability, with relatively small impact on final performance. This experiment is also conducted under **50M steps, 5 seeds, 12M params**.
- On **DMC**, the authors say that under a unified protocol (**1M environment steps, 5 seeds, 12M parameters**), NE-Dreamer is **on par with or slightly better than** DreamerV3, R2-Dreamer, and DreamerPro, indicating that removing reconstruction does not hurt standard continuous-control performance; however, the excerpt does not provide specific average scores.
- For representation diagnostics, the authors train a **post hoc decoder** and claim that NE-Dreamer’s frozen latent states preserve object identity and spatial layout more stably, while Dreamer/R2-Dreamer are more likely to lose task-relevant attributes over time; this is qualitative evidence, not standard benchmark metrics.

## Link
- [http://arxiv.org/abs/2603.02765v1](http://arxiv.org/abs/2603.02765v1)
