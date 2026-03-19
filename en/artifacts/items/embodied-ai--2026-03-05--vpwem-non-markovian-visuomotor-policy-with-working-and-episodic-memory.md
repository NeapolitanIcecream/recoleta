---
source: arxiv
url: http://arxiv.org/abs/2603.04910v1
published_at: '2026-03-05T07:52:50'
authors:
- Yuheng Lei
- Zhixuan Liang
- Hongyuan Zhang
- Ping Luo
topics:
- robot-imitation-learning
- diffusion-policy
- long-term-memory
- non-markovian-policy
- mobile-manipulation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# VPWEM: Non-Markovian Visuomotor Policy with Working and Episodic Memory

## Summary
This paper proposes VPWEM, a non-Markovian control method that augments visuomotor policies with “working memory + episodic memory,” using fixed-size memory summaries to represent long histories. It is mainly designed for robot imitation learning tasks that require long-term memory, and outperforms strong baselines on multiple benchmarks.

## Problem
- Existing visuomotor/diffusion policies typically only use single-step observations or very short histories, making them difficult to apply to **non-Markovian** robot tasks that require remembering earlier information.
- Directly enlarging the context window brings high computation and VRAM costs (e.g., self-attention grows with sequence length), and also tends to overfit spurious correlations in history, leading to failures under distribution shift.
- This matters because real robot tasks often involve partial observability, long-horizon dependencies, and multiple sub-goals; if a policy cannot retain key past information, it will make mistakes in manipulation and mobile manipulation.

## Approach
- VPWEM keeps a small number of recent observations as **working memory** (a sliding-window short-term memory) for current local decision-making.
- For older observations that fall outside the window, instead of discarding them completely, it uses a **Transformer contextual memory compressor** to recursively compress them into a fixed number of **episodic memory tokens**.
- The compressor applies self-attention over past summary tokens on one side, and cross-attention over a cache of historical observations on the other, thereby condensing “important information from the entire trajectory” into a small number of tokens.
- The compressor is trained jointly end-to-end with the diffusion policy; action generation is conditioned on both short-term working memory and long-term episodic memory, so memory and computation per inference step remain nearly constant.
- The authors instantiate this framework on diffusion policy baselines (e.g., DP, MaIL), and use caching, subsampling, and gradient truncation during training to reduce cost and overfitting.

## Results
- On **MIKASA** memory-intensive manipulation tasks, VPWEM achieves **more than 20% improvement over state-of-the-art baselines**, including diffusion policies and VLA models.
- On the **MoMaRT** mobile manipulation benchmark, VPWEM achieves an **average 5% improvement**.
- On approximately Markovian **Robomimic** tasks, the authors say its performance is **roughly on par** with baselines, suggesting that adding memory does not significantly hurt scenarios that do not strongly require long-term memory.
- The paper provides implementation and experimental-setting figures, for example: default short-term token count **L=2**, long-term memory token count **M=2**, cache size **8**, diffusion sampling steps **50**, and action chunk length **H=8**.
- The provided excerpt does not include complete per-task table values, standard deviations, or more specific baseline-by-baseline breakdowns, so it is not possible to list finer-grained quantitative comparisons.

## Link
- [http://arxiv.org/abs/2603.04910v1](http://arxiv.org/abs/2603.04910v1)
