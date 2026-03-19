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
- visuomotor-policy
- long-term-memory
- diffusion-policy
- non-markovian-control
relevance_score: 0.24
run_id: materialize-outputs
language_code: en
---

# VPWEM: Non-Markovian Visuomotor Policy with Working and Episodic Memory

## Summary
VPWEM proposes a non-Markovian visuomotor policy for robot imitation learning that combines short-term working memory with long-term episodic memory, enabling use of the full trajectory history with low and approximately constant per-step cost. It primarily targets manipulation tasks that require long-term memory, improving success rates while maintaining real-time performance.

## Problem
- Existing visuomotor policies typically consider only single frames or very short histories, making them difficult to apply to non-Markovian tasks that require remembering critical early information.
- Directly extending the history window incurs high computation / memory costs (e.g., attention grows with sequence length) and also makes it easier to learn spurious correlations, leading to catastrophic failures under distribution shift.
- Real robot tasks often require long-term memory because of partial observability, environmental randomness, and long-horizon subgoals, so short context alone is insufficient.

## Approach
- Use **working memory** to retain a fixed-length window of recent observations, capturing short-term local information.
- Use a **Transformer memory compressor** to recursively compress older observations that slide out of the window into a fixed number of **episodic memory tokens**, effectively condensing long histories into summaries.
- The compressor applies self-attention over past summary tokens and cross-attention over a cache of historical observations, allowing it to integrate long-range dependencies under a fixed memory budget.
- Feed both working memory and episodic memory as conditioning input to a **diffusion policy** for action generation; the compressor and policy are trained jointly end-to-end so the system can automatically preserve task-relevant information and filter irrelevant history.
- At inference time, it maintains an observation cache and a summary cache, enabling processing of the full history with approximately constant per-step memory and computation, without continually expanding the context window.

## Results
- On the memory-intensive manipulation tasks in **MIKASA**, VPWEM improves over SOTA baselines (including diffusion policies and VLA models) by **more than 20%**.
- On the **MoMaRT** mobile manipulation benchmark, VPWEM achieves an **average improvement of about 5%**, outperforming multiple baselines.
- On approximately Markovian **Robomimic** tasks, the authors claim VPWEM performs **comparably** to baselines, suggesting that the additional memory module does not significantly hurt short-memory tasks.
- The method is instantiated on two diffusion-policy baselines (**DP** and **MaIL**) and evaluated extensively across three benchmark families.
- The excerpt does not provide more detailed per-task tables, standard deviations, or exact baseline-by-baseline scores; the clearest quantitative conclusions are **MIKASA >20%** and **MoMaRT average +5%**.

## Link
- [http://arxiv.org/abs/2603.04910v1](http://arxiv.org/abs/2603.04910v1)
